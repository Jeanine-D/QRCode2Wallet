# Handoff – QRCode2Wallet

**Stand:** 11.10.2026 · **Branch:** `claude/qrcode2wallet-mvp` (Basis: `main`) · **Letzter inhaltlicher Commit:** `e0d073e` (Recherche)

Dieses Dokument richtet sich an alle, die das Projekt übernehmen oder später fortsetzen: eine neue Claude-Session, Entwickler oder den Product Owner selbst. Es beschreibt, was entschieden und erledigt ist, was offen ist und wie es weitergeht.

---

## 1. Kurzfassung

- **Produkt:** Native **iOS-App** (SwiftUI) für den öffentlichen App Store. Sie wandelt Tickets, Kundenkarten, Bordkarten, Coupons und Mitgliedskarten aus Foto, Screenshot, PDF oder Live-Kamera in **Apple-Wallet-Pässe (.pkpass)** um. Ein **Python-Backend (FastAPI)** signiert die Pässe.
- **Stand:** **Phase 1 (Recherche) ist abgeschlossen**, gegengeprüft und gepusht. **Phase 2 (Konzept + MVP) hat noch nicht begonnen.**
- **Warum Pause:** Der Product Owner hat ausdrücklich angewiesen, nach der Recherche alles ins Repo zu schreiben und zu **warten**. Vor jeder Umsetzung braucht es eine **ausdrückliche Freigabe** und die Antworten auf die [offenen Entscheidungen](#6-offene-entscheidungen).
- **Nächster Schritt:** Freigabe und Entscheidungen einholen → API-Vertrag festschreiben → Backend, iOS-App und Konzept umsetzen → gegenprüfen → fertigstellen.

---

## 2. Beteiligte und Arbeitsweise

| Rolle | Wer | Hinweise |
|---|---|---|
| Product Owner | Repo-Owner (GitHub `Jeanine-D`) | Senior ERP-Projektmanagement mit über 10 Jahren Erfahrung, programmiert hauptsächlich Python. Kommunikation auf **Deutsch**. |
| Umsetzung bisher | Claude Code (Cloud-Session) | Recherche als Multi-Agent-Workflow: 5 Recherche-Agents und 5 unabhängige Faktenprüfer |

**Sprachregel:** Dokumentation auf Deutsch, Code, Bezeichner und Code-Kommentare auf Englisch.

---

## 3. Getroffene Entscheidungen

| Datum | Frage | Entscheidung | Herkunft |
|---|---|---|---|
| 10.10.2026 | Wallet-Plattform | **Nur Apple Wallet** (kein Google Wallet) | Product Owner |
| 10.10.2026 | App-Form | **Native Mobile-App**. Da nur Apple Wallet unterstützt wird: **iOS mit SwiftUI** | Product Owner, technisch abgeleitet |
| 10.10.2026 | Zielgruppe | **Öffentliches Produkt** (viele Nutzer, App Store) | Product Owner |
| 10.10.2026 | Lieferumfang | **Konzept + lauffähiges MVP** | Product Owner |
| 10.10.2026 | Signierung | **Serverseitig in Python (FastAPI).** Der private Schlüssel des Pass Type ID darf nie in die App, sonst kann ihn jeder auslesen und in unserem Namen signieren. | technisch zwingend |
| 10.10.2026 | Git | `main` als Basis (nur `.gitignore`), Arbeit auf `claude/qrcode2wallet-mvp`. **Kein Pull Request**, solange der Product Owner keinen verlangt. | Claude (Konvention) |
| 10.10.2026 | Ablauf | „Nach der Recherche alles ins Repo schreiben und warten“ | Product Owner, ✅ erledigt |
| 11.10.2026 | Handoff | Dieses Dokument | Product Owner |

---

## 4. Repo-Stand

```
QRCode2Wallet/
├── README.md                     Projektüberblick, Status, Grundsatzentscheidungen
├── HANDOFF.md                    dieses Dokument
├── .gitignore                    schließt Signiermaterial (*.p12, *.pem, *.key, *.cer, .env) aus;
│                                 Ausnahme: öffentliches App-Attest-Root-Zertifikat (Testdaten)
└── docs/recherche/
    ├── README.md                 ★ deutsche Management-Zusammenfassung (Einstieg!)
    ├── 01-pass-format.md         .pkpass-Aufbau, pass.json, Stile, Barcodes, Bilder, iOS 27
    ├── 02-ios-apis.md            VisionKit, Vision, PDFKit, PassKit, SwiftData, App Attest, XcodeGen
    ├── 03-signierung-backend.md  PKCS#7 in Python, Zertifikate, FastAPI, App Attest, KMS, Hosting
    ├── 04-barcodes.md            Symbologien in der Praxis, Umwandlungsregeln, Binärdaten
    ├── 05-recht-produkt.md       Apple-Lizenzvertrag, Review-Richtlinien, DSGVO, Marken, Markt
    ├── rohdaten/recherche-ergebnisse.json   vollständige Rohdaten (ca. 430 KB)
    └── prototypen/               verifizierte Recherche-Prototypen (nicht produktionsreif)
        ├── README.md             Inhalt, Ausführung, Testergebnisse, bekannte Lücken
        ├── pkpass.py, images.py, app.py, appattest.py, mkpki.py
        ├── test_*.py
        └── testdaten/            Apples App-Attest-Beispielvektor + Root-CA (öffentlich)
```

Die Verzeichnisse `backend/` und `ios/` existieren noch nicht. Sie sind geplant, siehe [Abschnitt 7](#7-geplanter-ablauf-phase-2).

**Git-Historie:**

| Commit | Branch | Inhalt |
|---|---|---|
| `8625655` | `main`, `claude/qrcode2wallet-mvp` | Initial commit: `.gitignore` |
| `e0d073e` | `claude/qrcode2wallet-mvp` | Recherche, Prototypen, README |

---

## 5. Wichtigste Erkenntnisse

Die Details mit Quellen stehen in [docs/recherche/README.md](docs/recherche/README.md).

1. **Aktuell ist iOS 27** (WWDC26, Juni 2026). Neu sind der Stil `posterGeneric`, die Barcode-Formate EAN-13, Code 39, Codabar und ITF, Fallback-Listen mit mehreren Barcodes, `featuredActions` sowie neue PassKit-APIs zum Hinzufügen.
2. **iOS 27 kann in Wallet selbst Pässe erstellen.** Das ist das größte Produktrisiko. Das Produkt muss sich abheben: PDF- und Mehrfach-Tickets, Bahn- und Flugtickets, automatische Felderkennung, iOS 26 und Datenschutz.
3. **Plattformregeln** (DPLA Anlage 5 §1/§2.3, Guideline 1.5) erzwingen ein **Issuer-Modell**: Jeder Pass ist eine persönliche digitale Kopie unter der eigenen Marke, ohne Fremdlogos und mit eigenen Kontaktdaten auf der Rückseite. Eine Ablehnung im App Review bleibt möglich.
4. **Barcodes:** Bis iOS 26 nur QR, PDF417, Aztec und Code 128, Apple Watch ohne Code 128. Deshalb: Originalformat zuerst, dann Fallback, `altText` immer setzen. Die Regeltabelle steht in [04 E2](docs/recherche/04-barcodes.md#e2).
5. **Binäre Bahntickets** (UIC 918.3) gehen über `payloadData` und `messageEncoding: "iso-8859-1"`. Apple dokumentiert das nicht, also gilt es als **experimentell**, bis Gerätetests es bestätigen.
6. **Nicht konvertierbar:** dynamische und rotierende Codes (z. B. Ticketmaster SafeTix), reine NFC-Karten.
7. **Die Signierung ist das wichtigste Gut des Systems.** Bei Missbrauch kann Apple das Zertifikat widerrufen, dann funktionieren alle Pässe nicht mehr richtig. Für die Produktion: App Attest, Quoten, Not-Aus und ein Schlüssel im KMS/HSM in einer EU-Region.
8. **Die Signierung ist verifiziert.** Etwa 70 Zeilen mit `cryptography`, `PKCS7Options.Binary` ist Pflicht, WWDR **G4**, Manifest mit SHA-1. Externe Pass-Pakete sind veraltet oder fehlerhaft.
9. **Der App-Name „QRCode2Wallet“ ist ein Markenrisiko** („QR Code“ gehört DENSO WAVE, „Wallet“ ist Apples App-Name). Bis auf Weiteres bleibt er Arbeitstitel.

---

## 6. Offene Entscheidungen

Die vollständige Tabelle mit Begründungen steht in [docs/recherche/README.md, Abschnitt 5](docs/recherche/README.md#5-offene-entscheidungen-für-den-product-owner). Für den **Start des MVP** sind diese Punkte relevant:

| # | Entscheidung | Empfehlung | Blockiert MVP-Start? |
|---|---|---|---|
| 1 | Produktfokus angesichts der Wallet-Funktion in iOS 27 | Fokus auf Fälle, die Wallet nicht abdeckt | **Ja.** Bestimmt den Umfang |
| 2 | Issuer-Modell | annehmen, plus frühe Klärung mit Apple | **Ja.** Bestimmt `organizationName` und die Rückseite |
| 4 | Signiermodus | inhaltsbewusst (Server prüft und speichert nichts), **nicht** Hash-only | **Ja.** Bestimmt den API-Vertrag |
| 5 | iOS-Mindestversion | iOS 26 | **Ja.** Bestimmt die APIs der iOS-App |
| 6 | Binäre Bahntickets im MVP | ja, als „Beta“ | nein. Standard ist „ja, Beta“ |
| 9 | App Attest | im Backend vorbereitet. Für Entwicklung und TestFlight reicht ein API-Schlüssel, vor dem öffentlichen Launch ist App Attest Pflicht | nein. Das ist der Standard |
| 12 | Apple Developer Account vorhanden? | wird für Pass Type ID und Zertifikat gebraucht | nein für den Code, **ja für Gerätetests** |
| 3, 7, 8, 10, 11 | App-Name, Deutschlandticket, Hosting, Monetarisierung, Rechtsträger | siehe Recherche | nein. Erst vor dem Launch |

Wenn der Product Owner nur „Go“ sagt, ohne Einzelentscheidungen zu treffen, gelten die Empfehlungen als Standard. Das sollte dann im Konzept dokumentiert werden.

---

## 7. Geplanter Ablauf Phase 2

> Das ist ein **Vorschlag** und mit dem Product Owner noch nicht abgestimmt.

### 7.1 Schritte

1. **API-Vertrag festschreiben**: `docs/API.md` plus eine Golden-Fixture `docs/examples/pass-request.json`. Backend-Tests und iOS-Tests nutzen **dieselbe** Datei, damit App und Server nicht auseinanderlaufen.
2. **Parallel umsetzen.** Jeder Bereich schreibt nur in sein eigenes Verzeichnis:
   - `backend/`: FastAPI-Signierdienst mit Tests
   - `ios/`: SwiftUI-App mit XcodeGen-Projekt
   - `docs/KONZEPT.md` (Produkt- und Technikkonzept mit Roadmap und Risiken) und `docs/APPLE-SETUP.md` (Anleitung für Pass Type ID, Zertifikat und WWDR G4)
3. **Gegenprüfen** (adversarial):
   - Backend: Spec-Konformität, Signatur per `openssl`, Sicherheit und Robustheit
   - iOS: API-Korrektheit gegen die Apple-Doku (hier gibt es keinen Compiler!), Swift-6-Concurrency, Übereinstimmung mit dem API-Vertrag
   - Doku: Konsistenz mit Code und Recherche
4. **Befunde beheben**, Tests grün, committen, pushen.

### 7.2 Geplante Struktur

```
backend/
├── pyproject.toml            Abhängigkeiten, ruff, mypy, pytest
├── Dockerfile
├── .env.example              ohne Geheimnisse
├── src/qrcode2wallet/
│   ├── main.py               App-Factory, Middleware (Body-Limit), Fehler als problem+json
│   ├── config.py             pydantic-settings (Zertifikat-Pfade/KMS, Team-Daten, Limits)
│   ├── api/                  Routen: health, meta, passes, (attest)
│   ├── models.py             Request-Schemas (strikt, extra="forbid")
│   ├── pkpass/               builder.py, signer.py, images.py, barcodes.py (Regeltabelle + Validierung)
│   └── security/             auth.py (API-Schlüssel, App-Attest-Schnittstelle), ratelimit.py
├── scripts/generate_dev_certs.py   Wegwerf-Test-PKI für lokale Tests
└── tests/                    pytest, inkl. openssl-Verifikation und Golden-Fixture
ios/
├── project.yml               XcodeGen (iOS 26, Swift 6, MainActor-Isolation)
├── QRCode2Wallet/
│   ├── App/                  App-Einstieg
│   ├── Models/               PassDraft, ScannedCode, PassStyle, StoredPass (SwiftData)
│   ├── Services/             BarcodeDetector (Vision), PDFRenderer, FieldSuggester,
│   │                         PassAPIClient, WalletService (PassKit)
│   ├── Features/             PassList, Import/Scanner, Editor, Preview
│   └── Resources/            Info.plist-Schlüssel, PrivacyInfo.xcprivacy, Localizable (de/en)
└── QRCode2WalletTests/       Unit-Tests der reinen Logik + Decoding der Golden-Fixture
.github/workflows/backend-ci.yml    ruff, mypy, pytest, openssl-Verifikation
```

### 7.3 API-Vertrag (Entwurf, nicht abgestimmt)

- `POST /v1/passes` → `200 application/vnd.apple.pkpass`. Fehler kommen als `application/problem+json` (RFC 9457): 401, 413, 422, 429, 500.
- `GET /v1/health` und `GET /v1/meta` (unterstützte Stile, Formate, Limits, damit die App sich anpassen kann)
- **Authentifizierung im MVP:** `Authorization: Bearer <API-Schlüssel>`. **Später:** `GET /v1/attest/challenge`, `POST /v1/attest`, danach pro Request die Header `X-Attest-KeyId` und `X-Attest-Assertion` (siehe [03 E4](docs/recherche/03-signierung-backend.md#e4)).
- **Vom Server festgelegt, nie vom Client:** `passTypeIdentifier` und `teamIdentifier` (aus dem Zertifikat), `formatVersion`, `organizationName` (eigene Marke) und der Pflichtblock auf der Rückseite mit den Ausstellerdaten. Kein `webServiceURL`, kein `authenticationToken`, keine `nfc`-Daten.
- **`serialNumber`:** Fehlt sie, erzeugt der Server eine UUID. Ist sie gesetzt, muss sie eine UUID sein. Das ist eine Neuausstellung, die den Pass in Wallet ersetzt.
- **Barcode-Eingabe (kanonisch):** `{ sourceSymbology, contentType: "text"|"binary", payloadBase64, altText? }`. Der Server leitet daraus `barcodes[]` nach der Regeltabelle ab ([04 E2](docs/recherche/04-barcodes.md#e2)) und validiert vor dem Signieren ([04 E7](docs/recherche/04-barcodes.md#e7)).
- **Inhalt:** `style` (storeCard | eventTicket | boardingPass + `transitType` | coupon | generic), `description`, `logoText`, Farben, Felder (header/primary/secondary/auxiliary/back mit Grenzen pro Stil), `relevantDates` bzw. `relevantDate`, `expirationDate`, `locations` (max. 10), optional ein eigenes Logo oder Thumbnail (neu kodiert, Größengrenze).

### 7.4 Technische Standards (falls nichts anderes entschieden wird)

| Bereich | Standard |
|---|---|
| Backend | Python ≥ 3.12 (lokal 3.13), FastAPI, pydantic v2, pydantic-settings, `cryptography>=50,<51`, Pillow, cbor2 (App Attest), pytest, ruff, mypy, Docker, GitHub Actions |
| iOS | iOS 26 als Mindestversion, Xcode 27, Swift 6, `SWIFT_DEFAULT_ACTOR_ISOLATION: MainActor`, XcodeGen, SwiftData, VisionKit `DataScannerViewController`, Vision `DetectBarcodesRequest`/`RecognizeDocumentsRequest`, PDFKit, PassKit. **Keine Fremdbibliotheken im MVP.** |
| Pass | Eine Pass Type ID, UUID als Seriennummer, `organizationName` als eigene Marke, Icon 38 pt (@1x/@2x/@3x), ISO-8601-Datumswerte mit Zeitzone |

---

## 8. Umgebung und Einschränkungen

Diese Punkte gelten für die Cloud-Umgebung, in der bisher gearbeitet wurde:

- **Linux-Container ohne Swift-Toolchain und ohne Xcode.** Der iOS-Code lässt sich hier **nicht kompilieren oder testen**. Er muss auf einem Mac mit Xcode 27 geprüft werden (`brew install xcodegen && cd ios && xcodegen`).
  - `apt` bietet kein `swiftlang` an.
  - `download.swift.org` ist über den Proxy gesperrt (403).
  - Der Docker-Daemon läuft nicht.
- **Netzwerk:**
  - `developer.apple.com` und PyPI sind erreichbar.
  - `www.apple.com/certificateauthority/` ist gesperrt. Das **WWDR-G4-Zertifikat** muss deshalb von Hand heruntergeladen werden: <https://www.apple.com/certificateauthority/AppleWWDRCAG4.cer>.
  - Die GitHub-Weboberfläche ist gesperrt, `git` über den Proxy funktioniert.
- **Python-Umgebung neu aufsetzen.** Das Scratchpad der Session ist flüchtig:
  ```bash
  python3 -m venv .venv && . .venv/bin/activate
  pip install "cryptography>=50,<51" fastapi "uvicorn[standard]" pydantic pydantic-settings pillow httpx cbor2 pytest ruff mypy
  ```
  Zuletzt getestete Versionen: Python 3.13.16, cryptography 50.0.2, FastAPI 0.143.0, Starlette 1.7.0, pydantic 2.14.0, pydantic-settings 2.15.0, Pillow 12.3.0, pytest 9.1.1, OpenSSL 3.0.13.
- **Umgebung prüfen:** die Prototyp-Tests laufen lassen, siehe [docs/recherche/prototypen/README.md](docs/recherche/prototypen/README.md#ausführen).
- **Hinweise zu Starlette 1.7:** `TestClient` mit `httpx` erzeugt eine Deprecation-Warnung, die `httpx2` empfiehlt. Die Body-Limit-Middleware ist `starlette.middleware.body_limit.RequestBodyLimitMiddleware`.

---

## 9. Konventionen

- **Niemals Geheimnisse committen:** `.p12`, `.pem`, `.key`, `.cer`, `.env`. Die `.gitignore` deckt das ab. Testzertifikate nur in temporären Verzeichnissen erzeugen.
- **Testdaten fiktiv**, z. B. „Erika Mustermann“. Keine echten personenbezogenen Daten, keine echten Tickets im Repo.
- **Kein Pull Request**, solange der Product Owner keinen verlangt. Auf `claude/qrcode2wallet-mvp` pushen.
- **Commit-Trailer** (für Claude-Sessions):
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01GwRq23ECMawLBV8ozoTdG8
  ```
  Eine neue Session nutzt ihren eigenen Session-Link.
- **Rechtliche Aussagen** immer als „keine Rechtsberatung“ kennzeichnen.
- **Recherche-Prototypen** unter `docs/recherche/prototypen/` nicht als Produktionscode weiterentwickeln, sondern im `backend/` sauber neu umsetzen.

---

## 10. Stolperfallen

| Bereich | Falle | Richtig |
|---|---|---|
| Signatur | Ohne `PKCS7Options.Binary` werden Zeilenenden umgewandelt, und die Signatur bricht | immer `DetachedSignature` + `Binary` |
| Zertifikate | WWDR **G3** statt **G4** führt zu einer ungültigen Signatur | WWDR G4 |
| Identität | `passTypeIdentifier`/`teamIdentifier` vom Client übernehmen | nur aus dem Zertifikat (UID- bzw. OU-Attribut) |
| Manifest | Hash über andere Bytes als die gezippten | `pass.json` einmal serialisieren und dieselben Bytes hashen und zippen |
| iOS-Kamera | `DataScannerViewController.isAvailable` als Prüfung „Kamera erlaubt“ | `AVCaptureDevice.authorizationStatus(for: .video)` |
| iOS-Extensions | App Attest in der Share-Extension | geht nicht. Die Extension legt Dateien nur in eine Inbox |
| SwiftData | Standard-Store landet bei aktivierter App Group im Gruppen-Container | Store-Ort explizit festlegen |
| Barcodes | Nur ein iOS-27-Format (z. B. EAN-13) angeben | Dann zeigen iOS 26 und älter keinen Barcode. Immer Fallback (Code 128 bzw. QR) mitgeben |
| Event-Tickets | Poster-Event-Ticket-Stil | ist mit Barcode-Einlass nicht kompatibel. Klassisches `eventTicket` nehmen |
| Bilder | Barcode als Bild in `strip.png` | Apple rät davon ab. Nur als ausdrücklich gewählte Notlösung |
| Doku | Pass-Referenz bei Apple ist unvollständig (`posterGeneric`, `featuredActions` fehlen) | WWDC26-Session 209 und Pass Builder als Ergänzung, keine undokumentierten Schlüssel ausgeben |

---

## 11. Checkliste zum Wiedereinstieg

1. [ ] Dieses Dokument und [docs/recherche/README.md](docs/recherche/README.md) lesen, mindestens die Abschnitte 1, 4 und 5.
2. [ ] Beim Product Owner **Freigabe für Phase 2** einholen und die Entscheidungen 1, 2, 4 und 5 klären (Fragen 12 und 6 möglichst gleich mit).
3. [ ] `git fetch origin && git checkout claude/qrcode2wallet-mvp`
4. [ ] Python-Umgebung aufsetzen und die Prototyp-Tests laufen lassen ([Abschnitt 8](#8-umgebung-und-einschränkungen)).
5. [ ] Entscheidungen in `README.md` und einer Entscheidungsliste im Konzept festhalten.
6. [ ] API-Vertrag und Golden-Fixture schreiben ([7.3](#73-api-vertrag-entwurf-nicht-abgestimmt)).
7. [ ] Backend, iOS und Konzept umsetzen, gegenprüfen, Befunde beheben ([7.1](#71-schritte)).
8. [ ] Committen, pushen, dieses Handoff aktualisieren.

---

## 12. Fragen an den Product Owner (vorbereitet)

Diese Fragen können beim nächsten Kontakt direkt gestellt werden:

1. **Go für Phase 2** (Konzept + MVP)?
2. Fokus auf das, was Wallet in iOS 27 **nicht** kann: PDF- und Mehrfach-Tickets, Bahn- und Flugtickets, Felderkennung, iOS 26? *(Empfehlung: ja)*
3. Issuer-Modell (eigene Marke, keine Fremdlogos) in Ordnung? *(Empfehlung: ja)*
4. Inhaltsbewusste Signierung (Server sieht Pass-Daten, speichert nichts) statt Hash-only? *(Empfehlung: inhaltsbewusst)*
5. iOS 26 als Mindestversion? *(Empfehlung: ja)*
6. Gibt es einen Apple-Developer-Account? Als Person oder als Organisation?
7. Gibt es schon einen Firmen- bzw. Markennamen, der statt „QRCode2Wallet“ verwendet werden soll?
