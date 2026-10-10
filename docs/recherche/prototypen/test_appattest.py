import sys, json, base64, datetime, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from appattest import verify_attestation
from cryptography import x509
v = json.load(open(sys.argv[1])); root = x509.load_pem_x509_certificate(open(sys.argv[2], "rb").read())
r = verify_attestation(base64.b64decode(v["attestationObject"]), base64.b64decode(v["keyId"]), v["challenge"].encode(),
                       f'{v["teamId"]}.{v["bundleId"]}', root, production=True,
                       now=datetime.datetime(2026, 4, 21, tzinfo=datetime.timezone.utc))
print("OK", r.counter, r.validation_category, r.bundle_version, len(r.receipt), "receipt bytes")
try:
    verify_attestation(base64.b64decode(v["attestationObject"]), base64.b64decode(v["keyId"]), b"wrong",
                       f'{v["teamId"]}.{v["bundleId"]}', root, production=True,
                       now=datetime.datetime(2026, 4, 21, tzinfo=datetime.timezone.utc))
except Exception as e: print("wrong challenge rejected:", e)
try:
    verify_attestation(base64.b64decode(v["attestationObject"]), base64.b64decode(v["keyId"]), v["challenge"].encode(),
                       f'{v["teamId"]}.{v["bundleId"]}', root, production=True)
except Exception as e: print("expired leaf (now) rejected:", e)
