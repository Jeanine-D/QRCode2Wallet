import sys, pathlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs7
from cryptography import x509
T = pathlib.Path(sys.argv[1])
real = serialization.load_pem_private_key((T/"pass.key").read_bytes(), None)
cert = x509.load_pem_x509_certificate((T/"pass.pem").read_bytes())
class RemoteKey(rsa.RSAPrivateKey):
    """Pretend KMS key: only sign() is remote."""
    def sign(self, data, padding, algorithm):
        import hashlib
        print("remote sign called: len(data)=%d padding=%s alg=%s data[0]=0x%02x" % (len(data), type(padding).__name__, getattr(algorithm, "name", algorithm), data[0]))
        from cryptography.hazmat.primitives.asymmetric import utils
        digest = hashlib.sha256(data).digest()   # what you would send to KMS (MessageType=DIGEST)
        return real.sign(digest, padding, utils.Prehashed(hashes.SHA256()))
    def public_key(self): return real.public_key()
    @property
    def key_size(self): return real.key_size
    def decrypt(self, *a): raise NotImplementedError
    def private_numbers(self): raise NotImplementedError
    def private_bytes(self, *a): raise NotImplementedError
    def __copy__(self): return self
    def __deepcopy__(self, memo): return self
try:
    sig = pkcs7.PKCS7SignatureBuilder().set_data((T/"out"/"manifest.json").read_bytes()).add_signer(cert, RemoteKey(), hashes.SHA256()).add_certificate(x509.load_pem_x509_certificate((T/"wwdr.pem").read_bytes())).sign(
        serialization.Encoding.DER, [pkcs7.PKCS7Options.DetachedSignature, pkcs7.PKCS7Options.Binary])
    (T/"sig_remote.der").write_bytes(sig)
    print("custom key accepted")
except Exception as e:
    print("custom key rejected:", type(e).__name__, e)
# CSR with a remote key (for Apple portal upload) -- does CertificateSigningRequestBuilder accept it too?
from cryptography.x509.oid import NameOID
csr = (x509.CertificateSigningRequestBuilder()
       .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "QRCode2Wallet Pass Signing"),
                                x509.NameAttribute(NameOID.EMAIL_ADDRESS, "ops@example.com"),
                                x509.NameAttribute(NameOID.COUNTRY_NAME, "DE")]))
       .sign(RemoteKey(), hashes.SHA256()))
(T/"remote.csr").write_bytes(csr.public_bytes(serialization.Encoding.PEM))
print("CSR signature valid:", csr.is_signature_valid)
