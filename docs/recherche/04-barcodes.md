# 04 · Barcode-Realität vs. Wallet-Unterstützung

> **Hinweis:** Vollständige Rohfassung der Recherche vom 10.10.2026: KI-Agenten-Recherche gegen Primärquellen, danach von einem unabhängigen Faktenprüfer adversarial gegengeprüft. Die Inhalte stehen in der Originalsprache Englisch. Die deutsche Zusammenfassung mit Bewertung steht in der [Übersicht](README.md). Rechtliche Aussagen sind **keine Rechtsberatung**.

**Recherchierter Umfang:** Barcode reality for tickets and loyalty cards (DACH/EU and global) compared with what Apple Wallet supports in pass.json, as of 2026-10-10 (iOS 27 / watchOS 27 is now current, not iOS 26)

**Inhalt:** 38 Fakten (Konfidenz hoch 22, mittel 14, niedrig 2) · 10 Empfehlungen · 23 Fallstricke · 11 offene Fragen · Faktencheck von 25 Kernaussagen: 19 bestätigt, 5 korrigiert, 1 nicht verifizierbar · 12 vom Faktenprüfer ergänzte Fakten

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

- **[KORRIGIERT]** Zügli builds {format: PKBarcodeFormatAztec, message: bytes(barcode_data).decode('iso-8859-1'), messageEncoding: 'iso-8859-1'} and serialises with json.dumps(...).encode('utf-8'). xi/db-pkpass does the same. KItinerary reads iso-8859-1 pkpass barcodes back with msg.toLatin1(). This is a proven production pattern.
  - **Ergebnis:** The code snippets are accurate: zuegli main/views/passes.py (e.g. lines ~420 and ~2941 at commit 99ec9bd, 2026-10-05; SNCB Train+ QR uses utf-8 instead), and json.dumps(pass_json).encode('utf-8') at ~5983. db_pkpass.py lines 241-247 use message.decode('iso-8859-1'). Three corrections. (1) Zügli is EUPL-1.2 (copyleft) and decodes images with the commercial Barkoder SDK (main/aztec.py, encodingCharacterSet='BINARY'), not zxing-cpp. (2) xi/db-pkpass (MIT) is not production evidence: its README says 'The PKPass file does not contain a signature, so it will not work with Apple Wallet' and the code 'has not been extensively tested'. (3) KItinerary (LGPL-2.0-or-later, pkpassdocumentprocessor.cpp) uses toLatin1() only when messageEncoding equals iso-8859-1 (case-insensitive) AND the message contains a null, non-printable or non-character code point. Otherwise it uses toUtf8(). Only Zügli is evidence that Wallet reproduces binary bytes in practice.
  - **Quelle:** <https://github.com/TheEnbyperor/zuegli/blob/master/main/views/passes.py>

- **[KORRIGIERT]** Core Image Aztec: compact up to 44 bytes in up to 4 layers, full-size up to 1914 bytes in up to 32 layers, correctionLevel 5-95. QR 40-L 2953 bytes / 7089 digits / 4296 alphanumeric; PDF417 1108 bytes / 1850 text / 2710 digits. All maxima assume the lowest error correction.
  - **Ergebnis:** The Aztec maximum does NOT assume the lowest EC. The archived CIAztecCodeGenerator reference gives inputCorrectionLevel 'Default value: 23.00 Minimum: 5.00 Maximum: 95.00' and full-size 'up to 1914 bytes of message data (including correction) in up to 32 layers ... no larger than 151 x 151'. A 32-layer full Aztec has (112+16\*32)\*32 = 19,968 bits = 1,664 12-bit codewords (formula from zxing-cpp AZEncoder.cpp TotalBitsInLayer). At the ISO 24778 recommended 23% + 3 codewords that leaves 1,278 data codewords = 15,336 bits, which gives exactly 1914 bytes / 3832 digits / 3067 text characters. 1914 B is therefore the default ~23%-EC figure; at 5% EC roughly 2,300+ bytes would theoretically fit. The QR 40-L figures (2953/7089/4296) and PDF417 figures (1108/1850/2710 at EC level 0) are correct lowest-EC maxima. Core Image's QR default EC is M, where 40-M holds about 2331 bytes. Wallet's actual EC choices remain undocumented.
  - **Quelle:** <https://developer.apple.com/library/archive/documentation/GraphicsImaging/Reference/CoreImageFilterReference/index.html>

- **[KORRIGIERT]** TN2325: UPC-A is reported as EAN-13 with a leading zero; EAN-2/EAN-5 are not supported; each AVCaptureMetadataOutput callback returns at most four barcodes, usually those nearest the centre; 1D detectors sample limited scan lines.
  - **Ergebnis:** TN2325 (2013) says: 'Only a single 1-dimensional code will be returned with each call ... and it will correspond to the center-most decodable barcode in the rectOfInterest.' The four-per-call limit applies only to 2D codes ('There is a limit of four barcodes per call ... which will usually correspond to the center-most codes'). PDF417 is treated as a stacked 1D code by the scan-line detector. 'A decoded UPC-A barcode is output as AVMetadataObjectTypeEAN13Code with a leading zero in the stringValue.' EAN-2/EAN-5: 'No.' Separately, a local zxing-cpp 3.1.1 round-trip test also reported a generated UPC-A as EAN-13 ('0'+12 digits, symbology identifier ]E0) when reading with default formats.
  - **Quelle:** <https://developer.apple.com/library/archive/technotes/tn2325/_index.html>

- **[KORRIGIERT]** DB online tickets carry a UIC 918.3 Aztec barcode with VDV-KA extensions; uic-918-3 documents 0080BL and 0080VU; DB's interoperability PDF reportedly specifies Aztec with 23% EC.
  - **Ergebnis:** uic-918-3 README (MIT) confirms '0080BL: A specific container on tickets from Deutsche Bahn ... used for proof-of-payment checks on the train' and '0080VU: A specific container on (some) tickets from Deutsche Bahn ... used on products, which are also accepted by other carriers, especially (local) public transport companies' (link bahn.de/vdv-barcode). 'VDV-KA extensions' is imprecise: 0080VU is a DB-defined record inside the UIC 918.3 container, not a VDV-KA barcode. The 23% Aztec EC claim could not be verified (no primary source reachable).
  - **Quelle:** <https://github.com/justusjonas74/uic-918-3>

- **[NICHT VERIFIZIERBAR]** Deutschlandticket barcodes are VDV-KA or UIC (signed). UIC FCB (918.9) inspection must be implemented nationwide. 918.9 was to replace 918.3 from 2024 to end of 2025. The D-Ticket barcode in DB Navigator changes monthly.
  - **Ergebnis:** kcd-nrw.de was unreachable from this environment. Search results only show that a KCD 'Ergebnisdokument der Arbeitsgruppe Kontrolle' exists (V1.3, 06/2024), and a Coburg tender annex lists inspection of VDV-KA cards, UIC 918-3 and 918-9 codes and VDV barcodes. The 2024-2025 timeline and the monthly barcode change were not verified.
  - **Quelle:** <https://kcd-nrw.de/fileadmin/user_upload/240625_Ergebnisdokument_der_Arbeitsgruppe_Kontrolle_V1.3.pdf>

- **[KORRIGIERT]** Ticketmaster SafeTix uses an encrypted barcode that refreshes about every 15 seconds and screenshots are not accepted. On iPhone it uses an NFC token in Wallet issued only by Ticketmaster.
  - **Ergebnis:** The cited TechCrunch article (2019) says the barcode 'automatically refreshes every few seconds'. The '15 seconds' figure and 'screenshots will not be accepted' come from venue notices (e.g. Syracuse/cuse.com, 2022). The venue notices say the Wallet version deploys an NFC token ('hold near reader'), and one says the SafeTix Wallet enhancements require iOS 16.4 or higher. The conclusion is unchanged: rotating codes cannot be copied to static passes. These are secondary sources; Ticketmaster's own pages were not reachable.
  - **Quelle:** <https://cuse.com/news/2022/8/25/safetix-in-place-for-jma-wireless-dome-events-this-year>

## Fakten

### F1 · Konfidenz: hoch

pass.json `barcodes[]` entries take exactly four keys: `format` (required), `message` (required), `messageEncoding` (required, an IANA charset name such as "iso-8859-1") and `altText` (optional; not shown on watchOS). The allowed `format` values are PKBarcodeFormatQR, PKBarcodeFormatPDF417, PKBarcodeFormatAztec, PKBarcodeFormatCode128, PKBarcodeFormatCode39, PKBarcodeFormatCodabar, PKBarcodeFormatEAN13 and PKBarcodeFormatI2of5. EAN-8, UPC-A, UPC-E, DataMatrix, GS1 DataBar, Code 93, MSI and MicroQR are not supported. There are no keys for error-correction level, module size, quiet zone, colours or ECI.

- **Bedeutung fürs Design:** The backend pass model needs exactly these 4 fields per barcode. Every other symbology needs a conversion rule. The app cannot control how dense the rendered barcode is, so its only lever on scan quality is the payload length.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary>

### F2 · Konfidenz: hoch

Code 39, Codabar, EAN-13 and ITF (PKBarcodeFormatI2of5) are new in iOS 27 (WWDC26 session 209). From the transcript: "If you only provide one of the new barcode types and nothing else, the pass will not render a barcode on iOS 26 and earlier." Apple 'strongly recommends' a barcodes array in priority order. If you cannot supply a fallback, Apple says to show the credential ID in a primaryField or headerField so staff can type it in.

- **Bedeutung fürs Design:** Any pass that uses a new 1D format must also carry a fallback entry, and the card number should always be printed in a prominent field. This changes the earlier plan, which assumed EAN-13 always needs conversion: on iOS 27 it is now native.
- **Quelle:** <https://developer.apple.com/videos/play/wwdc2026/209/>

### F3 · Konfidenz: hoch

In the Pass dictionary, `barcodes` is described as: "The system uses the first displayable barcode for the device." The singular `barcode` key is deprecated since iOS 9 / watchOS 2 and allowed only QR, PDF417 and Aztec. The current Barcodes page also says "In iOS 27 and later, you can provide more than one barcode as a fallback", but fallback through the array has worked since iOS 9. That sentence only concerns the new formats.

- **Bedeutung fürs Design:** Emit only `barcodes`. Order the array as [preferred native format, compatible fallback, final fallback the Watch can show]. The user cannot choose at display time, so the order chosen at pass build time is the policy.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### F4 · Konfidenz: mittel

