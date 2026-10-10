# 03 · Signierung und Backend-Sicherheit

> **Hinweis:** Vollständige Rohfassung der Recherche vom 10.10.2026: KI-Agenten-Recherche gegen Primärquellen, danach von einem unabhängigen Faktenprüfer adversarial gegengeprüft. Die Inhalte stehen in der Originalsprache Englisch. Die deutsche Zusammenfassung mit Bewertung steht in der [Übersicht](README.md). Rechtliche Aussagen sind **keine Rechtsberatung**.

**Recherchierter Umfang:** Generating and signing .pkpass files in Python, plus backend security for the public QRCode2Wallet signing service (verified 2026-10-10, iOS 27 / WWDC26 era)

**Inhalt:** 33 Fakten (Konfidenz hoch 27, mittel 5, niedrig 1) · 11 Empfehlungen · 18 Fallstricke · 9 offene Fragen · Faktencheck von 25 Kernaussagen: 20 bestätigt, 5 korrigiert, 0 nicht verifizierbar · 13 vom Faktenprüfer ergänzte Fakten

## Inhalt

1. [Korrekturen aus dem Faktencheck](#korrekturen-aus-dem-faktencheck)
2. [Fakten](#fakten)
3. [Empfehlungen](#empfehlungen)
4. [Fallstricke](#fallstricke)
5. [Offene Fragen](#offene-fragen)
6. [Faktencheck: alle geprüften Aussagen](#faktencheck-alle-geprüften-aussagen)
7. [Vom Faktenprüfer ergänzte wichtige Fakten](#vom-faktenprüfer-ergänzte-wichtige-fakten)

## Korrekturen aus dem Faktencheck

Diese Aussagen der Recherche hat der Faktenprüfer korrigiert oder nicht bestätigen können. **Bei Widerspruch gilt die Korrektur.**

- **[KORRIGIERT]** Apple's steps for building a pass: manifest.json maps each file path (e.g. en.lproj/logo.png) to its SHA-1 hex digest; PKCS #7 detached signature of manifest.json with the Pass Type ID private key; saved at the top level as `signature`; zip and rename to .pkpass; keep .DS_Store out; manifest is still SHA-1 in 2026, only the CMS signature uses SHA-256.
  - **Ergebnis:** The steps, the SHA-1-per-file manifest, the .lproj example and the .DS_Store note all match the current page. However, Apple's 'Building a Pass' page never mentions SHA-256, the CMS digest algorithm or the WWDR intermediate. It only says 'Create a PKCS #7 detached signature for the manifest that uses the private key of the pass identifier signing certificate.' SHA-256 comes from Apple's Pass Builder code (swift-certificates defaults to sha256WithRSAEncryption), not from the docs. The Pass Builder repo also uses Insecure.SHA1 for the manifest (Sources/PassBuilder/PassSigning/Manifest/Data+SHA1.swift), which independently confirms SHA-1.
  - **Quelle:** <https://developer.apple.com/documentation/walletpasses/building-a-pass>

- **[KORRIGIERT]** PKCS7SignatureBuilder API and options (Text/Binary/DetachedSignature/NoCapabilities/NoAttributes/NoCerts); NoCapabilities makes the output match Apple's Pass Builder byte for byte in structure; Text+DER errors; NoAttributes cannot be combined with NoCapabilities.
  - **Ergebnis:** The API facts are confirmed: versionadded 3.2; rsa_padding versionadded 42.0.0 (None means PKCS1v15); add_certificate can be called repeatedly; Text+DER raises 'The Text option is only available for SMIME serialization'; NoAttributes+NoCapabilities raises 'NoAttributes is a superset of NoCapabilities'; NoCerts output fails `openssl cms -verify` with 'signer certificate not found'. WRONG: the output is not structurally identical to Pass Builder. cryptography writes SignerInfo.signatureAlgorithm = rsaEncryption (1.2.840.113549.1.1.1), while swift-certificates writes sha256WithRSAEncryption (1.2.840.113549.1.1.11). The certificate order also differs (swift-certificates puts the intermediates first, then the leaf). Both forms are valid CMS and both verify with OpenSSL. With NoCapabilities the signed attributes are contentType, signingTime and messageDigest (DER SET).
  - **Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/docs/hazmat/primitives/asymmetric/serialization.rst>

- **[KORRIGIERT]** HIG image specs (2026-06-08 iOS 27 update): icon 38x38; logo 50-160x50; primaryLogo 30-126x30; secondaryLogo 12-135x12; strip 375x144; thumbnail 60-90x90; background.png 343x503 (non-poster) or 358x448 (poster); footer 268x15. Pass Builder: icon 38x38, background 345x505, artwork 358x448, footer max 286x15, logo max 160x50, primaryLogo max 126x30, secondaryLogo max 135x12, strip 375x144, thumbnail 90x90.
  - **Ergebnis:** Poster pass backgrounds are NOT background.png: the HIG lists filename `artwork.png` (358x448 pt) for poster event tickets and poster generic passes. background.png (343x503 pt) is listed only for (non-poster) event tickets. The HIG says 'Create pass images in PNG format in @2x and @3x format' (no 1x). All other HIG values and the 2026-06-08 change-log entry are confirmed. The Pass Builder values are confirmed in Sources/PassBuilder/PassPackage/PassPackage.swift. RequiredImagesValidator makes the icon mandatory: missing icon is an error; missing @2x or @3x is a warning. Note the HIG/Pass Builder mismatch for background (343x503 vs 345x505) and footer (268 vs max 286).
  - **Quelle:** <https://developer.apple.com/design/human-interface-guidelines/wallet>

- **[KORRIGIERT]** App Attest server validation steps (x5c to root, nonce=SHA256(authData||clientDataHash) vs OID 1.2.840.113635.100.8.2, SHA256(point)==keyId, rpIdHash, counter 0, aaguid, credentialId, apple_validation_category_01 (4 App Store, 2 TestFlight, 3 dev) and apple_bundle_version_01); assertions: nonce, ECDSA signature, rpId, strictly increasing counter.
  - **Ergebnis:** The attestation steps are confirmed, including the validation category table (0 invalid, 1 OS executable, 2 TestFlight, 3 development, 4 App Store, 5 Enterprise/ad-hoc, 6 Developer ID, 10 other). The assertion list is incomplete. Apple's current doc also requires: (6) 'Verify that the embedded challenge in the client data matches the earlier challenge'; (7) verify validationCategory and (8) bundleVersion in the assertion's authenticator-data extensions. Counter rule: 'greater than the value from the previous assertion, or greater than 0 on the first assertion'. Also required: store one (key, receipt) pair per device, keep development and production pairs separate, ensure the public key is not already associated with another user, and verify and store the receipt immediately after attestation.
  - **Quelle:** <https://developer.apple.com/documentation/devicecheck/validating-apps-that-connect-to-your-server>

- **[KORRIGIERT]** STACKIT KMS is GA, v1beta removed after 2025-10-15; RSA keys exist but only AES-256-GCM and RSA-OAEP are listed; RSASSA-PKCS1-v1_5 signing unconfirmed.
  - **Ergebnis:** From STACKIT's official SDKs (stackit-sdk-go and stackit-sdk-python, services/kms): Purpose includes 'asymmetric_sign_verify', but the Algorithm enum is aes_256_gcm, rsa_2048/3072/4096_oaep_sha256, rsa_4096_oaep_sha512, hmac_sha256/384/512, ecdsa_p256_sha256/p384_sha384/p521_sha512. RSA appears only as OAEP encryption, so RSA-PKCS1 signing (needed for a standard RSA Pass Type ID key) is not offered; only ECDSA signing is. SDK changelog: 'v1betaapi: This API was removed after the announced deprecation period' and 'hsm' key protection is 'Only as private preview feature available'. The GA status and the 2025-10-15 date were not verified (docs.stackit.cloud unreachable). Whether Apple issues Pass Type ID certificates for EC CSRs is unverified (Pass Builder does try EC keys first).
  - **Quelle:** <https://raw.githubusercontent.com/stackitcloud/stackit-sdk-go/main/services/kms/model_algorithm.go>

## Fakten

### F1 · Konfidenz: hoch

Apple's steps for building a pass: (1) write manifest.json, a JSON dictionary that maps each file's path relative to the bundle root (for example "en.lproj/logo.png") to the SHA-1 hex digest of that file; (2) create a PKCS #7 detached signature of manifest.json with the private key of the Pass Type ID certificate; (3) save it at the top level as a file named `signature`; (4) zip the bundle and rename the archive .pkpass. Metadata files such as .DS_Store must stay out of the bundle. The manifest digest is still SHA-1 per file in the 2026 docs; only the CMS signature uses SHA-256.

- **Bedeutung fürs Design:** The server builder must use hashlib.sha1 for manifest entries and SHA-256 for the CMS signature. Every file in the zip except manifest.json and signature must appear in the manifest, including files inside .lproj folders.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/building-a-pass>

### F2 · Konfidenz: hoch

Apple's 'Common Problems' list for passes: passTypeIdentifier must match the signing certificate, teamIdentifier must match the certificate's developer account, the certificate must not be expired, all required keys and images must be present, and the JSON must be valid. Required pass.json keys: formatVersion (must be 1), passTypeIdentifier, serialNumber, teamIdentifier, organizationName, description.

- **Bedeutung fürs Design:** The server should always overwrite passTypeIdentifier, teamIdentifier, formatVersion and serialNumber from its own certificate and config, and never take them from the client.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### F3 · Konfidenz: hoch

Apple's own open-source Pass Builder (github.com/apple/pass-builder, Apache-2.0, 'early preview', Swift 6.3+, macOS 14+ or Linux, announced in WWDC26 session 209) signs the manifest with swift-certificates `CMS.sign(manifest, additionalIntermediateCertificates: [wwdr], certificate: passCert, privateKey: key, signingTime: Date())`, which produces a detached signature by default. For RSA keys swift-certificates uses `.sha256WithRSAEncryption` (PKCS#1 v1.5), and the signed attributes are exactly contentType, messageDigest and signingTime (no SMIMECapabilities).

- **Bedeutung fürs Design:** This is Apple's reference: SHA-256 digest, RSA PKCS#1 v1.5, a signing-time attribute, the WWDR intermediate embedded, and detached content. The Python implementation should produce the same structure.
- **Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassSigning/ManifestSignatureGenerator.swift>

### F4 · Konfidenz: hoch

Pass Builder reads identity from the Pass Type ID certificate subject: the passTypeIdentifier is in attribute OID 0.9.2342.19200300.100.1.1 (UID) and the Team ID is in OU (2.5.4.11). Its validateAttributes(for:) throws when they do not match pass.json.

- **Bedeutung fürs Design:** In Python read them with cert.subject.get_attributes_for_oid(NameOID.USER_ID) and NameOID.ORGANIZATIONAL_UNIT_NAME, then inject both into pass.json. This removes a whole class of 'pass won't open' errors.
- **Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassSigning/PassCertificate%2BAttributes.swift>

### F5 · Konfidenz: hoch

Apple's WWDR intermediate generations: G2 = Apple Pay ECDSA; G3 = software signing (Apple Development/Distribution and others); G4 = 'Features supported by APNs': Pass Type ID, Pass Type ID with NFC, APNs SSL, Order Type ID, Website Push ID, WatchKit, VoIP; G5 = App Store signing; G6 = ECDSA software and services; G7 = App Store receipt signing. WWDR certificates are distributed on the Apple PKI site (https://www.apple.com/certificateauthority/; file AppleWWDRCAG4.cer).

- **Bedeutung fürs Design:** Embed WWDR \*\*G4\*\* in every signature. Bundling G3 or the old G1 produces passes Wallet rejects.
- **Quelle:** <https://developer.apple.com/help/account/certificates/wwdr-intermediate-certificates>

### F6 · Konfidenz: mittel

Pass Type ID certificates issued after January 27, 2022 chain to the 'Worldwide Developer Relations G4 sub CA'. Apple says the correct intermediate has an expiration date in 2030 and 'G4' in the Organization field. I could not fetch the exact notAfter date because www.apple.com is unreachable from this environment; from memory it is 2030-12-10, but that is unverified.

- **Bedeutung fürs Design:** Read the G4 notAfter at startup with cryptography (cert.not_valid_after_utc), export it as a metric, and alert well before 2030. Plan a WWDR rotation the same way as the yearly leaf rotation.
- **Quelle:** <https://developer.apple.com/support/expiration/>

### F7 · Konfidenz: hoch

The original WWDR intermediate (G1, 'Apple Worldwide Developer Relations Certification Authority', still served at developer.apple.com/certificationauthority/AppleWWDRCA.cer) expired on Feb 7, 2023 21:48:47 GMT. I confirmed this by downloading it and running openssl x509 -dates.

- **Bedeutung fürs Design:** Many older tutorials and libraries still link to AppleWWDRCA.cer. Do not use it.
- **Quelle:** <https://developer.apple.com/help/account/certificates/wwdr-intermediate-certificates>

### F8 · Konfidenz: hoch

cryptography 50.0.2 (latest, released 2026-09-30) rejects SHA-1 in PKCS7SignatureBuilder.add_signer with `TypeError: hash_algorithm must be one of hashes.SHA224, SHA256, SHA384, or SHA512`, even though the docs' PKCS7HashTypes alias still lists SHA1. The changelog for 39.0.0 says MD5/SHA1 support in PKCS7 was removed. I verified the rejection locally.

- **Bedeutung fürs Design:** Use hashes.SHA256(); it matches Apple's Pass Builder. Libraries that sign with SHA1 (such as applepassgenerator) fail on any modern cryptography version.
- **Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/CHANGELOG.rst>

### F9 · Konfidenz: hoch

PKCS7SignatureBuilder API (since 3.2): set_data(bytes); add_signer(certificate, private_key, hash_algorithm, \*, rsa_padding=None), where rsa_padding (since 42.0.0) defaults to PKCS1v15 for RSA; add_certificate(cert), which can be called repeatedly; sign(encoding, options). Options: Text (SMIME only, rejected with DER: ValueError 'The Text option is only available for SMIME serialization'), Binary (no LF to CRLF conversion), DetachedSignature, NoCapabilities (drops SMIMECapabilities), NoAttributes (drops all authenticated attributes; cannot be combined with NoCapabilities), NoCerts.

- **Bedeutung fürs Design:** Required options: DetachedSignature and Binary. Optional: NoCapabilities (makes the output match Apple's Pass Builder byte for byte in structure). Forbidden: Text (errors with DER), NoAttributes (removes signingTime) and NoCerts (drops the leaf certificate). Without DetachedSignature you get an attached signature, which does not follow Apple's spec.
- **Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/docs/hazmat/primitives/asymmetric/serialization.rst>

### F10 · Konfidenz: hoch

Local experiment with cryptography 50.0.2 and OpenSSL 3.0.13. Signing a manifest that contains LF newlines \*\*without\*\* PKCS7Options.Binary produces a signature that FAILS `openssl cms -verify -binary` against the raw manifest bytes (CMS_SignerInfo_verify_content: verification failure), because the content is canonicalized LF to CRLF before hashing. With Binary it verifies. By default cryptography adds the signed attributes contentType, signingTime (UTCTime), messageDigest and SMIMECapabilities; NoCapabilities leaves contentType, signingTime and messageDigest.

- **Bedeutung fürs Design:** Always pass Binary. Some third-party libraries omit it and only work because their manifest is compact JSON without newlines, which is fragile.
- **Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/docs/hazmat/primitives/asymmetric/serialization.rst>

### F11 · Konfidenz: hoch

Verified OpenSSL CLI equivalents (OpenSSL 3.0 defaults to SHA-256). Sign: `openssl smime -sign -binary -in manifest.json -signer pass.pem -inkey pass.key -certfile wwdr_g4.pem -outform DER -out signature`, or `openssl cms -sign -binary -md sha256 -nosmimecap -in manifest.json -signer pass.pem -inkey pass.key -certfile wwdr_g4.pem -outform DER -out signature` (cms -sign is detached unless -nodetach is given). Verify the signature only: `openssl cms -verify -binary -noverify -inform DER -in signature -content manifest.json -out /dev/null`. Verify with the chain: `openssl cms -verify -binary -inform DER -in signature -content manifest.json -CAfile AppleRootCA.pem -purpose any -out /dev/null`. Changing a single byte of the manifest makes verification fail.

- **Bedeutung fürs Design:** Put `openssl cms -verify` in CI and in a debug endpoint. Use `-purpose any` because Pass Type ID certificates are not S/MIME email certificates; I did not test with a real Apple leaf certificate. Use `-noverify` for checks that do not need the chain.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/building-a-pass>

### F12 · Konfidenz: hoch

Creating the certificate (Account Holder or Admin role). Register the ID: Certificates, Identifiers & Profiles &gt; Identifiers &gt; + &gt; Pass Type IDs &gt; description and identifier &gt; Register. Create the certificate: Certificates &gt; + &gt; Services: Pass Type ID Certificate &gt; select the ID &gt; upload the CSR (.certSigningRequest) &gt; Download, which gives a .cer file. Apple's CSR page describes Keychain Access and shows openssl genrsa/req commands as an option for other certificate types.

- **Bedeutung fürs Design:** Generate the key on the server side (openssl or a KMS/HSM) instead of exporting it from Keychain. Run `openssl genrsa -out pass.key 2048`, then `openssl req -new -key pass.key -out pass.csr -subj "/emailAddress=ops@example.com/CN=QRCode2Wallet Pass Signing/C=DE"`, then convert the download with `openssl x509 -inform DER -in pass.cer -out pass.pem`.
- **Quelle:** <https://developer.apple.com/help/account/capabilities/create-wallet-identifiers-and-certificates/>

### F13 · Konfidenz: hoch

Effect of expiry and revocation on Pass Type ID certificates: 'If your certificate expires, passes that are already installed on users' devices will continue to function normally. However, you'll no longer be able to sign new passes or send updates to existing passes. If your certificate is revoked, your passes will no longer function properly.' If the key is suspected compromised, email product-security@apple.com, and you can request an additional certificate in the account. 'Apple can revoke digital certificates at any time at its sole discretion.'

- **Bedeutung fürs Design:** Expiry only stops new signing. Revocation (for example after abuse of the public endpoint) breaks every pass already issued. This is why the signing key and the endpoint are the crown jewel.
- **Quelle:** <https://developer.apple.com/help/account/certificates/certificates-overview>

### F14 · Konfidenz: mittel

Pass Type ID certificates are valid for about one year. Apple's documentation does not state the length; the sources are an Apple Developer Forums community answer and vendor docs (PassEntry says 1 year, PassSlot says 356 days).

- **Bedeutung fürs Design:** Rotate yearly: alert at 60, 30 and 7 days from cert.not_valid_after_utc. A new certificate for the same Pass Type ID keeps passTypeIdentifier and Team ID the same, so new or updated passes with the same serial replace the old ones (pass identity is passTypeIdentifier plus serialNumber).
- **Quelle:** <https://developer.apple.com/forums/thread/64215>

### F15 · Konfidenz: hoch

A .p12 encrypted with legacy pbeWithSHA1And40BitRC2-CBC (typical of older Keychain exports) fails in the OpenSSL 3 CLI with 'unsupported ... RC2-40-CBC' unless `-legacy` is given (`openssl pkcs12 -legacy -in cert.p12 -clcerts -nokeys -out pass.pem`; `openssl pkcs12 -legacy -in cert.p12 -nocerts -nodes -out pass.key`). cryptography's `pkcs12.load_key_and_certificates(data, password)` loads it without problems. Verified locally.

- **Bedeutung fürs Design:** Load the .p12 directly with cryptography (it returns key, cert and extra certs) or skip .p12 entirely by generating key and CSR on Linux or in a KMS.
- **Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/docs/hazmat/primitives/asymmetric/serialization.rst>

### F16 · Konfidenz: hoch

Python library status (PyPI, checked 2026-10-10). wallet-py3k 0.0.4: last release 2018, shells out to `openssl smime`. passbook 1.0.2: last release 2016. applepassgenerator 0.0.2: last release 2023-02, pins cryptography&lt;38 and signs with hashes.SHA1(), so it is broken on current cryptography. py-pkpass 1.0.2: released 2025-04, cryptography&gt;=44.0.1, SHA256 + DetachedSignature but no Binary, and an odd 'swig' dependency. edutap.wallet_apple 1.0.0a5: 2026-08, alpha, includes FastAPI web-service and APNs handlers, but its sign_manifest() emits an ATTACHED signature (detached=False). django-walletpass 5.0.1: 2026-04, Django only. passes-rs-py 4.0.2: 2026-05, Rust binding, Python &gt;=3.12.

- **Bedeutung fürs Design:** None of the pure-Python libraries is both well maintained and correct out of the box. Writing your own builder is about 70 to 150 lines and only needs cryptography (code tested below).
- **Quelle:** <https://pypi.org/project/py-pkpass/>

### F17 · Konfidenz: hoch

Image specifications in the HIG ('Updated to reflect guidance for iOS 27 and the Pass Designer app', 2026-06-08), PNG at @2x and @3x: icon.png 38x38 pt; logo.png 50 to 160 pt wide x 50 pt high; primaryLogo.png 30 to 126 x 30 pt (semantic passes); secondaryLogo.png 12 to 135 x 12 pt (poster event); strip.png 375x144 pt; thumbnail.png 60 to 90 x 90 pt; background.png 343x503 pt (non-poster) or 358x448 pt (poster); footer.png 268x15 pt (airline boarding only). Apple's Pass Builder validator uses slightly different values: icon required 38x38, background 345x505, a new 'artwork' 358x448, footer max 286x15, logo max 160x50, primaryLogo max 126x30, secondaryLogo max 135x12, strip 375x144, thumbnail 90x90.

- **Bedeutung fürs Design:** The default icon is now 38 pt, not the legacy 29 pt: generate icon.png 38x38, icon@2x.png 76x76 and icon@3x.png 114x114. Keep icon.png (1x) as well, because Apple's own manifest example lists icon.png, icon@2x.png and icon@3x.png. Validate user images against these boxes.
- **Quelle:** <https://developer.apple.com/design/human-interface-guidelines/wallet>

### F18 · Konfidenz: hoch

WWDC26 session 209 introduced Pass Designer (a Mac app that saves .pkpasstemplate files), Pass Builder (Swift on Server, Mac and Linux, with Swift API and the `buildpass` CLI: `buildpass sign|validate|personalize`), protobuf definitions of the pass package format for use from other languages, the Poster Generic style, new barcode formats and a pass actions API.

- **Bedeutung fürs Design:** Options: (a) a Python signer as the main path, with `buildpass validate` (Swift container) as a CI oracle; or (b) call `buildpass sign` as a subprocess. Option (a) avoids the Swift toolchain at runtime. Server-side pass.json validation must not reject new iOS 27 keys if you plan to use them.
- **Quelle:** <https://developer.apple.com/videos/play/wwdc2026/209/>

### F19 · Konfidenz: hoch

Starlette 1.6.0 (2026-08-08) added `max_body_size` to Starlette and route classes, backed by `starlette.middleware.body_limit.RequestBodyLimitMiddleware(app, max_body_size: int)`. FastAPI 0.143.0 (2026-10-08, starlette 1.7.0) has no constructor parameter for it, but `app.add_middleware(RequestBodyLimitMiddleware, max_body_size=256*1024)` works. Verified locally: a 300 KB body gets HTTP 413, an unknown JSON field gets 422 with pydantic ConfigDict(extra='forbid'), and the response is 200 with `application/vnd.apple.pkpass` plus Content-Disposition attachment.

- **Bedeutung fürs Design:** Limit request size at both the edge (load balancer or gateway) and the app. Use a pydantic v2 model with extra='forbid' and max_length on every field. Use a sync `def` endpoint so CPU-bound signing runs in the threadpool.
- **Quelle:** <https://github.com/Kludex/starlette/blob/main/docs/release-notes.md>

### F20 · Konfidenz: hoch

App Attest server validation per Apple's 2026 docs: decode the CBOR attestation (fmt 'apple-appattest', attStmt.x5c, receipt, authData); validate x5c up to the Apple App Attestation Root CA; compute nonce = SHA256(authData || clientDataHash) and compare it with the octet string in the credCert extension with OID 1.2.840.113635.100.8.2; check SHA256(uncompressed EC point) == keyId; check rpIdHash == SHA256('&lt;TeamID&gt;.&lt;bundleID&gt;'); counter == 0; aaguid == 'appattestdevelop' or 'appattest'+7x0x00; credentialId == keyId. New in the docs: check `apple_validation_category_01` (UInt32; 4 = App Store, 2 = TestFlight, 3 = development) and `apple_bundle_version_01` in the authData extensions CBOR map. Assertions: nonce = SHA256(authenticatorData || SHA256(clientData)); verify the ECDSA-SHA256 signature with the stored key; rpId must match; counter must increase strictly.

- **Bedeutung fürs Design:** Implement the checks in full, including validation category (allow only 4 in production, 2 for TestFlight) and bundle version. Store (keyId, public key, counter, receipt) per device. Persist the counter atomically to prevent replay.
- **Quelle:** <https://developer.apple.com/documentation/devicecheck/validating-apps-that-connect-to-your-server>

### F21 · Konfidenz: hoch

Apple's official 'Attestation Object Validation Guide' sample (teamID 1234567890, bundle com.example.myapp, challenge 'example_server_challenge') passes my own verifier (cryptography + cbor2, about 80 lines). Three quirks: (1) the composite is authData || RAW challenge bytes, not SHA256(challenge), even though the text says to hash the challenge; (2) the authData flags byte is 0x40 (ED bit not set) yet an extensions CBOR map follows the COSE key; (3) apple_validation_category_01 is a 4-byte little-endian byte string (value 1), and apple_bundle_version_01 is '1', not the '1.0' the text says. The sample leaf certificate is only valid 2026-04-20 to 2026-04-23.

- **Bedeutung fürs Design:** The server must compute clientDataHash exactly as the app did. Specify it in the API contract: app sends clientDataHash = SHA256(challenge). Parse extensions whenever bytes remain, without relying on the ED flag. Use the sample as a unit test with verification time fixed to 2026-04-21.
- **Quelle:** <https://developer.apple.com/documentation/devicecheck/attestation-object-validation-guide>

### F22 · Konfidenz: mittel

The Apple App Attestation Root CA (official download https://www.apple.com/certificateauthority/private/, not reachable from this environment) is 'CN=Apple App Attestation Root CA, O=Apple Inc., ST=California', valid 2020-03-18 to 2045-03-15, SHA-256 fingerprint 1C:B9:82:3B:A2:8B:A6:AD:2D:33:A0:06:94:1D:E2:AE:4F:51:3E:F1:D4:E8:31:B9:F7:E0:FA:7B:62:42:C9:32. I read these from the copy bundled in pyattest 1.0.5. Its SKI AC:91:10:53:...:8A:A1 matches the AKI of the intermediate 'Apple App Attestation CA 1' (valid until 2030-03-13) in Apple's official guide.

- **Bedeutung fürs Design:** Pin this root, and check its fingerprint in a unit test. The intermediate expires 2030-03-13, so validation must build the chain dynamically and not pin the intermediate.
- **Quelle:** <https://developer.apple.com/documentation/devicecheck/attestation-object-validation-guide>

### F23 · Konfidenz: hoch

pyattest 1.0.5 (2026-07-14; deps cbor2, pyhanko_certvalidator, pyjwt, python-jose[cryptography], cryptography) bundles the root CA and implements the attestation checks. Gaps: it does not check the new apple_validation_category_01 / apple_bundle_version_01 extensions; AppleAssertionVerifier only checks the signature (no rpId or counter checks); and its attestation verifier always computes SHA256(challenge) itself.

- **Bedeutung fürs Design:** Either wrap pyattest and add the missing rpId, counter and extension checks, or own about 120 lines (cryptography + cbor2) tested against Apple's sample. Owning the code avoids python-jose.
- **Quelle:** <https://pypi.org/project/pyattest/>

### F24 · Konfidenz: hoch

App Attest fraud metric: POST the base64 receipt with `Authorization: <JWT>` to https://data-development.appattest.apple.com/v1/attestationData (sandbox) or https://data.appattest.apple.com/v1/attestationData (production). Receipt checks: field 2 = App ID, field 12 = creation time no older than 5 minutes, field 6 = ATTEST or RECEIPT, field 17 = risk metric (attested keys on the device over 30 days), field 19 = do not refresh before this date (otherwise 304). Keys do not survive reinstall, backup restore or device migration. DCAppAttestService requires iOS 14.0+; check `isSupported`; among extensions only Action, extensible SSO and watchOS extensions are supported. Apps with millions of DAU must ramp up attestation gradually.

- **Bedeutung fürs Design:** Treat the risk metric as an optional abuse signal; a high metric earns stricter quotas. The share extension (if planned) cannot use App Attest: route its requests through the host app or give them lower quotas. Plan a fallback path for unsupported devices.
- **Quelle:** <https://developer.apple.com/documentation/devicecheck/assessing-fraud-risk>

### F25 · Konfidenz: hoch

Sign in with Apple identity token verification: fetch keys with `GET https://appleid.apple.com/auth/keys` (JWKSet; keys have kty 'RSA'; pick by `kid`; the key set changes over time). Verify iss == 'https://appleid.apple.com', aud == client_id (the app's bundle ID for native apps), exp, and the nonce (if nonce_supported is true, nonce is mandatory). The prose in 'Verifying a user' says 'JWS E256', but the JWKS documents RSA keys, so the token is RS256 in practice.

- **Bedeutung fürs Design:** Use PyJWT 2.15.1: `jwks = jwt.PyJWKClient('https://appleid.apple.com/auth/keys', cache_keys=True, lifespan=3600)`; `key = jwks.get_signing_key_from_jwt(tok)`; `jwt.decode(tok, key, algorithms=['RS256'], audience=BUNDLE_ID, issuer='https://appleid.apple.com', options={'require':['exp','iat','iss','aud','sub']})`; then compare the nonce.
- **Quelle:** <https://developer.apple.com/documentation/signinwithapplerestapi/fetch-apple's-public-key-for-verifying-token-signature>

### F26 · Konfidenz: hoch

App Review Guideline 5.1.1(v): 'If your app supports account creation, you must also offer account deletion within the app.'

- **Bedeutung fürs Design:** Adding Sign in with Apple accounts creates obligations: in-app account deletion and token revocation, plus GDPR data for the account. App Attest alone avoids accounts entirely.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F27 · Konfidenz: hoch

slowapi 0.1.10 (2026-06-13) wraps the `limits` library. The endpoint must take an explicit `request: Request` argument, and the 'redis' extra pins `redis<4.0.0,>=3.4.1`. limits 5.8.0 (2026-02) is the underlying engine and supports Redis and memory backends.

- **Bedeutung fürs Design:** Do not use the slowapi[redis] extra (it pins an ancient redis client). Use `limits` directly with a current redis storage, or rate-limit at the edge, and key limits by attested keyId in addition to IP.
- **Quelle:** <https://pypi.org/project/slowapi/>

### F28 · Konfidenz: hoch

PassKit web service for updates: add `webServiceURL` and `authenticationToken` to pass.json. Endpoints: POST {webServiceURL}/v1/devices/{deviceLibraryIdentifier}/registrations/{passTypeIdentifier}/{serialNumber} (body PushToken); GET /v1/devices/{deviceLibraryIdentifier}/registrations/{passTypeIdentifier}?passesUpdatedSince=...; GET /v1/passes/{passTypeIdentifier}/{serialNumber}; DELETE (unregister); POST /v1/log. Auth header `Authorization: ApplePass <authenticationToken>`. The push uses 'the same certificate and private key that the creator of the pass used to sign the original', the device's push token and an empty JSON payload, and works only in production. You need device, pass and registration tables. HTTPS is mandatory in production.

- **Bedeutung fürs Design:** Updates turn the stateless signer into a stateful service: pass content, device library IDs and push tokens are personal data. APNs mTLS with the Pass Type ID certificate is hard if that key lives only in a cloud KMS, because Python's ssl module cannot use KMS keys.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/adding-a-web-service-to-update-passes>

### F29 · Konfidenz: mittel

Local test with cryptography 50.0.2: PKCS7SignatureBuilder.add_signer and CertificateSigningRequestBuilder.sign both accept a Python subclass of `rsa.RSAPrivateKey` and call its `sign(data, padding, algorithm)` method, passing the DER SET of signed attributes (164 bytes, first byte 0x31), PKCS1v15 and SHA256. Signing SHA256(data) remotely with `utils.Prehashed(hashes.SHA256())` semantics produced a signature that `openssl cms -verify` accepts and a CSR that `openssl req -verify` accepts. cryptography does not document this as a supported contract.

- **Bedeutung fürs Design:** Cloud KMS or HSM signing works without hand-written ASN.1. Implement a `KmsRsaKey(rsa.RSAPrivateKey)` whose sign() sends sha256(data) to the KMS: AWS `kms.sign(KeyId=..., Message=digest, MessageType='DIGEST', SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256')`, or GCP `asymmetric_sign(name=..., digest={'sha256': digest})` with key algorithm RSA_SIGN_PKCS1_2048_SHA256. Use the same class to build Apple's CSR. Pin the cryptography version and keep an integration test.
- **Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/docs/hazmat/primitives/asymmetric/serialization.rst>

### F30 · Konfidenz: mittel

AWS KMS Sign: with MessageType=DIGEST KMS skips hashing, and the message must have the digest length. RSASSA_PKCS1_V1_5_SHA_256 is a supported SigningAlgorithm (AWS recommends PSS for new designs, but Apple's format needs PKCS#1 v1.5). Google Cloud KMS lists RSA_SIGN_PKCS1_2048_SHA256 (RSASSA-PKCS1 v1.5, 2048-bit, SHA-256). I could not reach the docs pages directly; these come from search results.

- **Bedeutung fürs Design:** Both work in EU regions (AWS eu-central-1 Frankfurt, GCP europe-west3 Frankfurt). Budget for per-request KMS latency of tens of milliseconds and per-call cost; signing is one call per pass.
- **Quelle:** <https://docs.aws.amazon.com/cli/latest/reference/kms/sign.html>

### F31 · Konfidenz: niedrig

STACKIT (a German sovereign cloud) KMS is GA; the v1beta API was removed after 2025-10-15. It generates RSA-2048/3072/4096 keys, but its algorithm list only shows AES-256-GCM and RSA-OAEP. I could not confirm that RSASSA-PKCS1-v1_5 signing is supported.

- **Bedeutung fürs Design:** If German-only hosting is required, confirm STACKIT signing support with the provider first, or fall back to an encrypted software key in a secrets manager.
- **Quelle:** <https://docs.stackit.cloud/products/security/kms/>

### F32 · Konfidenz: hoch

In Pillow 12.3.0, Image.open raises DecompressionBombError when an image has more than 2 \* Image.MAX_IMAGE_PIXELS pixels (and warns above MAX_IMAGE_PIXELS). ImageFont.load_default(size) returns a FreeType font. Generated 38/76/114 px icons are about 200 to 340 bytes each.

- **Bedeutung fürs Design:** Re-encode every user-supplied image server-side with Pillow (decode, convert, thumbnail into the pt box at @1x/@2x/@3x, save as PNG without metadata). Never put raw uploaded bytes into a pass you sign.
- **Quelle:** <https://pillow.readthedocs.io/en/stable/reference/Image.html>

### F33 · Konfidenz: hoch

PKPass(data:) throws `invalidSignature` when the pass signature is invalid and `invalidDataError` when the data is invalid. PKPassKitError codes: unknownError, invalidDataError, unsupportedVersionError, invalidSignature, notEntitledError.

- **Bedeutung fürs Design:** The iOS app should construct PKPass(data:) on the downloaded bytes before calling PKAddPassesViewController or PKPassLibrary, and report invalidSignature as telemetry, which is the best early warning for certificate or WWDR problems.
- **Quelle:** <https://developer.apple.com/documentation/passkit/pkpass/init(data:)>

## Empfehlungen

### E1

**Empfehlung:** Write your own pass builder (about 70 lines) on `cryptography>=50,<51` (pinned) instead of depending on a Python pkpass library. Reference code, verified with openssl cms -verify: `key, cert, _ = pkcs12.load_key_and_certificates(p12, pw)`; `wwdr = x509.load_der_x509_certificate(open('AppleWWDRCAG4.cer','rb').read())`; force `pj['passTypeIdentifier'] = cert.subject.get_attributes_for_oid(NameOID.USER_ID)[0].value` and `pj['teamIdentifier'] = cert.subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value`; build `bundle = {'pass.json': json.dumps(pj, ensure_ascii=False, separators=(',',':')).encode(), **images}`; build `manifest = json.dumps({n: hashlib.sha1(d).hexdigest() for n, d in sorted(bundle.items())}, separators=(',',':')).encode()`; sign with `sig = pkcs7.PKCS7SignatureBuilder().set_data(manifest).add_signer(cert, key, hashes.SHA256()).add_certificate(wwdr).sign(serialization.Encoding.DER, [pkcs7.PKCS7Options.DetachedSignature, pkcs7.PKCS7Options.Binary, pkcs7.PKCS7Options.NoCapabilities])`; then write a zip (ZIP_DEFLATED) with every file at the root plus manifest.json and signature. Reject bundle paths starting with '/' or containing '..', and reject client-supplied pass.json, manifest.json or signature. A full tested version is at docs/recherche/prototypen/pkpass.py.

**Begründung:** The available libraries are abandoned (wallet-py3k, passbook), broken (applepassgenerator uses SHA1 and cryptography&lt;38), deviate from the spec (edutap emits an attached signature; py-pkpass omits Binary) or are framework-bound. The format is small, Apple's Pass Builder documents the exact CMS shape, and keeping the code yourself gives full control over the trust-critical signing path.

### E2

**Empfehlung:** Validate the output in three layers in CI: (1) `openssl cms -verify -binary -inform DER -in signature -content manifest.json -CAfile AppleRootCA.pem -purpose any`; (2) `buildpass validate` from Apple's Pass Builder in a swift:6.3 Linux container for structure and image sizes; (3) an iOS simulator or device smoke test that drops the .pkpass on the device or calls `PKPass(data:)`.

**Begründung:** openssl checks the cryptography; Apple's validator catches pass.json and image errors; only Wallet itself is the final oracle.

### E3

**Empfehlung:** Generate the Pass Type ID private key outside any Mac Keychain. Best: create a non-exportable RSA-2048 key in an EU cloud KMS or HSM, build the CSR in Python with a `KmsRsaKey(rsa.RSAPrivateKey)` adapter (cryptography's CSR builder calls its sign()), upload the CSR to Apple, and convert the .cer from DER to PEM. Simpler alternative: `openssl genrsa` and `openssl req` on a locked-down machine, storing the PEM key encrypted in a secrets manager (GCP Secret Manager, AWS Secrets Manager, Azure Key Vault) and loading it once at startup through pydantic-settings SecretStr.

**Begründung:** Revocation after a key leak breaks every issued pass. A non-exportable KMS key removes key exfiltration as a risk. I verified locally that cryptography 50.0.2 calls custom key objects for both PKCS7 signing and CSR signing.

### E4

**Empfehlung:** Treat the signing endpoint as the crown jewel and layer the defenses. (a) App Attest is mandatory for the production app: GET /v1/attest/challenge (16+ random bytes, single use, Redis TTL about 5 min); POST /v1/attest (attestationObject, keyId), full verification including validation category 4 (App Store) or 2 (TestFlight) and bundle version, then store keyId, public key, counter=0 and receipt. On every POST /v1/passes require headers X-Attest-KeyId and X-Attest-Assertion over clientData = {challenge, sha256(body)}, and update the counter atomically (UPDATE ... SET counter=:new WHERE key_id=:k AND counter &lt; :new). (b) Quotas per attested key (for example 20 passes per hour and 100 per day), per IP at the edge, and a global circuit breaker or kill switch (feature flag) that stops all signing instantly. (c) The server picks serialNumber (uuid4), passTypeIdentifier, teamIdentifier and formatVersion; the client never sets webServiceURL, authenticationToken or NFC keys. (d) Alert on spikes and on many distinct keys per IP. (e) Make Sign in with Apple optional, for later per-user quotas and bans.

**Begründung:** Anyone who can call the endpoint signs passes under our Team ID, and Apple can revoke certificates at its discretion; revocation means 'passes will no longer function properly'. App Attest gives device and app genuineness without user accounts (no account-deletion duty, better GDPR posture). Quotas limit the damage from attested but malicious users.

### E5

**Empfehlung:** Implement App Attest verification in-house with cryptography + cbor2 (about 120 lines, code tested against Apple's official sample at docs/recherche/prototypen/appattest.py), pin the App Attest Root CA by fingerprint, and fix the API contract: the app sends clientDataHash = SHA256(challenge) for attestation and SHA256(clientData) for assertions.

**Begründung:** pyattest is maintained but skips the 2026 extension checks and the assertion rpId and counter checks, and pulls in python-jose. Apple's own sample deviates from the prose (raw challenge, ED flag unset), so a bespoke implementation with Apple's sample as a unit test is safer.

### E6

**Empfehlung:** Stateless signing for version 1: do not persist pass.json, barcode messages, names or images. Keep only the anti-abuse state (attested keyId, public key, counter, receipt, quota counters), retained for at most the app lifetime and deleted when inactive. Log in JSON (structlog 26.x or stdlib logging) with request_id, serial, style, a hash of keyId, latency and byte size, and never log barcode content, field values or images. Do not set webServiceURL or authenticationToken in version 1.

**Begründung:** Without server-push updates, Apple requires nothing to be stored server-side. This is GDPR Art. 5(1)(c) data minimisation and shrinks the breach impact to almost nothing.

### E7

**Empfehlung:** FastAPI shape: a sync `def create_pass(req: PassRequest, ...) -> Response` returning `Response(content=pkpass_bytes, media_type='application/vnd.apple.pkpass', headers={'Content-Disposition': f'attachment; filename="{serial}.pkpass"', 'Cache-Control': 'no-store'})`. Add `app.add_middleware(RequestBodyLimitMiddleware, max_body_size=256*1024)` (from starlette.middleware.body_limit, Starlette 1.6+), or about 3 MB if user images are uploaded. Use a pydantic v2 model with `ConfigDict(extra='forbid', str_strip_whitespace=True)`, Literal enums for style and barcode format, and max_length on all strings and lists. Use pydantic-settings BaseSettings with SecretStr, env_prefix and secrets_dir. Disable docs_url and openapi_url in production. Run Uvicorn behind the proxy with proxy headers enabled so per-IP limits see the real client IP. I verified this setup end to end: 200 with the pkpass media type, 422 for extra fields, 413 for oversized bodies.

**Begründung:** These are verified current APIs (FastAPI 0.143.0, Starlette 1.7.0, pydantic 2.14, pydantic-settings 2.15). Strict validation caps how much content an attacker can put inside a pass that we sign.

### E8

**Empfehlung:** Generate default images server-side with Pillow: icon.png, icon@2x.png and icon@3x.png at 38, 76 and 114 px (opaque square; the system rounds the corners), plus an optional transparent logo at 50 pt high, up to 160 pt wide, at @1x/@2x/@3x. Re-encode any client-supplied image: set MAX_IMAGE_PIXELS, call verify(), convert('RGBA'), thumbnail into the pt box × scale with LANCZOS, and save as PNG.

**Begründung:** The iOS 27 HIG and Apple's Pass Builder both specify a 38 pt icon. Re-encoding removes EXIF and GPS metadata and polyglot payloads, and caps file size.

### E9

**Empfehlung:** Hosting: an EU region with managed key custody. Preferred: Google Cloud Run in europe-west3 plus Cloud KMS (HSM protection level) plus Secret Manager, or AWS ECS Fargate or Lambda in eu-central-1 plus AWS KMS plus Secrets Manager, or Azure Container Apps in Germany West Central plus Key Vault Premium or Managed HSM. If a German-only provider is mandatory, confirm STACKIT KMS RSA-PKCS1 signing first; otherwise use Hetzner or IONOS with an encrypted software key loaded from a secrets store. Put a WAF or rate limiter (Cloud Armor, AWS WAF or Azure Front Door) in front, and run the signer under a dedicated service account that has sign-only IAM on the key.

**Begründung:** KMS signing is one remote call per pass (fine for this load), keeps the key non-exportable, and gives audit logs of every signature. EU regions keep processing inside the EU. The KMS adapter approach was verified locally.

### E10

**Empfehlung:** Write a certificate operations runbook: a yearly Pass Type ID rotation (create the new certificate before expiry, deploy, keep the old one until cut-over); export cert notAfter (leaf and WWDR G4) as Prometheus or Cloud Monitoring metrics with alerts at 60, 30 and 7 days; a compromise procedure (revoke in the portal and email product-security@apple.com, issue a new certificate, possibly a new Pass Type ID); and a separate Pass Type ID or certificate for dev and staging.

**Begründung:** Expiry silently stops all new pass creation; revocation breaks every issued pass. Both are predictable operational risks.

### E11

**Empfehlung:** If pass updates are wanted later, add the PassKit web service as a separate stateful service: v1 registration endpoints with `Authorization: ApplePass <token>`, per-pass random authenticationToken (at least 16 chars, 32 bytes of randomness recommended), stored devices, passes and registrations in an EU database, and APNs pushes (HTTP/2, production only, empty payload, topic = passTypeIdentifier) over mTLS with the Pass Type ID certificate. Decide early whether that key will live in KMS, because Python's ssl/httpx cannot do mTLS with a KMS key; you would need a PKCS#11 provider or proxy, or a software key for the APNs client.

**Begründung:** Apple's doc requires the push to use the same certificate and key that signed the pass. This is the main architectural coupling between choosing KMS custody and adding update support later.

## Fallstricke

1. Leaving out PKCS7Options.Binary: cryptography converts LF to CRLF before hashing, so any manifest with newlines (for example pretty-printed JSON) gets a signature that Wallet and openssl reject. Verified locally.
2. Using hashes.SHA1() with cryptography &gt;=39 raises TypeError (applepassgenerator still does this). The manifest digests stay SHA-1 (hashlib.sha1); only the CMS signature uses SHA-256.
3. Using PKCS7Options.NoAttributes removes signingTime. Apple's Pass Builder, OpenSSL and cryptography all include it by default. Whether Wallet strictly requires it is undocumented, so do not remove it.
4. Text with DER raises ValueError. Leaving out DetachedSignature produces an attached signature; edutap.wallet_apple does this by default, which does not follow Apple's 'detached' requirement.
5. Bundling the expired WWDR G1 (AppleWWDRCA.cer, expired 2023-02-07) or the wrong generation (G3 or G6). Pass Type ID certificates need G4, and the G4 intermediate itself expires in 2030.
6. openssl smime/cms -verify without -binary when verifying, or without -purpose any (or -noverify): you get false negatives that look like signing bugs.
7. The OpenSSL 3 CLI fails on legacy RC2-40 .p12 files from older Keychain exports unless -legacy is given. cryptography loads them fine.
8. Letting the client set passTypeIdentifier, teamIdentifier, serialNumber, webServiceURL or authenticationToken. Always derive or overwrite these on the server; a client-chosen serial lets an attacker overwrite another user's pass on the same device (same type plus serial means replace).
9. Using the old 29 pt icon size from older tutorials: the iOS 27 HIG and Apple's Pass Builder use 38x38 pt. The HIG and Pass Builder also disagree on background (343x503 vs 345x505) and footer (268x15 vs max 286x15).
10. Including .DS_Store or other non-pass files in the zip and manifest; putting the files in a subfolder inside the zip; leaving manifest entries out for files inside .lproj folders.
11. App Attest: following the doc prose blindly (SHA256 of the challenge) when the app actually passed something else; Apple's own sample uses the raw challenge bytes. Relying on the ED flag to parse extensions (Apple's sample has extensions with ED unset). Skipping the rpId and counter checks for assertions (pyattest's assertion verifier does not do them). Not handling serverUnavailable retries. Expecting App Attest in a share extension (only Action, extensible SSO and watchOS extensions are supported). Testing on the Simulator, where isSupported is false.
12. App Attest keys reset on reinstall, restore or migration, so counting keys per device is expected to grow a little. Do not ban on a single metric.
13. slowapi needs an explicit `request: Request` argument in every limited endpoint, and its redis extra pins redis&lt;4. Per-IP limits behind a proxy are useless unless Uvicorn trusts the forwarded headers.
14. The Sign in with Apple docs say 'JWS E256', but Apple publishes RSA keys: pin algorithms=['RS256'] and select the key by kid. Adding accounts triggers App Review 5.1.1(v) (in-app account deletion).
15. The KMS adapter relies on cryptography calling a Python-level sign() on custom RSAPrivateKey subclasses, which works in 50.0.2 but is undocumented. Pin the version and keep an integration test that verifies the output with openssl.
16. KMS custody plus future PassKit updates: APNs needs mTLS with the same Pass Type ID certificate, which plain Python ssl cannot do with a KMS key.
17. Certificate revocation, triggered by abuse or by Apple's discretion, breaks every pass already issued, unlike expiry. The public signing endpoint can therefore damage existing users' passes, not only future ones.
18. Apple's www.apple.com/certificateauthority pages (WWDR G4, App Attest root) could not be fetched from this research environment. Download them on a trusted machine and pin their fingerprints in the repository.

## Offene Fragen

1. What is the exact notAfter of AppleWWDRCAG4.cer? Apple only says '2030' (from memory 2030-12-10, unverified). Download it from https://www.apple.com/certificateauthority/AppleWWDRCAG4.cer and pin its SHA-256 fingerprint.
2. Does Wallet on iOS 26/27 strictly require the CMS signingTime attribute, and does it reject SMIMECapabilities? Neither is documented. The recommended output (contentType, signingTime, messageDigest) matches Apple's Pass Builder exactly, which avoids both questions.
3. Can a single Pass Type ID have two active certificates at the same time (one KMS-held key for signing, one software key for APNs mTLS, or overlapping rotation)? Unverified; ask Apple DTS or test in the portal.
4. Is the Pass Type ID certificate validity exactly 12 months? Apple's docs do not say; forum and vendor sources say about one year. Check the notAfter of the first certificate you issue.
5. Product and legal: since the server signs any barcode content the user enters, how do we handle impersonation (organizationName or logoText showing third-party brands) and forged tickets? This decides whether organizationName is fixed to 'QRCode2Wallet' or user-defined, and whether we need terms of use or brand filtering.
6. Fallback for devices or contexts without App Attest (isSupported == false, share extension): deny, require Sign in with Apple, or allow a much lower quota?
7. Hosting decision: a US hyperscaler EU region (GCP europe-west3, AWS eu-central-1, Azure Germany West Central) or a German provider (STACKIT, where RSA-PKCS1 signing support in KMS is unconfirmed; Hetzner or IONOS without managed KMS)? Depends on DSGVO/Schrems II risk appetite and budget.
8. Should the server also accept the new iOS 27 pass features (Poster Generic, new barcode formats, pass actions, the 'artwork' image)? The exact pass.json keys need a separate check against the Pass reference before the pydantic schema allows them.
9. Is calling Apple's Pass Builder (`buildpass validate` or `buildpass sign`, Swift, early preview, APIs may change) as a sidecar acceptable operationally, or should it be used only as a CI validation oracle?

## Faktencheck: alle geprüften Aussagen

### P1 · KORRIGIERT

**Geprüfte Aussage:** Apple's steps for building a pass: manifest.json maps each file path (e.g. en.lproj/logo.png) to its SHA-1 hex digest; PKCS #7 detached signature of manifest.json with the Pass Type ID private key; saved at the top level as `signature`; zip and rename to .pkpass; keep .DS_Store out; manifest is still SHA-1 in 2026, only the CMS signature uses SHA-256.

**Ergebnis:** The steps, the SHA-1-per-file manifest, the .lproj example and the .DS_Store note all match the current page. However, Apple's 'Building a Pass' page never mentions SHA-256, the CMS digest algorithm or the WWDR intermediate. It only says 'Create a PKCS #7 detached signature for the manifest that uses the private key of the pass identifier signing certificate.' SHA-256 comes from Apple's Pass Builder code (swift-certificates defaults to sha256WithRSAEncryption), not from the docs. The Pass Builder repo also uses Insecure.SHA1 for the manifest (Sources/PassBuilder/PassSigning/Manifest/Data+SHA1.swift), which independently confirms SHA-1.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/building-a-pass>

### P2 · BESTÄTIGT

**Geprüfte Aussage:** Common Problems: passTypeIdentifier must match the cert, teamIdentifier must match the account, cert not expired, required keys and images present, valid JSON. Required pass.json keys: formatVersion (=1), passTypeIdentifier, serialNumber, teamIdentifier, organizationName, description.

**Ergebnis:** Content is correct, but the 'Common Problems' list is on the Building a Pass page, not on the Pass reference page. The full list also covers: the signing machine has the certificate; the manifest includes files in subdirectories; images are in the correct format; ISO 8601 date values; localization folder names, pass.strings syntax and key parity. The six required keys and 'formatVersion: The value needs to be 1' are confirmed on the Pass reference page. Note: serialNumber is described as 'An alphanumeric serial number'. Also on the Pass page: `barcode` and `relevantDate` are deprecated (use `barcodes` and `relevantDates`), and many new keys arrived in 26.0 (e.g. upcomingPassInformation, managementURL, changeSeatURL).

**Quelle:** <https://developer.apple.com/documentation/walletpasses/building-a-pass>

### P3 · BESTÄTIGT

**Geprüfte Aussage:** Apple's Pass Builder (github.com/apple/pass-builder, Apache-2.0, early preview, Swift 6.3+, macOS 14+/Linux, WWDC26 session 209) signs with swift-certificates CMS.sign(manifest, additionalIntermediateCertificates:[wwdr], certificate:, privateKey:, signingTime: Date()), detached by default; RSA uses sha256WithRSAEncryption (PKCS#1 v1.5); signed attributes are exactly contentType, messageDigest, signingTime.

**Ergebnis:** Verified in the source: ManifestSignatureGenerator.swift calls CMS.sign as described (comment: 'detached: true is the default'). In swift-certificates CMSOperations.swift, signWithSigningTime adds exactly contentType, messageDigest and signingTime. CertificatePrivateKey.swift returns .sha256WithRSAEncryption for RSA, and Signature.swift uses _RSA.Signing.Padding.insecurePKCS1v1_5. Package.swift has swift-tools-version 6.3 and .macOS(.v14); the README says 'Early preview' and 'macOS 14+ or Linux'. WWDC26 session 209 'What's new in Wallet' introduces Pass Builder ('runs on Mac and Linux', CLI `buildpass`). Extra detail: Pass Builder signs only from a .p12 (it throws certificateInvalid otherwise) and tries an EC private key before RSA. `buildpass sign` therefore cannot use a KMS key; only `buildpass validate` fits a KMS design.

**Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassSigning/ManifestSignatureGenerator.swift>

### P4 · BESTÄTIGT

**Geprüfte Aussage:** WWDR generations: G2 Apple Pay ECDSA; G3 software signing; G4 APNs features incl. Pass Type ID, Pass Type ID with NFC, APNs SSL, Order Type ID, Website Push ID, WatchKit, VoIP; G5 App Store signing; G6 ECDSA software/services; G7 App Store receipt signing. Distributed at apple.com/certificateauthority (file AppleWWDRCAG4.cer).

**Ergebnis:** The table matches. Exact wording: G3 = 'Software signing and services' (also Swift Package Collection and Merchant Identity); G6 = 'ECDSA Signing - Software and Services' (Swift signing); G5 and G7 = 'Apple Managed certificates'. The page lists only G2 to G7, not G1 or G8. The file name AppleWWDRCAG4.cer and the design claim that bundling G3 or G1 makes Wallet reject the pass are NOT on the page (www.apple.com was unreachable), so treat both as unverified.

**Quelle:** <https://developer.apple.com/help/account/certificates/wwdr-intermediate-certificates>

### P5 · BESTÄTIGT

**Geprüfte Aussage:** Pass Type ID certs issued after Jan 27, 2022 chain to the WWDR G4 sub CA; Apple says the correct intermediate expires in 2030 and has 'G4' in the Organization field; notAfter believed to be 2030-12-10 (unverified).

**Ergebnis:** Apple's text is confirmed verbatim ('expiration date is set to 2030 and the Organization field is set to G4'). From a copy of the G4 certificate (bundled as test data in edutap.wallet_apple 1.0.0a5, not downloaded from Apple): subject 'CN=Apple Worldwide Developer Relations Certification Authority, OU=G4, O=Apple Inc., C=US', issuer Apple Root CA, notBefore 2020-12-16 19:36:04Z, notAfter 2030-12-10 00:00:00Z, SHA-256 fingerprint EA:47:57:88:55:38:DD:8C:B5:9F:F4:55:6F:67:60:87:D8:3C:85:E7:09:02:C1:22:E4:2C:08:08:B5:BC:E1:4C. So 'G4' is actually in the OU attribute, not O; check OU in code. Medium confidence: re-verify against Apple's PKI download.

**Quelle:** <https://developer.apple.com/support/expiration/>

### P6 · BESTÄTIGT

**Geprüfte Aussage:** cryptography 50.0.2 (2026-09-30) rejects SHA-1 in PKCS7SignatureBuilder.add_signer with TypeError, though the docs' PKCS7HashTypes still lists SHA1; the 39.0.0 changelog removed MD5/SHA1 in PKCS7.

**Ergebnis:** Reproduced with cryptography==50.0.2: 'TypeError: hash_algorithm must be one of hashes.SHA224, SHA256, SHA384, or SHA512'. The runtime PKCS7HashTypes alias excludes SHA1, but serialization.rst at tag 50.0.2 still lists SHA1. The 39.0.0 (2023-01-01) changelog says 'Support for using MD5 or SHA1 in CertificateBuilder, other X.509 builders, and PKCS7 has been removed.' Also note: 50.0.x wheels are compiled with OpenSSL 4.0.x (50.0.2: 4.0.3), while a typical CI `openssl` CLI is 3.x.

**Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/CHANGELOG.rst>

### P7 · KORRIGIERT

**Geprüfte Aussage:** PKCS7SignatureBuilder API and options (Text/Binary/DetachedSignature/NoCapabilities/NoAttributes/NoCerts); NoCapabilities makes the output match Apple's Pass Builder byte for byte in structure; Text+DER errors; NoAttributes cannot be combined with NoCapabilities.

**Ergebnis:** The API facts are confirmed: versionadded 3.2; rsa_padding versionadded 42.0.0 (None means PKCS1v15); add_certificate can be called repeatedly; Text+DER raises 'The Text option is only available for SMIME serialization'; NoAttributes+NoCapabilities raises 'NoAttributes is a superset of NoCapabilities'; NoCerts output fails `openssl cms -verify` with 'signer certificate not found'. WRONG: the output is not structurally identical to Pass Builder. cryptography writes SignerInfo.signatureAlgorithm = rsaEncryption (1.2.840.113549.1.1.1), while swift-certificates writes sha256WithRSAEncryption (1.2.840.113549.1.1.11). The certificate order also differs (swift-certificates puts the intermediates first, then the leaf). Both forms are valid CMS and both verify with OpenSSL. With NoCapabilities the signed attributes are contentType, signingTime and messageDigest (DER SET).

**Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/docs/hazmat/primitives/asymmetric/serialization.rst>

### P8 · BESTÄTIGT

**Geprüfte Aussage:** OpenSSL CLI equivalents: `openssl smime -sign -binary ... -outform DER`, or `openssl cms -sign -binary -md sha256 -nosmimecap ...` (detached by default); verify with `cms -verify -binary -noverify ... -content manifest.json`, or with -CAfile AppleRootCA.pem -purpose any; a one-byte change fails verification.

**Ergebnis:** Reproduced on OpenSSL 3.0.13 with a self-made root, intermediate and leaf chain. Both sign commands give eContent ABSENT (detached) and sha256 (smime also adds SMIMECapabilities). All verify commands succeed, a one-byte change fails ('verification failure'), and without `-purpose any` verification fails with 'unsuitable certificate purpose'. The cited Apple page contains no OpenSSL commands; the authoritative source is the OpenSSL docs. Not tested with a real Apple leaf certificate or Apple Root CA.

**Quelle:** <https://docs.openssl.org/3.0/man1/openssl-cms/>

### P9 · BESTÄTIGT

**Geprüfte Aussage:** Pass Type ID certs are valid about one year; Apple docs do not state the length; sources are a forum community answer and vendors.

**Ergebnis:** Thread 64215 contains only a 2016 community reply ('These certificates only last a year'), with no Apple staff. Apple's Certificates support page states no validity period. It does state: on expiry, 'passes that are already installed on users' devices will continue to function normally. However, you'll no longer be able to sign new passes or send updates to existing passes'; on revocation, 'your passes will no longer function properly'; 'Apple can revoke digital certificates at any time at its sole discretion'. The PassSlot '356 days' figure is unverified. Read notAfter from the actual certificate.

**Quelle:** <https://developer.apple.com/support/certificates/>

### P10 · BESTÄTIGT

**Geprüfte Aussage:** A .p12 encrypted with pbeWithSHA1And40BitRC2-CBC fails in the OpenSSL 3 CLI unless -legacy is given; cryptography's pkcs12.load_key_and_certificates loads it.

**Ergebnis:** Reproduced: OpenSSL 3.0.13 without -legacy fails with 'unsupported ... Algorithm (RC2-40-CBC : 0)'. With -legacy, both -clcerts -nokeys and -nocerts -nodes succeed. cryptography 50.0.2 load_key_and_certificates returns (RSAPrivateKey, cert, []). That macOS Keychain exports actually use RC2-40 was not verified.

**Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/docs/hazmat/primitives/asymmetric/serialization.rst>

### P11 · BESTÄTIGT

**Geprüfte Aussage:** Python library status: wallet-py3k 0.0.4 (2018, shells out to openssl smime); passbook 1.0.2 (2016); applepassgenerator 0.0.2 (2023-02, cryptography&lt;38, SHA1); py-pkpass 1.0.2 (2025-04, cryptography&gt;=44.0.1, SHA256+Detached, no Binary, swig dep); edutap.wallet_apple 1.0.0a5 (2026-08, attached signature); django-walletpass 5.0.1 (2026-04, Django); passes-rs-py 4.0.2 (2026-05, Python&gt;=3.12).

**Ergebnis:** All confirmed against PyPI JSON and the sdist source: upload dates, requires_dist (applepassgenerator 'cryptography (&gt;=37.0.2,&lt;38.0.0)'; py-pkpass 'swig; python_version &gt;= "3.10"'), applepassgenerator `hashes.SHA1()`, py-pkpass options [DetachedSignature] only, edutap sign_manifest passes `detached=False` (its docstring says 'Produces an \*attached\* signature'), wallet-py3k runs ['openssl','smime','-binary','-sign',...]. Extra: django-walletpass 5.0.1 signs with SHA256+DetachedSignature (no Binary), and its DEFAULT WWDR is the expired G1 'AppleWWDRCA' (notAfter 2023-02-07), so you must override it.

**Quelle:** <https://pypi.org/project/py-pkpass/>

### P12 · KORRIGIERT

**Geprüfte Aussage:** HIG image specs (2026-06-08 iOS 27 update): icon 38x38; logo 50-160x50; primaryLogo 30-126x30; secondaryLogo 12-135x12; strip 375x144; thumbnail 60-90x90; background.png 343x503 (non-poster) or 358x448 (poster); footer 268x15. Pass Builder: icon 38x38, background 345x505, artwork 358x448, footer max 286x15, logo max 160x50, primaryLogo max 126x30, secondaryLogo max 135x12, strip 375x144, thumbnail 90x90.

**Ergebnis:** Poster pass backgrounds are NOT background.png: the HIG lists filename `artwork.png` (358x448 pt) for poster event tickets and poster generic passes. background.png (343x503 pt) is listed only for (non-poster) event tickets. The HIG says 'Create pass images in PNG format in @2x and @3x format' (no 1x). All other HIG values and the 2026-06-08 change-log entry are confirmed. The Pass Builder values are confirmed in Sources/PassBuilder/PassPackage/PassPackage.swift. RequiredImagesValidator makes the icon mandatory: missing icon is an error; missing @2x or @3x is a warning. Note the HIG/Pass Builder mismatch for background (343x503 vs 345x505) and footer (268 vs max 286).

**Quelle:** <https://developer.apple.com/design/human-interface-guidelines/wallet>

### P13 · BESTÄTIGT

**Geprüfte Aussage:** Starlette 1.6.0 (2026-08-08) added max_body_size, backed by starlette.middleware.body_limit.RequestBodyLimitMiddleware(app, max_body_size:int); FastAPI 0.143.0 (starlette 1.7.0) has no constructor param but add_middleware works; 413 for 300 KB, 422 for extra field, 200 with application/vnd.apple.pkpass.

**Ergebnis:** Release notes: '1.6.0 (August 8, 2026) Add max_body_size to Starlette and route classes'. Reproduced with fastapi 0.143.0, starlette 1.7.0 and pydantic 2.14.0. Signature is (self, app, max_body_size: int); the Starlette and starlette Route constructors have max_body_size, while FastAPI and APIRoute do not. Results: 413, 422, 200 with the pkpass content type, and a chunked body without Content-Length also gets 413. Starlette 1.7.0 warns that using httpx with TestClient is deprecated (use httpx2).

**Quelle:** <https://github.com/Kludex/starlette/blob/main/docs/release-notes.md>

### P14 · KORRIGIERT

**Geprüfte Aussage:** App Attest server validation steps (x5c to root, nonce=SHA256(authData||clientDataHash) vs OID 1.2.840.113635.100.8.2, SHA256(point)==keyId, rpIdHash, counter 0, aaguid, credentialId, apple_validation_category_01 (4 App Store, 2 TestFlight, 3 dev) and apple_bundle_version_01); assertions: nonce, ECDSA signature, rpId, strictly increasing counter.

**Ergebnis:** The attestation steps are confirmed, including the validation category table (0 invalid, 1 OS executable, 2 TestFlight, 3 development, 4 App Store, 5 Enterprise/ad-hoc, 6 Developer ID, 10 other). The assertion list is incomplete. Apple's current doc also requires: (6) 'Verify that the embedded challenge in the client data matches the earlier challenge'; (7) verify validationCategory and (8) bundleVersion in the assertion's authenticator-data extensions. Counter rule: 'greater than the value from the previous assertion, or greater than 0 on the first assertion'. Also required: store one (key, receipt) pair per device, keep development and production pairs separate, ensure the public key is not already associated with another user, and verify and store the receipt immediately after attestation.

**Quelle:** <https://developer.apple.com/documentation/devicecheck/validating-apps-that-connect-to-your-server>

### P15 · BESTÄTIGT

**Geprüfte Aussage:** Apple's Attestation Object Validation Guide sample passes a cryptography+cbor2 verifier; quirks: composite uses RAW challenge; flags 0x40 yet an extensions map follows; apple_validation_category_01 is a 4-byte LE byte string (1) and apple_bundle_version_01 is '1' not '1.0'; leaf valid 2026-04-20 to 2026-04-23.

**Ergebnis:** Reproduced all of it: nonce matches SHA256(authData||b'example_server_challenge') and not SHA256(authData||SHA256(challenge)); flags 0x40; ext = {'apple_bundle_version_01': '1', 'apple_validation_category_01': b'\x01\x00\x00\x00'}; leaf valid 2026-04-20T18:13:12Z to 2026-04-23T18:13:12Z; chain verifies. A FOURTH quirk the researcher missed: the guide's 'Expected public key SHA256 hash' (inGjK2JbaAEhAsYwCns2zTyZDzsJ3OKx3Q2nnxk+mkY=) matches neither SHA256(uncompressed point), which equals keyId zgSY9YSD..., nor SHA256(SPKI). Compare against keyId, not that printed value. The guide's 'Expected clientDataHash' is actually the composite authData||challenge, not a hash.

**Quelle:** <https://developer.apple.com/documentation/devicecheck/attestation-object-validation-guide>

### P16 · BESTÄTIGT

**Geprüfte Aussage:** Apple App Attestation Root CA: CN=Apple App Attestation Root CA, O=Apple Inc., ST=California, valid 2020-03-18 to 2045-03-15, SHA-256 1C:B9:82:3B:...:C9:32 (from pyattest 1.0.5 copy); SKI AC:91:10:53...8A:A1 matches the AKI of 'Apple App Attestation CA 1' (valid until 2030-03-13).

**Ergebnis:** Values reproduced from the pyattest copy (notAfter 2045-03-15 00:00:00Z, SKI ac91105333bdbe6841ffa70ca9e5faeae5e58aa1). Stronger evidence: the intermediate embedded in Apple's official guide verifies cryptographically (verify_directly_issued_by) against this root, and its notAfter is 2030-03-13. The download from www.apple.com was not possible from this environment.

**Quelle:** <https://developer.apple.com/documentation/devicecheck/attestation-object-validation-guide>

### P17 · BESTÄTIGT

**Geprüfte Aussage:** pyattest 1.0.5 (2026-07-14; deps cbor2, pyhanko_certvalidator, pyjwt, python-jose[cryptography], cryptography) bundles the root; lacks the validation_category/bundle_version checks; AppleAssertionVerifier only checks the signature; the attestation verifier always computes SHA256(challenge).

**Ergebnis:** Confirmed in the sdist. AppleAssertionVerifier.verify computes sha256(authenticatorData + expected_hash) and checks the ECDSA signature only (it unpacks rp_id and counter but never checks them). The attestation code has `client_data_hash = auth_data + sha256(nonce).digest()`, so it cannot verify Apple's own sample. There is no handling of extensions or receipts. AppleAttestationVerifier.verify is async (awaits pyhanko chain validation).

**Quelle:** <https://pypi.org/project/pyattest/>

### P18 · BESTÄTIGT

**Geprüfte Aussage:** App Attest fraud metric: POST base64 receipt with Authorization: &lt;JWT&gt; to data-development / data.appattest.apple.com/v1/attestationData; fields 2, 12 (&lt;=5 min), 6, 17 (30-day key count), 19 (304 if early); keys don't survive reinstall/restore/migration; DCAppAttestService iOS 14.0+, isSupported; only Action, extensible SSO and watchOS extensions; millions-DAU apps must ramp up.

**Ergebnis:** All confirmed in Apple's current docs. Missing details: receipts must be verified (signature, chain up to Apple Root CA - G3, field 3 attested public key matches the stored key); field 21 = expiration time, after which Apple 'might not honor the request', so refresh periodically; response codes 400 Incorrect Environment, 401, 404, 429. Apple recommends one key 'for each user account on each device'.

**Quelle:** <https://developer.apple.com/documentation/devicecheck/assessing-fraud-risk>

### P19 · BESTÄTIGT

**Geprüfte Aussage:** Sign in with Apple: GET https://appleid.apple.com/auth/keys (JWKSet, kty RSA, pick by kid, set changes); verify iss, aud == client_id, exp, nonce (mandatory if nonce_supported true); prose says 'JWS E256' but keys are RSA so RS256 in practice.

**Ergebnis:** Confirmed: the endpoint and 'The endpoint can return multiple keys, and the count of keys can vary over time... select the key with the matching key identifier (kid)'. JWKSet.Keys says kty 'You must set to "RSA"'. The 'Verifying a user' page literally says 'Verify the JWS E256 signature'. The nonce_supported semantics come from secondary copies of Apple's docs (the official page was not fetched), so medium confidence on that point. appleid.apple.com itself was unreachable from here.

**Quelle:** <https://developer.apple.com/documentation/signinwithapplerestapi/fetch-apple's-public-key-for-verifying-token-signature>

### P20 · BESTÄTIGT

**Geprüfte Aussage:** App Review Guideline 5.1.1(v): 'If your app supports account creation, you must also offer account deletion within the app.'

**Ergebnis:** Quote is verbatim. The same guideline also says: 'If your app doesn't include significant account-based features, let people use it without a login.' The same document has Wallet-specific rules the researcher missed (1.5 and 3.2.1(iv)); see missing facts.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P21 · BESTÄTIGT

**Geprüfte Aussage:** slowapi 0.1.10 (2026-06-13) wraps limits; endpoint needs an explicit request: Request argument; the redis extra pins redis&lt;4.0.0,&gt;=3.4.1; limits 5.8.0 (2026-02) supports Redis and memory.

**Ergebnis:** Confirmed (PyPI requires_dist; README: 'The request argument must be explicitly passed to your endpoint'). Caveat for the recommendation: limits 5.8.0's own `redis` extra pins 'redis!=4.5.2,!=4.5.3,&lt;8.0.0,&gt;3', while the current redis-py is 8.1.0 (2026-07-30). 'Current redis' therefore means redis-py 7.x under limits. slowapi without its redis extra can use limits' Redis storage via storage_uri.

**Quelle:** <https://pypi.org/project/slowapi/>

### P22 · BESTÄTIGT

**Geprüfte Aussage:** PassKit web service: webServiceURL + authenticationToken; endpoints POST/GET/DELETE registrations, GET /v1/passes/..., POST /v1/log; Authorization: ApplePass &lt;token&gt;; push with the same cert/key that signed the original, the push token and an empty JSON payload, production only; device/pass/registration tables; HTTPS mandatory in production.

**Ergebnis:** All confirmed, including the query string `?passesUpdatedSince={previousLastUpdated}` and register responses 200 (already registered), 201 and 401. Also: 'You can update any type of pass and any information in the pass, except for the authentication token and the serial number'; the serial-numbers endpoint is authenticated by the deviceLibraryIdentifier, not the token; HTTP is allowed during testing; delete the device when APNs reports an invalid token.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/adding-a-web-service-to-update-passes>

### P23 · BESTÄTIGT

**Geprüfte Aussage:** cryptography 50.0.2 PKCS7SignatureBuilder.add_signer and CertificateSigningRequestBuilder.sign accept a Python subclass of rsa.RSAPrivateKey and call sign(data, padding, algorithm) with the DER SET of signed attributes (164 bytes, 0x31), PKCS1v15, SHA256; remote prehashed signing verifies with openssl; not a documented contract.

**Ergebnis:** Reproduced with 50.0.2. PKCS7 calls sign() once with the DER SET (first byte 0x31): 164 bytes with default options, 107 bytes with NoCapabilities (the option the researcher recommends). Padding is PKCS1v15 and the hash SHA256. The CSR builder calls sign() with the 317-byte TBS (0x30); the CSR passes `openssl req -verify`; the signature passes `openssl cms -verify`. This behaviour is undocumented, so pin the version and keep an integration test.

**Quelle:** <https://github.com/pyca/cryptography/blob/50.0.2/docs/hazmat/primitives/asymmetric/serialization.rst>

### P24 · BESTÄTIGT

**Geprüfte Aussage:** AWS KMS Sign with MessageType=DIGEST skips hashing and the message must have the digest length; RSASSA_PKCS1_V1_5_SHA_256 supported (AWS prefers PSS); GCP KMS has RSA_SIGN_PKCS1_2048_SHA256.

**Ergebnis:** Verified from AWS's official botocore service model (kms 2014-11-01). SigningAlgorithmSpec includes RSASSA_PKCS1_V1_5_SHA_256. MessageType: 'When the value is DIGEST, KMS skips the hashing step... the length of the Message value must match the length of hashed messages'. Message is 0 to 4096 bytes, so the 107-byte signed-attribute SET could also be sent RAW. SigningAlgorithm doc: 'RSASSA-PSS algorithms are preferred. We include RSASSA-PKCS1-v1_5 algorithms for compatibility'. GCP googleapis resources.proto: 'RSASSA-PKCS1-v1_5 with a 2048 bit key and a SHA256 digest. RSA_SIGN_PKCS1_2048_SHA256 = 5', ProtectionLevel HSM = 2; AsymmetricSignRequest takes a digest. Availability in the Frankfurt regions was not verified.

**Quelle:** <https://raw.githubusercontent.com/boto/botocore/develop/botocore/data/kms/2014-11-01/service-2.json>

### P25 · KORRIGIERT

**Geprüfte Aussage:** STACKIT KMS is GA, v1beta removed after 2025-10-15; RSA keys exist but only AES-256-GCM and RSA-OAEP are listed; RSASSA-PKCS1-v1_5 signing unconfirmed.

**Ergebnis:** From STACKIT's official SDKs (stackit-sdk-go and stackit-sdk-python, services/kms): Purpose includes 'asymmetric_sign_verify', but the Algorithm enum is aes_256_gcm, rsa_2048/3072/4096_oaep_sha256, rsa_4096_oaep_sha512, hmac_sha256/384/512, ecdsa_p256_sha256/p384_sha384/p521_sha512. RSA appears only as OAEP encryption, so RSA-PKCS1 signing (needed for a standard RSA Pass Type ID key) is not offered; only ECDSA signing is. SDK changelog: 'v1betaapi: This API was removed after the announced deprecation period' and 'hsm' key protection is 'Only as private preview feature available'. The GA status and the 2025-10-15 date were not verified (docs.stackit.cloud unreachable). Whether Apple issues Pass Type ID certificates for EC CSRs is unverified (Pass Builder does try EC keys first).

**Quelle:** <https://raw.githubusercontent.com/stackitcloud/stackit-sdk-go/main/services/kms/model_algorithm.go>

## Vom Faktenprüfer ergänzte wichtige Fakten

1. BLOCKER, legal (Apple Developer Program License Agreement, last updated 2026-08-18, Attachment 5 §1): 'You may distribute Your Pass Type ID as incorporated into Your Pass ... only so long as such distribution is under Your own trademark or brand, or if You reference a third party's trademark or brand within Your Pass ... You represent and warrant that You have any necessary rights. You agree not to share, provide or transfer Your Pass Type ID to any third party ... nor use Your Pass Type ID to sign a third party's pass.' Converting other companies' tickets and loyalty cards into passes signed with OUR Pass Type ID conflicts with this. Section 1.2 also defines Passes as 'developed by You ... under Your own trademark or brand'. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
2. BLOCKER, App Review (Guideline 1.5): 'ensure that Wallet passes include valid contact information from the issuer and are signed with a dedicated certificate assigned to the brand or trademark owner of the pass.' Guideline 3.2.1(iv): 'Wallet passes can be used to make or receive payments, transmit offers, or offer identification (such as movie tickets, coupons, and VIP credentials). Other uses may result in the rejection of the app and the revocation of Wallet credentials.' A revoked Pass Type ID breaks EVERY issued pass ('your passes will no longer function properly'), so this is an existential risk for a single shared signing certificate. Get legal review and Apple clarification before building. Mitigations to consider: generic, unbranded 'personal' passes with no third-party logos or trademarks and our own organizationName, and/or a pre-launch contact with Apple. Source: https://developer.apple.com/app-store/review/guidelines/
3. DPLA Attachment 5 §2.3: 'You agree to state on the Pass the name and address, and the contact information (telephone number; email address) to which any end user questions, complaints, or claims with respect to Your Pass should be directed' and 'You may not charge any fees to end users in order to use Wallet to access Your Pass.' The server must inject our company name, address, phone and email (e.g. as back fields) into every pass, and the monetization model must not charge for Wallet access to a pass. §3.1 requires choosing the relevant template ('You will not use the boarding pass template for a movie ticket'), so the style mapping must be semantically correct. §3.3 forbids linking pass data for targeted advertising or sharing it with data brokers. §4 lets Apple review, reject or revoke 'for any reason and at any time'. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
4. Competition and possible obsolescence: secondary sources (MacRumors, AppleInsider, Tom's Guide, iGeeksBlog, June 2026) and Apple support article 127821 ('Create a pass using Siri Mode in Apple Wallet') report that iOS 27 Wallet has a built-in 'Create a Pass' option (+ menu: Standard, Membership and Event templates; scanning via Visual Intelligence, reportedly on newer devices or with Apple Intelligence; manual entry otherwise). This overlaps the core value of QRCode2Wallet. support.apple.com was unreachable from here, so verify the details. Source: https://support.apple.com/en-gb/127821
5. iOS 27 pass format changes the signing backend's pass.json schema must handle (WWDC26 session 209): new `posterGeneric` style (iOS 27+; include `generic` alongside it for iOS 26 and earlier); new barcode formats PKBarcodeFormatEAN13, Code 39, PKBarcodeFormatCodabar and ITF in `barcodes` ('If you only provide one of the new barcode types and nothing else, the pass will not render a barcode on iOS 26 and earlier'); `featuredActions` array (max 2 per pass). Many retail loyalty cards use EAN-13 or Code 39, so the server must gate them by minimum iOS version or decide on a fallback. Source: https://developer.apple.com/videos/play/wwdc2026/209
6. Certificate expiry vs revocation (Apple support page): when the Pass Type ID certificate expires, installed passes keep working, but you can no longer sign new passes or send updates. Revocation breaks installed passes, and Apple may revoke 'at any time at its sole discretion'. If a compromise is suspected, email product-security@apple.com and request an additional certificate. Source: https://developer.apple.com/support/certificates/
7. Poster passes use `artwork.png` (358x448 pt), not background.png. background.png (343x503 pt in the HIG, 345x505 in Pass Builder) is for non-poster event tickets. The researcher's image recommendation and validator must include artwork.png. Source: https://developer.apple.com/design/human-interface-guidelines/wallet
8. Apple's Pass Builder confirms the researcher's certificate-attribute extraction: passTypeIdentifier = subject attribute OID 0.9.2342.19200300.100.1.1 (UID), Team ID = OID 2.5.4.11 (OU) (PassCertificate+Attributes.swift). Pass Builder signing accepts only a .p12 bundle, so with a KMS key only `buildpass validate` (not `buildpass sign`) can be used in CI. Source: https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassSigning/PassCertificate%2BAttributes.swift
9. App Attest sample quirk not reported by the researcher: the 'Expected public key SHA256 hash' printed in Apple's Attestation Object Validation Guide (inGjK2JbaAEhAsYwCns2zTyZDzsJ3OKx3Q2nnxk+mkY=) does not equal SHA256 of the 65-byte uncompressed point, which equals keyId zgSY9YSD..., nor SHA256(SPKI). Unit tests must assert against keyId. App Attest assertions must also check the challenge embedded in clientData and the validationCategory and bundleVersion extensions, per Apple's current doc. Source: https://developer.apple.com/documentation/devicecheck/attestation-object-validation-guide
10. If German-only hosting with STACKIT is required: STACKIT KMS (official SDK enums) offers only ECDSA P-256/P-384/P-521 for signing, with RSA only as OAEP encryption, and HSM protection is in private preview. An RSA Pass Type ID key therefore cannot live in STACKIT KMS. An EC Pass Type ID key would be needed (Apple's acceptance of EC CSRs for Pass Type IDs is unverified), or an encrypted software key. Source: https://raw.githubusercontent.com/stackitcloud/stackit-sdk-python/main/services/kms/src/stackit/kms/models/algorithm.py
11. django-walletpass 5.0.1 ships the expired WWDR G1 (AppleWWDRCA, notAfter 2023-02-07) as its default APPLE_WWDRCA_CERT_PATH. Several pass libraries omit the Binary option (py-pkpass, django-walletpass), which matters only if manifest bytes contain LF that could be converted. Source: https://pypi.org/project/django-walletpass/
12. Rate-limit dependency detail: limits 5.8.0's redis extra requires redis-py &lt;8.0.0 while redis-py 8.1.0 is current, so pin redis-py 7.x if using limits with Redis. Source: https://pypi.org/project/limits/
13. cryptography 50.0.x wheels bundle OpenSSL 4.0.x (50.0.2: OpenSSL 4.0.3), while CI `openssl cms -verify` typically runs OpenSSL 3.x. Keep both in the test matrix. Source: https://github.com/pyca/cryptography/blob/50.0.2/CHANGELOG.rst
