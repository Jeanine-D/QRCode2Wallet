"""Create a throwaway test PKI that mimics Apple Root CA -> WWDR G4 -> Pass Type ID leaf."""
import datetime, sys, pathlib
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12

out = pathlib.Path(sys.argv[1])
now = datetime.datetime.now(datetime.timezone.utc)
def key(): return rsa.generate_private_key(public_exponent=65537, key_size=2048)
def name(*attrs): return x509.Name([x509.NameAttribute(o, v) for o, v in attrs])
root_k, int_k, leaf_k = key(), key(), key()
root_n = name((NameOID.COMMON_NAME, "TEST Root CA"), (NameOID.ORGANIZATION_NAME, "TEST"))
int_n = name((NameOID.COMMON_NAME, "TEST WWDR CA"), (NameOID.ORGANIZATIONAL_UNIT_NAME, "G4"), (NameOID.ORGANIZATION_NAME, "TEST"))
leaf_n = name((NameOID.USER_ID, "pass.com.example.test"), (NameOID.COMMON_NAME, "Pass Type ID: pass.com.example.test"),
              (NameOID.ORGANIZATIONAL_UNIT_NAME, "ABCDE12345"), (NameOID.ORGANIZATION_NAME, "Example GmbH"), (NameOID.COUNTRY_NAME, "DE"))
def cert(subj, issuer, pub, signk, ca, days):
    b = (x509.CertificateBuilder().subject_name(subj).issuer_name(issuer).public_key(pub)
         .serial_number(x509.random_serial_number()).not_valid_before(now - datetime.timedelta(days=1))
         .not_valid_after(now + datetime.timedelta(days=days))
         .add_extension(x509.BasicConstraints(ca=ca, path_length=None), critical=True))
    return b.sign(signk, hashes.SHA256())
root = cert(root_n, root_n, root_k.public_key(), root_k, True, 3650)
inter = cert(int_n, root_n, int_k.public_key(), root_k, True, 3000)
leaf = cert(leaf_n, int_n, leaf_k.public_key(), int_k, False, 365)
(out/"root.pem").write_bytes(root.public_bytes(serialization.Encoding.PEM))
(out/"wwdr.pem").write_bytes(inter.public_bytes(serialization.Encoding.PEM))
(out/"wwdr.cer").write_bytes(inter.public_bytes(serialization.Encoding.DER))  # Apple ships .cer as DER
(out/"pass.pem").write_bytes(leaf.public_bytes(serialization.Encoding.PEM))
(out/"pass.key").write_bytes(leaf_k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
(out/"pass.p12").write_bytes(pkcs12.serialize_key_and_certificates(b"pass", leaf_k, leaf, None,
    serialization.BestAvailableEncryption(b"testpw")))
print("ok")