Apple's archived Wallet Developer Guide says watchOS does not support PKBarcodeFormatCode128. If a Code128 entry is in the array, the next entry is used on the Watch. If Code128 is the only barcode, the Watch shows no barcode. The deprecated Pass.Barcode docs repeat that Code128 is not supported on watchOS. No current doc says whether watchOS 27 renders Code128 or the four new 1D formats.

- **Bedeutung fürs Design:** For Watch coverage, end every 1D-based array with a 2D entry (QR) holding the same data, and tell users the Watch may show a QR code instead of the 1D code. Test on watchOS 27 hardware.
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### F5 · Konfidenz: hoch

A pass viewed on Apple Watch does not show the strip image, the thumbnail image or the back of the pass. The archived guide adds that the Watch rotates rectangular barcodes to portrait and suggests square barcodes such as QR for the Watch's smaller screen.

- **Bedeutung fürs Design:** A barcode drawn into strip.png or thumbnail.png is invisible on Apple Watch. The image fallback only works on iPhone, so the UI must say so.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/creating-a-store-card-pass>

### F6 · Konfidenz: hoch

Apple: "Most laser scanners can't reliably read barcodes displayed on LCD screens. To scan pass barcodes, use an optical barcode scanner." The same guide says scanners typically use ISO 8859-1 or Windows-1252, that "Unicode is poorly supported by most systems", and that "PassKit supports all encodings supported by the NSString class."

- **Bedeutung fürs Design:** 1D loyalty cards (EAN, Code39, Codabar) are the cases most often read by older laser POS or library scanners, which may fail on any phone screen, native barcode or image. The app should warn about this and always show the number for manual entry.
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### F7 · Konfidenz: hoch

messageEncoding is defined as "The IANA character set name of the text encoding to use to convert `message` from a string representation to a data representation that the system renders as a barcode". Apple does not explicitly document that iso-8859-1 is byte-transparent for 0x00-0xFF.

- **Bedeutung fürs Design:** Wallet works as: JSON string -&gt; encode with messageEncoding -&gt; bytes -&gt; symbol. To reproduce arbitrary bytes, map byte N to Unicode code point U+00NN and declare iso-8859-1.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary>

### F8 · Konfidenz: hoch

Community practice for binary rail payloads: Zügli (TheEnbyperor/zuegli, a production Python/Django service that converts UIC 918.3, UIC DOSIPAS, VDV, SSB, SNCF, RSP and other tickets into Apple and Google Wallet passes) builds `{"format":"PKBarcodeFormatAztec","message": bytes(barcode_data).decode("iso-8859-1"),"messageEncoding":"iso-8859-1"}` and serialises it with `json.dumps(pass_json).encode("utf-8")`, where the default ensure_ascii=True produces \u00XX escapes. xi/db-pkpass does the same for DB PDF tickets (`message.decode('iso-8859-1')`). KDE KItinerary reads such pkpass barcodes back as binary with `msg.toLatin1()` when messageEncoding is iso-8859-1, with the comment 'binary barcode content (which wont survive a JSON/QString roundtrip)'.

- **Bedeutung fürs Design:** This proven pattern is the recommended binary pipeline: raw bytes -&gt; latin-1 str -&gt; JSON escapes -&gt; Wallet re-encodes as iso-8859-1 -&gt; identical bytes. zlib-compressed and signed UIC 918.3 payloads (which contain 0x00 and 0x80-0x9F) survive in practice.
- **Quelle:** <https://github.com/TheEnbyperor/zuegli/blob/master/main/views/passes.py>

### F9 · Konfidenz: hoch

Python's 'iso-8859-1'/'latin-1' codec maps all 256 byte values 1:1 to U+0000-U+00FF and round-trips. A local test (`bytes(range(256)).decode('iso-8859-1')` -&gt; json.dumps -&gt; json.loads -&gt; `.encode('iso-8859-1')`) returned identical bytes. 'cp1252' raises on 0x81 and 'utf-8' raises on arbitrary binary. json.dumps escapes control characters as \u0000 even with ensure_ascii=False, so the JSON stays valid.

- **Bedeutung fürs Design:** In FastAPI, never decode binary payloads as utf-8 or cp1252. Carry them as base64 in the API (`payload_b64`) and convert with `.decode('latin-1')` only when building pass.json.
- **Quelle:** <https://docs.python.org/3/library/codecs.html#standard-encodings>

### F10 · Konfidenz: mittel

Apple's Core Image Code 128 generator says the barcode "can contain any of the 128 ASCII characters" and its sample uses `.data(using: .ascii)`. Apple does not document whether Wallet renders through Core Image or how it handles non-ASCII bytes in a Code128 message.

- **Bedeutung fürs Design:** Treat PKBarcodeFormatCode128 as ASCII-only: reject or fall back for payloads with bytes above 0x7F, and never put binary data in Code128.
- **Quelle:** <https://developer.apple.com/documentation/coreimage/cifilter-swift.class/code128barcodegenerator()>

### F11 · Konfidenz: hoch

Core Image Aztec generator: compact Aztec holds up to 44 bytes in up to 4 layers, full-size Aztec up to 1914 bytes in up to 32 layers, and correctionLevel ranges from 5 to 95 percent. QR version 40-L holds at most 2953 bytes (7089 digits, 4296 alphanumeric). PDF417 holds at most 1108 bytes in byte compaction, 1850 text characters or 2710 digits. All maxima assume the lowest error correction.

- **Bedeutung fürs Design:** Server-side hard limits: Aztec 1914 bytes, QR 2953 bytes, PDF417 1108 bytes. Apple notes the practical limit is lower (Watch, poor light, cheap scanners), so warn well before these limits. Wallet's EC level is unknown, so the real usable maximum is probably lower.
- **Quelle:** <https://developer.apple.com/documentation/coreimage/cifilter-swift.class/azteccodegenerator()>

### F12 · Konfidenz: hoch

Apple's archived guide says each format has a hard maximum, but "scanning conditions often lower this limit", giving the example of an Apple Watch in poor light with an inexpensive scanner. Current docs: "Wallet optimizes the presentation of passes in order to facilitate a successful scan."

- **Bedeutung fürs Design:** Long PDF417 and Code128 payloads produce thin modules on a phone-width box. The app has to test real scans because it cannot adjust rendering.
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### F13 · Konfidenz: mittel

Whether GS1-128 (Code128 with FNC1) can be produced in Wallet is undocumented. An Apple Developer Forums question from 2017 asking how to add FNC1 to a PKBarcodeFormatCode128 pass has no replies.

- **Bedeutung fürs Design:** GS1-128 coupons and GS1 DataMatrix codes (FNC1 / AI semantics) cannot be reproduced faithfully. Classify them as high risk and use the image fallback or manual entry.
- **Quelle:** <https://developer.apple.com/forums/thread/80458>

### F14 · Konfidenz: hoch

Vision symbologies: VNBarcodeSymbology / BarcodeSymbology include aztec, codabar (iOS 15), code39 (+checksum, fullASCII, fullASCIIChecksum), code93, code93i, code128, dataMatrix, ean8, ean13, gs1DataBar, gs1DataBarExpanded, gs1DataBarLimited (iOS 15), i2of5, i2of5Checksum, itf14, microPDF417, microQR (iOS 15), msiPlessey (iOS 17), pdf417, qr and upce. There is no UPC-A constant. The Swift-native API `DetectBarcodesRequest` (iOS 18+, revision4) returns `BarcodeObservation` with `payloadData: Data?`, `payloadString: String?`, `isColorInverted`, `isGS1DataCarrier`, `supplementalPayloadString/Data`, `symbology` and `boundingRegion`.

- **Bedeutung fürs Design:** Detection covers far more symbologies than Wallet can render, so the conversion table is required. With an iOS 18 minimum, use DetectBarcodesRequest. isGS1DataCarrier flags GS1 content that cannot be reproduced.
- **Quelle:** <https://developer.apple.com/documentation/vision/barcodesymbology>

### F15 · Konfidenz: mittel

VNBarcodeObservation.payloadData and isColorInverted are available from iOS 17 and barcodeDescriptor (CIBarcodeDescriptor) from iOS 11. Apple describes payloadData only as 'The raw data representation of the barcode's payload'. Whether it is the decoded byte stream or raw codewords for binary Aztec/QR is not documented. CIAztecCodeDescriptor.errorCorrectedPayload holds codewords that you would have to decode yourself.

- **Bedeutung fürs Design:** Do not rely on payloadStringValue for binary tickets. Verify payloadData byte-for-byte against zxing-cpp on real DB, ÖBB and VDV tickets before trusting it, and keep a zxing-cpp path.
- **Quelle:** <https://developer.apple.com/documentation/vision/vnbarcodeobservation/payloaddata>

### F16 · Konfidenz: mittel

Apple TN2325: UPC-A is reported as EAN-13 with a leading zero. EAN-2/EAN-5 add-ons are not supported. Each AVCaptureMetadataOutput callback returns at most four barcodes, usually the ones nearest the centre. 1D detectors sample limited scan lines because 1D codes were designed for laser scanners.

- **Bedeutung fürs Design:** UPC-A arrives as a 13-digit value starting with 0. That is fine for PKBarcodeFormatEAN13, whose bars are identical, but human-readable text should strip the 0 only when the source is known to be UPC-A. For multi-code tickets, prefer Vision or zxing-cpp over AVCaptureMetadataOutput.
- **Quelle:** <https://developer.apple.com/library/archive/technotes/tn2325/_index.html>

### F17 · Konfidenz: hoch

DataScannerViewController (VisionKit, iOS 16+) needs an A12 Bionic or later (`isSupported`). `.barcode(symbologies:)` takes VNBarcodeSymbology values. RecognizedItem.Barcode exposes `payloadStringValue` and `observation: VNBarcodeObservation`, so payloadData is reachable from live scanning.

- **Bedeutung fürs Design:** Use it for live camera capture with recognizesMultipleItems. Read observation.payloadData for binary codes, and run a second still-image pass for the bytes.
- **Quelle:** <https://developer.apple.com/documentation/visionkit/datascannerviewcontroller/issupported>

### F18 · Konfidenz: hoch

