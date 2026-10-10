# Recherche QRCode2Wallet – Übersicht und Bewertung

**Stand:** 10.10.2026 · **Status:** Recherche abgeschlossen, Umsetzung noch nicht begonnen (wartet auf Freigabe)

Diese Recherche ist die Grundlage für Konzept und MVP einer **nativen iOS-App** (öffentliches App-Store-Produkt). Die App wandelt Tickets, Kundenkarten, Bordkarten, Coupons und Mitgliedskarten aus Foto, Screenshot, PDF oder Live-Kamera in **Apple-Wallet-Pässe (.pkpass)** um. Signiert wird über ein **Python-Backend (FastAPI)**.

> **Wichtig:** Rechtliche Aussagen in dieser Recherche sind eine fachliche Einschätzung und **keine Rechtsberatung**. Vor dem Launch sollten eine Anwältin oder ein Anwalt (IT-/Markenrecht, Datenschutz) und gegebenenfalls Apple selbst die markierten Punkte prüfen.

## Inhalt

1. [Management Summary](#1-management-summary)
2. [Korrekturen durch den Faktencheck](#2-korrekturen-durch-den-faktencheck)
3. [Konsequenzen für die Architektur](#3-konsequenzen-für-die-architektur)
4. [Zielkonflikte](#4-zielkonflikte)
5. [Offene Entscheidungen für den Product Owner](#5-offene-entscheidungen-für-den-product-owner)
6. [Zwingende Gerätetests vor dem Launch](#6-zwingende-gerätetests-vor-dem-launch)
7. [Verzeichnis der Recherche-Dokumente](#7-verzeichnis-der-recherche-dokumente)
8. [Methodik und Grenzen](#8-methodik-und-grenzen)

---

## 1. Management Summary

### Ampel

| Bereich | Bewertung | Kurzbegründung |
|---|---|---|
| Technische Machbarkeit (Backend, Signierung) | 🟢 | Signierung in Python mit `cryptography` ist nachgebaut und mit `openssl` verifiziert. Ein externes Pass-Paket wird nicht gebraucht. |
| Technische Machbarkeit (iOS-Erkennung) | 🟢 | Vision, VisionKit, PDFKit und PassKit decken Scan, Import und „Zu Wallet hinzufügen“ vollständig ab. |
| Binäre Bahntickets (DB, ÖBB, SBB) | 🟡 | Die Community-Praxis funktioniert, Apple dokumentiert sie aber nicht. Gerätetests sind Pflicht. |
| Wettbewerb / Produktwert | 🟠 | **iOS 27 enthält eine eigene Funktion „Pass erstellen“ in Wallet.** Ohne klare Differenzierung fehlt der Mehrwert. |
| Plattform-Richtlinien (Apple) | 🟠 | Lizenzvertrag und Review-Guideline 1.5 stehen in Spannung zu „Pässe für fremde Marken signieren“. Gelöst wird das über ein Issuer-Modell, ein Restrisiko bleibt. |
| Datenschutz (DSGVO) | 🟢 | Erkennung läuft auf dem Gerät, das Backend signiert ohne zu speichern. Das ist gut lösbar. |
| Betrieb / Sicherheit | 🟡 | Der Signierschlüssel ist das wichtigste Gut. App Attest, Quoten, KMS/HSM und Zertifikats-Monitoring sind nötig. |

### Die zentralen Erkenntnisse

1. **Aktueller Plattformstand ist iOS 27.** WWDC26 hat im Juni 2026 iOS 27 vorgestellt, und Apples Wallet-Dokumentation wurde am 08.06.2026 auf iOS 27 aktualisiert. Neu sind der Pass-Stil `posterGeneric`, die Barcode-Formate EAN-13, Code 39, Codabar und ITF sowie Fallback-Listen mit mehreren Barcodes und `featuredActions`. Ab iOS 27 lassen sich Pässe außerdem direkt aus Daten hinzufügen. → [01](01-pass-format.md), [02](02-ios-apis.md)

2. **Größtes Produktrisiko: Wallet kann in iOS 27 selbst Pässe erstellen.** Es gibt Vorlagen (Standard, Mitgliedschaft, Event) und eine manuelle Erfassung. Der Scan aus Kamera, Foto oder Screenshot braucht laut Sekundärquellen Apple Intelligence (ab iPhone 15 Pro). Die Konfidenz ist mittel, weil apple.com und support.apple.com nicht direkt erreichbar waren. Der triviale Fall „einen Code abscannen“ ist damit kostenlos im System. **Differenzierung muss gezielt dort ansetzen, wo Wallet nicht hilft:**
   - PDF- und Mehrfach-Ticket-Import
   - binäre, signierte Bahn- und ÖPNV-Tickets (UIC 918.3/918.9, VDV-KA)
   - automatische Felderkennung (Datum, Sitz, Gleis, Gate)
   - ältere Geräte und iOS 26
   - Batch-Import
   - Datenschutz als Verkaufsargument

   → [05 E11](05-recht-produkt.md#e11), [04 E10](04-barcodes.md#e10)

3. **Größtes Plattformrisiko: Apples Lizenzvertrag und Review-Richtlinien.**
   - DPLA Anlage 5 §1 erlaubt den Pass Type ID nur für Pässe „unter Ihrer eigenen Marke“.
   - Guideline 1.5 verlangt, dass Pässe „mit einem Zertifikat des Marken-Inhabers“ signiert sind und gültige Kontaktdaten des Ausstellers enthalten.
   - Anlage 5 §2.3 verlangt Name, Anschrift, Telefon und E-Mail des Ausstellers auf jedem Pass.

   **Lösung: das Issuer-Modell.** Jeder Pass ist eine „persönliche digitale Kopie, erstellt mit QRCode2Wallet“:
   - `organizationName` ist die eigene Marke.
   - Der Kartenname steht nur als Text auf dem Pass.
   - Es gibt keine fremden Logos und keinen Logo-Katalog.
   - Die eigenen Kontaktdaten stehen auf der Pass-Rückseite.

   So arbeiten bestehende Konverter-Apps. Eine Ablehnung im App Review bleibt trotzdem möglich. Empfohlen ist daher eine **frühe Klärung**: Anfrage beim App Review oder früher externer TestFlight-Test. → [05 E2](05-recht-produkt.md#e2), [05 E14](05-recht-produkt.md#e14)

4. **Barcode-Formate sind der Kern der Produktqualität.**
   - Bis iOS 26 rendert Wallet nur **QR, PDF417, Aztec und Code 128**.
   - Ab iOS 27 kommen **EAN-13, Code 39, Codabar und ITF** dazu, plus Fallback-Listen.
   - Die Apple Watch zeigt Code 128 laut älterer Dokumentation nicht an.
   - EAN-8, DataMatrix, GS1 DataBar und GS1-128 sind auch unter iOS 27 nicht nativ unterstützt.

   Empfehlung:
   - Originalformat zuerst, dann ein kompatibler Fallback (Code 128 bzw. QR).
   - Die Kartennummer immer als `altText` und als Feld auf dem Pass.
   - Den Nutzer klar warnen, wenn der Fallback an der Kasse eventuell nicht akzeptiert wird.

   Die komplette Regeltabelle steht in [04 E2](04-barcodes.md#e2).

5. **Binäre Bahntickets sind machbar, aber „experimentell“.** Ein DB-Ticket im Format UIC 918.3 enthält zlib-komprimierte, signierte Binärdaten.
   - Die App liest die Rohbytes über `payloadData` (Vision, ab iOS 17).
   - Das Backend legt sie als ISO-8859-1-String mit `messageEncoding: "iso-8859-1"` in den Pass. Jedes Byte entspricht dabei genau einem Zeichen.
   - Das Open-Source-Projekt Zügli nutzt diese Technik produktiv.
   - Apple dokumentiert nicht, dass Wallet die Bytes 1:1 zurückschreibt.

   → Feature erst nach Gerätetests freigeben. → [04](04-barcodes.md), [01 offene Frage 1](01-pass-format.md#offene-fragen)

6. **Nicht konvertierbar (klar kommunizieren):**
   - **dynamische Codes**, z. B. Ticketmaster SafeTix mit wechselndem Barcode oder Codes mit TOTP
   - **reine NFC-Karten**: NFC braucht eine separate Apple-Freigabe
   - Tickets, deren Tarifbestimmungen Kopien verbieten. Viele Verkehrsunternehmen erkennen Kopien von Handytickets nicht an, das Deutschlandticket ist personengebunden.

   → [04 E8](04-barcodes.md#e8), [05 E9](05-recht-produkt.md#e9)

7. **Die Signierung ist das wichtigste Gut des Systems.** Wer den Signier-Endpunkt missbraucht, signiert Pässe unter unserer Team ID. Apple kann das Zertifikat jederzeit widerrufen, und dann funktionieren **alle** ausgegebenen Pässe nicht mehr richtig. Für die Produktion werden deshalb empfohlen:
   - **App Attest** (Nachweis „echte App auf echtem Gerät“, ohne Nutzerkonten)
   - Quoten pro Gerät
   - ein Not-Aus-Schalter
   - der Schlüssel in einem **KMS/HSM**: nicht exportierbar, in einer EU-Region
   - Zertifikats-Monitoring (Ablauf jährlich)

   → [03 E3, E4, E9, E10](03-signierung-backend.md#empfehlungen)

8. **Die Signierung selbst ist einfach und verifiziert.**
   - `manifest.json` enthält die SHA-1-Hashes aller Dateien.
   - Die abgelöste PKCS#7/CMS-Signatur (DER, SHA-256) enthält das Apple-Zwischenzertifikat **WWDR G4** und signingTime.
   - Daraus entsteht ein ZIP ohne Unterordner.
   - Mit `cryptography` reichen etwa 70 Zeilen. **Die Option `PKCS7Options.Binary` ist Pflicht**, sonst bricht die Signatur.

   Bestehende Python-Pakete sind veraltet oder fehlerhaft. Prototypen liegen unter [prototypen/](prototypen/README.md). → [03 E1](03-signierung-backend.md#e1)

9. **Datenschutz ist ein Differenzierungsmerkmal.**
   - Die Erkennung läuft komplett auf dem Gerät.
   - Das Backend signiert zustandslos und speichert keine Pass-Inhalte, Namen, Barcodes oder Bilder.
   - Logs enthalten keine Inhalte.

   Achtung: Gespeicherte IP-Logs oder App-Attest-Schlüssel wirken sich auf das App-Store-Datenschutzlabel aus. Siehe [Zielkonflikte](#4-zielkonflikte). → [03 E6](03-signierung-backend.md#e6), [05 E4, E12](05-recht-produkt.md#empfehlungen)

10. **Geschäftliche Voraussetzungen:**
    - Veröffentlichung über eine **juristische Person** (UG oder GmbH) mit D-U-N-S-Nummer als Apple-Organisations-Account, mit Website und Domain der Organisation.
    - Teilnahme am **Small Business Program**: 15 % statt 26 % Provision in der EU. Ab 01.10.2026 gelten neue EU-Bedingungen (DPLA Anlage 14).
    - Monetarisierung: großzügige Gratis-Stufe plus Einmalkauf „Pro“ (vorgeschlagen 5,99–9,99 €), keine Wochen-Abos.
    - Achtung: Anlage 5 §2.3 verbietet Gebühren dafür, „Wallet zur Nutzung des Passes zu verwenden“. Das Preismodell sollte rechtlich geprüft werden.

    → [05 E1, E6, E7](05-recht-produkt.md#empfehlungen)

11. **Der App-Name ist ein Risiko.** „QR Code“ ist laut Sekundärquellen eine eingetragene Marke von DENSO WAVE, „Wallet“ ist Apples App-Name. Die Konfidenz ist mittel bis niedrig, deshalb vor dem Launch eine Markenrecherche machen und eher umbenennen. → [05, ergänzte Fakten Nr. 14](05-recht-produkt.md#vom-faktenprüfer-ergänzte-wichtige-fakten)

---

## 2. Korrekturen durch den Faktencheck

Ein unabhängiger Faktenprüfer hat 125 Kernaussagen gegen Primärquellen geprüft: **107 bestätigt, 16 korrigiert, 2 nicht verifizierbar.** Die Korrekturen stehen ausführlich am Anfang jedes Themendokuments. Die folgende Tabelle zeigt die für das Design relevanten. Sie enthält auch Korrekturen an Empfehlungen, die der Faktenprüfer im Abschnitt „ergänzte Fakten“ gemeldet hat, z. B. zu SwiftData.

| Thema | Korrektur | Auswirkung |
|---|---|---|
| Passformat | Die Relevanz-Regel gilt auch für `generic`: Ohne Datum braucht es Standorte. Dass Wallet abgelaufene Pässe automatisch ausblendet, ist nur für Bordkarten und Event-Tickets belegt. Entwickler melden, dass Event-Tickets ca. 24 h nach `relevantDate` ausgeblendet werden. | Mehrtägige Tickets und Saisonkarten testen, eventuell `relevantDates` (ab iOS 18) nutzen. |
| Passformat / Bilder | Poster-Pässe nutzen `artwork.png` (358×448 pt), nicht `background.png`. Laut HIG gibt es Bilder nur in @2x/@3x. | Die Bild-Pipeline muss `artwork.png` und `primaryLogo.png` kennen. |
| iOS | `DataScannerViewController.isAvailable` ist **auch vor** der Kamera-Abfrage `true`. | Die Berechtigung über `AVCaptureDevice.authorizationStatus` prüfen. Fehler von `startScanning()` generisch abfangen. |
| iOS | `PhotosPickerItem` ist selbst nicht `Transferable`, lädt aber Transferable-Typen. | Kleine API-Korrektur. |
| iOS / Persistenz | SwiftData legt den Standard-Store bei aktivierter App Group **im Gruppen-Container** an (`groupContainer: .automatic`). | Store-Ort explizit festlegen, wenn eine Share-Extension dazukommt. |
| Signierung | SHA-256 für die CMS-Signatur stammt aus Apples Pass Builder, nicht aus der Doku. Die Ausgabe von `cryptography` ist strukturell nicht identisch mit Pass Builder, aber beide sind gültiges CMS. | Keine Änderung. In der CI mit `openssl` und auf echten Geräten testen. |
| Signierung / App Attest | Die Assertion-Prüfung braucht zusätzlich: Challenge in den Client-Daten, `validationCategory`, `bundleVersion`, ein Schlüsselpaar pro Gerät und getrennte Dev-/Prod-Schlüssel. | Für die Backend-Implementierung berücksichtigen. Der Prototyp prüft das noch nicht. |
| Hosting | STACKIT KMS bietet **keine RSA-PKCS#1-Signatur**, nur ECDSA. | Mit einem RSA-Pass-Schlüssel ist STACKIT KMS ungeeignet. Besser GCP, AWS oder Azure in einer EU-Region. |
| Barcodes | Zügli steht unter EUPL-1.2 (Copyleft) und nutzt ein kommerzielles SDK. db-pkpass erzeugt unsignierte, ungetestete Pässe. | Keinen Code übernehmen, nach Spezifikation selbst implementieren. |
| Barcodes | Die Aztec-Grenze von 1914 Byte gilt bei ca. 23 % Fehlerkorrektur, nicht bei minimaler. | Als konservative Obergrenze verwenden. |
| Barcodes | Ticketmaster SafeTix: Der Code wechselt „alle paar Sekunden“. Die 15 s stammen aus Hinweisen von Veranstaltungsorten. | Die Schlussfolgerung bleibt: nicht konvertierbar. |
| Recht | Die Listen der Required-Reason-Codes im Privacy Manifest waren unvollständig. | Die vollständige Liste steht in [05](05-recht-produkt.md#korrekturen-aus-dem-faktencheck). |
| Nicht verifizierbar | Die Gerätekompatibilität von iOS 27 (iPhone 11 und neuer) ist nur über Sekundärquellen belegt. Details zur Kontrolle des Deutschlandtickets (UIC 918.9, monatlicher Codewechsel) ließen sich nicht prüfen. | Vor Entscheidungen auf Primärquellen prüfen. |

---

## 3. Konsequenzen für die Architektur

Konsolidierte Empfehlungen aus allen fünf Themen. Die Nummern verweisen auf die Themendokumente, z. B. „03 E1“ = Signierung, Empfehlung 1.

### Gesamtarchitektur

```
iPhone (SwiftUI-App, iOS 26+)                     Backend (Python/FastAPI, EU-Region)
┌───────────────────────────────────┐             ┌────────────────────────────────────┐
│ Import: Kamera / Fotos / Dateien  │             │ App-Attest-Prüfung + Quoten        │
│         / PDF / Share-Extension   │             │ Validierung (Formate, Längen,      │
│ Erkennung auf dem Gerät:          │   HTTPS     │   Prüfziffern, Feldgrenzen)        │
│   Vision (Barcodes, Rohbytes),    │ ─────────►  │ pass.json + Bilder + manifest      │
│   Text-/Datenerkennung            │  Pass-Daten │ PKCS#7-Signatur (Schlüssel im KMS) │
│ Editor: Stil, Felder, Farben      │ ◄─────────  │ .pkpass zurück, nichts gespeichert │
│ PassKit: „Zu Wallet hinzufügen“   │   .pkpass   └────────────────────────────────────┘
│ SwiftData: lokale Pass-Historie   │
└───────────────────────────────────┘
```

Der private Schlüssel des Pass Type ID darf **nie** in die App. Er ließe sich auslesen, und dann könnte jeder in unserem Namen signieren. Die Signierung muss deshalb auf dem Server laufen.

### Backend

| Thema | Empfehlung | Quelle |
|---|---|---|
| Pass-Erzeugung | Eigener Builder auf `cryptography` (≥ 50, gepinnt). Paket im Speicher bauen, ZIP ohne Unterordner, MIME-Typ `application/vnd.apple.pkpass`. | 01 E1, 03 E1 |
| Signatur | `PKCS7SignatureBuilder` mit `DetachedSignature` + **`Binary`**, SHA-256, WWDR G4 als Zusatzzertifikat. Manifest mit SHA-1 pro Datei. | 01, 03 E1 |
| Identität | Ein einziger Pass Type ID für alle Pässe. `passTypeIdentifier` und `teamIdentifier` kommen **nur** aus dem Zertifikat, nie vom Client. `serialNumber` ist eine UUID. Zum Bearbeiten wird der Pass mit derselben Seriennummer neu ausgestellt und ersetzt dann den alten. | 01 E2, 03 E4 |
| Pass-Stile | Kundenkarte/Fitness → `storeCard` oder `generic`. Coupon → `coupon`. Event → klassisches `eventTicket`: Poster-Event-Tickets sind mit Barcode-Einlass nicht kompatibel. Bahn/Bus/Flug → `boardingPass` mit `transitType`. `posterGeneric` (iOS 27) nur zusätzlich, mit Fallback-Stil. | 01 E3, 05 E8 |
| Barcodes | Kanonisches Modell vom Gerät: Symbologie, Rohbytes (Base64), Inhaltstyp text/binär. Daraus serverseitig `barcodes[]` in Prioritätsreihenfolge, `altText` immer gesetzt. | 04 E1–E3 |
| Validierung | Vor dem Signieren streng prüfen: Encoding, Prüfziffern (EAN/UPC), Zeichensätze (Code 39/128), gerade Länge (ITF), Längengrenzen pro Format, Feldanzahl und -längen. | 04 E7, 03 E7 |
| Bilder | Icon (38 pt, @2x/@3x) ist Pflicht, Standardbilder per Pillow. Nutzerbilder neu kodieren (EXIF entfernen, Schutz vor Dekompressionsbomben). **Keine Barcodes in Bildern**, davon rät Apple ab. Budget ca. 1 MB pro Pass. | 01 E6, 03 E8 |
| Datumswerte | ISO 8601 mit Zeitzone und Minuten. `relevantDates` ab iOS 18, bei älterem Ziel zusätzlich `relevantDate`. | 01 E7 |
| Rückseite | Pflichtblock mit den Kontaktdaten des Ausstellers (eigene Firma) und dem Hinweis „persönliche digitale Kopie“. | 01 E8, 05 E2 |
| Updates | Kein `webServiceURL` in v1. Push-Updates kämen später als eigener, zustandsbehafteter Dienst. | 01 E11, 03 E11 |
| Missbrauchsschutz | App Attest (Challenge → Attestierung → Assertion pro Request), Quoten pro Schlüssel und IP, Not-Aus, Alarm bei Auffälligkeiten. | 03 E4, E5 |
| Schlüssel und Hosting | Nicht exportierbarer RSA-Schlüssel in einem Cloud-KMS/HSM in einer EU-Region, z. B. GCP europe-west3 + Cloud KMS oder AWS eu-central-1 + KMS. Der KMS-Adapter ist im Prototyp verifiziert. | 03 E3, E9 |
| Betrieb | Runbook für die jährliche Zertifikatsrotation, Ablaufalarme nach 60/30/7 Tagen, Vorgehen bei Kompromittierung. | 03 E10 |
| Tests in der CI | `openssl cms -verify`, Apples `buildpass validate` (prüft nur einen Teil, siehe [01](01-pass-format.md#vom-faktenprüfer-ergänzte-wichtige-fakten)), Simulator-Test. | 01 E9, 03 E2 |

### iOS-App

| Thema | Empfehlung | Quelle |
|---|---|---|
| Mindestversion | **iOS 26** (Build mit Xcode 27 / iOS-27-SDK), iOS-27-Features hinter `#available`. Untergrenze notfalls iOS 18, nie unter iOS 17. Laut Recherche liefen im Juni 2026 79 % aller iPhones mit iOS 26. | 02 E1 |
| Swift-Einstellungen | Swift 6, `SWIFT_DEFAULT_ACTOR_ISOLATION: MainActor`, Approachable Concurrency. Rechenintensives wie PDF-Rendering und Erkennung als `@concurrent`. | 02 E2 |
| Live-Scan | `DataScannerViewController` (VisionKit) in SwiftUI eingebettet, explizite Liste der Symbologien, Qualität `.accurate`. | 02 E3 |
| Bilder/PDF | Vision `DetectBarcodesRequest` und `RecognizeDocumentsRequest` (iOS 26). PDF-Seiten mit ca. 300 dpi rendern, Pixelgrenze gegen Speicherprobleme. | 02 E4, E5 |
| Felderkennung | Texterkennung (de/en) plus Datenerkennung (Termine, Flugnummern, Adressen) als Vorschläge für Felder. | 02 E6 |
| Importwege | `PhotosPicker`, `.fileImporter`, Share-Extension für PDFs aus Mail und Safari. App Attest funktioniert **nicht** in Extensions. | 02 E7 |
| Wallet | `PKPass(data:)` → `AddPassToWalletButton` bzw. `PKAddPassesViewController`. Zum Ersetzen und Lesen eigener Pässe braucht die App die Wallet-Capability (Entitlement `pass-type-identifiers`). | 02 E8, 01 ergänzte Fakten Nr. 4 |
| Persistenz | SwiftData, Quelldaten jedes Passes lokal speichern. So lässt sich jeder Pass bei einem Zertifikatswechsel neu signieren. | 02 E9, 05 E10 |
| Projekt | XcodeGen (`project.yml`) statt handgeschriebener `.xcodeproj`. | 02 E11 |

### Recht und Compliance

| Thema | Empfehlung | Quelle |
|---|---|---|
| Issuer-Modell | Eigene Marke als Aussteller, Kartenname nur als Text, kein Logo-Katalog, Pflichthinweis auf der Rückseite (de/en). | 05 E2, E3 |
| Ticket-Integrität | Barcode-Inhalt bei Tickets nicht editierbar. Warnung bei signierten ÖPNV-Tickets und Deutschlandticket. AGB-Klausel zu rechtmäßig erworbenen Tickets (§ 265a, § 267 StGB). Teilen nicht bewerben. | 05 E9 |
| Datenschutz | Erkennung auf dem Gerät, keine Speicherung von Inhalten, AVV mit dem Hoster, Datenschutzerklärung, Verzeichnis der Verarbeitungstätigkeiten, TOMs. | 05 E4, E5, E13 |
| Konten | v1 ohne Nutzerkonten (keine Löschpflicht nach 5.1.1(v), keine Pflicht zu Sign in with Apple). Pro-Freischaltung über StoreKit-2-JWS, serverseitig geprüft. | 05 E6 |
| Pflichtdokumente | Datenschutzerklärung, Impressum (§ 5 DDG), EULA/AGB, Privacy Manifest (`PrivacyInfo.xcprivacy`), `ITSAppUsesNonExemptEncryption = NO`. | 05 E12, E13 |
| App Review | Review-Notiz zu Issuer-Modell, Kontaktdaten, fehlenden Fremdlogos, Verarbeitung auf dem Gerät und zustandsloser Signierung. Demo-Material mit fiktiven Daten. | 05 E14 |
| Keine Integrationen | Kein Abgreifen von DB-, Payback- oder Airline-Konten. Nur importieren, was der Nutzer selbst besitzt. | 05 E15 |

---

## 4. Zielkonflikte

Die Recherche-Agents und Faktenprüfer haben einige Empfehlungen gefunden, die sich gegenseitig widersprechen. Diese Konflikte muss das Konzept bewusst auflösen:

1. **Datenschutz vs. Missbrauchskontrolle („Hash-only“-Signierung).** Die Rechtsrecherche schlägt vor, dass die App den Pass selbst baut und nur das Manifest mit den Hashes zum Signieren schickt. Dann sieht der Server keine Inhalte, was beim Datenschutz maximal günstig ist. Der Faktenprüfer hält dagegen: Damit wird das Backend zum **Signier-Orakel**. Ein manipulierter Client kann beliebige Pässe signieren lassen, auch solche, die Marken imitieren. Laut DPLA §5.1 sind wir für jeden signierten Pass verantwortlich.
   **Meine Empfehlung:** inhaltsbewusste Signierung. Der Server sieht die Pass-Daten, prüft sie, verarbeitet sie nur flüchtig und speichert nichts.

2. **App Attest vs. „Keine Daten erhoben“ im App-Store-Label.** App Attest verlangt serverseitig pro Gerät einen öffentlichen Schlüssel und einen Zähler. Das zählt bei Apple vermutlich als „Geräte-ID für App-Funktionalität“. Dasselbe gilt für IP-Logs, die länger als für den Request gespeichert werden.
   **Empfehlung:** minimale Speicherung, ehrlich deklarieren und in der Datenschutzerklärung beschreiben.

3. **Share-Extension vs. App Attest.** In Extensions schlägt `generateKey` fehl.
   **Empfehlung:** Die Extension legt Dateien nur in eine Inbox, und die Haupt-App übernimmt die Signierung.

4. **Server- vs. clientgewählte Seriennummer.** Aus Sicherheitsgründen soll der Server die Seriennummer wählen. Zum Bearbeiten muss der Client aber die bestehende Seriennummer wieder mitschicken, damit der Pass ersetzt wird.
   **Empfehlung:** Der Server vergibt die UUID bei der Erstausstellung. Bei einer Neuausstellung schickt der Client sie mit, und der Server prüft nur das Format.

5. **Issuer-Modell vs. Nutzererwartung.** Nutzer wollen, dass die Karte „wie das Original“ aussieht, mit Logo und Farben. Die Plattformregeln verlangen die eigene Marke.
   **Empfehlung:** Farben frei, Kartenname als Text, eigene Bilder optional auf eigenes Risiko (AGB), kein Logo-Katalog.

6. **Mindestversion iOS 26 vs. Reichweite.** iOS 26 vereinfacht die Entwicklung deutlich, weil es nur eine Erkennungs-Pipeline braucht. Verloren gehen aber iPhone XS und XR sowie alle, die nicht aktualisiert haben.

---

## 5. Offene Entscheidungen für den Product Owner

Diese Punkte muss der Product Owner entscheiden, bevor Konzept und MVP final werden. Bei jedem steht meine Empfehlung.

| # | Entscheidung | Optionen | Empfehlung |
|---|---|---|---|
| 1 | **Produktfokus angesichts der Wallet-Funktion in iOS 27** | (a) allgemeiner Konverter · (b) Fokus auf Fälle, die Wallet nicht abdeckt | **(b):** PDF- und Mehrfach-Tickets, Bahn- und Flugtickets, automatische Felderkennung, iOS 26, Datenschutz |
| 2 | **Issuer-Modell** (eigene Marke, keine Fremdlogos) | annehmen · anders lösen | **Annehmen**, plus frühe Klärung mit Apple (Review-Anfrage oder externer TestFlight-Test) |
| 3 | **App-Name** | „QRCode2Wallet“ behalten · umbenennen | **Markenrecherche**, eher vor dem Launch umbenennen. Arbeitstitel bleibt vorerst |
| 4 | **Signiermodus** | inhaltsbewusst · Hash-only | **Inhaltsbewusst**, flüchtig verarbeitet, nichts gespeichert |
| 5 | **iOS-Mindestversion** | iOS 26 · iOS 18 | **iOS 26** |
| 6 | **Binäre Bahntickets im MVP** | ja (experimentell) · später | **Ja, als „Beta“ markiert**, Freigabe erst nach Gerätetests |
| 7 | **Deutschlandticket und Verbund-Handytickets** | blockieren · warnen | **Warnen.** Tarifbestimmungen prüfen, eventuell später blockieren |
| 8 | **Hosting** | GCP · AWS · Azure (EU-Region) · deutscher Anbieter | **GCP europe-west3 + Cloud KMS (HSM)**. Ein deutscher Anbieter nur mit verschlüsseltem Software-Schlüssel |
| 9 | **App Attest** | ab MVP · vor dem öffentlichen Launch | **Im Backend ab MVP vorbereitet, Pflicht vor dem öffentlichen Launch.** Für Entwicklung und TestFlight reicht vorerst ein API-Schlüssel |
| 10 | **Monetarisierung** | Freemium + Einmalkauf · Abo · kostenlos | **Freemium + Einmalkauf „Pro“**. Anlage 5 §2.3 rechtlich prüfen lassen |
| 11 | **Rechtsträger** | UG/GmbH · Einzelperson | **UG/GmbH** mit D-U-N-S, Organisations-Account, Small Business Program |
| 12 | **Apple Developer Account** | vorhanden? | Wird für den Pass Type ID und das Signierzertifikat gebraucht. Ohne ihn ist kein Test auf echten Geräten möglich |

---

## 6. Zwingende Gerätetests vor dem Launch

Diese Fragen ließen sich aus der Dokumentation **nicht** beantworten und lassen sich nur auf echten Geräten klären:

1. Bleiben binäre Aztec- und PDF417-Inhalte (UIC 918.3, auch Byte `0x00` und `0x80–0x9F`) über `iso-8859-1` byte-genau erhalten? Gegenprobe mit einem Prüfgerät bzw. einer Kontroll-App.
2. Was genau liefert `payloadData` bei binären Codes: die dekodierten Bytes oder Codewörter?
3. Zeigt watchOS 26/27 Code 128 und die neuen iOS-27-Formate an?
4. Akzeptieren deutsche Kassensysteme (REWE, dm, EDEKA, Payback-Partner) Code 128 oder QR statt EAN-13 für Kundennummern?
5. Welche Nachrichtenformate erwartet Wallet für die neuen 1D-Formate (EAN-13 mit 12 oder 13 Stellen, Start/Stopp bei Codabar)?
6. Was tut Wallet bei zu langen oder nicht kodierbaren Inhalten: Pass abgelehnt, kein Barcode oder abgeschnitten?
7. Wann blendet Wallet Event-Tickets aus (Wechselwirkung zwischen `relevantDate` und `expirationDate`)?
8. PDF-Rendering: Welche Auflösung erkennt dichte Codes zuverlässig, und welcher Speicherbedarf entsteht auf schwachen Geräten (iPhone SE 2, iPhone 11) und in der Share-Extension?
9. Was kann die iOS-27-Funktion „Pass erstellen“ im Auslieferungszustand in Deutschland tatsächlich (PDF? binäre Tickets? Geräte?), als Grundlage für die Differenzierung?

---

## 7. Verzeichnis der Recherche-Dokumente

| Dokument | Inhalt | Umfang |
|---|---|---|
| [01-pass-format.md](01-pass-format.md) | Aufbau von .pkpass, pass.json-Schlüssel, Stile, Felder, Barcodes, Bilder, Neuerungen in iOS 27 | 44 Fakten · 12 Empfehlungen · Faktencheck 23/2/0 |
| [02-ios-apis.md](02-ios-apis.md) | VisionKit, Vision, PDFKit, PhotosUI, PassKit, SwiftData, App Attest, Swift 6, XcodeGen | 44 Fakten · 11 Empfehlungen · Faktencheck 21/3/1 |
| [03-signierung-backend.md](03-signierung-backend.md) | PKCS#7 in Python, Zertifikate, Bibliotheken, FastAPI, App Attest, KMS, Hosting, Betrieb | 33 Fakten · 11 Empfehlungen · Faktencheck 20/5/0 |
| [04-barcodes.md](04-barcodes.md) | Symbologien in der Praxis (Bahn, Flug, Events, Handel), Umwandlungsregeln, Binärdaten, Erkennung | 38 Fakten · 10 Empfehlungen · Faktencheck 19/5/1 |
| [05-recht-produkt.md](05-recht-produkt.md) | Apple-Lizenzvertrag, App-Review-Richtlinien, DSGVO, Markenrecht, Ticket-Integrität, Wettbewerb, Monetarisierung | 60 Fakten · 15 Empfehlungen · Faktencheck 24/1/0 |
| [prototypen/](prototypen/README.md) | Lauffähige, verifizierte Prototypen: Pass-Builder, Signierung, Bilder, FastAPI-Skizze, App Attest, KMS-Adapter | 10 Skripte und Tests |
| [rohdaten/recherche-ergebnisse.json](rohdaten/recherche-ergebnisse.json) | Vollständige strukturierte Rohdaten aller Recherche- und Prüf-Agents | ca. 430 KB |

Faktencheck-Angaben: bestätigt / korrigiert / nicht verifizierbar.

---

## 8. Methodik und Grenzen

- **Vorgehen:** Fünf parallele Recherche-Agents (je ein Thema) haben gegen Primärquellen recherchiert: developer.apple.com (DocC-JSON, HIG, WWDC-Sessions), Apples Open-Source-Projekt Pass Builder, cryptography.io, PyPI, die Rechtstexte Apple DPLA und App Review Guidelines sowie GitHub-Projekte. Anschließend hat **pro Thema ein unabhängiger Faktenprüfer** versucht, die designrelevanten Kernaussagen zu widerlegen, und fehlende Fakten ergänzt. Insgesamt 10 Agents, rund 900 Werkzeugaufrufe.
- **Lokale Verifikation:** Signierung, FastAPI-Skizze, KMS-Adapter und App-Attest-Prüfung wurden lokal ausgeführt und getestet (siehe [prototypen/](prototypen/README.md)). Zusätzlich hat `openssl cms -verify` die Signatur unabhängig bestätigt.
- **Grenzen:**
  - apple.com, support.apple.com, apps.apple.com und einige Behörden- und Verbandsseiten waren aus der Recherche-Umgebung teilweise nicht erreichbar. Betroffene Aussagen stützen sich auf Sekundärquellen und sind entsprechend mit niedrigerer Konfidenz markiert: die iOS-27-Funktion „Pass erstellen“, Wettbewerberpreise, Details zum Deutschlandticket.
  - Es gab **keinen Test auf echten Apple-Geräten**. Die Linux-Umgebung hat weder Xcode noch Swift-Compiler.
  - Rechtliche Aussagen sind **keine Rechtsberatung**.
- **Sprache:** Diese Übersicht ist auf Deutsch. Die Themendokumente enthalten die vollständigen Rohinhalte in der Originalsprache Englisch, damit beim Übersetzen keine Details verloren gehen.
