# Recherche-Prototypen

> **Status: Recherche-Prototypen, nicht produktionsreif.** Die Skripte sind während der Recherche entstanden. Sie zeigen, dass die zentralen technischen Annahmen funktionieren. Für das MVP-Backend werden sie sauber neu umgesetzt, mit Tests, Typisierung, Konfiguration und Fehlerbehandlung. Die bekannten Lücken stehen unten.

## Inhalt

| Datei | Zweck |
|---|---|
| `pkpass.py` | Minimaler .pkpass-Builder: `PassSigner` lädt `.p12` und WWDR, liest `passTypeIdentifier` und `teamIdentifier` aus dem Zertifikat und erzeugt die abgelöste PKCS#7-Signatur (DER, SHA-256, `DetachedSignature` + `Binary`). `build_pkpass()` erstellt Manifest (SHA-1) und ZIP. |
| `images.py` | Standard-Icon (38 pt @1x/@2x/@3x) und Logo per Pillow. Nutzerbilder werden neu kodiert (Schutz vor Dekompressionsbomben, EXIF entfernt). |
| `app.py` | FastAPI-Skizze `POST /v1/passes`: strikte pydantic-Validierung (`extra="forbid"`), Body-Limit 256 KB, Seriennummer vom Server, Logging ohne Inhalte. |
| `appattest.py` | App-Attest-Prüfung (Attestierung und Assertion) mit `cryptography` und `cbor2` |
| `mkpki.py` | Erzeugt eine **Wegwerf-Test-PKI**, die Apples Kette nachbildet (Root → „WWDR“ → Pass Type ID). Damit lässt sich ohne Apple-Account testen. |
| `test_sign.py` | Signiert einen Testpass und probiert Optionsvarianten durch: SHA-1 wird abgelehnt, Text+DER wird abgelehnt usw. |
| `test_app.py` | Testet die API-Skizze: 200 mit gültigem .pkpass, 422 bei unerlaubtem Zusatzfeld (`passTypeIdentifier`), 413 bei Übergröße |
| `test_extkey.py` | Zeigt, dass ein **KMS-/HSM-Schlüssel** (nur `sign()` remote) für PKCS#7 und für die CSR an Apple funktioniert |
| `test_assert.py` | Assertion-Prüfung: gültig, Replay abgelehnt, manipulierte Client-Daten abgelehnt |
| `test_appattest.py` | Attestierung gegen **Apples offiziellen Beispielvektor**. Falsche Challenge und abgelaufenes Zertifikat werden abgelehnt. |
| `testdaten/apple-app-attest-beispielvektor.json` | Beispiel-Attestierung aus Apples „Attestation Object Validation Guide“ |
| `testdaten/Apple_App_Attestation_Root_CA.pem` | Öffentliches Root-Zertifikat von Apple für App Attest, SHA-256-Fingerprint `1C:B9:82:3B:A2:8B:A6:AD:2D:33:A0:06:94:1D:E2:AE:4F:51:3E:F1:D4:E8:31:B9:F7:E0:FA:7B:62:42:C9:32`. Offizielle Quelle: <https://www.apple.com/certificateauthority/> |

## Ausführen

Voraussetzung: Python ≥ 3.11 und `openssl`.

```bash
cd docs/recherche/prototypen
python3 -m venv .venv && . .venv/bin/activate
pip install "cryptography>=50,<51" fastapi pydantic pydantic-settings pillow httpx cbor2

T=$(mktemp -d)                      # Arbeitsverzeichnis für Test-PKI und Ausgaben
python mkpki.py "$T"                # Wegwerf-Zertifikate erzeugen (NICHT committen)
python test_sign.py "$T"            # signiert $T/out.pkpass
openssl cms -verify -binary -inform DER -in "$T/out/signature" \
  -content "$T/out/manifest.json" -CAfile "$T/root.pem" -purpose any -out /dev/null
python test_app.py "$T"             # FastAPI-Skizze
python test_extkey.py "$T"          # KMS-Adapter
python test_assert.py               # App-Attest-Assertion
python test_appattest.py testdaten/apple-app-attest-beispielvektor.json \
  testdaten/Apple_App_Attestation_Root_CA.pem
```

## Verifizierte Ergebnisse (10.10.2026)

Getestet mit Python 3.13, cryptography 50.0.2, FastAPI 0.143, Starlette 1.7, pydantic 2.14, Pillow 12.3 und OpenSSL 3.0.13:

```
passTypeIdentifier pass.com.example.test team ABCDE12345
zip entries ['pass.json', 'icon.png', 'icon@2x.png', 'manifest.json', 'signature']
SHA1 rejected: TypeError hash_algorithm must be one of hashes.SHA224, SHA256, SHA384, or SHA512
Text with DER rejected: The Text option is only available for SMIME serialization
CMS Verification successful
200 application/vnd.apple.pkpass attachment; filename="<uuid>.pkpass" 7434
['icon.png', 'icon@2x.png', 'icon@3x.png', 'logo.png', 'logo@2x.png', 'logo@3x.png', 'manifest.json', 'pass.json', 'signature']
extra field -> 422
oversize -> 413
custom key accepted
CSR signature valid: True
counter -> 1
replay rejected: counter replay
tampered clientData rejected: InvalidSignature
OK 0 1 1 3977 receipt bytes
wrong challenge rejected: nonce
expired leaf (now) rejected: certificate not valid at verification time
```

**Grenze:** Diese Tests beweisen die kryptografische Korrektheit gegen eine Test-PKI. Ob Wallet einen Pass annimmt, zeigt sich erst mit einem **echten Pass-Type-ID-Zertifikat auf einem iPhone oder im Simulator**.

## Bekannte Lücken (für die MVP-Umsetzung)

- `appattest.verify_assertion` prüft noch **nicht**: die Challenge in den Client-Daten, `validationCategory`/`bundleVersion` in den Erweiterungen der Assertion, Schlüssel pro Gerät, getrennte Dev-/Prod-Schlüssel. Siehe Korrektur in [03-signierung-backend.md](../03-signierung-backend.md#korrekturen-aus-dem-faktencheck).
- `appattest.verify_attestation` prüft die Validierungskategorie (4 = App Store, 2 = TestFlight) nicht verbindlich. Zur Typprüfung nutzt es `assert`, das in optimiertem Python entfällt.
- `app.py` wählt die Seriennummer immer neu. Bearbeiten und Ersetzen eines Passes ist damit nicht möglich (siehe Zielkonflikt 4 in der [Übersicht](../README.md#4-zielkonflikte)).
- `app.py` hat keine Authentifizierung, keine Quoten, keine Pflicht-Rückseite mit Ausstellerdaten und keine Barcode-Validierung (Prüfziffern, Zeichensätze, Längen).
- `images.py` erzeugt @1x-Bilder. Laut HIG reichen @2x/@3x, @1x schadet aber nicht.
- Unter Starlette 1.7 erzeugt `TestClient` mit `httpx` eine Deprecation-Warnung. Im MVP berücksichtigen.