zxing-cpp (Apache-2.0; PyPI `zxing-cpp` 3.1.1, released 2026-07-29) Python API: `zxingcpp.read_barcodes(image, formats=..., try_rotate=True, try_downscale=True, try_invert=True, text_mode=HRI, binarizer=LocalAverage, is_pure=False, return_errors=False)`. Each Barcode has `.bytes`, `.text`, `.format`, `.content_type` (Text/Binary/Mixed/GS1/ISO15434/UnknownECI), `.symbology_identifier`, `.ec_level` and `.position`. The repo also ships a Swift Package (`ZXingCpp`, iOS 12+) whose `ZXIResult.bytes` is NSData, with `ZXIReaderOptions.tryInvert`, `minLineCount`, `validateCode39CheckSum` and `validateITFCheckSum`.

- **Bedeutung fürs Design:** Use one decoder on both sides: server (FastAPI) for PDFs and uploads, client SPM for byte-exact on-device decoding. content_type==Binary picks the latin-1 path. Pin a release tag, because the master API (e.g. rotation vs orientation) is still changing.
- **Quelle:** <https://github.com/zxing-cpp/zxing-cpp/blob/master/wrappers/python/zxing.cpp>

### F19 · Konfidenz: hoch

ISO/IEC 15424 symbology identifiers emitted by zxing-cpp: ]E0 for EAN-13 and UPC-A, ]E4 for EAN-8, ]C0 for Code 128 and ]C1 for GS1-128 (FNC1 first), ]A0 for Code 39, ]F0 for Codabar, ]I0/]I1 for ITF (1 when a valid GTIN check digit is present), ]G0 for Code 93.

- **Bedeutung fürs Design:** Re-encoding EAN digits as Code128 changes what an AIM-ID-aware POS scanner transmits (]E0 to ]C0). Store the original symbology identifier so you can explain the risk and choose the fallback.
- **Quelle:** <https://github.com/zxing-cpp/zxing-cpp/blob/master/core/src/oned/ODCode128Reader.cpp>

### F20 · Konfidenz: niedrig

zxing-cpp's Codabar result text includes the A-D start/stop characters. WWDC26 shows a PKBarcodeFormatCodabar entry with message "123456789" (no start/stop). Apple does not document whether Wallet expects or adds start/stop characters for Codabar, or check digits for EAN13, Code39 or I2of5.

- **Bedeutung fürs Design:** Message normalisation rules for the new 1D formats must be checked on an iOS 27 device and compared byte-for-byte with what a real scanner outputs. Library cards are the main affected case.
- **Quelle:** <https://developer.apple.com/videos/play/wwdc2026/209/>

### F21 · Konfidenz: hoch

