"""Minimal App Attest attestation verifier (cryptography + cbor2), per Apple's 'Validating apps that connect to your server'."""
from __future__ import annotations
import datetime, hashlib, struct
from dataclasses import dataclass
import cbor2
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

NONCE_OID = x509.ObjectIdentifier("1.2.840.113635.100.8.2")
AAGUID_PROD = b"appattest" + b"\x00" * 7
AAGUID_DEV = b"appattestdevelop"

class AttestationError(Exception): ...

@dataclass
class AttestedKey:
    key_id: bytes
    public_key_der: bytes   # store this per (user, device)
    receipt: bytes          # store for fraud-metric refresh
    counter: int
    validation_category: int | None
    bundle_version: str | None

def _der_octet_string_in_sequence(ext_value: bytes) -> bytes:
    # SEQUENCE { [1] EXPLICIT OCTET STRING(32) } -> Apple: "extract the single octet string"
    i = ext_value.rfind(b"\x04\x20")
    if i < 0 or len(ext_value) < i + 34:
        raise AttestationError("nonce extension malformed")
    return ext_value[i + 2:i + 34]

def verify_attestation(att_obj: bytes, key_id: bytes, client_data_hash: bytes, app_id: str,
                       root: x509.Certificate, production: bool,
                       now: datetime.datetime | None = None) -> AttestedKey:
    now = now or datetime.datetime.now(datetime.timezone.utc)
    obj = cbor2.loads(att_obj)
    if obj.get("fmt") != "apple-appattest":
        raise AttestationError("fmt")
    x5c = obj["attStmt"]["x5c"]; auth = obj["authData"]
    leaf, inter = (x509.load_der_x509_certificate(c) for c in x5c[:2])
    # 1. chain: leaf <- intermediate <- pinned Apple App Attestation Root CA
    for child, parent in ((leaf, inter), (inter, root)):
        child.verify_directly_issued_by(parent)
        if not (child.not_valid_before_utc <= now <= child.not_valid_after_utc):
            raise AttestationError("certificate not valid at verification time")
    # 2-4. nonce = SHA256(authData || clientDataHash); clientDataHash = exactly what the app passed to attestKey
    #      (docs: SHA256(challenge); Apple's own sample vector passes the raw challenge bytes)
    nonce = hashlib.sha256(auth + client_data_hash).digest()
    ext = leaf.extensions.get_extension_for_oid(NONCE_OID).value.value
    if _der_octet_string_in_sequence(ext) != nonce:
        raise AttestationError("nonce")
    # 5. keyId == SHA256(uncompressed EC point of credCert public key)
    pub = leaf.public_key(); assert isinstance(pub, ec.EllipticCurvePublicKey)
    point = pub.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    if hashlib.sha256(point).digest() != key_id:
        raise AttestationError("keyId")
    # 6. RP ID hash
    if auth[:32] != hashlib.sha256(app_id.encode()).digest():
        raise AttestationError("rpId")
    flags = auth[32]
    counter = struct.unpack(">I", auth[33:37])[0]
    if counter != 0:
        raise AttestationError("counter")
    aaguid = auth[37:53]
    if aaguid != (AAGUID_PROD if production else AAGUID_DEV):
        raise AttestationError(f"aaguid {aaguid!r}")
    cred_len = struct.unpack(">H", auth[53:55])[0]
    cred_id = auth[55:55 + cred_len]
    if cred_id != key_id:
        raise AttestationError("credentialId")
    # COSE key, then optional extensions map (flag ED = 0x80)
    rest = auth[55 + cred_len:]
    import io
    f = io.BytesIO(rest); dec = cbor2.CBORDecoder(f)
    _cose = dec.decode()
    exts = dec.decode() if f.tell() < len(rest) else {}   # Apple sample has extensions but ED flag (0x80) unset
    vc = exts.get("apple_validation_category_01"); bv = exts.get("apple_bundle_version_01")
    if isinstance(vc, bytes): vc = int.from_bytes(vc, "little")  # observed encoding in Apple's sample: 4 bytes
    return AttestedKey(key_id, pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo),
                       obj["attStmt"]["receipt"], counter, vc, bv)


def verify_assertion(assertion: bytes, client_data: bytes, public_key_der: bytes, app_id: str,
                     last_counter: int) -> int:
    """Returns the new counter (persist it atomically: UPDATE ... WHERE counter < :new)."""
    from cryptography.hazmat.primitives import hashes
    obj = cbor2.loads(assertion)
    auth, sig = obj["authenticatorData"], obj["signature"]
    nonce = hashlib.sha256(auth + hashlib.sha256(client_data).digest()).digest()
    pub = serialization.load_der_public_key(public_key_der)
    pub.verify(sig, nonce, ec.ECDSA(hashes.SHA256()))          # raises InvalidSignature
    if auth[:32] != hashlib.sha256(app_id.encode()).digest():
        raise AttestationError("rpId")
    counter = struct.unpack(">I", auth[33:37])[0]
    if counter <= last_counter:
        raise AttestationError("counter replay")
    return counter
