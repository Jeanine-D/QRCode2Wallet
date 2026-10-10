import sys, pathlib, hashlib, struct, json, cbor2
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from appattest import verify_assertion, AttestationError
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
k = ec.generate_private_key(ec.SECP256R1()); app_id = "ABCDE12345.de.example.qrcode2wallet"
pub = k.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
def mk(counter, client_data):
    auth = hashlib.sha256(app_id.encode()).digest() + b"\x40" + struct.pack(">I", counter)
    nonce = hashlib.sha256(auth + hashlib.sha256(client_data).digest()).digest()
    return cbor2.dumps({"signature": k.sign(nonce, ec.ECDSA(hashes.SHA256())), "authenticatorData": auth})
cd = json.dumps({"challenge": "abc", "bodySha256": hashlib.sha256(b"{}").hexdigest()}).encode()
print("counter ->", verify_assertion(mk(1, cd), cd, pub, app_id, 0))
try: verify_assertion(mk(1, cd), cd, pub, app_id, 1)
except AttestationError as e: print("replay rejected:", e)
try: verify_assertion(mk(2, cd), cd + b"x", pub, app_id, 1)
except Exception as e: print("tampered clientData rejected:", type(e).__name__)
