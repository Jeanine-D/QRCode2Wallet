"""Minimal, dependency-light .pkpass builder (cryptography>=42). Stateless: input dict + images -> bytes."""
from __future__ import annotations

import hashlib
import io
import json
import zipfile
from dataclasses import dataclass

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs7, pkcs12
from cryptography.x509.oid import NameOID

PKPASS_MEDIA_TYPE = "application/vnd.apple.pkpass"
_UID_OID = NameOID.USER_ID  # 0.9.2342.19200300.100.1.1 -> passTypeIdentifier in Apple's leaf cert


@dataclass(frozen=True)
class PassSigner:
    cert: x509.Certificate          # Pass Type ID certificate (leaf)
    key: rsa.RSAPrivateKey          # its private key
    wwdr: x509.Certificate          # Apple WWDR G4 intermediate

    @classmethod
    def from_p12(cls, p12: bytes, password: bytes | None, wwdr_der_or_pem: bytes) -> "PassSigner":
        key, cert, _extra = pkcs12.load_key_and_certificates(p12, password)
        if key is None or cert is None:
            raise ValueError("p12 must contain the private key and the Pass Type ID certificate")
        wwdr = (x509.load_pem_x509_certificate(wwdr_der_or_pem) if wwdr_der_or_pem.lstrip().startswith(b"-----")
                else x509.load_der_x509_certificate(wwdr_der_or_pem))
        return cls(cert=cert, key=key, wwdr=wwdr)

    @property
    def pass_type_identifier(self) -> str:
        return self.cert.subject.get_attributes_for_oid(_UID_OID)[0].value

    @property
    def team_identifier(self) -> str:
        return self.cert.subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value

    def sign_manifest(self, manifest: bytes) -> bytes:
        return (
            pkcs7.PKCS7SignatureBuilder()
            .set_data(manifest)
            .add_signer(self.cert, self.key, hashes.SHA256())   # RSA -> PKCS#1 v1.5 by default
            .add_certificate(self.wwdr)
            .sign(serialization.Encoding.DER,
                  [pkcs7.PKCS7Options.DetachedSignature, pkcs7.PKCS7Options.Binary])
        )


def build_pkpass(signer: PassSigner, pass_json: dict, files: dict[str, bytes]) -> bytes:
    """files: relative path -> bytes (e.g. 'icon.png', 'icon@2x.png', 'de.lproj/pass.strings')."""
    pj = dict(pass_json)
    # Bind identity to the certificate: client can never choose these.
    pj["passTypeIdentifier"] = signer.pass_type_identifier
    pj["teamIdentifier"] = signer.team_identifier
    pj.setdefault("formatVersion", 1)
    bundle: dict[str, bytes] = {"pass.json": json.dumps(pj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")}
    for name, data in files.items():
        if name in ("pass.json", "manifest.json", "signature") or name.startswith("/") or ".." in name.split("/"):
            raise ValueError(f"illegal bundle path: {name}")
        bundle[name] = data
    if "icon.png" not in bundle:
        raise ValueError("icon.png is required")
    manifest = json.dumps({n: hashlib.sha1(d).hexdigest() for n, d in sorted(bundle.items())},
                          separators=(",", ":")).encode("utf-8")
    signature = signer.sign_manifest(manifest)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for n, d in bundle.items():
            zf.writestr(n, d)
        zf.writestr("manifest.json", manifest)
        zf.writestr("signature", signature)
    return buf.getvalue()