UIC 918.3 container layout (from Zügli's parser): ASCII '#UT' + 2-digit version ('01' or '02') + 4-digit issuer RICS + 5-character key ID + signature (v1: 50 bytes DER DSA/SHA-1; v2: 64 bytes r||s, e.g. ECDSA/DSA) + 4-digit ASCII length + zlib-compressed records such as U_HEAD, U_TLAY, U_FLEX and DB's 0080BL / 0080VU (the VDV-accepted container). The whole payload is binary.

- **Bedeutung fürs Design:** DB/ÖBB tickets must be copied byte-for-byte (signature!) as Aztec. Never re-serialise them. Fields such as passenger and train can be shown on the pass by decoding locally (zlib + record parsing), but the barcode stays the original bytes.
- **Quelle:** <https://github.com/TheEnbyperor/zuegli/blob/master/main/uic/envelope.py>

### F22 · Konfidenz: mittel

Deutsche Bahn online tickets carry an Aztec barcode following UIC 918.3 with VDV-KA extensions. The uic-918-3 project documents the DB records 0080BL (proof of payment) and 0080VU (accepted by local transport). Search results describe DB's interoperability PDF as specifying Aztec with 23% error correction; that PDF could not be fetched directly.

- **Bedeutung fürs Design:** Target PKBarcodeFormatAztec. Wallet chooses its own EC level and layer count, which is fine because validators read the data, not the geometry.
- **Quelle:** <https://github.com/justusjonas74/uic-918-3>

### F23 · Konfidenz: mittel

Deutschlandticket: barcodes are issued as VDV-KA or UIC barcodes (signed). Inspection of the UIC FCB (918.9) format has to be implemented on all inspection devices nationwide. UIC 918.9 was planned to replace 918.3 for barcode tickets from 2024 to the end of 2025. Press reports say the D-Ticket barcode in DB Navigator changes monthly.

- **Bedeutung fürs Design:** Subscription tickets have barcodes limited to a period. Store `expirationDate` from the decoded validity and remind the user to re-import each month. The app cannot push updated barcodes because it does not own the ticket backend.
- **Quelle:** <https://www.kcd-nrw.de/fileadmin/01_Ergebnisdokument_Deutschlandticket_UIC__V1.03.pdf>

### F24 · Konfidenz: mittel

VDV-KA barcodes are BER-TLV structures with an ISO 9796-2 RSA signature (message recovery), residual data and a CA certificate. Zügli detects them by a successful BER-TLV parse and puts them in Wallet as PKBarcodeFormatAztec.

- **Bedeutung fürs Design:** Same binary latin-1 Aztec path as UIC. Their content can only be read with VDV PKI certificates, so show minimal fields (or OCR'd PDF text) unless you implement VDV decoding.
- **Quelle:** <https://github.com/TheEnbyperor/zuegli/blob/master/main/vdv/envelope.py>

### F25 · Konfidenz: hoch

Zügli's payload classifier, which can be reused as a format detector: base64 that decodes to '#UT' means UIC; 114-byte payloads with high nibble 3 mean ERA SSB; 107 bytes is SSB v1; 'i0CV' is SNCF; '#UT' is UIC 918.3; 'TS2'; 'UIC:' is UIC QR; 516 bytes is Renfe/ADIF; '06'/'08' is UK RSP; 'FT' is FlexiTicket; 'A1'/'B1' is HŽPP; 'e' is ELB; 'M' is IATA BCBP; first byte 0x0a is SwissPass (protobuf, rendered as QR); first byte 0x06 is MÁV; a UPER parse means DOSIPAS (UIC 918.9); a BER-TLV parse means VDV; 42 bytes is RSP v11.

- **Bedeutung fürs Design:** Build a server-side `classify(payload_bytes)` that picks pass style (eventTicket vs boardingPass vs storeCard), the target symbology, and whether the pass is a binary ticket that must be copied byte-for-byte.
- **Quelle:** <https://github.com/TheEnbyperor/zuegli/blob/master/main/ticket.py>

### F26 · Konfidenz: mittel

SBB: KDE's reverse-engineering wiki describes the SBB/SwissPass barcode as a QR code with protobuf content, and Zügli renders SwissPass as PKBarcodeFormatQR. ÖBB uses Aztec UIC 918.3, with a JSON vendor record per the KDE wiki and ÖBB's own FAQ on the Aztec security code.

- **Bedeutung fürs Design:** DACH rail covers both Aztec (DB, ÖBB, VDV) and QR (SBB). Both are native in Wallet, but both carry binary data.
- **Quelle:** <https://community.kde.org/KDE_PIM/KItinerary/SBB_Barcode>

### F27 · Konfidenz: mittel

IATA BCBP (Resolution 792): paper boarding passes use PDF417. Mobile BCBP may use Aztec, DataMatrix or QR. The data is ASCII and starts with 'M' plus the number of legs. Found via secondary sources quoting the IATA Implementation Guide v7; the guide itself was not readable here. Zügli renders IATA as Aztec.

- **Bedeutung fürs Design:** BCBP from PDF417 or Aztec maps 1:1. BCBP from DataMatrix should be re-encoded as Aztec or QR, which IATA-compliant gate readers should accept. Use the boardingPass style with transitType PKTransitTypeAir.
- **Quelle:** <https://www.iata.org/contentassets/1dccc9ed041b4f3bbdcf8ee8682e75c4/2021_03_02-bcbp-implementation-guide-version-7-.pdf>

### F28 · Konfidenz: hoch

Ticketmaster SafeTix uses an encrypted barcode that refreshes about every 15 seconds, and screenshots are not accepted at entry. On iPhone it uses an NFC token in Wallet, issued only by Ticketmaster.

- **Bedeutung fürs Design:** Rotating, TOTP or animated codes (SafeTix, some HandyTicket apps, pretix TOTP records seen in Zügli) cannot become static passes. Detect them (repeated scans differ, known issuers) and refuse with an explanation.
- **Quelle:** <https://techcrunch.com/?p=1828729>

### F29 · Konfidenz: hoch

Health certificates: Apple's native import for SMART Health Cards replaces 'shc:/' with 'https://redirect.health.apple.com/SMARTHealthCard/#' (iOS 15.1+). For EU DCC it replaces 'HC1:' with 'https://redirect.health.apple.com/EU-DCC/#' plus the URL-encoded rest (iOS 15.4+). EU DCC is Base45 in a QR, chosen to fit QR alphanumeric mode.

- **Bedeutung fürs Design:** Detect the 'HC1:' and 'shc:/' prefixes and send the user to Apple's verified Health/Wallet import instead of building a generic pass, which also avoids health-data and App Review problems.
- **Quelle:** <https://developer.apple.com/health-fitness/add-to-apple-wallet-and-health-guidelines>

### F30 · Konfidenz: mittel

Library and patron cards mostly use 14-digit Codabar or Code 39 barcodes, depending on the library system (ILS) and its scanners.

- **Bedeutung fürs Design:** On iOS 27 these map to PKBarcodeFormatCodabar or Code39 natively. On older devices a Code128 fallback is high risk, because library scanners are often configured for only those symbologies.
- **Quelle:** <https://www.troup.org/fs/pages/4805>

### F31 · Konfidenz: niedrig

DACH loyalty cards: forum sources say Payback cards use EAN-13 (13-digit card number), while REWE and dm coupons use Code 128. No official issuer specifications were found.

- **Bedeutung fürs Design:** Expect EAN-13 and Code128 to dominate retail loyalty, so EAN-13 handling is the most important path. iOS 27 solves it natively, and iOS 26 or older needs a fallback policy.
- **Quelle:** <https://vielfliegertreff.de/forum/threads/fragen-rund-um-payback.9752/post-2722844>

### F32 · Konfidenz: mittel

Before iOS 27, competitors such as Pass2U converted unsupported formats (EAN-8, EAN-13, UPC-A, Code39, Code93) into strip images. Pass2U 3.6 added native support for the four iOS 27 formats.

- **Bedeutung fürs Design:** Strip-image fallback is established practice but limited: no Watch display, cropping, and it sits behind the primary fields.
- **Quelle:** <https://apps.apple.com/us/app/pass2u-wallet-add-store-card/id1142473931>

### F33 · Konfidenz: mittel

iOS 27 Wallet has its own 'Create a Pass' (+ &gt; Create a Pass). It builds passes from a physical card, photo or screenshot, with Standard, Membership and Event templates. The automatic scan path needs Apple Intelligence hardware (iPhone 15 Pro or iPhone 16 and later), and manual creation is available otherwise. Reports say it does not check what the barcode means.

- **Bedeutung fürs Design:** Simple loyalty-card conversion is now a built-in iOS 27 feature. The product has to stand out on binary rail/transport tickets, PDFs with several tickets, payload decoding into semantic fields, fallbacks for iOS 26 and earlier, and devices without Apple Intelligence.
- **Quelle:** <https://appleinsider.com/articles/26/06/09/how-apple-wallets-create-a-pass-works-in-ios-27>

### F34 · Konfidenz: mittel

Image slots, from the older archived guide (iPhone 6-era point sizes): strip is 375x98 pt for event tickets, 375x144 pt for coupons and gift cards, 375x123 pt otherwise, and sits behind the primary fields. Thumbnail is 90x90 pt with aspect 2:3 to 3:2, otherwise cropped. Images are 'scaled (preserving aspect ratio) to fill' their slot. Strip exists only for coupon, eventTicket and storeCard (not generic or boardingPass). `suppressStripShine` now defaults to true.

- **Bedeutung fürs Design:** An image fallback must use storeCard, coupon or eventTicket style, render at @3x (about 1125x432 px for 375x144 pt), keep primaryFields empty so no text covers the bars, and pad generous quiet zones because of fill-cropping.
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### F35 · Konfidenz: hoch

Apple's current sample pass.json in 'Creating a store card pass' and 'Creating a Poster Generic Pass' shows `"barcodes": { ... }` as an object (it must be an array) and leaves out commas between keys.

- **Bedeutung fürs Design:** Do not copy Apple's samples verbatim. Validate generated pass.json against a strict schema (barcodes is an array of objects) in backend CI.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/creating-a-poster-generic-pass>

### F36 · Konfidenz: hoch

`groupingIdentifier` groups only boarding passes and event tickets (same groupingIdentifier, passTypeIdentifier and type).

- **Bedeutung fürs Design:** A PDF with several barcodes (multiple travellers, outward and return, several legs) should become one pass per barcode, grouped with groupingIdentifier when it is a boardingPass or eventTicket.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### F37 · Konfidenz: hoch

PDF decoding approaches: xi/db-pkpass pulls the embedded barcode bitmap out of the PDF without resampling (PyMuPDF `page.get_images()` + `pdf.extract_image(xref)`) and decodes it with zxing-cpp `read_barcodes(..., formats=...)` using `result.bytes`. It contains a bug: `BarcodeFormat.Aztec or BarcodeFormat.Code128 or ...` evaluates to Aztec only; it should use `|`. Zügli rasterises pages with `page.get_pixmap(dpi=300)` (900 dpi in its API) and decodes with the commercial Barkoder SDK set to `encodingCharacterSet = "BINARY"`.

- **Bedeutung fürs Design:** Server pipeline for PDFs: (1) extract embedded images and decode them at native resolution; (2) if nothing is found, rasterise at 300 dpi, then 600-900 dpi; (3) decode in binary mode.
- **Quelle:** <https://github.com/xi/db-pkpass/blob/main/db_pkpass.py>

### F38 · Konfidenz: hoch

KDE KItinerary's barcode decoder pre-filters candidate images by aspect ratio (≤1.35 means Aztec or QR; 1.5-6.5 means PDF417; 1.95-8.0 means 1D), uses ZXing with the FixedThreshold binarizer, and treats ZXing ContentType != Text (or text with bytes above 0x7F) as binary. KPkPass already parses all eight iOS 27 PKBarcodeFormat values.

- **Bedeutung fürs Design:** Use the same cheap aspect-ratio heuristics to rank candidate regions and pick the primary barcode, and use content_type to decide between the binary and text paths.
- **Quelle:** <https://github.com/KDE/kitinerary/blob/master/src/lib/barcodedecoder.cpp>

## Empfehlungen

### E1

**Empfehlung:** Canonical barcode model end to end: the iOS app sends {symbology (Vision/zxing name), symbology_identifier (e.g. ']E0'), content_type ('text'|'binary'|'gs1'), payload_b64 (raw bytes), payload_text (optional), bbox, source ('camera'|'photo'|'pdf'), is_inverted}. The FastAPI backend builds `barcodes[]`. For every 2D target (QR, Aztec, PDF417): `message = raw_bytes.decode('latin-1')`, `messageEncoding = 'iso-8859-1'`. For 1D targets: require ASCII, `message = payload_text`, `messageEncoding = 'iso-8859-1'`. Use 'utf-8' only when the payload exists solely as text, with no raw bytes. Serialise with `json.dumps(obj)` (ensure_ascii default).

**Begründung:** Copying the bytes exactly preserves signatures (UIC 918.3, VDV, DOSIPAS) and makes charset guessing unnecessary, including for UTF-8 QR codes with non-Latin text: the original UTF-8 bytes are reproduced byte-for-byte. Zügli, db-pkpass and KDE use this in production. Base64 in the API stops any HTTP or JSON layer from mangling the bytes. Caveat: an ECI designator in the original symbol is not reproduced.

### E2

**Empfehlung:** Conversion rule table (source -&gt; barcodes[] in priority order; risk; German user message). QR -&gt; [QR]; low. Aztec -&gt; [Aztec]; low. PDF417 -&gt; [PDF417, Aztec if payload ≤ ~1000 B for Watch]; low/medium. Code128 (plain ASCII) -&gt; [Code128, QR]; low on iPhone, medium on Watch ('Auf der Apple Watch wird ein QR-Code angezeigt'). GS1-128 (FNC1) -&gt; image fallback + number field; high ('GS1-Code kann nicht exakt nachgebildet werden'). EAN-13 -&gt; [EAN13, Code128(13 digits), QR]; low on iOS 27, medium on iOS ≤26 ('Auf älteren iOS-Versionen als Code 128 – nicht jede Kasse akzeptiert das; Nummer manuell eingeben lassen'). UPC-A -&gt; [EAN13('0'+12 digits), Code128(12 digits), QR]; low on iOS 27 (identical bars). UPC-E -&gt; expand to UPC-A, then as UPC-A; medium. EAN-8 -&gt; [Code128(8), QR] or opt-in strip image; medium/high (not native even on iOS 27). Code39 -&gt; [Code39, Code128, QR]; low on iOS 27, medium otherwise; Code39 full-ASCII: test first. ITF/ITF-14 -&gt; [I2of5, Code128, QR]; ITF only for even digit counts. Codabar -&gt; [Codabar, Code128, QR]; medium on iOS 27 (start/stop chars unclear), high on iOS ≤26 because library scanners are often Codabar-only. DataMatrix (non-GS1) -&gt; [Aztec or QR with same bytes]; medium. GS1 DataMatrix / GS1 DataBar / Code93 / MSI / Telepen -&gt; opt-in strip image + number field; high. MicroQR / rMQR / MicroPDF417 -&gt; QR / PDF417 with same bytes; medium. Rotating/TOTP/animated codes -&gt; refuse ('Dynamischer Code – Kopie wäre ungültig'). HC1: / shc:/ -&gt; forward to Apple Health redirect, no pass.

**Begründung:** This follows Apple's first-displayable-barcode rule and fallback guidance (WWDC26), Watch's lack of Code128, and the fact that EAN-8, DataMatrix, DataBar and FNC1 are not native even on iOS 27. Ending each array with QR keeps something visible on old iOS and on the Watch, but the UI must say the alternative may not be accepted.

### E3

**Empfehlung:** Always put the human-readable credential (card number or ticket ID) in `altText` and in a prominent primaryField or headerField. Never put binary data in altText; for binary tickets use the order or booking number if one is decoded.

**Begründung:** Apple explicitly recommends making manual entry easy when a scan may fail. altText is not shown on watchOS, so the field copy is needed. Laser POS scanners often cannot read screens at all.

### E4

**Empfehlung:** Image fallback (render the original symbology into strip.png) only as an opt-in 'Original-Barcode als Bild' mode. Use storeCard, coupon or eventTicket style only. Render server-side at @3x with integer module widths, wide quiet zones (≥10 modules each side) and no primaryFields covering the strip. Never show a native barcode at the same time, and warn: 'Wird auf der Apple Watch nicht angezeigt'.

**Begründung:** Strip images are not shown on Apple Watch, are scaled to fill and may crop, and sit behind the primary fields. Two barcodes on one screen confuse scanners and staff. Python renderers: treepoem 3.29.0 (BWIPP; every symbology incl. GS1 DataBar, DataMatrix, Codabar) or zint-bindings 1.2.2; python-barcode 0.16.1 for EAN/UPC/Code39/ITF.

### E5

**Empfehlung:** Detection pipeline: on device, VisionKit DataScannerViewController (live, A12+, recognizesMultipleItems) plus DetectBarcodesRequest (iOS 18+) on stills. Add zxing-cpp via SPM (`ZXingCpp`, ZXIResult.bytes, tryInvert=true, minLineCount ≥ 2, validateITFCheckSum, validateCode39CheckSum where applicable) whenever Vision reports binary data, symbology aztec/qr/pdf417/dataMatrix, or payloadString == nil. Server-side, re-decode uploaded PDFs and images with zxingcpp.read_barcodes(try_invert=True) and PyMuPDF (embedded image extraction first, then 300/600/900 dpi rasterisation). Set the app's minimum iOS to 18.

**Begründung:** Apple does not document whether Vision payloadData is byte-exact for binary symbols, while zxing-cpp `.bytes` and content_type are proven in KDE, db-pkpass and Zügli. Decoding the PDF server-side gets native-resolution bitmaps and keeps the key-free iOS client simple.

### E6

**Empfehlung:** Multi-barcode selection: (1) collect every decode from all pages and frames and remove duplicates by bytes; (2) rank by successful payload classification (UIC '#UT', DOSIPAS, VDV BER-TLV, SSB, IATA 'M', 'HC1:', EAN check digit valid) &gt; 2D over 1D &gt; bounding-box area &gt; closeness to the page or screen centre; (3) show the user the top candidate's crop next to the barcode regenerated from the decoded data, plus the decoded text or summary, and let them confirm or choose another; (4) make one pass per distinct ticket barcode, grouped with groupingIdentifier for boardingPass or eventTicket.

**Begründung:** Wallet shows only one barcode per pass. Tickets often carry several codes (Aztec plus a booking-number Code128, outward and return, several travellers). A classifier ranking avoids picking an advertising QR or app-download QR from a screenshot.

### E7

**Empfehlung:** Server-side validation before signing: `message.encode(messageEncoding)` must succeed strictly. EAN-13/UPC-A must have a valid GS1 mod-10 check digit. ITF needs an even number of digits. Code39 charset is [0-9A-Z -.$/+%] unless the source was full-ASCII. Code128 must be ASCII only. Hard caps: Aztec 1914 B, QR 2953 B, PDF417 1108 B, with a soft warning well below (e.g. &gt;800 B for Aztec/QR, &gt;~25 characters for Code128). Run JSON schema validation on pass.json.

**Begründung:** Wallet behaviour for messages that cannot be encoded or are too long is undocumented, and Apple's own samples are malformed. Catching these cases before signing avoids silently broken or barcode-less passes.

### E8

**Empfehlung:** Treat time-limited and dynamic credentials explicitly. Store the decoded validity in `expirationDate` / `relevantDates`. Remind the user to re-import subscription barcodes such as the monthly D-Ticket. Detect rotating codes (two live scans a few seconds apart that differ, or known TOTP records) and refuse. Show a disclaimer that carriers' tariff rules may require the original app or PDF.

**Begründung:** Static passes cannot follow server-side rotation (SafeTix 15 s refresh) or monthly reissue. Tariff and validity risk is real for DACH transport (reports say screenshots are not valid).

### E9

**Empfehlung:** Test matrix before launch: iPhone on iOS 26 and iOS 27 (fallback order), Apple Watch on watchOS 26 and 27 (Code128 and the new 1D formats), small screens (iPhone SE), plus real readers: retail imager vs laser POS, a library Codabar scanner, a DB inspection device or the Deutschlandticket-Kontrolle app, and IATA gate or ZXing as a reference. Use golden test vectors (real DB/ÖBB/VDV/SBB/IATA payloads) and compare scanner output byte-for-byte with the source.

**Begründung:** Several behaviours that are critical for this product (Codabar start/stop, EAN13 12 vs 13 digits, watchOS support for the new formats, ECI emission, payload limits) are not in Apple's docs and can only be established empirically.

### E10

**Empfehlung:** Product positioning: lean on what iOS 27's built-in 'Create a Pass' does not cover: binary and signed rail and transport tickets (UIC 918.3/918.9/DOSIPAS, VDV-KA, SSB), PDF import with several tickets, semantic fields decoded from payloads (train, seat, validity), fallbacks for iOS 26 and earlier, devices without Apple Intelligence, and health-certificate routing.

**Begründung:** Apple now handles simple loyalty cards from photos in Wallet itself (scan path on iPhone 15 Pro, iPhone 16 and later), so a plain EAN/QR-to-pass converter has less unique value from iOS 27 on.

## Fallstricke

1. Decoding binary payloads with UTF-8 or cp1252 (instead of latin-1) corrupts UIC 918.3/VDV/DOSIPAS bytes and silently breaks the signature. The pass still looks fine, but inspection devices reject it.
2. Using AVFoundation `stringValue` or Vision `payloadStringValue`/`payloadString` for binary symbols: these are nil or lossy. payloadData (iOS 17+) has undocumented semantics, so verify it against zxing-cpp `.bytes`.
3. Putting only a new iOS 27 format (EAN13/Code39/Codabar/I2of5) in `barcodes`: on iOS 26 and earlier no barcode renders at all (WWDC26). Code128 alone shows nothing on Apple Watch.
4. Assuming the iOS 27 Barcodes page sentence 'In iOS 27 and later, you can provide more than one barcode as a fallback' means arrays are new. Fallback arrays have worked since iOS 9; only the four formats are new.
5. Copying Apple's current sample pass.json: `barcodes` appears as an object and commas are missing.
6. Re-encoding EAN-13 as Code128: the POS receives the same digits, but the AIM symbology ID changes from ]E0 to ]C0. Scanners or POS set to EAN only, self-checkouts and some loyalty back-ends may reject it. There is no fix except native EAN13 (iOS 27) or manual entry.
7. UPC-A arrives from Apple's frameworks as 13-digit EAN-13 with a leading 0 (TN2325). Stripping it from a real EAN-13 that starts with 0 corrupts the number. For PKBarcodeFormatEAN13 keep all 13 digits.
8. EAN-8, UPC-E, DataMatrix, GS1 DataBar, Code 93, MSI and MicroQR remain unsupported even in iOS 27. Do not market 'all barcodes'.
9. GS1 content (FNC1, AIs, GS separators; Vision isGS1DataCarrier == true, zxing content_type GS1, ]C1/]d2/]Q3) cannot be reproduced in Wallet. Turning it into plain Code128 or QR drops the GS1 semantics.
10. Image fallbacks in strip.png do not appear on Apple Watch, are scaled to fill and may crop, and sit behind the primary fields. The shine effect is suppressed by default now (`suppressStripShine` default true), but don't set it to false.
11. Laser scanners generally cannot read phone screens (Apple). Customers blame the app, so put the number in a prominent field.
12. Screenshots: status bar, notification banners, app chrome and promo QRs (app download, social links) appear alongside the real code. Dark-mode apps show inverted (white-on-black) codes; use Vision isColorInverted or zxing try_invert. Animated or rotating codes cannot be detected from a single screenshot.
13. Low-resolution PDF rasterisation smears dense Aztec/PDF417 modules. Extract the embedded bitmap first (PyMuPDF extract_image), otherwise rasterise at 300-900 dpi as Zügli does.
14. Python `zxingcpp.BarcodeFormat.Aztec or ...` (as in db-pkpass) selects only Aztec. Combine formats with `|`.
15. 1D misreads: Code39, Codabar and ITF have no mandatory check character, so a partial or angled read can yield a wrong but plausible number. Require several identical live reads (zxing minLineCount) and show the decoded number for user confirmation. EAN/UPC can be checked with their check digit.
16. Damaged or partially covered 2D codes may decode thanks to error correction while the user's photo still looks broken. Conversely, Wallet regenerates the symbol with its own EC level, which is fine because readers check data, not geometry.
17. Multi-ticket PDFs (several travellers, outward and return) silently lose tickets if only the first decode is used. Wallet shows one barcode per pass.
18. Monthly or period-bound subscription barcodes (e.g. Deutschlandticket) go stale. The converter app cannot push updates because it does not own the issuer backend.
19. EU DCC and SMART Health Card QRs made into generic passes duplicate Apple's verified import and raise health-data and App Review concerns. Route them to redirect.health.apple.com instead.
20. Long PDF417/Code128 payloads on narrow phone boxes give modules too thin to scan. The Watch reduces capacity further and rotates rectangular barcodes.
21. Non-ASCII bytes in Code128 messages are likely unsupported (Core Image Code128 is ASCII-only), so never route binary data to Code128.
22. ECI designators in source QR/Aztec codes are not reproduced. Scanners then fall back to charset guessing (usually UTF-8; rarely an issue in DACH).
23. Tariff conditions: some carriers say only the original app, PDF or official Wallet issue is valid. A re-rendered barcode can be refused at inspection even when it scans.

