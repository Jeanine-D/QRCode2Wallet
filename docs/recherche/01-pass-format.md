# 01 · Apple-Wallet-Passformat (.pkpass)

> **Hinweis:** Vollständige Rohfassung der Recherche vom 10.10.2026: KI-Agenten-Recherche gegen Primärquellen, danach von einem unabhängigen Faktenprüfer adversarial gegengeprüft. Die Inhalte stehen in der Originalsprache Englisch. Die deutsche Zusammenfassung mit Bewertung steht in der [Übersicht](README.md). Rechtliche Aussagen sind **keine Rechtsberatung**.

**Recherchierter Umfang:** Apple Wallet pass package format (.pkpass): complete and current as of 2026-10-10 (iOS 18 / 26 / 27, verified against the live developer.apple.com DocC JSON, HIG Wallet (updated June 8, 2026), WWDC24/25/26 Wallet sessions, the archived Wallet Developer Guide, and Apple's open-source Pass Builder (github.com/apple/pass-builder) source)

**Inhalt:** 44 Fakten (Konfidenz hoch 35, mittel 6, niedrig 3) · 12 Empfehlungen · 18 Fallstricke · 12 offene Fragen · Faktencheck von 25 Kernaussagen: 23 bestätigt, 2 korrigiert, 0 nicht verifizierbar · 16 vom Faktenprüfer ergänzte Fakten

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

- **[KORRIGIERT]** Up to 10 locations {latitude, longitude, altitude, relevantText} and up to 10 distinct beacon UUIDs. maxDistance in meters (the smaller of this value and the default applies). Archived rules: coupons and store cards do not support relevant date and must provide locations if they carry relevance info.
  - **Ergebnis:** Limits and keys confirmed. The relevance rule is incomplete: it applies to generic passes too. Current doc: 'Set a date by adding the relevantDate key to Pass for boarding passes, event tickets, and generic passes' and 'Coupons, store cards, and generic passes must provide locations if you added any other type of relevance information to the pass object.' Archived Table 4-2 also gives Generic: relevant date 'Optional', relevant locations 'Required if relevance information is provided'. The archived table interprets location radius as small (~100 m) for coupon, store card and generic, and large (~1000 m) for boarding pass and event ticket. Beacons: 'Add up to ten different UUIDs'. maxDistance: 'The system uses the smaller of this distance or the default distance.'
  - **Quelle:** <https://developer.apple.com/documentation/walletpasses/showing-a-pass-on-the-lock-screen>

- **[KORRIGIERT]** Other keys: expirationDate (Wallet auto-hides expired passes), voided (default false), sharingProhibited (iOS 11+, only removes the Share button), suppressStripShine (default true), groupingIdentifier (boarding passes and event tickets only), logoText (not on poster event tickets), userInfo, appLaunchURL + associatedStoreIdentifiers (not on watchOS).
  - **Ergebnis:** All quoted key semantics match the Pass reference, except 'Wallet auto-hides expired passes', which the Pass reference does not state. Apple Support (Remove passes from Apple Wallet) says limited or single-use passes such as boarding passes and event tickets are hidden after they expire, governed by the user setting 'Hide Expired Passes'. Hiding of store cards or generic passes is not documented. Developer reports on Apple's forum (thread 708761, iOS 15.6.1–17.6.1, FB9813388) say event tickets are hidden about 24 h after relevantDate even when expirationDate is in the future. expirationDate must include hours and minutes. Verbatim confirmations: sharingProhibited 'introduced in iOS 11 ... nor does it prevent sharing the pass in some other way'; suppressStripShine 'The default value is true'; associatedStoreIdentifiers '[number] ... A link to launch the app is on the back of the pass ... isn't supported for watchOS'.
  - **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

## Fakten

### F1 · Konfidenz: mittel

The current OS generation is iOS 27, not iOS 26. WWDC26 session 209 introduces iOS 27 Wallet features. The HIG Wallet change log reads 'June 8, 2026 – Updated to reflect guidance for iOS 27 and the Pass Designer app'. Pass Designer requires macOS 27. Apple docs now show watchOS 27 APIs as non-beta. That iOS 27 has shipped publicly is an inference from the usual September release, not something I verified directly.

- **Bedeutung fürs Design:** Treat iOS 27 / Xcode 27 as current, not iOS 26. Design pass.json so that iOS 27-only features (posterGeneric, new barcode formats, featuredActions) degrade cleanly on iOS 26 and earlier.
- **Quelle:** <https://developer.apple.com/design/human-interface-guidelines/wallet>

### F2 · Konfidenz: hoch

Package layout: a directory holding pass.json, PNG images (icon is mandatory), optional localization folders '&lt;lang&gt;[-&lt;region&gt;].lproj/' (each with pass.strings and/or localized images), manifest.json and signature. The whole thing is ZIPped and renamed from .zip to .pkpass. Metadata files such as .DS_Store must not be in the manifest or the archive.

- **Bedeutung fürs Design:** The backend builds the package in memory: dict of filename -&gt; bytes, then manifest, then signature, then zip. Never zip a temp directory that could pick up stray files.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/building-a-pass>

### F3 · Konfidenz: hoch

manifest.json is a flat JSON object. Keys are file paths relative to the pass root, using '/' as separator (e.g. 'en.lproj/pass.strings', 'icon@2x.png'). Values are the hex-encoded SHA-1 of each file's exact bytes. It covers every file except manifest.json and signature, including files in subdirectories. SHA-1 is still the algorithm in 2026: Apple's own Pass Builder computes data.sha1Hash() per file.

- **Bedeutung fürs Design:** Python: hashlib.sha1(file_bytes).hexdigest() for each file. Hash exactly the bytes you write into the zip (serialize pass.json once, then reuse those bytes).
- **Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassSigning/Manifest/InMemoryManifestGenerator.swift>

### F4 · Konfidenz: hoch

signature is a PKCS#7/CMS detached signature over the exact bytes of manifest.json. It is made with the private key of the Pass Type ID certificate, must include the Apple WWDR intermediate certificate, and must carry the S/MIME signing-time attribute. Apple's Pass Builder calls CMS.sign(manifest, additionalIntermediateCertificates:[wwdr], certificate:passCert, privateKey:key, signingTime:Date()) and writes the DER bytes to a file named 'signature'.

- **Bedeutung fürs Design:** Backend signer contract: input manifest bytes, output DER CMS SignedData (detached) with signer cert, WWDR G4 and signingTime. Also confirmed in https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassSigning/ManifestSignatureGenerator.swift
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### F5 · Konfidenz: hoch

Pass Type ID certificates (including 'Pass Type ID with NFC') are issued under WWDR intermediate G4. G3 is for software signing and is the wrong intermediate for passes.

- **Bedeutung fürs Design:** Bundle AppleWWDRCAG4.cer (from https://www.apple.com/certificateauthority/) with the signer service. Using the wrong intermediate is a classic cause of 'invalid signature'.
- **Quelle:** <https://developer.apple.com/help/account/certificates/wwdr-intermediate-certificates/>

### F6 · Konfidenz: hoch

Python signing with pyca/cryptography (tested locally on 50.0.1; PyPI latest is 50.0.2): pkcs7.PKCS7SignatureBuilder().set_data(manifest_bytes).add_signer(pass_cert, private_key, hashes.SHA256()).add_certificate(wwdr_g4_cert).sign(serialization.Encoding.DER, [pkcs7.PKCS7Options.DetachedSignature, pkcs7.PKCS7Options.Binary]). By default the builder adds the signed attributes contentType, signingTime, messageDigest and SMIMECapabilities, which I confirmed with openssl asn1parse. Without PKCS7Options.Binary the library converts LF to CRLF before signing, and 'openssl smime -verify -binary' against the original manifest then FAILS. I confirmed that failure empirically.

- **Bedeutung fürs Design:** No third-party pkpass library is needed. A signer of about 40 lines on top of cryptography is enough. Load the .p12 with cryptography.hazmat.primitives.serialization.pkcs12.load_key_and_certificates. PKCS7Options.Binary is mandatory.
- **Quelle:** <https://raw.githubusercontent.com/pyca/cryptography/main/docs/hazmat/primitives/asymmetric/serialization.rst>

### F7 · Konfidenz: hoch

ZIP structure: files sit at the archive root, with no top-level folder. Apple's Pass Builder runs 'zip -r -q &lt;output&gt; .' with the working directory set to the pass directory.

- **Bedeutung fürs Design:** Python zipfile: writestr('pass.json', ...) and so on at the root, ZIP_DEFLATED. Do not prefix entries with 'MyPass.pass/'.
- **Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassSigning/Zipper.swift>

### F8 · Konfidenz: hoch

MIME types: a single pass is application/vnd.apple.pkpass (the response type of the 'Send an Updated Pass' endpoint; Mail and Safari expect it). A bundle is application/vnd.apple.pkpasses: a .zip of .pkpass files renamed to .pkpasses, holding at most 10 passes or 150 MB.

- **Bedeutung fürs Design:** FastAPI: Response(content=pkpass_bytes, media_type='application/vnd.apple.pkpass'). The archive guide also confirms the single-pass type: https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/DistributingPasses.html
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/distributing-and-updating-a-pass>

### F9 · Konfidenz: niedrig

Apple documents no maximum size for a single .pkpass; only the .pkpasses bundle limit (10 passes / 150 MB) is official. Third-party vendors suggest keeping a pass under about 5 MB and each image around 100 KB. The HIG says: 'Keep image file sizes small.'

- **Bedeutung fürs Design:** Set an internal budget, e.g. 1 MB per pass, and recompress PNGs with Pillow optimize=True. User photos used as artwork are the main risk.
- **Quelle:** <https://developer.apple.com/design/human-interface-guidelines/wallet>

### F10 · Konfidenz: hoch

Required top-level pass.json keys: formatVersion (number, must be 1), passTypeIdentifier (must match the signing certificate; reverse-DNS starting with 'pass.'), serialNumber (unique per passTypeIdentifier), teamIdentifier (must match the certificate's team), organizationName (localizable), description (localizable; used for accessibility/VoiceOver). In addition, exactly one style key is needed (boardingPass | coupon | eventTicket | generic | storeCard), plus optionally posterGeneric on iOS 27.

- **Bedeutung fürs Design:** Backend pydantic model: these 6 fields are non-optional. teamIdentifier and passTypeIdentifier come from server config, never from the client.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### F11 · Konfidenz: hoch

Same passTypeIdentifier + serialNumber = the same pass. Adding a pass with an identifier pair already on the device overwrites the old one, and an update is simply a new pass with the same pair. authenticationToken and serialNumber cannot change in an update. PKPassLibrary.replacePass(with:) -&gt; Bool (iOS 6+) succeeds only if that pass already exists.

- **Bedeutung fürs Design:** Use UUIDv4 serials per converted card. To let users edit a card, re-issue it with the same serial (replace). Never reuse a serial for a different card. Update rules: https://developer.apple.com/documentation/walletpasses/adding-a-web-service-to-update-passes
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/building-a-pass>

### F12 · Konfidenz: hoch

Colors (backgroundColor, foregroundColor, labelColor, footerBackgroundColor) are CSS-style RGB triples such as 'rgb(23, 187, 82)'. Apple's Pass Builder will also decode '#RRGGBB'/'#RGB', but it always writes 'rgb(r,g,b)'. If a background image is provided, backgroundColor is ignored.

- **Bedeutung fürs Design:** Always emit rgb(); do not rely on hex. Derive colors from the scanned card image (dominant color plus a contrast check) on the server or in the app. Hex decoding: https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassPackage/Pass/PassColor.swift
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### F13 · Konfidenz: hoch

Barcodes: use 'barcodes' (an array, iOS 9+; the first format the device can display wins). The single 'barcode' dictionary is deprecated, and the deprecated form only allowed QR/PDF417/Aztec. Each entry has format (required), message (required), messageEncoding (required) and altText (optional; not shown on watchOS). Allowed format values: PKBarcodeFormatQR, PKBarcodeFormatPDF417, PKBarcodeFormatAztec, PKBarcodeFormatCode128 (iOS 9+), plus PKBarcodeFormatCode39, PKBarcodeFormatCodabar, PKBarcodeFormatEAN13 and PKBarcodeFormatI2of5, which are new in iOS 27.

- **Bedeutung fürs Design:** The scanner's symbology must map to these 8 values. Symbologies outside the list (EAN-8, UPC-A/E, DataMatrix, Code93, GS1 DataBar) have no native format. Fall back to QR/Code128 only where the acceptance point can read it, or show the number as text.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary>

### F14 · Konfidenz: hoch

The four iOS 27 barcode formats do not render on iOS 26 and earlier. A pass that contains only a new format shows NO barcode on those devices. Apple recommends listing barcodes in priority order with a widely supported fallback such as QR, and, where fallbacks are impossible, showing the credential ID prominently in a headerField or primaryField for manual entry.

- **Bedeutung fürs Design:** For EAN-13 loyalty cards (common in DE retail), emit barcodes=[EAN13, fallback] and always put the number in altText and in a header or primary field. Whether a Code128 or QR fallback is accepted at the till is retailer-specific.
- **Quelle:** <https://developer.apple.com/videos/play/wwdc2026/209/>

### F15 · Konfidenz: mittel

watchOS does not support PKBarcodeFormatCode128. If Code128 is in the barcodes array, an alternative entry is used; if Code128 is the only barcode, none is displayed on Apple Watch. Apple's 2026 Pass Builder protobuf still carries the comment 'PKBarcodeFormatCode128 isn't supported for watchOS'.

- **Bedeutung fürs Design:** Add a QR or other fallback after Code128 if Watch display matters, but only when the acceptance point can scan that format. Watch support for the four iOS 27 formats is undocumented. Also stated in https://github.com/apple/pass-builder/blob/main/Protobufs/PassBarcode.proto
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### F16 · Konfidenz: niedrig

messageEncoding is an IANA charset name used to turn the 'message' string into the bytes that are rendered. Apple's example and recommendation is 'iso-8859-1', because scanners typically use Latin-1/Windows-1252 and support Unicode poorly. The archived guide says PassKit supports all encodings NSString supports. Apple does not document a way to carry arbitrary binary bytes. Mapping each byte to the Latin-1 code point U+0000–U+00FF (JSON \u00XX escapes) should round-trip under iso-8859-1 in theory, but this is my inference and untested.

- **Bedeutung fürs Design:** Text payloads are safe. Binary payloads (e.g. UIC 918.3 / DB / ÖBB Aztec rail tickets, which are zlib-compressed binary) need an on-device proof that the rendered barcode is byte-identical before this is promised as a feature.
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### F17 · Konfidenz: hoch

Raw barcode bytes on iOS: VNBarcodeObservation.payloadData: Data? (iOS 17.0+) and the Swift Vision BarcodeObservation.payloadData (iOS 18.0+) return the raw payload, unlike payloadStringValue.

- **Bedeutung fürs Design:** The app should capture payloadData plus the symbology and send both to the backend, so the server can choose the encoding and detect binary payloads instead of trusting a lossy string.
- **Quelle:** <https://developer.apple.com/documentation/vision/vnbarcodeobservation/payloaddata>

### F18 · Konfidenz: hoch

Dates: every date (relevantDate, relevantDates entries, expirationDate, date field values, semantic dates) is a W3C/ISO 8601 timestamp with a full date, hours and minutes, optional seconds, and a time zone. Field values that are dates must include a time zone. Apple's Pass Builder parser accepts only 'Z' or '±HH:MM' as the zone designator, with optional fractional seconds.

- **Bedeutung fürs Design:** Python: tz-aware datetime.isoformat(timespec='minutes'), e.g. '2026-10-10T19:30+02:00'. Never emit naive datetimes. Note that Apple's own poster-generic example uses '-7:00', which is invalid; do not copy it. Parser: https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/Codable/PassDateTimeFormatter.swift
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/passfieldcontent>

### F19 · Konfidenz: hoch

relevantDate (a single date string) is deprecated: the Pass reference says 'This object is deprecated. Use relevantDates instead.' relevantDates (iOS 18+ / watchOS 11+) is an array of objects with either 'date', or 'startDate' plus 'endDate' (endDate is required when startDate is given).

- **Bedeutung fürs Design:** Emit relevantDates. If the minimum supported iOS is below 18, also emit relevantDate for older devices; that it is still honored there is an inference.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/relevantdates-data.dictionary>

### F20 · Konfidenz: hoch

locations: an array of at most 10 objects {latitude (required), longitude (required), altitude, relevantText}. beacons (iOS 7+): at most 10 distinct UUIDs, {proximityUUID (required), major, minor, relevantText}. maxDistance is in meters; the system uses the smaller of this value and its default. In the archived rules, coupons and store cards do not support a relevant date and must provide locations if they carry any relevance information.

- **Bedeutung fürs Design:** Optional 'show near store' feature: geocode up to 10 store locations per pass, chosen by the user; never exceed 10. Archived relevance rules by style: https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/showing-a-pass-on-the-lock-screen>

### F21 · Konfidenz: hoch

Other top-level keys. expirationDate: a date string; Wallet auto-hides expired passes. voided: bool, default false. sharingProhibited: bool, iOS 11+; it only removes the Share button and does not prevent other sharing. suppressStripShine: bool, default true. groupingIdentifier: only for boarding passes and event tickets. logoText: not used on poster event tickets. userInfo: any JSON, never displayed. appLaunchURL plus associatedStoreIdentifiers (array of numeric App Store IDs; adds an app link on the pass; not supported on watchOS).

- **Bedeutung fürs Design:** Set associatedStoreIdentifiers to QRCode2Wallet's App Store ID so every pass links back to the app. Put a deep link in appLaunchURL. Use expirationDate and voided for coupons and tickets.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### F22 · Konfidenz: hoch

webServiceURL plus authenticationToken make a pass updatable. Production requires HTTPS (HTTP is allowed only in testing). Update pushes are APNs notifications with an empty JSON payload, sent with the same Pass Type ID certificate and key, and they work only in the APNs production environment. The authenticationToken and serialNumber of a pass cannot be changed. An often-cited 'at least 16 characters' rule for authenticationToken does not appear in current docs.

- **Bedeutung fürs Design:** Optional v2 feature for edits made in the app to reach installed passes. FastAPI implements the 5 Wallet web-service endpoints. Use a random token of 32 or more characters per pass anyway.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/adding-a-web-service-to-update-passes>

### F23 · Konfidenz: hoch

nfc {message (required, at most 64 bytes, truncated beyond that), encryptionPublicKey (required; Base64 X.509 SubjectPublicKeyInfo, ECDH P-256), requiresAuthentication (bool, iOS 13.1+)} needs a special entitlement issued by Apple, i.e. an NFC-enabled Pass Type ID certificate.

- **Bedeutung fürs Design:** QRCode2Wallet cannot reproduce NFC/VAS loyalty or tickets of third-party merchants. Never emit the nfc key.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/nfc-data.dictionary>

### F24 · Konfidenz: hoch

semantics (SemanticTags, iOS 12+) can be placed at the root of pass.json or inside any field dictionary (header, primary, secondary, auxiliary, back); placement does not change behavior. Tag examples: eventName, venueName, venueLocation {latitude, longitude}, eventStartDate, eventEndDate, eventType (PKEventTypeGeneric|LivePerformance|Movie|Sports|Conference|Convention|Workshop|SocialGathering), seats[], balance and totalPrice (CurrencyAmount), passengerName, airlineCode, flightNumber, etc.

- **Bedeutung fürs Design:** Cheap to add: when OCR or AI extraction finds event name, venue or date, emit the matching semantic tags as well as visible fields. Full tag list: https://developer.apple.com/documentation/walletpasses/semantictags
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/supporting-semantic-tags-in-wallet-passes>

### F25 · Konfidenz: hoch

PassFields groups (each an array of field dictionaries): headerFields, primaryFields, secondaryFields, auxiliaryFields, backFields, additionalInfoFields (iOS 18+, poster event tickets only), and footerFields (posterGeneric, iOS 27). footerFields is shown in the WWDC26 sample and in Apple's Pass Builder model, but is missing from the PassFields reference page.

- **Bedeutung fürs Design:** The model needs footerFields even though the reference does not list it yet. backFields is the place for long text: terms, original card number, and the required issuer contact info. footerFields in source: https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassPackage/Fields/Pass+Fields.swift
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/passfields>

### F26 · Konfidenz: hoch

Field dictionary keys: key (required, unique); value (required; string, number or ISO 8601 date with time zone); label; attributedValue (overrides value; only the &lt;a href&gt; tag is supported; not used on watchOS); changeMessage (format string containing %@; needed for update notifications); currencyCode (ISO 4217); dataDetectorTypes (array of PKDataDetectorTypePhoneNumber | PKDataDetectorTypeLink | PKDataDetectorTypeAddress | PKDataDetectorTypeCalendarEvent; back fields only; [] disables); dateStyle and timeStyle (PKDateStyleNone | Short | Medium | Long | Full); ignoresTimeZone (default false = device zone); isRelative (default false); numberStyle (PKNumberStyleDecimal | Percent | Scientific | SpellOut); textAlignment (PKTextAlignmentLeft | Center | Right | Natural; invalid for primary and back fields); row (auxiliaryFields on event tickets only, 0 or 1); semantics.

- **Bedeutung fürs Design:** Model these as enums in pydantic. Apple's validator warns when currencyCode and numberStyle are set together. Validator rule: https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/Validation/Validators/FieldFormattingValidator.swift
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/passfieldcontent>

### F27 · Konfidenz: mittel

Front-of-pass field limits. General: up to 3 header, 1 primary, 4 secondary and 4 auxiliary fields. Boarding pass: up to 2 primary and up to 5 auxiliary, with auxiliary shown above secondary. Coupons, store cards and generic passes with a square barcode (QR/Aztec): at most 4 secondary plus auxiliary combined; a store card shows them all on one row. Generic with a rectangular barcode keeps 4 secondary and 4 auxiliary separate. Event ticket: an extra auxiliary row of up to 4 fields via row:1. posterGeneric (iOS 27): one header field, up to 4 primary fields, a footer, back fields and additionalInfo fields. Long text can hide fields, and Apple advises against including more fields than are displayed.

- **Bedeutung fürs Design:** Layout templates per style must enforce these counts server-side and truncate or move overflow to backFields. Current-doc sources: https://developer.apple.com/documentation/walletpasses/defining-the-metadata-of-your-wallet-pass and https://developer.apple.com/documentation/walletpasses/creating-a-poster-generic-pass
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### F28 · Konfidenz: mittel

The posterGeneric footer limit is inconsistent. The poster-generic article says 'two footer fields', but WWDC26 says 'the pass face supports a single footer field… only the first will be displayed'.

- **Bedeutung fürs Design:** Emit at most 1 footer field.
- **Quelle:** <https://developer.apple.com/videos/play/wwdc2026/209/>

### F29 · Konfidenz: hoch

boardingPass requires transitType: PKTransitTypeAir | PKTransitTypeBoat | PKTransitTypeBus | PKTransitTypeGeneric | PKTransitTypeTrain. The key is invalid on other styles. watchOS may show a transit icon.

- **Bedeutung fürs Design:** Train, bus and ferry tickets (DB, FlixBus) map to boardingPass with the matching transitType, using non-semantic fields.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/boardingpass-data.dictionary>

### F30 · Konfidenz: hoch

Image files (HIG, June 2026), sizes in points, delivered as PNG @2x and @3x. icon.png: 38x38, all styles, REQUIRED. logo.png: height 50, width 50–160; non-semantic boarding passes, coupons, non-poster event tickets, generic, store cards. primaryLogo.png: height 30, width 30–126; semantic airline boarding passes, poster event tickets, posterGeneric. secondaryLogo.png: height 12, width 12–135; poster event tickets only. strip.png: 375x144; coupon and store card only. thumbnail.png: height 90, width 60–90; event ticket and generic. background.png: 343x503; non-poster event tickets (blurred). artwork.png: 358x448; poster event tickets and posterGeneric (shown unblurred, with a material strip over the bottom). footer.png: 268x15; airline boarding passes.

- **Bedeutung fürs Design:** Pixels = points x scale. icon 76x76 / 114x114. logo up to 320x100 / 480x150. primaryLogo up to 252x60 / 378x90. strip 750x288 / 1125x432. thumbnail up to 180x180 / 270x270. background 686x1006 / 1029x1509. artwork 716x896 / 1074x1344. footer 536x30 / 804x45. secondaryLogo up to 270x24 / 405x36.
- **Quelle:** <https://developer.apple.com/design/human-interface-guidelines/wallet>

### F31 · Konfidenz: hoch

Icon requirement in Apple's validator: a missing icon is an ERROR; a missing icon@2x.png or icon@3x.png is a warning. The archived guide recommends original (@1x), @2x and @3x for all art. Apple's manifest example ships icon.png, icon@2x.png and icon@3x.png. The archived (pre-2025) sizes differ from the current HIG: icon 29pt, background 180x220, footer 286x15, strip 375x98 for event tickets / 375x123 elsewhere. The Pass Designer article calls the current HIG sizes 'pixels', which is inconsistent.

- **Bedeutung fürs Design:** Always ship icon.png, icon@2x.png and icon@3x.png (cheap, maximally compatible), plus @2x/@3x for other images. Use the HIG point sizes. Archived sizes: https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html
- **Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/Validation/Validators/RequiredImagesValidator.swift>

### F32 · Konfidenz: hoch

Archived rule: an event ticket with strip.png must not also have background.png or thumbnail.png. Apple Watch shows no strip image, no thumbnail and no back of the pass; watchOS crops strip images and white space. backFields display on watchOS 7+.

- **Bedeutung fürs Design:** Never put essential data such as the card number only in an image. Image and field combinations per style are validated server-side. Current-doc watchOS note: https://developer.apple.com/documentation/walletpasses/creating-a-store-card-pass
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### F33 · Konfidenz: hoch

Localization: localizable strings in pass.json are keys looked up in '&lt;lang&gt;.lproj/pass.strings' ("key" = "value"; lines). Apple says to save files with non-ASCII characters as UTF-16. Dates, times and currencies in standard formats are localized automatically, even without .lproj folders. A same-named image at the top level overrides localized copies. Each .lproj needs the same set of image resolutions and the same string keys. Localized images may not update after the pass has been added.

- **Bedeutung fürs Design:** For a user-generated pass, localization folders are mostly unnecessary: render labels server-side in the user's language. If pass.strings is used (e.g. de + en), write it as UTF-16 (Python: text.encode('utf-16'), which includes a BOM).
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/creating-the-source-for-a-pass>

### F34 · Konfidenz: hoch

Poster event tickets were introduced in iOS 18 (WWDC24); the current article says 'iOS 26 and later', which conflicts. They require preferredStyleSchemes ['posterEventTicket','eventTicket'], an eventTicket dictionary, artwork.png or background.png, and the required semantics: eventName, venueName, venueRegionName, venueRoom; for sports also awayTeamAbbreviation and homeTeamAbbreviation; for live performances performerNames. If any are missing, the pass falls back to the legacy event ticket. The article states: 'Poster event tickets aren't compatible with tickets that require a QR code or barcode for entry'. Apple's Pass Builder validator raises an ERROR when nfc is missing on a posterEventTicket. NFC requires an Apple entitlement.

- **Bedeutung fürs Design:** QRCode2Wallet (barcode-based, no NFC entitlement) cannot produce poster event tickets. Use the classic eventTicket for concerts and other events, or optionally posterGeneric on iOS 27 with a generic/eventTicket fallback. Validator: https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/Validation/Validators/EventTicketValidator.swift. WWDC24 (iOS 18): https://developer.apple.com/videos/play/wwdc2024/10108/
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/creating-an-event-pass-using-semantic-tags>

### F35 · Konfidenz: mittel

Poster-event-only top-level keys (all optional): eventLogoText, footerBackgroundColor, suppressHeaderDarkening, useAutomaticColors, accessibilityURL, addOnURL, bagPolicyURL, contactVenueEmail, contactVenuePhoneNumber, contactVenueWebsite, directionsInformationURL, merchandiseURL, orderFoodURL, parkingInformationURL, purchaseParkingURL, sellURL, transferURL, transitInformationURL, auxiliaryStoreIdentifiers. The DocC JSON reports 'introduced 6.0.0' for many of these keys, which is clearly a placeholder.

- **Bedeutung fürs Design:** Do not trust per-key 'introduced' versions on the Pass page. Gate features by the style, WWDC session and article instead.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### F36 · Konfidenz: hoch

iOS 26 additions. (a) upcomingPassInformation: an array of UpcomingPassInformationEntry {type:'event' (required), identifier (required, unique), name (required), dateInformation, semantics, additionalInfoFields, backFields, URLs, images, isActive (default false), auxiliaryStoreIdentifiers}, for multi-event poster tickets. (b) Semantic ('upgraded') airline boarding passes: preferredStyleSchemes ['semanticBoardingPass','boardingPass'], transitType PKTransitTypeAir, and required semantics airlineCode, flightNumber, departureAirportCode, departureCityName, departureLocationTimeZone, destinationAirportCode, destinationCityName, destinationLocationTimeZone, originalArrivalDate, originalBoardingDate, originalDepartureDate, passengerName. Wallet tracks the flight via Apple's flight service and starts a Live Activity; listing your App Store ID in associatedStoreIdentifiers suppresses the Wallet Live Activity. (c) New boarding-pass URL keys: changeSeatURL, entertainmentURL, purchaseAdditionalBaggageURL, purchaseLoungeAccessURL, purchaseWifiURL, upgradeURL, managementURL, registerServiceAnimalURL, reportLostBagURL, requestWheelchairURL, transitProviderEmail, transitProviderPhoneNumber, transitProviderWebsiteURL; trackBagsURL in 26.1. No entitlement or approval is documented for semantic boarding passes.

- **Bedeutung fürs Design:** Semantic boarding passes need times and time zones that a screenshot or IATA BCBP barcode alone does not contain; v1 should emit legacy boardingPass. The semantic upgrade (BCBP parsing plus a flight-data API) belongs on a later roadmap. Session: https://developer.apple.com/videos/play/wwdc2025/202/
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/creating-an-airline-boarding-pass-using-semantic-tags>

### F37 · Konfidenz: hoch

iOS 27 posterGeneric style: a top-level key 'posterGeneric' (field dictionary with headerFields, primaryFields, footerFields, backFields, additionalInfoFields). The face shows artwork.png, primaryLogo.png, header, primary, footer and an optional barcode. It requires iOS 27+, and Apple recommends adding a 'generic' (or storeCard/coupon/eventTicket) dictionary in the same pass.json as a fallback. Wallet prefers posterGeneric when it is present and older OS versions use the legacy style. It is aimed at membership, loyalty, store, coupon, rewards and gift cards. Generic passes do not auto-expire, so use expirationDate.

- **Bedeutung fürs Design:** Strong fit for loyalty, gym and membership cards: the user's own photo or brand art can be the artwork. Always emit posterGeneric plus generic together. posterGeneric is not yet a property on the Pass reference page; the authoritative shape is WWDC26 plus Pass Builder: https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassPackage/Pass/PassStyle.swift
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/creating-a-poster-generic-pass>

### F38 · Konfidenz: mittel

iOS 27 featuredActions: a top-level array of at most 2 actions, in priority order, for all pass styles. Each action is {"identifier": unique string, "type": action type, "url": string}. Types: viewSchedule, watchTrailer, listenToMusic, call, place, addToBalance, order, shop, membershipBenefits, bookAppointment, bookCar, bookFlight, bookStay, viewOffersRewards. The per-type value semantics (e.g. what 'call' or 'place' expect in url) are not specified.

- **Bedeutung fürs Design:** Optional: let users attach a 'shop' or 'membershipBenefits' link for a card. Key shape is confirmed by the WWDC26 sample and https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassPackage/Pass/Pass+Action.swift; it is not yet in the Pass reference.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/defining-the-metadata-of-your-wallet-pass>

### F39 · Konfidenz: hoch

iOS 27 tooling. Pass Designer is a Mac app (macOS 27) that saves .pkpasstemplate bundles. Pass Builder is apple/pass-builder: Apache-2.0, Swift 6.3+, macOS 14+ or Linux, early preview (0.1.0). Its CLI is 'buildpass personalize &lt;template&gt; --protobuf &lt;pb&gt; --output &lt;dir&gt;', 'buildpass sign &lt;dir&gt; --pass-certificate cert.p12 --wwdr-certificate wwdr.cer' (password from the BUILDPASS_PASS_CERTIFICATE_PASSWORD env var), and 'buildpass validate &lt;dir&gt;'. The repo includes Protobuf definitions of the pass package.

- **Bedeutung fürs Design:** Use 'buildpass validate' in Linux CI as a conformance oracle against packages generated by the Python backend. Signing can stay in Python. Note that proto field names (e.g. PassAction.action_type) do NOT map 1:1 to pass.json keys ('type').
- **Quelle:** <https://github.com/apple/pass-builder>

### F40 · Konfidenz: niedrig

Pass Builder's Pass model also contains top-level keys that are absent from Apple's Pass reference: stripColor and logoSymbolName (described as 'An SF Symbol to display as a logo image'). Conversely, it lacks userInfo, suppressStripShine and trackBagsURL.

- **Bedeutung fürs Design:** Do not emit undocumented keys such as logoSymbolName or stripColor until they appear in the Wallet Passes reference.
- **Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassPackage/Pass/Pass.swift>

### F41 · Konfidenz: hoch

Apple's documentation samples contain invalid JSON: 'barcodes' written as an object instead of an array, missing commas, a malformed time zone ('-7:00'), and a semantics key written as 'semantictags' in the prose.

- **Bedeutung fürs Design:** Do not copy samples verbatim. Generate pass.json from a typed model and validate it.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/creating-a-store-card-pass>

### F42 · Konfidenz: hoch

App Store Review Guideline 1.5: 'ensure that Wallet passes include valid contact information from the issuer and are signed with a dedicated certificate assigned to the brand or trademark owner of the pass.' Guideline 3.2.1(iv): passes may be used to make or receive payments, transmit offers, or offer identification (such as movie tickets, coupons and VIP credentials); other uses may lead to rejection and revocation of Wallet credentials. Separately, style docs require contact info for the signing organization on the back of every pass.

- **Bedeutung fürs Design:** This is the largest product risk. A converter app signs third-party-branded cards with its own certificate. Mitigation: organizationName and back-field contact info identify QRCode2Wallet as issuer, no third-party logos or trademarks by default, and a clear 'user-created copy' disclaimer. Prepare a review note.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F43 · Konfidenz: hoch

Certificate lifecycle: if the Pass Type ID certificate expires, installed passes keep working, but new passes cannot be signed and existing ones cannot be updated. If it is revoked, the passes no longer work properly.

- **Bedeutung fürs Design:** Monitor certificate expiry, keep the key server-side only, and plan rotation. Revocation (e.g. after an App Review dispute) would break all users' passes.
- **Quelle:** <https://developer.apple.com/wallet/get-started/>

### F44 · Konfidenz: hoch

App-side PassKit APIs: PKPass(data: Data) throws, with PKPassKitError.Code values invalidDataError, invalidSignature, unsupportedVersionError, notEntitledError, unknownError. PKAddPassesViewController.canAddPasses() (iOS 8+). PKPassLibrary.containsPass(_:) -&gt; Bool (works without entitlements). PKPassLibrary.replacePass(with:) -&gt; Bool (iOS 6+). PKPassLibrary.Capability.backgroundAddPasses with requestAuthorization(for:completion:) and authorizationStatus(for:) (iOS 26.0+) adds passes without a per-pass confirmation prompt after a one-time permission; the app must be running.

- **Bedeutung fürs Design:** Flow: backend returns .pkpass bytes, the app calls PKPass(data:), then presents PKAddPassesViewController or uses addPasses with background authorization on iOS 26+. Map invalidSignature to a backend alert. PKPass(data:) reference: https://developer.apple.com/documentation/passkit/pkpass/init(data:)
- **Quelle:** <https://developer.apple.com/documentation/passkit/pkpasslibrary/capability/backgroundaddpasses>

## Empfehlungen

### E1

**Empfehlung:** Build the .pkpass server-side in Python. The pipeline: pydantic model to pass.json bytes, image renditions, manifest.json (SHA-1 hex), then signature (pyca/cryptography PKCS7SignatureBuilder with DetachedSignature + Binary, DER, SHA-256, plus the WWDR G4 cert), then a root-level ZIP served as application/vnd.apple.pkpass.

**Begründung:** Every step is verified against Apple's reference implementation (Pass Builder) and was tested locally. Python pkpass libraries on PyPI are mostly stale (wallet-py3k 2018, passbook 2016, applepassgenerator 2023), and the signer is about 40 lines.

### E2

**Empfehlung:** Use one Pass Type ID, e.g. pass.&lt;company&gt;.qrcode2wallet, for all passes, with a UUIDv4 serialNumber per converted card. Re-issue with the same serial to edit or replace a card.

**Begründung:** The pair (passTypeIdentifier, serialNumber) defines identity and replace behavior. Each extra Pass Type ID would need its own certificate and key.

### E3

**Empfehlung:** Map input to styles: loyalty, customer and gym cards to storeCard or generic; on iOS 27 additionally emit posterGeneric in the same pass.json, with generic as fallback. Coupons go to coupon; event tickets to classic eventTicket (no preferredStyleSchemes); train, bus, ferry and flight tickets to boardingPass with the right transitType (legacy, non-semantic).

**Begründung:** Poster event tickets require NFC (an Apple entitlement) and exclude barcode entry. Semantic boarding passes need flight times and time zones that a screenshot does not contain. posterGeneric supports barcodes and works for any card type.

### E4

**Empfehlung:** Barcode strategy: keep the original symbology. Emit barcodes[] in priority order (the original format first, then a scanner-compatible fallback), always set altText to the human-readable number, and repeat the ID in a header or primary field. Use messageEncoding 'iso-8859-1' for text payloads.

**Begründung:** The iOS 27 formats (EAN-13, Code39, Codabar, ITF) render nothing on iOS 26 and earlier, and Code128 renders nothing on Apple Watch. Showing the number allows manual entry at the till.

### E5

**Empfehlung:** In the app, capture raw bytes with VNBarcodeObservation.payloadData (iOS 17+) or BarcodeObservation.payloadData (iOS 18+) plus the symbology, and send both to the backend. Treat binary payloads (e.g. UIC 918.3 Aztec rail tickets) as 'experimental' until device tests show the rendered code is byte-identical.

**Begründung:** Apple documents no binary support for message, and payloadStringValue loses data.

### E6

**Empfehlung:** Images: icon.png, icon@2x.png and icon@3x.png are always required (the backend can derive them from the app icon). Generate the other images at @2x and @3x using the HIG point sizes, compressed (Pillow optimize), with an internal budget of about 1 MB per pass. Never put barcodes or critical text inside images.

**Begründung:** Apple's validator errors without an icon. The HIG (June 2026) prescribes @2x/@3x and small files. watchOS drops strip and thumbnail images.

### E7

**Empfehlung:** Generate dates as tz-aware ISO 8601 strings with minutes and a '±HH:MM' or 'Z' offset (datetime.isoformat(timespec='minutes')). Use relevantDates (iOS 18+), and also relevantDate if the deployment target is below iOS 18.

**Begründung:** Apple's parser rejects anything else, and date field values must include a time zone. relevantDate is deprecated.

### E8

**Empfehlung:** Put QRCode2Wallet's support contact and a 'user-created copy' note in backFields. Set organizationName to the issuer (QRCode2Wallet, optionally with the user's label in logoText). Do not reproduce third-party logos or trademarks by default. Prepare an App Review note on guideline 1.5.

**Begründung:** Guideline 1.5 requires issuer contact info and signing by the brand or trademark owner's dedicated certificate, which is a structural tension for a converter app.

### E9

**Empfehlung:** Add CI conformance checks: run Apple's 'buildpass validate' (Linux, Swift 6.3) on unzipped generated packages, run 'openssl smime -verify -binary -inform DER -in signature -content manifest.json -noverify', and do a Simulator drag-and-drop smoke test.

**Begründung:** These catch manifest, signature, field and image errors before users see the 'cannot add pass' message. Apple's own samples contain JSON errors.

### E10

**Empfehlung:** Set associatedStoreIdentifiers to the app's App Store ID and appLaunchURL to a deep link (e.g. qrcode2wallet://card/&lt;serial&gt;). Keep userInfo free of personal data.

**Begründung:** This gives a free link back from Wallet to the app (not on watchOS). Passes sync via iCloud and can be shared, so userInfo travels with the pass.

### E11

**Empfehlung:** Defer the webServiceURL update service (5 REST endpoints plus APNs with the Pass Type ID cert) to v2. In v1, replace passes by re-adding them with the same serial.

**Begründung:** Updates need HTTPS, an APNs production push and device registration storage. Re-adding with the same serial already overwrites the pass.

### E12

**Empfehlung:** Never emit nfc, personalization or undocumented keys (logoSymbolName, stripColor). Treat featuredActions (max 2) and posterGeneric/footerFields as iOS 27 extras, based on WWDC26 and Pass Builder rather than the Pass reference page.

**Begründung:** NFC needs an Apple entitlement. Undocumented keys may change, and the reference pages lag behind the iOS 27 features.

## Fallstricke

1. Forgetting PKPassOptions/PKCS7Options.Binary in pyca/cryptography: the LF to CRLF conversion invalidates the signature (verified empirically).
2. Including the wrong WWDR intermediate (G3 instead of G4), or none: Pass Type ID certificates chain to WWDR G4.
3. Zipping the folder instead of its contents (entries prefixed with 'X.pass/'), or including .DS_Store/__MACOSX files that are not in the manifest.
4. Re-serializing pass.json after hashing it (whitespace or key-order changes), which makes the manifest SHA-1 mismatch.
5. passTypeIdentifier or teamIdentifier not matching the signing certificate: Wallet silently refuses the pass and the error appears only in the device console.
6. 'barcodes' given as an object (as in Apple's own samples) instead of an array. Using the deprecated 'barcode' key alone.
7. Offering only an iOS 27 barcode format (EAN13/Code39/Codabar/I2of5), so no barcode renders on iOS 26 and earlier. Offering only Code128, so no barcode on Apple Watch.
8. Naive or malformed datetimes (no offset, or '-7:00' instead of '-07:00'), causing date field rendering or ingestion failures.
9. Using textAlignment on primaryFields or backFields (invalid). dataDetectorTypes on front fields (ignored). attributedValue with tags other than &lt;a href&gt;.
10. Exceeding field limits or putting long text on the front: fields silently disappear. Apple warns that hidden fields may become visible in future layouts.
11. Exceeding 10 locations or 10 beacon UUIDs. Coupons and store cards do not support relevant dates.
12. Setting preferredStyleSchemes 'posterEventTicket' on a barcode ticket: it requires NFC and the required semantics, otherwise it falls back. The legacy fields must still be valid, or ingestion fails on all devices.
13. Emitting posterGeneric without a fallback generic/storeCard dictionary, so the pass breaks on iOS 26 and earlier.
14. Writing pass.strings as UTF-8 with non-ASCII text, where Apple says to use UTF-16. Putting a same-named image both at the top level and in .lproj (the top level wins).
15. Trusting DocC 'introduced 6.0.0' metadata for newer keys, or copying Apple sample JSON verbatim (it contains syntax errors).
16. Assuming certificate expiry kills passes (it does not, though updates stop) and ignoring revocation risk (it breaks all passes). App Review guideline 1.5 is a real rejection or revocation vector for converter apps.
17. Treating barcode payloads as strings on the scanning side (payloadStringValue) and losing binary data. Use payloadData.
18. Including the nfc key without the NFC entitlement, which yields an invalid pass.

## Offene Fragen

1. Can arbitrary binary barcode payloads (UIC 918.3 / DB / ÖBB / SBB Aztec, zlib-compressed) be reproduced byte-exactly via messageEncoding 'iso-8859-1' with \u00XX-mapped characters, including 0x00? This needs on-device testing on iOS 26 and 27 and comparison with a reference decoder.
2. Will App Review accept a converter app that signs passes for third-party brands under its own Pass Type ID, given guideline 1.5 ('signed with a dedicated certificate assigned to the brand or trademark owner')? Which presentation (organizationName, logos) minimizes risk?
3. posterGeneric footer field count: the article says 2, WWDC26 says only the first footer is displayed. Which is correct on iOS 27.x?
4. Exact value semantics per featuredActions type (e.g. does 'call' take a tel: URL, does 'place' take a Maps URL or a Place ID?). The docs list only type names.
5. Are the iOS 27 barcode formats (EAN13, Code39, Codabar, I2of5) rendered on watchOS 27, and is Code128 still unsupported on watchOS 26/27? The 2026 proto comment says Code128 is unsupported.
6. Does a Code128 or QR fallback carrying the same digits work at typical German POS scanners for EAN-13 loyalty cards on iOS 26 and earlier devices?
7. Is there any official per-pass size limit? Only the bundle limit (10 passes / 150 MB) is documented.
8. Are @1x images still used anywhere (e.g. Mail on macOS or other surfaces), or are @2x/@3x sufficient? The HIG and Pass Designer say @2x/@3x; the archived guide says @1x/@2x/@3x.
9. Is the 'authenticationToken must be at least 16 characters' rule still enforced? It is absent from current docs.
10. Do semantic (upgraded) boarding passes or the Apple flight-service tracking require any airline-side approval or entitlement? The docs are silent.
11. What minimum iOS deployment target should the app use (e.g. iOS 18 for relevantDates and Vision BarcodeObservation, or iOS 26 for backgroundAddPasses)? This determines whether legacy keys (relevantDate) must be emitted.
12. Should the Pass Builder Protobuf definitions be used to generate Python models? Proto field names (e.g. action_type) differ from pass.json keys (type), so a mapping layer would be required.

## Faktencheck: alle geprüften Aussagen

### P1 · BESTÄTIGT

**Geprüfte Aussage:** iOS 27 is the current OS generation, not iOS 26. WWDC26 session 209 covers iOS 27 Wallet features, the HIG Wallet change log has the entry 'June 8, 2026 – Updated to reflect guidance for iOS 27 and the Pass Designer app', Pass Designer requires macOS 27, and watchOS 27 APIs show as non-beta. The public release of iOS 27 was inferred, not verified.

**Ergebnis:** Confirmed, and the inference is now backed by evidence. HIG change log entry verified word for word. WWDC26 session 209 'What's new in Wallet' says: 'In iOS 27, we're taking passes further than ever.' Pass Designer article: 'Make sure you have macOS 27.0 or later installed.' BarcodeObservation.payloadData lists watchOS 27.0 with beta:false. Evidence that iOS 27 shipped publicly: Apple's Xcode release-notes index lists 'Xcode 27 Release Notes' (final; 'SDKs for iOS 27 ... watchOS 27 ... macOS 27'), 'Xcode 27.1 RC' and 'Xcode 27.2 Beta 2'. Treat iOS 27 as current and iOS 26 as N-1.

**Quelle:** <https://developer.apple.com/documentation/xcode-release-notes>

### P2 · BESTÄTIGT

**Geprüfte Aussage:** Package layout: pass.json, PNG images (icon mandatory), optional '&lt;lang&gt;[-&lt;region&gt;].lproj/' folders holding pass.strings and/or localized images, manifest.json and signature, zipped and renamed to .pkpass. .DS_Store and similar files must not appear in the manifest or the archive.

**Ergebnis:** Confirmed. Building a Pass: 'Zip the resulting directory. Change the file extension ... from .zip to .pkpass' and 'Don't include metadata files ... such as the .DS_Store file in the manifest or distributable pass.' Creating the Source for a Pass: 'All passes require an icon' and lproj naming '[language identifier]-[region identifier].lproj'. Additions: (1) Apple's Pass Builder runs `zip -r -q <out> .` inside the pass directory, so files sit at the ZIP root with no wrapping folder. (2) 'Adding an image of the same name to the top-level folder of the pass overrides any localized versions.' (3) 'Each folder must contain the same number of resolutions for an image.'

**Quelle:** <https://developer.apple.com/documentation/walletpasses/building-a-pass>

### P3 · BESTÄTIGT

**Geprüfte Aussage:** manifest.json is a flat JSON object mapping '/'-separated relative paths to hex SHA-1 of the exact file bytes. It covers every file, subdirectories included, except manifest.json and signature. Apple's Pass Builder computes sha1Hash() per file.

**Ergebnis:** Confirmed. Building a Pass: 'a dictionary of the SHA1 hashes for each of the source files ... key is the pathname of the file relative to the top level of the pass'. Common Problems: 'manifest.json contains all the source files, including those in subdirectories'. Pass Builder InMemoryManifestGenerator walks subdirectories with prefix + "/" + filename and uses Insecure.SHA1 with lowercase hex. Apple's example writes 'en.lproj\/logo.png'; JSON treats that as identical to 'en.lproj/logo.png', so Python json.dumps output is fine.

**Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassSigning/Manifest/InMemoryManifestGenerator.swift>

### P4 · BESTÄTIGT

**Geprüfte Aussage:** signature is a PKCS#7/CMS detached signature over the manifest.json bytes, made with the Pass Type ID private key. It includes the WWDR intermediate and carries the S/MIME signing-time attribute. Pass Builder calls CMS.sign(..., additionalIntermediateCertificates:[wwdr], certificate:, privateKey:, signingTime: Date()) and writes the DER to 'signature'.

**Ergebnis:** Confirmed. Archived guide, verbatim: 'make a PKCS #7 detached signature of the manifest file, using the private key associated with your signing certificate. Include the WWDR intermediate certificate as part of the signature ... Include the date and time that the pass was signed using the S/MIME signing-time attribute.' The current 'Building a Pass' page names only 'PKCS #7 detached signature ... private key of the pass identifier signing certificate'; it states neither the WWDR nor the signing-time requirement. ManifestSignatureGenerator.swift (commit 8908b95, Aug 2026) matches the quoted CMS.sign call, with the comment 'detached: true is the default'.

**Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### P5 · BESTÄTIGT

**Geprüfte Aussage:** Pass Type ID certificates, including 'Pass Type ID with NFC', chain to WWDR G4. G3 is for software signing and is the wrong intermediate.

**Ergebnis:** Confirmed. G4 row: 'Features supported by Apple Push Notification service | Pass Type ID, Pass Type ID with NFC, Apple Push Notification service SSL, Order Type ID, Website Push ID, WatchKit Services, VoIP Services'. G3: 'Software signing and services'. Pass Builder's README only says 'WWDR intermediate certificate' from apple.com/certificateauthority and does not name G4.

**Quelle:** <https://developer.apple.com/help/account/certificates/wwdr-intermediate-certificates/>

### P6 · BESTÄTIGT

**Geprüfte Aussage:** pyca/cryptography signing: PKCS7SignatureBuilder().set_data(manifest).add_signer(cert, key, SHA256()).add_certificate(wwdr).sign(DER, [DetachedSignature, Binary]). Default signed attributes are contentType, signingTime, messageDigest and SMIMECapabilities. Without Binary, LF is converted to CRLF and openssl verification fails. PyPI latest is 50.0.2.

**Ergebnis:** Reproduced independently on cryptography 50.0.1 with OpenSSL 3.0.13 and a self-signed RSA cert. With [DetachedSignature, Binary], `openssl smime -verify -binary -inform DER -content manifest.json -noverify` prints 'Verification successful'. Without Binary it prints 'Verification failure ... digest failure'. asn1parse shows the signed attributes contentType, signingTime, messageDigest and 'S/MIME Capabilities'. Docs: 'Signature and envelope creation normally converts line endings (LF to CRLF). When passing this option, the data will not be converted.' PyPI JSON reports latest 50.0.2, uploaded 2026-09-30. Not verified here: acceptance on a real iPhone (no device available). The CMS structure matches what Pass Builder produces.

**Quelle:** <https://raw.githubusercontent.com/pyca/cryptography/main/docs/hazmat/primitives/asymmetric/serialization.rst>

### P7 · BESTÄTIGT

**Geprüfte Aussage:** Apple documents no maximum size for a single .pkpass; the only official limit is the .pkpasses bundle (10 passes / 150 MB). The HIG says 'Keep image file sizes small.' Third parties suggest under 5 MB per pass and about 100 KB per image.

**Ergebnis:** Confirmed for the Apple parts. Distributing and updating a pass: 'You can have up to 10 passes or 150 MB for a bundle of passes', MIME 'application/vnd.apple.pkpasses'. HIG: 'Keep image file sizes small. People can receive passes via email or a webpage...' I found no single-pass size limit in the current WalletPasses docs, the archived PassKit guide, or Pass Builder's validators (no size check). The third-party 5 MB / 100 KB figures were not verified and are not Apple guidance.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/distributing-and-updating-a-pass>

### P8 · BESTÄTIGT

**Geprüfte Aussage:** Required top-level keys: formatVersion=1, passTypeIdentifier (matches the cert, starts with 'pass.'), serialNumber, teamIdentifier, organizationName, description. Exactly one style key is required, plus optional posterGeneric on iOS 27.

**Ergebnis:** Confirmed. The Pass reference marks formatVersion, passTypeIdentifier, serialNumber, teamIdentifier, organizationName and description as required ('The value needs to be 1'). Poster-generic article: 'the string always begins with pass, and uses reverse DNS style'. Precision on the style key: the legacy key paired with posterGeneric may be any of 'storeCard, generic, eventTicket, or coupon', and 'Wallet's style resolution prioritizes posterGeneric when present'. It does not have to be generic. The reference calls serialNumber 'An alphanumeric serial number', but Apple explicitly allows 'an increasing integer or a UUID'.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### P9 · BESTÄTIGT

**Geprüfte Aussage:** passTypeIdentifier + serialNumber defines identity. Re-adding a pass overwrites it. authenticationToken and serialNumber cannot change. PKPassLibrary.replacePass(with:) -&gt; Bool (iOS 6+) succeeds only if the pass already exists.

**Ergebnis:** Confirmed. Building a Pass: 'Adding a pass with the same pass identifier and serial number as one that already exists on a users' device overwrites the old one.' Web-service article: 'You can update ... any information in the pass, except for the authentication token and the serial number.' replacePass(with:): iOS 6.0, 'func replacePass(with pass: PKPass) -&gt; Bool', 'If there isn't such a pass in the user's pass library, the replacement fails.' Missing caveat: the app can see or replace only passes whose type is in its com.apple.developer.pass-type-identifiers entitlement. passes() docs: 'Your app only has access to certain passes according to its entitlements.'

**Quelle:** <https://developer.apple.com/documentation/passkit/pkpasslibrary/replacepass(with:)>

### P10 · BESTÄTIGT

**Geprüfte Aussage:** barcodes (array, iOS 9+) replaces the deprecated 'barcode' dict, which allowed only QR/PDF417/Aztec. Each entry has format, message and messageEncoding (required) and altText (optional, not shown on watchOS). Values: QR, PDF417, Aztec, Code128 (iOS 9+), plus Code39, Codabar, EAN13 and I2of5, new in iOS 27.

**Ergebnis:** Confirmed. Pass.Barcodes allowed values: PKBarcodeFormatQR, PKBarcodeFormatPDF417, PKBarcodeFormatAztec, PKBarcodeFormatCode128, PKBarcodeFormatCode39, PKBarcodeFormatCodabar, PKBarcodeFormatEAN13, PKBarcodeFormatI2of5. Deprecated Pass.Barcode allows QR/PDF417/Aztec, deprecated at iOS 9. Pass reference: 'The system uses the first displayable barcode for the device.' Code128 on iOS 9 comes from the archived guide. Caveat: the current Pass.Barcodes Discussion says 'In iOS 27 and later, you can provide more than one barcode as a fallback'. That is misleading, because array fallback has worked since iOS 9 (archived: 'PassKit displays the first supported barcode in this array'). There are only four keys, so Apple offers no control over error-correction level, QR version or Aztec layers.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary>

### P11 · BESTÄTIGT

**Geprüfte Aussage:** The iOS 27 barcode formats do not render on iOS 26 and earlier. A pass with only a new format shows no barcode there. Apple recommends a priority-ordered array with a fallback, or else showing the ID in a primary or header field.

**Ergebnis:** Confirmed by the WWDC26 209 transcript: 'If you only provide one of the new barcode types and nothing else, the pass will not render a barcode on iOS 26 and earlier.' 'we strongly recommend providing an array of barcodes in priority order.' 'surface the credential ID in a pass field ... Consider using a primaryField, or headerField'. Apple also advises: 'make sure your front-line staff are trained for manual entry workflows.'

**Quelle:** <https://developer.apple.com/videos/play/wwdc2026/209/>

### P12 · BESTÄTIGT

**Geprüfte Aussage:** watchOS does not support PKBarcodeFormatCode128. If an alternative is present it is used; if Code128 is the only barcode, none is displayed. The 2026 Pass Builder proto still has this comment.

**Ergebnis:** Confirmed (medium). Archived guide, verbatim: 'watchOS does not support the PKBarcodeFormatCode128 format ... if a PKBarcodeFormatCode128 barcode is the only barcode you supply, no barcode is displayed.' The deprecated Pass.Barcode reference says 'PKBarcodeFormatCode128 isn't supported for watchOS'. Protobufs/PassBarcode.proto has the same comment. However, the current Pass.Barcodes (array) reference no longer states this caveat, so it may be stale for watchOS 26/27. Test on a current watch. Watch support for Code39, Codabar, EAN13 and I2of5 is undocumented.

**Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### P13 · BESTÄTIGT

**Geprüfte Aussage:** messageEncoding is an IANA charset name. Apple's example is iso-8859-1, and PassKit supports all NSString encodings. No binary mechanism is documented. Mapping bytes to U+0000–U+00FF under iso-8859-1 is an untested inference.

**Ergebnis:** The documented parts are confirmed. Pass.Barcodes: 'The IANA character set name of the text encoding to use to convert message from a string representation to a data representation ... such as "iso-8859-1"'. Archived: 'Barcode scanners and software typically use the ISO 8859-1 encoding ... Unicode is poorly supported by most systems. PassKit supports all encodings supported by the NSString class.' The Latin-1 byte-mapping round trip remains unverified; I found no Apple source for it. Extra risk: NUL (\u0000) inside an NSString message is a common truncation point, and Wallet regenerates the symbol, so original Aztec/QR parameters are not preserved.

**Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### P14 · BESTÄTIGT

**Geprüfte Aussage:** VNBarcodeObservation.payloadData: Data? (iOS 17.0+) and Vision BarcodeObservation.payloadData (iOS 18.0+) return raw payload bytes.

**Ergebnis:** Confirmed. VNBarcodeObservation.payloadData: 'var payloadData: Data? { get }', iOS 17.0 (macOS 14.0), 'The raw data representation of the barcode's payload.' BarcodeObservation.payloadData: 'let payloadData: Data?', iOS 18.0 and watchOS 27.0.

**Quelle:** <https://developer.apple.com/documentation/vision/vnbarcodeobservation/payloaddata>

### P15 · BESTÄTIGT

**Geprüfte Aussage:** All dates are W3C/ISO 8601 with date, hours, minutes, optional seconds and a time zone. Pass Builder accepts only 'Z' or '±HH:MM'. Apple's poster-generic sample uses an invalid '-7:00'.

**Ergebnis:** Confirmed. PassFieldContent.value: 'A date or time value needs to include a time zone.' expirationDate and relevantDate: 'complete date that includes hours and minutes, and may optionally include seconds'. PassDateTimeFormatter.hasWellFormedTimeZone requires exactly 'Z' or 6 characters '±HH:MM'. 'Creating a Poster Generic Pass' contains "value" : "2026-01-02T00:00-7:00". That sample also has other JSON errors: a missing comma, trailing commas, and 'barcodes' written as an object rather than an array. Nuance: the strict parser is Pass Builder's. iOS Wallet's own parser is undocumented, but the W3C datetime note mandates the same TZD form.

**Quelle:** <https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/Codable/PassDateTimeFormatter.swift>

### P16 · BESTÄTIGT

**Geprüfte Aussage:** relevantDate is deprecated in favor of relevantDates (iOS 18+ / watchOS 11+): objects with 'date', or 'startDate'+'endDate' (endDate required with startDate).

**Ergebnis:** Confirmed. Pass reference: 'This object is deprecated. Use relevantDates instead.' Pass.RelevantDates: iOS 18.0, watchOS 11.0. endDate: 'Required when providing startDate.' date: 'Wallet automatically calculates a relevancy interval from this date.' Note: 'Showing a Pass on the Lock Screen' still uses relevantDate in its text and example, so it is stale.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/relevantdates-data.dictionary>

### P17 · KORRIGIERT

**Geprüfte Aussage:** Up to 10 locations {latitude, longitude, altitude, relevantText} and up to 10 distinct beacon UUIDs. maxDistance in meters (the smaller of this value and the default applies). Archived rules: coupons and store cards do not support relevant date and must provide locations if they carry relevance info.

**Ergebnis:** Limits and keys confirmed. The relevance rule is incomplete: it applies to generic passes too. Current doc: 'Set a date by adding the relevantDate key to Pass for boarding passes, event tickets, and generic passes' and 'Coupons, store cards, and generic passes must provide locations if you added any other type of relevance information to the pass object.' Archived Table 4-2 also gives Generic: relevant date 'Optional', relevant locations 'Required if relevance information is provided'. The archived table interprets location radius as small (~100 m) for coupon, store card and generic, and large (~1000 m) for boarding pass and event ticket. Beacons: 'Add up to ten different UUIDs'. maxDistance: 'The system uses the smaller of this distance or the default distance.'

**Quelle:** <https://developer.apple.com/documentation/walletpasses/showing-a-pass-on-the-lock-screen>

### P18 · KORRIGIERT

**Geprüfte Aussage:** Other keys: expirationDate (Wallet auto-hides expired passes), voided (default false), sharingProhibited (iOS 11+, only removes the Share button), suppressStripShine (default true), groupingIdentifier (boarding passes and event tickets only), logoText (not on poster event tickets), userInfo, appLaunchURL + associatedStoreIdentifiers (not on watchOS).

**Ergebnis:** All quoted key semantics match the Pass reference, except 'Wallet auto-hides expired passes', which the Pass reference does not state. Apple Support (Remove passes from Apple Wallet) says limited or single-use passes such as boarding passes and event tickets are hidden after they expire, governed by the user setting 'Hide Expired Passes'. Hiding of store cards or generic passes is not documented. Developer reports on Apple's forum (thread 708761, iOS 15.6.1–17.6.1, FB9813388) say event tickets are hidden about 24 h after relevantDate even when expirationDate is in the future. expirationDate must include hours and minutes. Verbatim confirmations: sharingProhibited 'introduced in iOS 11 ... nor does it prevent sharing the pass in some other way'; suppressStripShine 'The default value is true'; associatedStoreIdentifiers '[number] ... A link to launch the app is on the back of the pass ... isn't supported for watchOS'.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### P19 · BESTÄTIGT

**Geprüfte Aussage:** webServiceURL + authenticationToken make a pass updatable. HTTPS is required in production. APNs push uses an empty JSON payload, the same Pass Type ID cert and key, and works in production only. Token and serial cannot change. The '16 characters' rule is not in current docs.

**Ergebnis:** Confirmed. 'Your web service must use an HTTPS connection for production, but you can use an HTTP connection during testing.' 'The notification uses the same certificate and private key that the creator of the pass used to sign the original, the push token registered by the device, and an empty JSON dictionary for the payload.' 'A push notification for a pass update works only in the production environment.' The current Pass reference gives authenticationToken no length rule.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/adding-a-web-service-to-update-passes>

### P20 · BESTÄTIGT

**Geprüfte Aussage:** nfc {message ≤64 bytes (truncated beyond), encryptionPublicKey (Base64 X.509 SPKI, ECDH P-256), requiresAuthentication (iOS 13.1+)} requires an Apple-issued entitlement (NFC-enabled Pass Type ID cert).

**Ergebnis:** Confirmed. 'The size needs to be no more than 64 bytes. The system truncates messages longer than 64 bytes.' 'Base64-encoded X.509 SubjectPublicKeyInfo structure that contains an ECDH public key for group P256.' requiresAuthentication 'valid in iOS 13.1 and later'. Note: 'Adding NFC to a Pass requires a special entitlement issued by Apple.' The WWDR page lists a 'Pass Type ID with NFC' certificate.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/nfc-data.dictionary>

### P21 · BESTÄTIGT

**Geprüfte Aussage:** semantics (iOS 12+) may sit at the root or in any header, primary, secondary, auxiliary or back field, and placement does not change behavior. Tags include eventType values, venueLocation, seats, balance/totalPrice and passengerName.

**Ergebnis:** Confirmed. 'Where you choose to add the semantic tags, whether to the top-level Pass dictionary or to a field dictionary, doesn't affect their functionality.' SemanticTags: iOS 12.0. eventType allowed values: PKEventTypeGeneric, LivePerformance, Movie, Sports, Conference, Convention, Workshop, SocialGathering. balance is 'only for a store card pass'. totalPrice is 'for any pass type'. passengerName is PersonNameComponents.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/supporting-semantic-tags-in-wallet-passes>

### P22 · BESTÄTIGT

**Geprüfte Aussage:** PassFields groups: header, primary, secondary, auxiliary, back, additionalInfoFields (iOS 18+, poster event tickets only) and footerFields (posterGeneric, iOS 27). footerFields is missing from the PassFields reference.

**Ergebnis:** Confirmed. The PassFields reference lists six groups and no footerFields. footerFields appears in the WWDC26 sample, in Pass+Fields.swift ('fields that display in the footer of a pass face'), and in the HIG ('Footer fields: Show supplemental information, such as pass category'). Nuance: the AdditionalInfoFields reference says 'Only poster event ticket passes support the Additional Info section', but 'Creating a Poster Generic Pass' says the posterGeneric layout has 'headerFields, primaryFields, footerFields, backFields, and additionalInfoFields'. The reference is stale on this.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/passfields>

### P23 · BESTÄTIGT

**Geprüfte Aussage:** Field keys: key, value, label, attributedValue (&lt;a href&gt; only, not on watchOS), changeMessage (%@), currencyCode, dataDetectorTypes (back only, [] disables), dateStyle/timeStyle, ignoresTimeZone, isRelative, numberStyle, textAlignment (invalid for primary and back), row (event-ticket auxiliary, 0/1), semantics. Validator warns on currencyCode + numberStyle.

**Ergebnis:** Confirmed word for word against PassFieldContent. 'row' is documented on PassFields.AuxiliaryFields ('Set the value to 1 to add an auxiliary row. Each row displays up to four fields.'), not on PassFieldContent. 'semantics' inside fields comes from the semantic-tags article. FieldFormattingValidator emits a warning, VALIDATION_ISSUE_CURRENCY_CODE_AND_NUMBER_FORMATTER, when both are set.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/passfieldcontent>

### P24 · BESTÄTIGT

**Geprüfte Aussage:** Front-field limits: general 3/1/4/4. Boarding pass 2 primary and 5 auxiliary, auxiliary above secondary. Square-barcode coupon, store card and generic: 4 secondary+auxiliary combined; store card on one row. Rectangular-barcode generic: 4+4 separate. Event ticket row:1 adds 4. posterGeneric: 1 header, 4 primary, footer, back, additionalInfo.

**Ergebnis:** Confirmed (medium). Archived, verbatim: 'up to three header fields, a single primary field, up to four secondary fields, and up to four auxiliary fields'; 'Boarding passes can have up to two primary fields and up to five auxiliary fields'; 'Coupons, store cards, and generic passes with a square barcode can have a total of up to four secondary and auxiliary fields, combined'. Current docs contradict each other on generic. 'Defining the metadata' says generic keeps 4+4 separate ('a total of eight displayed fields') without a barcode-shape condition, while 'Creating a Poster Generic Pass' says generic has 'up to four secondary and auxiliary fields combined'. Use the stricter combined-4 rule when a QR or Aztec barcode is present.

**Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html>

### P25 · BESTÄTIGT

**Geprüfte Aussage:** The posterGeneric footer limit is inconsistent: the article says two footer fields, WWDC26 says a single one.

**Ergebnis:** Confirmed. The article says 'A Poster Generic Pass can have a header field, up to four primary fields, two footer fields, back fields, and additional info field.' WWDC26 says 'the pass face supports a single footer field, so if you include more than one, only the first will be displayed.' Emitting one footer field is the safe choice.

**Quelle:** <https://developer.apple.com/documentation/walletpasses/creating-a-poster-generic-pass>

## Vom Faktenprüfer ergänzte wichtige Fakten

1. BIGGEST PRODUCT RISK: iOS 27 Wallet has a native 'Create a Pass' feature. Users can make passes from physical cards or barcodes/QR codes via camera, photo or screenshot (Siri Mode / Apple Intelligence; Apple Support lists iPhone 15 Pro or later), or manually from Standard, Membership and Event templates. Fields can be edited after adding, and passes can be pinned to the Apple Watch Smart Stack. This overlaps directly with QRCode2Wallet's core value. Differentiate on: PDF/multi-page input, iOS 26-and-earlier devices and non-Apple-Intelligence devices, multi-barcode fallbacks, batch import, richer layouts (posterGeneric, featuredActions). Medium confidence: apple.com and support.apple.com were seen only through search results and could not be fetched from this sandbox. Sources: https://www.apple.com/newsroom/2026/06/apple-unveils-innovative-features-and-intelligence-experiences-across-services/ , https://support.apple.com/guide/iphone/create-passes-el8l5r9jnhyv/ios , https://support.apple.com/en-us/127821
2. Apple Support warns that codes which rotate or expire (for example concert tickets) won't work when captured as a static photo. The same limit applies to any converter. The app should detect or warn on dynamic tickets (rotating-barcode tickets, time-based codes) rather than promise conversion. Source: https://support.apple.com/en-us/127821 (medium; via search)
3. iOS 26+ background add: PKPassLibrary.Capability.backgroundAddPasses with requestAuthorization(for:completion:) or the async requestAuthorization(for:) -&gt; PKPassLibrary.AuthorizationStatus, then addPasses(_:withCompletionHandler:). After a one-time permission this adds passes without a per-pass confirmation (the system sends a notification). It requires the app to be running. Otherwise addPasses prompts for each pass, or the app uses PKAddPassesViewController. This removes friction from the convert-and-add flow on iOS 26+. https://developer.apple.com/documentation/passkit/pkpasslibrary/capability/backgroundaddpasses and https://developer.apple.com/documentation/walletpasses/distributing-and-updating-a-pass
4. The app needs the Wallet capability, i.e. the com.apple.developer.pass-type-identifiers entitlement listing pass.&lt;company&gt;.qrcode2wallet, for PKPassLibrary.passes(), containsPass(_:), replacePass(with:) and removePass(_:) to see its own passes ('PassKit doesn't return passes that your app can't access'). Without it, the in-app 'edit/replace card' flow cannot detect installed passes. https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.pass-type-identifiers
5. App Review: besides 1.5 ('ensure that Wallet passes include valid contact information from the issuer and are signed with a dedicated certificate assigned to the brand or trademark owner of the pass'), guideline 3.2.1(iv) reads: 'Wallet passes can be used to make or receive payments, transmit offers, or offer identification (such as movie tickets, coupons, and VIP credentials). Other uses may result in the rejection of the app and the revocation of Wallet credentials.' Revocation would hit the single shared Pass Type ID used for all users' passes. Assess this before committing to one cert. Guidelines updated June 8, 2026. https://developer.apple.com/app-store/review/guidelines/
6. The posterGeneric fallback does not have to be 'generic'. Apple: 'include an additional style dictionary on the same pass, for example, storeCard, generic, eventTicket, or coupon. Wallet's style resolution prioritizes posterGeneric when present.' Loyalty and gym cards can therefore be posterGeneric + storeCard, and coupons posterGeneric + coupon. The researcher's 'generic as fallback' recommendation is narrower than necessary. https://developer.apple.com/documentation/walletpasses/creating-a-poster-generic-pass
7. posterGeneric uses different images: artwork.png (358×448 pt, unblurred; a material strip covers the bottom edge; leave a barcode safe area) and primaryLogo.png (height 30 pt, width 30–126 pt). It does not use logo/strip/thumbnail. Pass Builder declares artwork 358×448 as a required size and primaryLogo with a 126×30 maximum. The image pipeline must produce these at @2x/@3x when posterGeneric is emitted. https://developer.apple.com/design/human-interface-guidelines/wallet and https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassPackage/PassPackage.swift
8. Apple says to put contact info for the SIGNER on the back: 'On the back of the pass, include contact information for the organization that signed the pass. If users interact with a different organization to redeem the pass, you may choose to provide two sets of contact information.' QRCode2Wallet is the signer, so its contact info is mandatory in backFields and the original issuer's contact info is optional. https://developer.apple.com/documentation/walletpasses/creating-a-poster-generic-pass
9. featuredActions (iOS/watchOS 27+; top-level; at most 2; entries {identifier, type, url}) has documented type values: viewSchedule, watchTrailer, listenToMusic, call, place, addToBalance, order, shop, membershipBenefits, bookAppointment, bookCar, bookFlight, bookStay, viewOffersRewards. The links are universal links / web pages. The key is absent from the Pass reference; the list is in 'Defining the metadata of your Wallet Pass'. https://developer.apple.com/documentation/walletpasses/defining-the-metadata-of-your-wallet-pass and https://developer.apple.com/wallet/whats-new/
10. The researcher's CI rationale overstates 'buildpass validate'. PassValidator runs only 5 plugins (EventTicketValidator, SeatValidator, BoardingPassValidator, FieldFormattingValidator [currencyCode+numberStyle], RequiredImagesValidator [icon]). It works on an uncompressed .pass directory, so it checks no manifest, signature, field counts or barcode formats; JSON and date decoding errors surface only through PassPackage parsing. Missing icon@2x or icon@3x is only a WARNING ('RECOMMENDED_IMAGE_NOT_PROVIDED'). Only some icon is an error. So '@1x/@2x/@3x always required' is overstated. Pass Builder is an 'Early preview' with no API stability and shells out to the `zip` binary. Requirements: Swift 6.3+, macOS 14+ or Linux. https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/Validation/Validators/PassValidator.swift
11. Apple does not document the message rules for the iOS 27 symbologies: EAN-13 with 12 vs 13 digits and check-digit handling, ITF even digit count, Codabar start/stop characters, Code39 character set. Invalid messages may render nothing. Validate server-side and test every symbology on an iOS 27 device before launch. (Absence verified in https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary)
12. Apple Watch: the poster-generic article says 'A pass viewed on an Apple Watch doesn't show the strip image (banner image), thumbnail image, or the information on the back of the pass', while the BackFields reference says back fields display 'in watchOS 7 and later' and the HIG says watchOS 'crops the strip image'. The docs disagree, so never put the only copy of the card number or barcode fallback in strip, thumbnail or backFields. https://developer.apple.com/documentation/walletpasses/creating-a-poster-generic-pass
13. Poster event tickets (current article: iOS/watchOS 26+) need preferredStyleSchemes ['posterEventTicket'] plus the required semantic tags, and 'aren't compatible with tickets that require a QR code or barcode for entry'. This supports the researcher's choice of classic eventTicket for converted tickets. iOS 26 semantic boarding passes are air-only: 'Only the air travel boarding pass supports the new Semantic Pass designs available in iOS 26 and later.' https://developer.apple.com/documentation/walletpasses/creating-an-event-pass-using-semantic-tags
14. If pass.strings is used, for example for German labels: 'Use UTF-16 encoding for non-ASCII characters' (umlauts). Also, 'the localized image of a pass may not update after adding the pass to Wallet'. Simpler option: write German text directly into the UTF-8 pass.json and skip pass.strings. https://developer.apple.com/documentation/walletpasses/creating-the-source-for-a-pass
15. Relevance and auto-hide interplay: developers report that event tickets are hidden as expired about 24 h after relevantDate even when expirationDate is later. For multi-day or season tickets, test whether relevantDates startDate/endDate (iOS 18+) avoids this before emitting relevantDate. Low confidence: forum reports, no Apple answer. https://developer.apple.com/forums/thread/708761
16. The Pass reference (current) does not list posterGeneric, featuredActions or footerFields. Pass Builder's Pass model also contains the undocumented keys stripColor and logoSymbolName. This confirms the researcher's 'reference lags / do not emit undocumented keys' stance. Pass reference also adds many iOS 26 boarding-pass URL keys and upcomingPassInformation (iOS 26), which are irrelevant to a converter. https://github.com/apple/pass-builder/blob/main/Sources/PassBuilder/PassPackage/Pass/Pass.swift
