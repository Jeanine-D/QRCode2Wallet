import sys, pathlib, subprocess, zipfile, io, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pkpass import PassSigner, build_pkpass
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7
T = pathlib.Path(sys.argv[1])
s = PassSigner.from_p12((T/"pass.p12").read_bytes(), b"testpw", (T/"wwdr.cer").read_bytes())
print("passTypeIdentifier", s.pass_type_identifier, "team", s.team_identifier)
pj = {"description": "Test", "organizationName": "Example", "serialNumber": "123",
      "generic": {"primaryFields": [{"key": "n", "label": "Name", "value": "Müller"}]},
      "barcodes": [{"format": "PKBarcodeFormatQR", "message": "ABC", "messageEncoding": "iso-8859-1"}]}
pk = build_pkpass(s, pj, {"icon.png": b"\x89PNG fake", "icon@2x.png": b"\x89PNG fake2"})
(T/"out.pkpass").write_bytes(pk)
z = zipfile.ZipFile(io.BytesIO(pk)); print("zip entries", z.namelist())
z.extractall(T/"out")
# variants for experiments
man_nl = b'{\n "a" : "b"\n}\n'
(T/"man_nl.json").write_bytes(man_nl)
def sign(opts, h=hashes.SHA256(), data=man_nl):
    b = pkcs7.PKCS7SignatureBuilder().set_data(data).add_signer(s.cert, s.key, h).add_certificate(s.wwdr)
    return b.sign(serialization.Encoding.DER, opts)
O = pkcs7.PKCS7Options
for nm, opts in {"det_bin": [O.DetachedSignature, O.Binary], "det_only": [O.DetachedSignature],
                 "det_bin_nocap": [O.DetachedSignature, O.Binary, O.NoCapabilities],
                 "det_bin_noattr": [O.DetachedSignature, O.Binary, O.NoAttributes]}.items():
    (T/f"sig_{nm}.der").write_bytes(sign(opts))
try:
    (T/"sig_sha1.der").write_bytes(sign([O.DetachedSignature, O.Binary], hashes.SHA1())); print("SHA1 allowed")
except Exception as e:
    print("SHA1 rejected:", type(e).__name__, e)
try:
    sign([O.Binary])  # non-detached DER
    print("non-detached allowed (but WRONG for pkpass)")
except Exception as e: print("err", e)
try:
    sign([O.DetachedSignature, O.Text]); print("Text+DER allowed?")
except Exception as e: print("Text with DER rejected:", e)