## Offene Fragen

1. Does watchOS 27 render PKBarcodeFormatCode128, and does it render the iOS 27 formats EAN13, Code39, Codabar and I2of5? No current Apple doc says. This decides whether a trailing QR fallback is mandatory.
2. What exact message format does Wallet expect for the new 1D formats: EAN13 with 12 or 13 digits (computed or validated check digit?), Codabar with or without A-D start/stop, Code39 full-ASCII and check character, I2of5 with odd lengths or a check digit?
3. What does Wallet do when `message` contains characters the messageEncoding cannot represent, or is longer than the symbology allows: no barcode, a rejected pass, or truncation?
4. Is Wallet's iso-8859-1 mapping guaranteed byte-transparent for 0x00 and 0x80-0x9F? Production practice (Zügli, DB-style passes) says yes, but Apple doesn't state it.
5. Does Wallet emit an ECI segment for messageEncoding 'utf-8' in QR/Aztec, and which error-correction level and quiet zone does it use per format?
6. What exactly is VNBarcodeObservation/BarcodeObservation.payloadData for binary Aztec, QR and PDF417: the decoded byte stream, or raw codewords with mode indicators? This needs device tests with real DB/ÖBB tickets.
7. Does iOS 27 Wallet 'Create a Pass' handle Aztec/PDF417 binary tickets and PDFs, or only loyalty-style barcodes? Does it work offline, and are user-created passes synced to Apple Watch?
8. What do DB, ÖBB, SBB and the VDV/Deutschlandticket tariff conditions say about barcodes re-rendered into a third-party Wallet pass? Inspection devices verify the signature, but the rules may still require the original medium.
9. Do common DACH retail POS systems (REWE, dm, EDEKA, Payback partners) accept Code128 or QR in place of EAN-13 for loyalty IDs? This decides the risk level of the iOS 26 and earlier fallback.
10. How fast will iOS 27 be adopted among the target users? That decides how long the Code128/QR fallbacks for EAN-13/Code39/Codabar/ITF must be the default.
11. What is the authoritative current IATA BCBP edition (beyond guide v7, 2018/2021), and are there DataMatrix-only airlines in DACH? The IATA PDF could not be fetched in this session.

## Faktencheck: alle geprüften Aussagen

### P1 · BESTÄTIGT

**Geprüfte Aussage:** pass.json barcodes[] entries take exactly four keys: format (required), message (required), messageEncoding (required, IANA charset name) and altText (optional, not shown on watchOS). Allowed formats: PKBarcodeFormatQR, PDF417, Aztec, Code128, Code39, Codabar, EAN13, I2of5. EAN-8, UPC-A, UPC-E, DataMatrix, GS1 DataBar, Code 93, MSI and MicroQR are not supported. There are no keys for EC level, module size, quiet zone, colours or ECI.

**Ergebnis:** Matches the current Pass.Barcodes JSON doc word for word: altText (required=false, 'The alternative text isn't displayed for watchOS'), format (required, allowedValues = exactly those 8 strings), message (required), messageEncoding (required, '...such as "iso-8859-1"'). No other properties exist. Caveat: Apple's own article samples ('Creating a store card pass', 'Creating a coupon pass', 'Creating a Poster Generic Pass') wrongly write "barcodes": { ... } as an object instead of an array. Do not copy them; validate pass.json against a schema.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary>

### P2 · BESTÄTIGT

**Geprüfte Aussage:** Code 39, Codabar, EAN-13 and ITF (PKBarcodeFormatI2of5) are new in iOS 27 (WWDC26 session 209). A pass with only a new type renders no barcode on iOS 26 and earlier. Apple strongly recommends a priority-ordered barcodes array. If no fallback is possible, show the credential ID in a primaryField or headerField for manual entry.

**Ergebnis:** Session 209 is 'What's new in Wallet' (WWDC26). The transcript says verbatim: 'In iOS 27, Wallet passes support four new barcode types: EAN-13, Code 39, Codabar, and Interleaved 2 of 5 (ITF)'; 'we strongly recommend providing an array of barcodes in priority order'; 'If you only provide one of the new barcode types and nothing else, the pass will not render a barcode on iOS 26 and earlier'; 'surface the credential ID in a pass field so it can be entered manually ... Consider using a primaryField, or headerField'. Apple also says to train staff for manual entry. The transcript says nothing about watchOS or about message normalisation (start/stop characters, check digits).

**Quelle:** <https://developer.apple.com/videos/play/wwdc2026/209/>

### P3 · BESTÄTIGT

**Geprüfte Aussage:** Pass.barcodes: 'The system uses the first displayable barcode for the device.' The singular barcode key is deprecated since iOS 9 / watchOS 2 and allowed only QR/PDF417/Aztec. The Barcodes page sentence 'In iOS 27 and later, you can provide more than one barcode as a fallback' only concerns the new formats; array fallback has worked since iOS 9.

**Ergebnis:** Confirmed. Pass.barcode is marked deprecated ('Use barcodes instead'). The Pass.Barcode object shows deprecatedAt iOS 9.0 / watchOS 2.0, with allowedValues QR, PDF417 and Aztec only. The archived guide says 'This allows you to specify fallbacks ... PassKit displays the first supported barcode in this array.' Minor documentation inconsistencies: the Pass `barcodes` property shows introducedVersion 6.0.0, while the object page says iOS 9.0 / watchOS 2.0 and the archived guide says 'iOS 9.0 and watchOS 3.0'. Apple's own Pass Builder (2026) still sets the legacy `barcode` to barcodes.first when it personalises from protobuf (Pass+ProtoDecode.swift). Emitting only `barcodes` remains correct for iOS 9 and later.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### P4 · BESTÄTIGT

**Geprüfte Aussage:** The archived Wallet Developer Guide says watchOS does not support PKBarcodeFormatCode128: in an array the next entry is used, and Code128 alone shows no barcode on the Watch. No current doc covers watchOS 27 and Code128 or the 4 new formats.

**Ergebnis:** The archived text is confirmed verbatim. Correction to 'no current doc': Apple's 2026 Pass Builder source (Sources/PassBuilder/PassPackage/Pass/Pass+Barcode.swift and Protobufs/PassBarcode.proto, commit dated 2026-08-07) still says 'The barcode format PKBarcodeFormatCode128 isn't supported for watchOS.' The current WalletPasses Pass.Barcodes page has dropped that sentence. No Apple source states watchOS behaviour for Code39, Codabar, EAN13 or I2of5. The archived guide also says Apple Watch rotates rectangular barcodes to portrait and recommends 'square-sized barcodes, like QR codes' for the Watch.

**Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassPackage/Pass/Pass%2BBarcode.swift>

### P5 · BESTÄTIGT

**Geprüfte Aussage:** Apple: 'Most laser scanners can't reliably read barcodes displayed on LCD screens. To scan pass barcodes, use an optical barcode scanner.' Scanners typically use ISO 8859-1 or Windows-1252; 'Unicode is poorly supported by most systems'; 'PassKit supports all encodings supported by the NSString class.'

**Ergebnis:** All quotes are verbatim in the archived 'Pass Design and Creation' chapter. The same paragraph also says 'All of the supported barcode formats are two-dimensional', which is outdated: Code128 has been supported since iOS 9 and the new 1D formats since iOS 27.

**Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### P6 · BESTÄTIGT

**Geprüfte Aussage:** messageEncoding is 'The IANA character set name of the text encoding to use to convert message from a string representation to a data representation that the system renders as a barcode'. Apple does not document that iso-8859-1 is byte-transparent for 0x00-0xFF.

**Ergebnis:** Definition is verbatim. No Apple Wallet doc states byte transparency. The only related Apple statement is in Core Image, not Wallet: the archived CIQRCodeGenerator reference says 'To create a QR code from a string or URL, convert it to an NSData object using the NSISOLatin1StringEncoding string encoding.'

**Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary>

### P7 · KORRIGIERT

**Geprüfte Aussage:** Zügli builds {format: PKBarcodeFormatAztec, message: bytes(barcode_data).decode('iso-8859-1'), messageEncoding: 'iso-8859-1'} and serialises with json.dumps(...).encode('utf-8'). xi/db-pkpass does the same. KItinerary reads iso-8859-1 pkpass barcodes back with msg.toLatin1(). This is a proven production pattern.

**Ergebnis:** The code snippets are accurate: zuegli main/views/passes.py (e.g. lines ~420 and ~2941 at commit 99ec9bd, 2026-10-05; SNCB Train+ QR uses utf-8 instead), and json.dumps(pass_json).encode('utf-8') at ~5983. db_pkpass.py lines 241-247 use message.decode('iso-8859-1'). Three corrections. (1) Zügli is EUPL-1.2 (copyleft) and decodes images with the commercial Barkoder SDK (main/aztec.py, encodingCharacterSet='BINARY'), not zxing-cpp. (2) xi/db-pkpass (MIT) is not production evidence: its README says 'The PKPass file does not contain a signature, so it will not work with Apple Wallet' and the code 'has not been extensively tested'. (3) KItinerary (LGPL-2.0-or-later, pkpassdocumentprocessor.cpp) uses toLatin1() only when messageEncoding equals iso-8859-1 (case-insensitive) AND the message contains a null, non-printable or non-character code point. Otherwise it uses toUtf8(). Only Zügli is evidence that Wallet reproduces binary bytes in practice.

**Quelle:** <https://github.com/TheEnbyperor/zuegli/blob/master/main/views/passes.py>

### P8 · BESTÄTIGT

**Geprüfte Aussage:** Python iso-8859-1/latin-1 maps all 256 byte values 1:1 and round-trips through json.dumps/json.loads. cp1252 raises on 0x81 and utf-8 raises on arbitrary binary. json.dumps escapes control characters even with ensure_ascii=False.

**Ergebnis:** Re-tested on Python 3.13.16: bytes(range(256)) -&gt; decode('iso-8859-1') -&gt; json.dumps -&gt; json.loads -&gt; encode('iso-8859-1') returns identical bytes with both ensure_ascii=True and ensure_ascii=False. cp1252 fails on 0x81, 0x8D, 0x8F, 0x90 and 0x9D. utf-8 fails at 0x80. Nuance: with ensure_ascii=False, 0x7F-0x9F are written raw (still valid JSON, because JSON only requires escaping U+0000-U+001F). The ensure_ascii=True default (\u00XX escapes) is the safer choice. Codec aliases: 'iso-8859-1' and 'latin-1' both resolve to iso8859-1.

**Quelle:** <https://docs.python.org/3/library/codecs.html#standard-encodings>

### P9 · BESTÄTIGT

**Geprüfte Aussage:** Core Image's Code 128 generator says the barcode 'can contain any of the 128 ASCII characters' and its sample uses .data(using: .ascii). Apple does not document how Wallet handles non-ASCII in Code128.

**Ergebnis:** Confirmed. The archived Core Image Filter Reference is stricter. CICode128BarcodeGenerator inputMessage: 'Must not contain non-ASCII characters', and 'convert it to an NSData object using the NSASCIIStringEncoding string encoding'. It is still undocumented whether Wallet uses Core Image internally.

**Quelle:** <https://developer.apple.com/library/archive/documentation/GraphicsImaging/Reference/CoreImageFilterReference/index.html>

### P10 · KORRIGIERT

**Geprüfte Aussage:** Core Image Aztec: compact up to 44 bytes in up to 4 layers, full-size up to 1914 bytes in up to 32 layers, correctionLevel 5-95. QR 40-L 2953 bytes / 7089 digits / 4296 alphanumeric; PDF417 1108 bytes / 1850 text / 2710 digits. All maxima assume the lowest error correction.

**Ergebnis:** The Aztec maximum does NOT assume the lowest EC. The archived CIAztecCodeGenerator reference gives inputCorrectionLevel 'Default value: 23.00 Minimum: 5.00 Maximum: 95.00' and full-size 'up to 1914 bytes of message data (including correction) in up to 32 layers ... no larger than 151 x 151'. A 32-layer full Aztec has (112+16\*32)\*32 = 19,968 bits = 1,664 12-bit codewords (formula from zxing-cpp AZEncoder.cpp TotalBitsInLayer). At the ISO 24778 recommended 23% + 3 codewords that leaves 1,278 data codewords = 15,336 bits, which gives exactly 1914 bytes / 3832 digits / 3067 text characters. 1914 B is therefore the default ~23%-EC figure; at 5% EC roughly 2,300+ bytes would theoretically fit. The QR 40-L figures (2953/7089/4296) and PDF417 figures (1108/1850/2710 at EC level 0) are correct lowest-EC maxima. Core Image's QR default EC is M, where 40-M holds about 2331 bytes. Wallet's actual EC choices remain undocumented.

**Quelle:** <https://developer.apple.com/library/archive/documentation/GraphicsImaging/Reference/CoreImageFilterReference/index.html>

### P11 · BESTÄTIGT

**Geprüfte Aussage:** The archived guide: the format sets a hard maximum but 'scanning conditions often lower this limit' (example: Apple Watch in poor light with an inexpensive scanner). Current docs: 'Wallet optimizes the presentation of passes in order to facilitate a successful scan.'

**Ergebnis:** Both quotes are confirmed. The current sentence is in 'Creating a store card pass', 'Creating a coupon pass' and 'Creating a Poster Generic Pass': 'Wallet supports 2D barcodes using QR, PDF417, Aztec, Code128, Code 39, Codabar, EAN-13, and Interleaved 2 of 5 (ITF) formats. Wallet optimizes the presentation of passes in order to facilitate a successful scan.' Apple wrongly calls them all 2D.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/creating-a-store-card-pass>

### P12 · BESTÄTIGT

**Geprüfte Aussage:** Whether GS1-128 (Code128 with FNC1) is possible in Wallet is undocumented. Forum thread 80458 (2017) asking about FNC1 has no replies.

**Ergebnis:** Thread 'GS1-128 barcode format in Apple Wallet Pass', June 2017, 0 replies, about 5.6k views. Its sample uses message '8018131041711111111111', PKBarcodeFormatCode128, iso-8859-1. No Apple doc mentions FNC1.

**Quelle:** <https://developer.apple.com/forums/thread/80458>

### P13 · BESTÄTIGT

**Geprüfte Aussage:** The Vision symbology list (aztec ... upce, codabar/microQR/gs1DataBarLimited iOS 15, msiPlessey iOS 17) has no UPC-A constant. DetectBarcodesRequest (iOS 18+, revision4) returns BarcodeObservation with payloadData, payloadString, isColorInverted, isGS1DataCarrier, supplementalPayloadString/Data, symbology and boundingRegion.

**Ergebnis:** Confirmed against the BarcodeSymbology and VNBarcodeSymbology topic lists. Availability: codabar, gs1DataBar, gs1DataBarExpanded, gs1DataBarLimited and microQR are iOS 15.0; msiPlessey is iOS 17.0. DetectBarcodesRequest, BarcodeObservation and BarcodeSymbology are iOS 18.0 / macOS 15.0 and now also watchOS 27.0. Revision has only .revision4. The request also offers `coalescesCompositeSymbologies` and the observation offers `supplementalCompositeType` (BarcodeObservation.CompositeType).

**Quelle:** <https://developer.apple.com/documentation/vision/barcodeobservation>

### P14 · BESTÄTIGT

**Geprüfte Aussage:** VNBarcodeObservation.payloadData and isColorInverted are iOS 17+, barcodeDescriptor is iOS 11+. payloadData is only 'The raw data representation of the barcode's payload'. CIAztecCodeDescriptor.errorCorrectedPayload holds codewords.

**Ergebnis:** payloadData and isColorInverted are iOS 17.0 / macOS 14.0. barcodeDescriptor is iOS 11.0 ('Use this object to have Core Image regenerate the observed barcode'). payloadStringValue: 'Depending on the symbology or the payload data itself, a string representation of the payload may not be available.' CIAztecCodeDescriptor.errorCorrectedPayload is 'The error-corrected payload that comprises the Aztec code symbol', alongside isCompact, layerCount and dataCodewordCount.

**Quelle:** <https://developer.apple.com/documentation/vision/vnbarcodeobservation/payloaddata>

### P15 · KORRIGIERT

**Geprüfte Aussage:** TN2325: UPC-A is reported as EAN-13 with a leading zero; EAN-2/EAN-5 are not supported; each AVCaptureMetadataOutput callback returns at most four barcodes, usually those nearest the centre; 1D detectors sample limited scan lines.

**Ergebnis:** TN2325 (2013) says: 'Only a single 1-dimensional code will be returned with each call ... and it will correspond to the center-most decodable barcode in the rectOfInterest.' The four-per-call limit applies only to 2D codes ('There is a limit of four barcodes per call ... which will usually correspond to the center-most codes'). PDF417 is treated as a stacked 1D code by the scan-line detector. 'A decoded UPC-A barcode is output as AVMetadataObjectTypeEAN13Code with a leading zero in the stringValue.' EAN-2/EAN-5: 'No.' Separately, a local zxing-cpp 3.1.1 round-trip test also reported a generated UPC-A as EAN-13 ('0'+12 digits, symbology identifier ]E0) when reading with default formats.

**Quelle:** <https://developer.apple.com/library/archive/technotes/tn2325/_index.html>

### P16 · BESTÄTIGT

**Geprüfte Aussage:** DataScannerViewController (VisionKit, iOS 16+) needs A12 Bionic or later (isSupported). .barcode(symbologies:) takes VNBarcodeSymbology. RecognizedItem.Barcode exposes payloadStringValue and observation: VNBarcodeObservation.

**Ergebnis:** Declarations: `static func barcode(symbologies: [VNBarcodeSymbology] = []) -> DataScannerViewController.RecognizedDataType` and `var observation: VNBarcodeObservation`. isSupported: 'the device must have the A12 Bionic chip or later' and it is false on visionOS. The UIRequiredDeviceCapabilities subkey is `iphone-ipad-minimum-performance-a12`. capturePhoto() is available for a high-resolution still to re-decode.

**Quelle:** <https://developer.apple.com/documentation/visionkit/datascannerviewcontroller/issupported>

### P17 · BESTÄTIGT

**Geprüfte Aussage:** zxing-cpp (Apache-2.0, PyPI 3.1.1 released 2026-07-29) Python read_barcodes(...) returns Barcode objects with .bytes/.text/.format/.content_type/.symbology_identifier/.ec_level/.position. The Swift Package ZXingCpp (iOS 12+) has ZXIResult.bytes (NSData) and ZXIReaderOptions tryInvert/minLineCount/validateCode39CheckSum/validateITFCheckSum.

**Ergebnis:** PyPI: 3.1.1 uploaded 2026-07-29T08:50:14Z, license_expression Apache-2.0, requires Python &gt;=3.9. The installed 3.1.1 signature also has `ean_add_on_symbol=EanAddOnSymbol.Ignore`, and Barcode also exposes .orientation, .symbology, .valid, .error and .extra. At tag v3.1.1, Package.swift declares product 'ZXingCpp' with .iOS(.v12) and .macOS(.v13). Important for the design: the iOS ZXIResult has NO contentType property (it has text, bytes, format, ecLevel, symbologyIdentifier, orientation, lineCount, gtin, sequence\*), so content_type==Binary is only available server-side. In core v3.1.1, validateCode39CheckSum and validateITFCheckSum are [[deprecated]] aliases of validateOptionalChecksum, tryCode39ExtendedMode is a no-op, and minLineCount already defaults to 2.

**Quelle:** <https://github.com/zxing-cpp/zxing-cpp/blob/v3.1.1/wrappers/ios/Sources/Wrapper/Reader/ZXIResult.h>

### P18 · BESTÄTIGT

**Geprüfte Aussage:** zxing-cpp's Codabar text includes the A-D start/stop characters. The WWDC26 Codabar sample message is '123456789'. Apple does not document start/stop or check-digit handling for Codabar, EAN13, Code39 or I2of5.

**Ergebnis:** Local test with zxing-cpp 3.1.1: a Codabar symbol created as 'A123456789B' reads back with text 'A123456789B' (symbology identifier ]F0). Creating Codabar from '123456789' fails with 'Does not begin with "A", "B", "C" or "D"'. The WWDC26 fallback sample uses message "123456789" for both PKBarcodeFormatCodabar and PKBarcodeFormatQR. The Pass.Barcodes page has no normalisation rules.

**Quelle:** <https://developer.apple.com/videos/play/wwdc2026/209/>

### P19 · BESTÄTIGT

**Geprüfte Aussage:** UIC 918.3 layout (Zügli): '#UT' + 2-digit version + 4-digit RICS + 5-char key ID + signature (v1 50 bytes DER DSA/SHA-1, v2 64 bytes r||s) + 4-digit ASCII length + zlib records (U_HEAD, U_TLAY, U_FLEX, 0080BL, 0080VU). Binary.

**Ergebnis:** Confirmed in envelope.py parse(). Details: the signature covers the zlib-COMPRESSED bytes (signed_data = data[4:4+len]). v2 uses SHA256withECDSA or SHA224withDSA depending on key metadata. The key ID may be non-numeric. Each record has a 6-char ID + 2-digit version + 4-digit length (the length includes the 12-byte header). ticket.py treats 'U_\*', '0080BL' and '0080VU' as known records and also accepts '3606AA' as a layout record.

**Quelle:** <https://github.com/TheEnbyperor/zuegli/blob/master/main/uic/envelope.py>

### P20 · KORRIGIERT

**Geprüfte Aussage:** DB online tickets carry a UIC 918.3 Aztec barcode with VDV-KA extensions; uic-918-3 documents 0080BL and 0080VU; DB's interoperability PDF reportedly specifies Aztec with 23% EC.

**Ergebnis:** uic-918-3 README (MIT) confirms '0080BL: A specific container on tickets from Deutsche Bahn ... used for proof-of-payment checks on the train' and '0080VU: A specific container on (some) tickets from Deutsche Bahn ... used on products, which are also accepted by other carriers, especially (local) public transport companies' (link bahn.de/vdv-barcode). 'VDV-KA extensions' is imprecise: 0080VU is a DB-defined record inside the UIC 918.3 container, not a VDV-KA barcode. The 23% Aztec EC claim could not be verified (no primary source reachable).

**Quelle:** <https://github.com/justusjonas74/uic-918-3>

### P21 · NICHT VERIFIZIERBAR

**Geprüfte Aussage:** Deutschlandticket barcodes are VDV-KA or UIC (signed). UIC FCB (918.9) inspection must be implemented nationwide. 918.9 was to replace 918.3 from 2024 to end of 2025. The D-Ticket barcode in DB Navigator changes monthly.

**Ergebnis:** kcd-nrw.de was unreachable from this environment. Search results only show that a KCD 'Ergebnisdokument der Arbeitsgruppe Kontrolle' exists (V1.3, 06/2024), and a Coburg tender annex lists inspection of VDV-KA cards, UIC 918-3 and 918-9 codes and VDV barcodes. The 2024-2025 timeline and the monthly barcode change were not verified.

**Quelle:** <https://kcd-nrw.de/fileadmin/user_upload/240625_Ergebnisdokument_der_Arbeitsgruppe_Kontrolle_V1.3.pdf>

### P22 · BESTÄTIGT

**Geprüfte Aussage:** VDV-KA barcodes are BER-TLV with an ISO 9796-2 RSA signature (message recovery), residual data and a CA certificate. Zügli detects them by BER-TLV parse and emits PKBarcodeFormatAztec.

**Ergebnis:** Zügli main/vdv/envelope.py parses BER-TLV with signature tag (128-byte RSA signature), remaining-data tag, certificate and CA reference, and decrypts with ISO 9796-2. KItinerary src/lib/vdv/vdvticketparser.cpp does the same (TagSignature, TagSignatureRemainder, CV certificate, CA reference, Iso9796_2Decoder). KItinerary also ships 35 VDV certificate files (src/lib/vdv/certs), so decoding needs only the published VDV certificates, not membership.

**Quelle:** <https://github.com/TheEnbyperor/zuegli/blob/master/main/vdv/envelope.py>

### P23 · BESTÄTIGT

**Geprüfte Aussage:** SBB/SwissPass barcode is a QR code with protobuf content (KDE wiki); Zügli renders SwissPass as PKBarcodeFormatQR. ÖBB uses Aztec UIC 918.3 with a JSON vendor record.

**Ergebnis:** The KDE wiki was unreachable, so this was verified from source code. KItinerary src/lib/scripts/sbb.js parses the QR bytes with a protobuf stream reader (token 'qrcodebin:', provider uic:1085). Zügli passes.py (~5134-5140) emits PKBarcodeFormatQR for SwissPassTicketInstance. KItinerary oebb.js uses 'aztecbin:' tokens and parses UIC vendor block '118199' as JSON. The ÖBB FAQ was not verified.

**Quelle:** <https://github.com/KDE/kitinerary/blob/master/src/lib/scripts/sbb.js>

### P24 · BESTÄTIGT

**Geprüfte Aussage:** IATA BCBP (Res. 792): paper uses PDF417; mobile may use Aztec, DataMatrix or QR; data is ASCII starting with 'M' + number of legs; Zügli renders IATA as Aztec.

**Ergebnis:** The IATA guide PDF and iata.org were unreachable. Search results quote IATA's 2010 press release: mobile 2D passes can use Aztec, Datamatrix or QR, with the same data as printed passes. KItinerary iatabcbp.cpp requires data[0]=='M' and data[1] to be a digit (number of legs). Zügli passes.py (~5350-5356) emits PKBarcodeFormatAztec for IATATicketInstance. Treat the symbology rules as medium confidence until the IATA guide is read.

**Quelle:** <https://github.com/KDE/kitinerary/blob/master/src/lib/iata/iatabcbp.cpp>

### P25 · KORRIGIERT

**Geprüfte Aussage:** Ticketmaster SafeTix uses an encrypted barcode that refreshes about every 15 seconds and screenshots are not accepted. On iPhone it uses an NFC token in Wallet issued only by Ticketmaster.

**Ergebnis:** The cited TechCrunch article (2019) says the barcode 'automatically refreshes every few seconds'. The '15 seconds' figure and 'screenshots will not be accepted' come from venue notices (e.g. Syracuse/cuse.com, 2022). The venue notices say the Wallet version deploys an NFC token ('hold near reader'), and one says the SafeTix Wallet enhancements require iOS 16.4 or higher. The conclusion is unchanged: rotating codes cannot be copied to static passes. These are secondary sources; Ticketmaster's own pages were not reachable.

**Quelle:** <https://cuse.com/news/2022/8/25/safetix-in-place-for-jma-wireless-dome-events-this-year>

## Vom Faktenprüfer ergänzte wichtige Fakten

1. PRODUCT-LEVEL RISK (App Store Review Guidelines, current): Guideline 1.5 says 'ensure that Wallet passes include valid contact information from the issuer and are signed with a dedicated certificate assigned to the brand or trademark owner of the pass.' Guideline 3.2.1(iv) says 'Wallet passes can be used to make or receive payments, transmit offers, or offer identification ... Other uses may result in the rejection of the app and the revocation of Wallet credentials.' A converter that signs third-party credentials (DB, ÖBB, airlines, retailers) with QRCode2Wallet's own Pass Type ID conflicts with the literal text of 1.5. Design implications: never use the carrier's logo or organizationName as if it issued the pass; put the app's own contact details in the pass; budget for App Review push-back and Pass Type ID revocation. Source: https://developer.apple.com/app-store/review/guidelines/
2. Apple explicitly advises against the 'barcode as strip image' fallback in recommendation 4. Pass Designer article: 'You can provide all barcode information directly in the Pass Designer app, and the barcodes generate automatically, with no need to provide any barcodes as images ... Don't include any barcodes in images.' HIG Wallet (June 2026): 'Use Pass Designer or corresponding APIs to add barcodes rather than embedding them in pass images.' The docs also conflict on Apple Watch: the HIG says 'In every style, watchOS crops the strip image to fit the aspect ratio of the card interface', while 'Creating a store card pass' says Watch 'doesn't show the strip image'. Either way a strip-image barcode is unreliable on the Watch and is a review risk. Sources: https://developer.apple.com/documentation/walletpasses/creating-a-pass-with-pass-designer and https://developer.apple.com/design/human-interface-guidelines/wallet
3. Apple released Pass Builder at WWDC26 (github.com/apple/pass-builder, Apache-2.0, labelled 'Early preview: APIs may change without notice', Swift 6.3+, macOS 14+ or Linux). It provides PassPackage, PassSigner(passCertificate:wwdrCertificate:), PassValidator, a `buildpass` CLI and protobuf definitions of the pass format, so non-Swift backends can drive buildpass. Pass.BarcodeFormat cases are qr, pdf417, aztec, code128, code39, codabar, ean13 and i2of5, with default messageEncoding 'iso-8859-1'. The built-in validators (RequiredImages, Seat, BoardingPass, EventTicket, FieldFormatting) do NOT check barcode messages, encodings or lengths, so the server-side barcode validation is still needed. Decision for the Python backend: keep Python signing, or call buildpass as a sidecar. Source: https://github.com/apple/pass-builder
4. iOS/watchOS 27 add the Poster Generic style (`posterGeneric`). Apple says to put a legacy style key (generic/storeCard/coupon/eventTicket) next to it; 'Wallet's style resolution prioritizes posterGeneric when present'. Its layout is described 'with a square QR code', while generic passes use 'a rectangular barcode'. Apple's sample still uses Code128 and does not document how 1D formats look in the poster layout. The same article notes 'Generic passes don't auto-expire based on the signing date. Use expirationDate'. This matters for loyalty/membership conversions and for barcode choice (square 2D codes suit both the poster layout and the Watch). Source: https://developer.apple.com/documentation/walletpasses/creating-a-poster-generic-pass
5. The Aztec 1914-byte figure corresponds to the ISO-recommended / Core Image default error correction of about 23% + 3 codewords, not the lowest EC (see the claim 10 correction). Keep 1914 B as a conservative hard cap. Do not reason that 'Wallet's EC is unknown, so the real maximum is lower than the lowest-EC figure'. Source: https://developer.apple.com/library/archive/documentation/GraphicsImaging/Reference/CoreImageFilterReference/index.html
6. Recommendation 5's rationale is partly wrong. Zügli does not use zxing-cpp: it uses the commercial Barkoder SDK in 'BINARY' charset mode (main/aztec.py). db-pkpass uses zxing-cpp `.bytes` but produces unsigned, untested passes. Only KItinerary is real-world evidence for ZXing-cpp byte output. On iOS, the ZXingCpp wrapper at v3.1.1 exposes `bytes` but no `contentType`, so binary-vs-text classification on the client must use the raw bytes (UIC '#UT' magic, BER-TLV parse, non-printables) or be left to the server's zxingcpp `content_type`. Sources: https://github.com/TheEnbyperor/zuegli/blob/master/main/aztec.py and https://github.com/zxing-cpp/zxing-cpp/blob/v3.1.1/wrappers/ios/Sources/Wrapper/Reader/ZXIResult.h
7. License constraints on the reference implementations: Zügli is EUPL-1.2 (copyleft, so porting its UIC/VDV/SSB parsers into a closed commercial backend carries obligations). KItinerary is LGPL-2.0-or-later. db-pkpass, uic-918-3 (justusjonas74) and zxing-cpp are MIT / MIT / Apache-2.0. Pass Builder is Apache-2.0. Prefer re-implementing from the specs or using MIT/Apache code. Source: https://github.com/TheEnbyperor/zuegli/blob/master/LICENSE.md
8. The current Pass.Barcodes reference no longer carries the 'Code128 isn't supported for watchOS' note. The deprecated Pass.Barcode page and Apple's 2026 Pass Builder still do. There is still no Apple statement on watchOS 27 support for Code39, Codabar, EAN13 or I2of5. The archived guide adds that the Watch rotates rectangular barcodes to portrait and recommends square codes like QR. Keep a QR (or Aztec) final entry for Watch coverage and test on watchOS 27. Source: https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html
9. iOS 27 Wallet 'Create a Pass' (low confidence; support.apple.com was unreachable, only search snippets seen): there is a manual creation path in Wallet, plus a Siri Mode / Visual Intelligence scan path (Camera, or Photos/screenshot) that needs an Apple Intelligence iPhone (iPhone 15 Pro or later) with a supported language and region. Reports say user-created passes carry static data and may not be accepted everywhere. Because manual creation does not appear to need Apple Intelligence, 'devices without Apple Intelligence' is a weak differentiator in recommendation 10. The stronger differentiators are binary/signed transport payloads, multi-ticket PDFs and decoded semantics. Source: https://support.apple.com/en-us/127821
10. Health-certificate routing ('HC1:' EU DCC) has little value in 2026. The EU Digital COVID Certificate regulation expired on 30 June 2023 (from memory; eur-lex was unreachable, low confidence). Do not invest in that branch of the rule table.
11. `sharingProhibited` (iOS 11+) removes the Share button but 'does not prevent sharing the pass in some other way'. Consider setting it on personal, signed transport tickets to discourage redistribution of copies. `groupingIdentifier` is documented only for 'boarding passes or event tickets'. Source: https://developer.apple.com/documentation/walletpasses/pass
12. Vision's BarcodeObservation exposes `supplementalPayloadString/Data`, `supplementalCompositeType` and `coalescesCompositeSymbologies` for EAN add-ons and GS1 composites. Wallet cannot render add-ons or composites, so the converter must drop them (or show them as text) and warn the user. A periodical or book code with an EAN-5 add-on will lose the add-on. Source: https://developer.apple.com/documentation/vision/barcodeobservation
