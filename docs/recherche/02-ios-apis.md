# 02 · iOS-Frameworks und APIs

> **Hinweis:** Vollständige Rohfassung der Recherche vom 10.10.2026: KI-Agenten-Recherche gegen Primärquellen, danach von einem unabhängigen Faktenprüfer adversarial gegengeprüft. Die Inhalte stehen in der Originalsprache Englisch. Die deutsche Zusammenfassung mit Bewertung steht in der [Übersicht](README.md). Rechtliche Aussagen sind **keine Rechtsberatung**.

**Recherchierter Umfang:** iOS frameworks and APIs for the QRCode2Wallet SwiftUI app (VisionKit, Vision, DataDetection, PhotosUI, PDFKit, Share Extension, PassKit, SwiftData, URLSession, DeviceCheck App Attest, Swift 6 concurrency, deployment target, XcodeGen). Verified 2026-10-10, mostly against developer.apple.com DocC JSON. Note: the docs and the Xcode support page show that Xcode 27 / iOS 27 / Swift 6.4 are already current, not iOS 26 / Xcode 26 as the task text assumed.

**Inhalt:** 44 Fakten (Konfidenz hoch 42, mittel 2, niedrig 0) · 11 Empfehlungen · 17 Fallstricke · 8 offene Fragen · Faktencheck von 25 Kernaussagen: 21 bestätigt, 3 korrigiert, 1 nicht verifizierbar · 13 vom Faktenprüfer ergänzte Fakten

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

- **[NICHT VERIFIZIERBAR]** iOS 27 supports the same iPhones as iOS 26 (iPhone 11 and later, iPhone SE 2nd generation and later), all with an A13 or newer chip.
  - **Ergebnis:** I could not reach apple.com or support.apple.com from this environment. Several secondary outlets (AppleInsider, iClarified, 9to5Mac, Appleosophy) say Apple's list is 'iPhone 11 and later, including iPhone SE (2nd generation and later)' and that no models were dropped. Both iPhone 11 and SE 2 use the A13. Treat this as likely, but confirm on support.apple.com before relying on it.
  - **Quelle:** <https://appleinsider.com/articles/26/06/08/ios-27-keeps-iphone-11-and-newer-compatibility>

- **[KORRIGIERT]** isSupported (@MainActor class var) needs A12 Bionic or later and is false in visionOS. isAvailable is true only when the person has granted camera access and no restriction blocks it. startScanning() can throw ScanningUnavailable (.unsupported, .cameraRestricted). UIRequiredDeviceCapabilities can include 'iphone-ipad-minimum-performance-a12'.
  - **Ergebnis:** The isSupported details (A12, false in visionOS, the a12 capability subkey) and the two ScanningUnavailable cases are correct. ScanningUnavailable conforms to Error and Sendable. Two corrections. (1) Apple's camera-scanning article says isAvailable is true 'If the user doesn't deny your app access to the camera, or there's no other restrictions', so it is also true before the permission prompt (not determined), not only after access is granted. The prompt appears on first camera use, and a denial arrives through dataScanner(_:becameUnavailableWithError:). (2) The startScanning() page shows only '@MainActor func startScanning() throws' and does not document which error is thrown. ScanningUnavailable is documented only as the parameter type of becameUnavailableWithError, so catch any Error, not just ScanningUnavailable.
  - **Quelle:** <https://developer.apple.com/documentation/visionkit/scanning-data-with-the-camera>

- **[KORRIGIERT]** CIBarcodeDescriptor subclasses (QR, Aztec, PDF417, DataMatrix) expose errorCorrectedPayload as codewords, not decoded bytes (with the per-symbology details given). Extra properties: symbolVersion, maskPattern, errorCorrectionLevel, isCompact, layerCount, dataCodewordCount, rowCount, columnCount.
  - **Ergebnis:** The codeword semantics are correct. QR: 8-bit codewords from ISO/IEC 18004 §6.4.10. Aztec: 6/8/10/12-bit codewords from ISO/IEC 24778 §7.3.1.2, where 'Clients will need to remove these extra bits'. PDF417: 16-bit codewords 0…928, where the first codeword is a count that includes itself and padding. DataMatrix: 'de-interleaved bits ... at the end of Step 1: Data encodation'. The property list is incomplete: CIDataMatrixCodeDescriptor also has 'eccVersion: CIDataMatrixCodeDescriptor.ECCVersion'. Per class: QR has symbolVersion, maskPattern and errorCorrectionLevel; Aztec has isCompact, layerCount and dataCodewordCount; PDF417 has isCompact, rowCount and columnCount; DataMatrix has rowCount, columnCount and eccVersion.
  - **Quelle:** <https://developer.apple.com/documentation/coreimage/cidatamatrixcodedescriptor>

- **[KORRIGIERT]** PhotosPicker (iOS 16) is '@MainActor @preconcurrency struct' with single- and multi-selection inits. PhotosPickerItem is Sendable and Transferable with loadTransferable(type:) async throws -&gt; sending T?. SwiftUI Image loads only PNG and JPEG through Transferable. The picker is out of process, so no photo-library authorization is needed.
  - **Ergebnis:** Mostly correct: the declaration, the inits, 'func loadTransferable&lt;T&gt;(type: T.Type) async throws -&gt; sending T? where T : Transferable', the PNG/JPEG-only note for Image, and Data conforming to Transferable. The PhotoKit privacy article confirms that PHPickerViewController 'manages its life cycle in a separate process ... doesn't need to explicitly authorize'. Correction: PhotosPickerItem's documented conformances are only Equatable, Hashable and Sendable. Transferable is not in its relationships list, even though the overview text says it 'conforms to Transferable'. Treat it as an item that loads Transferable types, not as a Transferable value.
  - **Quelle:** <https://developer.apple.com/documentation/photosui/photospickeritem>

## Fakten

### F1 · Konfidenz: hoch

Toolchain right now: Xcode 27 ships Swift 6.4 and the iOS 27 SDK. It supports deployment targets from iOS 15 to iOS 27 and needs macOS Tahoe 26.6 or later. Xcode 27 installs and runs only on Apple-silicon Macs. Xcode 26 ships Swift 6.2 and the iOS 26 SDK. The release-notes index already lists Xcode 27.1 RC and 27.2 beta 2.

- **Bedeutung fürs Design:** Treat this as the iOS 27 / Xcode 27 era, not the iOS 26 era. CI and dev machines must be Apple silicon on macOS 26.6 or later. iOS 27-only APIs (listed below) need `if #available(iOS 27, *)` guards. Cross-check: https://developer.apple.com/support/xcode/
- **Quelle:** <https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes>

### F2 · Konfidenz: hoch

Since April 28, 2026, every upload to App Store Connect must be built with Xcode 26 or later against the iOS 26 SDK or newer. This rule is about the SDK you build with, not the deployment target.

- **Bedeutung fürs Design:** There is no reason to keep older toolchains. The deployment target can still be set lower than the SDK.
- **Quelle:** <https://developer.apple.com/news/upcoming-requirements/>

### F3 · Konfidenz: hoch

Apple's App Store usage numbers, measured June 7, 2026: 79% of all iPhones and 86% of iPhones introduced in the last four years run iOS 26.

- **Bedeutung fürs Design:** Supports choosing iOS 26.0 as the minimum deployment target for a product launching in late 2026 or 2027.
- **Quelle:** <https://developer.apple.com/support/app-store/>

### F4 · Konfidenz: mittel

iOS 27 supports the same iPhones as iOS 26: iPhone 11 and later, plus iPhone SE 2nd generation and later. All of these have an A13 chip or newer.

- **Bedeutung fürs Design:** With iOS 26 as the minimum, every supported iPhone meets DataScanner's A12 requirement. Keep the runtime check anyway, because it is false on Mac, visionOS and (probably) the Simulator. This comes from a secondary source; confirm on support.apple.com.
- **Quelle:** <https://appleinsider.com/articles/26/06/08/ios-27-keeps-iphone-11-and-newer-compatibility>

### F5 · Konfidenz: hoch

VisionKit `DataScannerViewController` is available from iOS 16.0. It is declared `@MainActor @objc class` and inherits from UIViewController. Initializer: `init(recognizedDataTypes: Set<DataScannerViewController.RecognizedDataType>, qualityLevel: QualityLevel, recognizesMultipleItems: Bool, isHighFrameRateTrackingEnabled: Bool, isPinchToZoomEnabled: Bool, isGuidanceEnabled: Bool, isHighlightingEnabled: Bool)`; Apple's sample also calls `init(recognizedDataTypes:)` alone. Members: `startScanning() throws`, `stopScanning()`, `isScanning`, `recognizedItems: AsyncStream<[RecognizedItem]>`, `capturePhoto() async throws -> UIImage`, `regionOfInterest: CGRect?`, `overlayContainerView`, `zoomFactor`/`minZoomFactor`/`maxZoomFactor`, and `supportedTextRecognitionLanguages`. `QualityLevel` has `.fast`, `.balanced` and `.accurate`. None of this is deprecated in the current SDK.

- **Bedeutung fürs Design:** This is the main live-scan component. Wrap it in UIViewControllerRepresentable. Use `.accurate` for dense Aztec and PDF417 codes on train and airline tickets. `capturePhoto()` can grab a high-resolution still to re-decode with Vision or to keep as the source image.
- **Quelle:** <https://developer.apple.com/documentation/visionkit/datascannerviewcontroller>

### F6 · Konfidenz: hoch

`DataScannerViewController.isSupported` (`@MainActor class var`) needs an A12 Bionic chip or later and is false in visionOS. `isAvailable` is true only when the person has granted camera access and no restriction such as Screen Time blocks the camera. `startScanning()` can throw `DataScannerViewController.ScanningUnavailable`, whose cases are `.unsupported` and `.cameraRestricted`. If scanning is a core feature, the Info.plist key `UIRequiredDeviceCapabilities` can include `iphone-ipad-minimum-performance-a12`.

- **Bedeutung fürs Design:** Gate the scan UI on `isSupported && isAvailable`, and fall back to photo, PDF or file import. Don't add UIRequiredDeviceCapabilities, because import works on every device. Related pages: https://developer.apple.com/documentation/visionkit/datascannerviewcontroller/isavailable and https://developer.apple.com/documentation/visionkit/datascannerviewcontroller/scanningunavailable
- **Quelle:** <https://developer.apple.com/documentation/visionkit/datascannerviewcontroller/issupported>

### F7 · Konfidenz: hoch

The `NSCameraUsageDescription` Info.plist key is required; without it the app hits a runtime error when it accesses the camera. If the user taps Don't Allow at the first prompt, the scanner calls `dataScanner(_:becameUnavailableWithError:)`. In the camera-scanning article Apple's own example passes `.text(languages: ["en-US", "fr-FR", "de-DE"])` to the scanner.

- **Bedeutung fürs Design:** Write a German and an English usage string. You can show a pre-permission screen using AVCaptureDevice `authorizationStatus(for: .video)` and `requestAccess(for: .video) async -> Bool` (iOS 7). Handle `becameUnavailableWithError` by switching to the import UI.
- **Quelle:** <https://developer.apple.com/documentation/visionkit/scanning-data-with-the-camera>

### F8 · Konfidenz: hoch

`RecognizedDataType.barcode(symbologies: [VNBarcodeSymbology] = [])` and `.text(languages: [String], textContentType: TextContentType?)` are both iOS 16. `DataScannerViewControllerDelegate` is a `@MainActor protocol ... : AnyObject` with these methods: `dataScanner(_:didTapOn:)`, `dataScanner(_:didAdd:allItems:)`, `dataScanner(_:didUpdate:allItems:)`, `dataScanner(_:didRemove:allItems:)`, `dataScannerDidZoom(_:)` and `dataScanner(_:becameUnavailableWithError:)`.

- **Bedeutung fürs Design:** Use `didAdd` and `didUpdate` for auto-capture, and require the same payload across several updates before accepting it. Use `didTapOn` when the user picks a code manually. The Coordinator must be main-actor isolated.
- **Quelle:** <https://developer.apple.com/documentation/visionkit/datascannerviewcontrollerdelegate>

### F9 · Konfidenz: hoch

`RecognizedItem` (iOS 16) is an enum with cases `.barcode(RecognizedItem.Barcode)` and `.text(RecognizedItem.Text)`. `RecognizedItem.Barcode` has `payloadStringValue: String?`, `bounds`, `id: UUID` and `observation: VNBarcodeObservation`. `RecognizedItem`, `RecognizedItem.Barcode` and `RecognizedItem.Text` conform only to `Identifiable`; they are not Sendable.

- **Bedeutung fürs Design:** Get the raw bytes from a live scan with `barcode.observation.payloadData` (iOS 17+) and the symbology with `barcode.observation.symbology`. Inside the delegate call, copy these right away into a Sendable DTO such as `ScannedCode { symbology: String; payload: Data?; text: String? }`.
- **Quelle:** <https://developer.apple.com/documentation/visionkit/recognizeditem/barcode>

### F10 · Konfidenz: hoch

`VNDetectBarcodesRequest` is iOS 11. The current way to list symbologies is the instance method `supportedSymbologies() throws -> [VNBarcodeSymbology]` (iOS 15); the class property `supportedSymbologies` has been deprecated since iOS 15. Revision constants: `VNDetectBarcodesRequestRevision1` (deprecated), `VNDetectBarcodesRequestRevision2` (deprecated in iOS 18 and renamed to Revision3), `VNDetectBarcodesRequestRevision3` (iOS 16) and `VNDetectBarcodesRequestRevision4` (iOS 17). Other members: `symbologies`, `coalesceCompositeSymbologies` and `results: [VNBarcodeObservation]?`.

- **Bedeutung fürs Design:** Use the Swift-native API for still images. Only fall back to VN\* for the VisionKit observation and for the CIBarcodeDescriptor path. Revision 4 page: https://developer.apple.com/documentation/vision/vndetectbarcodesrequestrevision4
- **Quelle:** <https://developer.apple.com/documentation/vision/vndetectbarcodesrequest>

### F11 · Konfidenz: hoch

`VNBarcodeSymbology` constants (lower-case; the upper-case versions such as `.QR` and `.Aztec` are deprecated): aztec, codabar, code39, code39Checksum, code39FullASCII, code39FullASCIIChecksum, code93, code93i, code128, dataMatrix, ean8, ean13, gs1DataBar, gs1DataBarExpanded, gs1DataBarLimited, i2of5, i2of5Checksum, itf14, microPDF417, microQR, msiPlessey, pdf417, qr, upce. Spot checks show codabar and microQR are iOS 15. The type is Sendable.

- **Bedeutung fürs Design:** Build the mapping table from Vision symbology to Wallet `format` from this list. Store the raw value with `VNBarcodeSymbology.rawValue` (a String).
- **Quelle:** <https://developer.apple.com/documentation/vision/vnbarcodesymbology>

### F12 · Konfidenz: hoch

`VNBarcodeObservation` has: `payloadStringValue: String?` (iOS 11; the docs say a string may not be available depending on symbology or payload), `payloadData: Data?` ("The raw data representation of the barcode's payload", iOS 17.0), `supplementalPayloadString`, `supplementalPayloadData` (iOS 17), `supplementalCompositeType`, `isGS1DataCarrier` (iOS 17), `isColorInverted`, `symbology`, and `barcodeDescriptor: CIBarcodeDescriptor?` (iOS 11).

- **Bedeutung fürs Design:** `payloadData` is the way to read binary tickets such as Deutsche Bahn UIC 918.3 Aztec codes. Any deployment target of iOS 17 or later removes the need for a fallback. Never round-trip binary payloads through String.
- **Quelle:** <https://developer.apple.com/documentation/vision/vnbarcodeobservation/payloaddata>

### F13 · Konfidenz: hoch

`CIBarcodeDescriptor` subclasses are `CIQRCodeDescriptor`, `CIAztecCodeDescriptor`, `CIPDF417CodeDescriptor` and `CIDataMatrixCodeDescriptor`. Each has `errorCorrectedPayload: Data`, and that value is codewords, not decoded bytes. For QR it is the 8-bit codewords right after 'bitstream to codeword conversion' (ISO 18004). For Aztec it is the 6/8/10/12-bit data codewords with inserted dummy bits that you must strip (ISO 24778). For PDF417 it is 16-bit codewords 0…928, with the first one giving the count (ISO 15438). For Data Matrix it is the de-interleaved data-encodation bits. The extra properties are `symbolVersion`, `maskPattern`, `errorCorrectionLevel`, `isCompact`, `layerCount`, `dataCodewordCount`, `rowCount` and `columnCount`.

- **Bedeutung fürs Design:** Before iOS 17, getting raw bytes meant writing your own high-level decoder per symbology. That is a strong reason not to support iOS 16. Keep the descriptor only for debugging or for re-rendering the identical symbol.
- **Quelle:** <https://developer.apple.com/documentation/coreimage/ciazteccodedescriptor>

### F14 · Konfidenz: hoch

Swift-native Vision `DetectBarcodesRequest` (struct, Sendable) is available from iOS 18.0. API: `init(_ revision: DetectBarcodesRequest.Revision?)` (the only revision is `.revision4`), `symbologies: [BarcodeSymbology]`, `supportedSymbologies` (documented as potentially expensive), `coalescesCompositeSymbologies`, and `perform(on: CGImage | URL | Data | CVPixelBuffer | CMSampleBuffer | CIImage, orientation: CGImagePropertyOrientation?) async throws`. `BarcodeSymbology` is a CaseIterable, Codable, Sendable enum with the same case names as `VNBarcodeSymbology`.

- **Bedeutung fürs Design:** Use this as the still-image and PDF-page decoder. It's async and Sendable, so it fits Swift 6 strict concurrency.
- **Quelle:** <https://developer.apple.com/documentation/vision/detectbarcodesrequest>

### F15 · Konfidenz: hoch

`BarcodeObservation` (iOS 18, Sendable, Codable) has `payloadString` (not `payloadStringValue`), `payloadData: Data?`, `supplementalPayloadString`, `supplementalPayloadData`, `supplementalCompositeType`, `symbology: BarcodeSymbology`, `isGS1DataCarrier`, `isColorInverted` and `boundingRegion`, plus `init(_ observation: VNBarcodeObservation)`. It has no `barcodeDescriptor`.

- **Bedeutung fürs Design:** Normalize both sources into one DTO: the VisionKit live path gives a VNBarcodeObservation, the still-image path gives a BarcodeObservation. `BarcodeObservation(vnObservation)` can do the conversion. Code that needs the CIBarcodeDescriptor must use the VN API.
- **Quelle:** <https://developer.apple.com/documentation/vision/barcodeobservation>

### F16 · Konfidenz: hoch

`ImageRequestHandler` (iOS 18) is a final, Sendable class. It has inits for CGImage, URL, Data, CIImage, CVPixelBuffer and CMSampleBuffer, each with `orientation:`. It offers `perform<each T>(repeat each T) async throws -> (repeat (each T).Result)` and `performAll(_:)`. The legacy `VNImageRequestHandler.perform(_ requests: [VNRequest]) throws` is synchronous and returns only after every request finishes. Neither `VNImageRequestHandler` nor `VNRequest` is Sendable.

- **Bedeutung fürs Design:** One pass works: `let (codes, text) = try await ImageRequestHandler(cgImage, orientation: o).perform(DetectBarcodesRequest(), RecognizeTextRequest())`. Legacy VN code has to run inside a single non-main isolation domain.
- **Quelle:** <https://developer.apple.com/documentation/vision/imagerequesthandler>

### F17 · Konfidenz: hoch

`RecognizeTextRequest` (iOS 18, Sendable) has `recognitionLanguages: [Locale.Language]`, `supportedRecognitionLanguages`, `automaticallyDetectsLanguage`, `usesLanguageCorrection`, `customWords`, `minimumTextHeightFraction` and `recognitionLevel` (`.accurate` or `.fast`). The only revision is `.revision3`. It returns `RecognizedTextObservation`, with `transcript`, `topCandidates(_:)`, `boundingRegion` and `recognitionLanguages`. The legacy `VNRecognizeTextRequest` (iOS 13) uses `recognitionLanguages: [String]` and `supportedRecognitionLanguages() throws`; Revision3 is iOS 16, and Revisions 1 and 2 are deprecated.

- **Bedeutung fürs Design:** For German, set `recognitionLanguages = [Locale.Language(identifier: "de-DE"), Locale.Language(identifier: "en-US")]` and check at runtime that they appear in `supportedRecognitionLanguages`. I didn't verify the German list for Vision itself; DataScanner's article does use "de-DE". VN page: https://developer.apple.com/documentation/vision/vnrecognizetextrequest
- **Quelle:** <https://developer.apple.com/documentation/vision/recognizetextrequest>

### F18 · Konfidenz: hoch

`RecognizeDocumentsRequest` (iOS 26.0) returns `DocumentObservation`. Its `document: DocumentObservation.Container` exposes `text`, `paragraphs`, `title`, `tables`, `lists` and `barcodes: [BarcodeObservation]`. `Container.Text` has `transcript`, `lines`, `words` and `detectedData: [DataDetectorMatch]`, where each match has `match: DataDetector.Match`. Configuration: `barcodeDetectionOptions` (`enabled`, `symbologies`, `coalesceCompositeSymbologies`) and `textRecognitionOptions` (`recognitionLanguages`, `automaticallyDetectLanguage`, `useLanguageCorrection`, `customWords`, `maximumCandidateCount`, `minimumTextHeightFraction`).

- **Bedeutung fürs Design:** On iOS 26 and later, a single request returns the barcodes, structured text and detected dates or flight numbers for a ticket photo or PDF page, which suits the field auto-suggestion feature. Watch out: the property names differ from RecognizeTextRequest (`automaticallyDetectLanguage` vs `automaticallyDetectsLanguage`, `useLanguageCorrection` vs `usesLanguageCorrection`) and from DetectBarcodesRequest (`coalesceCompositeSymbologies` vs `coalescesCompositeSymbologies`). Data detector page: https://developer.apple.com/documentation/vision/documentobservation/container/datadetectormatch
- **Quelle:** <https://developer.apple.com/documentation/vision/recognizedocumentsrequest>

### F19 · Konfidenz: hoch

The Swift DataDetection API is iOS 26.0: `StringProtocol.dataDetectorMatches(_ types: DataDetector.MatchType = .all, options: DataDetector.Options = .init()) -> some AsyncSequence<DataDetector.Match, Never>`. Match types: `.calendarEvent`, `.flightNumber`, `.moneyAmount`, `.postalAddress`, `.link`, `.emailAddress`, `.phoneNumber`, `.measurement`, `.shipmentTrackingNumber`, `.paymentIdentifier` and `.all`. A match has `details` (for example `.calendarEvent(CalendarEvent)` with `startDate`, `endDate`, `allDay`, `startTimeZone` and `endTimeZone`) and `range`. Options: `documentDate`, `documentLanguageCode`, `documentRegion` and `documentTimeZone`. The legacy `NSDataDetector` (iOS 4) takes `NSTextCheckingResult.CheckingType.date`; Apple says not to use it for validation, because it drops uncertain matches.

- **Bedeutung fürs Design:** Suggest relevantDate, expiry and flight number from OCR text. Set the options to `documentLanguageCode` .german, `documentRegion` .germany and `documentTimeZone` Europe/Berlin so German formats like dd.MM.yyyy parse correctly. Everything is a suggestion that the user confirms. NSDataDetector page: https://developer.apple.com/documentation/foundation/nsdatadetector
- **Quelle:** <https://developer.apple.com/documentation/swift/stringprotocol/datadetectormatches(_:options:)>

### F20 · Konfidenz: hoch

`PhotosPicker` (PhotosUI, iOS 16) is a `@MainActor @preconcurrency struct`. Inits include `init(selection: Binding<PhotosPickerItem?>, matching: PHPickerFilter?, preferredItemEncoding:, label:)` and a multi-selection version with `maxSelectionCount`. `PhotosPickerItem` is Sendable and Transferable, with `loadTransferable(type:) async throws -> sending T?`. SwiftUI `Image` loads only PNG and JPEG through Transferable. The picker runs out of process, so it needs no photo-library authorization.

- **Bedeutung fürs Design:** Use `matching: .images` (screenshots allowed) and `loadTransferable(type: Data.self)`; Data conforms to Transferable. Then decode with `UIImage(data:)` or CGImageSource so HEIC and EXIF orientation work. Don't add NSPhotoLibraryUsageDescription. Privacy page: https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app
- **Quelle:** <https://developer.apple.com/documentation/photosui/photospicker>

### F21 · Konfidenz: hoch

SwiftUI `.fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:)` is iOS 14; its result is `Result<[URL], Error>`. The URLs are security-scoped: call `startAccessingSecurityScopedResource()` before reading and `stopAccessingSecurityScopedResource()` afterwards.

- **Bedeutung fürs Design:** Use `allowedContentTypes: [.pdf, .image]`. Copy the file into the app sandbox right away, while access is open.
- **Quelle:** <https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:allowsmultipleselection:oncompletion:)>

### F22 · Konfidenz: hoch

PDFKit: `PDFDocument(url:)` and `PDFDocument(data:)` are failable inits. `pageCount` gives the page count; `page(at:)` is zero-based and raises an exception when out of bounds. `PDFPage.bounds(for: .mediaBox)` is in page space, so rotation may need a transform. `PDFPage.thumbnail(of: CGSize, for: PDFDisplayBox) -> UIImage` and `draw(with: PDFDisplayBox, to: CGContext)` are iOS 11. `UIGraphicsImageRenderer(size:format:)` with `UIGraphicsImageRendererFormat.scale` and `.opaque` produces a UIImage via `image(actions:)`.

- **Bedeutung fürs Design:** Render each page to a bitmap at about 300 dpi (scale ≈ 300/72), with a white background and a cap on pixel size. Then run DetectBarcodesRequest. Check `index < pageCount` before calling `page(at:)`. Page: https://developer.apple.com/documentation/pdfkit/pdfpage/draw(with:to:)
- **Quelle:** <https://developer.apple.com/documentation/pdfkit/pdfpage/thumbnail(of:for:)>

### F23 · Konfidenz: hoch

Share Extension Info.plist: `NSExtension` &gt; `NSExtensionPointIdentifier` = `com.apple.share-services`; `NSExtensionAttributes` &gt; `NSExtensionActivationRule`. The rule is either a dictionary (keys such as `NSExtensionActivationSupportsImageWithMaxCount`, `NSExtensionActivationSupportsFileWithMaxCount`, `NSExtensionActivationSupportsWebURLWithMaxCount`, `NSExtensionActivationSupportsAttachmentsWithMinCount`/`MaxCount`) or a SUBQUERY predicate string. Apple's single-PDF example is `SUBQUERY(extensionItems, $extensionItem, SUBQUERY($extensionItem.attachments, $attachment, ANY $attachment.registeredTypeIdentifiers UTI-CONFORMS-TO "com.adobe.pdf").@count == $extensionItem.attachments.@count).@count == 1`. If any extension contains `TRUEPREDICATE`, App Review rejects the app.

- **Bedeutung fürs Design:** Use a predicate that accepts com.adobe.pdf OR public.image, so Mail and Safari PDFs and images trigger the extension. Key reference: https://developer.apple.com/documentation/bundleresources/information-property-list/nsextension/nsextensionattributes/nsextensionactivationrule
- **Quelle:** <https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/ExtensionScenarios.html>

### F24 · Konfidenz: hoch

An app extension and its containing app can't reach each other's containers. To share data they need an App Group: entitlement `com.apple.security.application-groups`, and `UserDefaults(suiteName:)` or a shared container with coordinated access. `NSExtensionContext.open(_:)` is supported on iOS only by the Today and iMessage extension points, so a Share extension cannot officially launch its containing app.

- **Bedeutung fürs Design:** The share extension should copy the PDF or image into an App Group 'inbox' folder and tell the user it will appear in QRCode2Wallet. The main app picks up the inbox items on launch or when it becomes active. Load attachments with `NSItemProvider.loadFileRepresentation(for: .pdf, openInPlace: false)` or `loadDataRepresentation(for:)` (iOS 16, @Sendable handlers).
- **Quelle:** <https://developer.apple.com/documentation/foundation/nsextensioncontext/open(_:completionhandler:)>

### F25 · Konfidenz: hoch

`PKPass.init(data: Data) throws` expects a signed pass. Signature problems throw `PKPassKitError.Code.invalidSignature` and bad data throws `.invalidDataError`. The other codes are `.unsupportedVersionError`, `.notEntitledError` and `.unknownError`. `PKPass` is not Sendable.

- **Bedeutung fürs Design:** Download the .pkpass as `Data`, which is Sendable, then build the PKPass on the MainActor. Map invalidSignature to a 'backend signing broken' alert and telemetry event.
- **Quelle:** <https://developer.apple.com/documentation/passkit/pkpass/init(data:)>

### F26 · Konfidenz: hoch

`PKPassLibrary` is not thread-safe; use each instance on a single thread. `isPassLibraryAvailable()` does not tell you whether passes can be added; use `PKAddPassesViewController.canAddPasses()` (iOS 8) for that. `passes()` returns only the passes the app's entitlements allow. `containsPass(_:)` works without read entitlements. `replacePass(with:) -> Bool` replaces only an existing pass with the same passTypeIdentifier and serialNumber. `addPasses(_:withCompletionHandler:)` (iOS 7) has an async form, `addPasses(_:) async -> PKPassLibraryAddPassesStatus`, returning `.didAddPasses`, `.shouldReviewPasses` (you must then present PKAddPassesViewController) or `.didCancelAddPasses`.

- **Bedeutung fürs Design:** Keep one PKPassLibrary on the MainActor. Use `containsPass` to show an 'In Wallet' badge. A SwiftUI flow can call `await library.addPasses([pass])` and only present a VC on `.shouldReviewPasses`.
- **Quelle:** <https://developer.apple.com/documentation/passkit/pkpasslibrary>

### F27 · Konfidenz: hoch

Adding a pass needs no entitlement, because the user approves it explicitly. Reading, updating and deleting passes need the Pass Type IDs entitlement `com.apple.developer.pass-type-identifiers`, an array of pass type identifiers added through the Wallet capability; `$(TeamIdentifierPrefix)*` means all of the team's passes.

- **Bedeutung fürs Design:** V1 can ship without the Wallet capability. To edit or regenerate passes in place (`pass(withPassTypeIdentifier:serialNumber:)`, `replacePass`, `removePass`), enable Wallet with the backend's own Pass Type ID, since passes are signed by the backend under our team. Entitlement page: https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.pass-type-identifiers
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Apps.html>

### F28 · Konfidenz: hoch

New in iOS 26.0: `PKPassLibrary.Capability.backgroundAddPasses`, `requestAuthorization(for:) async -> PKPassLibrary.AuthorizationStatus` and `authorizationStatus(for:)`. Status values are `.authorized`, `.denied`, `.notDetermined` and `.restricted`. Once authorized, `addPasses` adds passes without a confirmation prompt and the system shows a notification instead. The permission prompt appears once and the user can change it in Settings. The app must be installed and running.

- **Bedeutung fürs Design:** This is optional. In a converter app the user should see the generated pass before it lands in Wallet, so the default should still go through review. Possible use: silent regeneration. Flow description: https://developer.apple.com/documentation/walletpasses/distributing-and-updating-a-pass
- **Quelle:** <https://developer.apple.com/documentation/passkit/pkpasslibrary/capability/backgroundaddpasses>

### F29 · Konfidenz: hoch

New in iOS 27.0: `PKPassLibrary.addPasses(data: [Data]) async -> PKPassLibraryAddPassesStatus`, `addPasses(fromArchiveData:)`, `addPasses(fromArchiveAt:)`, and `PKAddPassesViewController.init?(passesData: [Data])`, `init?(passesArchiveData:)` and `init?(passesArchiveAt:)`.

- **Bedeutung fürs Design:** These let you hand raw .pkpass bytes straight to Wallet without building a PKPass. Use them only behind `if #available(iOS 27, *)`; the iOS 26 baseline uses `PKPass(data:)`.
- **Quelle:** <https://developer.apple.com/documentation/passkit/pkpasslibrary/addpasses(data:completion:)>

### F30 · Konfidenz: hoch

`PKAddPassesViewController` (iOS 6) has `init?(pass:)`, `init?(passes:)` and `delegate: PKAddPassesViewControllerDelegate`, whose callback is `addPassesViewControllerDidFinish(_:)`. SwiftUI `AddPassToWalletButton` (PassKit, iOS 16, not available on visionOS) is `@MainActor @preconcurrency struct AddPassToWalletButton<Fallback: View>` with `init(_ passes: [PKPass], onCompletion: @escaping (Bool) -> Void)`, a `fallback:` variant and `init(action: @escaping () -> Void)`. The style modifier is `.addPassToWalletButtonStyle(_:)` (`.black`, `.blackOutline`). The UIKit equivalent is `PKAddPassButton(addPassButtonStyle:)` (iOS 9).

- **Bedeutung fürs Design:** Once the PKPass exists, use `AddPassToWalletButton([pass]) { added in ... }`. If you need to download or sign first, use `init(action:)` and then call `addPasses`. Wrap PKAddPassesViewController in UIViewControllerRepresentable only for the `.shouldReviewPasses` case.
- **Quelle:** <https://developer.apple.com/documentation/passkit/addpasstowalletbutton>

### F31 · Konfidenz: hoch

The Wallet pass `barcodes[]` object has the keys `format`, `message`, `messageEncoding` (an IANA charset such as "iso-8859-1") and an optional `altText`. Allowed `format` values: PKBarcodeFormatQR, PKBarcodeFormatPDF417, PKBarcodeFormatAztec, PKBarcodeFormatCode128, PKBarcodeFormatCode39, PKBarcodeFormatCodabar, PKBarcodeFormatEAN13 and PKBarcodeFormatI2of5. From iOS 27 you can list several barcodes as fallbacks: EAN-13 renders on iOS 27 and later, QR on older versions.

- **Bedeutung fürs Design:** The client needs a symbology-compatibility table. Data Matrix, EAN-8, UPC-E, ITF-14, Code 93, GS1 DataBar, microQR and microPDF417 can't be rendered by Wallet as-is. Send the raw bytes (base64) plus the symbology to the backend, and let it choose the format plus a fallback.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary>

### F32 · Konfidenz: hoch

The MIME type for a .pkpass is application/vnd.apple.pkpass. A .pkpasses bundle (a zip of .pkpass files) uses application/vnd.apple.pkpasses and is limited to 10 passes or 150 MB.

- **Bedeutung fürs Design:** The client should check the `Content-Type` and the 200 status before calling `PKPass(data:)`. Bundle limits: https://developer.apple.com/documentation/walletpasses/distributing-and-updating-a-pass
- **Quelle:** <https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/DistributingPasses.html>

### F33 · Konfidenz: hoch

SwiftData (iOS 17): the `@Model` macro adds Observable and PersistentModel conformances; the current SDK declaration also lists Sendable. `Schema.Attribute.Option.externalStorage` is iOS 17 and `#Unique<T>([\.keyPath], ...)` is iOS 18. `ModelConfiguration(_:schema:isStoredInMemoryOnly:allowsSave:groupContainer:cloudKitDatabase:)` accepts `.automatic`, `.identifier("group...")` or `.none`. `.modelContainer(for:inMemory:isAutosaveEnabled:isUndoEnabled:onSetup:)` is a `@MainActor` view modifier. `@ModelActor` gives background contexts, and `PersistentIdentifier` is Sendable and Codable.

- **Bedeutung fürs Design:** Model: `@Model final class PassRecord { #Unique<PassRecord>([\.serialNumber]); var serialNumber: String; var passTypeIdentifier: String; var symbology: String; @Attribute(.externalStorage) var payload: Data; @Attribute(.externalStorage) var pkpassData: Data?; @Attribute(.externalStorage) var sourceImage: Data?; var createdAt: Date }`. Pass PersistentIdentifier across actors, not model objects. Macro and attribute pages: https://developer.apple.com/documentation/swiftdata/model() and https://developer.apple.com/documentation/swiftdata/unique(_:)
- **Quelle:** <https://developer.apple.com/documentation/swiftdata/modelconfiguration>

### F34 · Konfidenz: hoch

URLSession async APIs (iOS 15): `data(for: URLRequest, delegate:) async throws -> (Data, URLResponse)`, `upload(for: URLRequest, from: Data, delegate:) async throws -> (Data, URLResponse)` and `download(for: URLRequest, delegate:) async throws -> (URL, URLResponse)`.

- **Bedeutung fürs Design:** POST the JSON with `upload(for:from:)` and `Content-Type: application/json`, receiving the .pkpass bytes in the response, or use a separate GET with `data(for:)`. Cast the response to HTTPURLResponse and check the status. Passes are small, so `data(for:)` is enough.
- **Quelle:** <https://developer.apple.com/documentation/foundation/urlsession/upload(for:from:delegate:)>

### F35 · Konfidenz: hoch

`DCAppAttestService.shared` (iOS 14) has `isSupported` plus async APIs: `generateKey() async throws -> String` (key identifier), `attestKey(_ keyId: String, clientDataHash: Data) async throws -> Data` (attestation object) and `generateAssertion(_ keyId: String, clientDataHash: Data) async throws -> Data`. `clientDataHash` is the SHA256 of data that includes a one-time server challenge of at least 16 bytes. On `serverUnavailable`, retry with the same key and hash; on any other error, discard the key. Keys survive app updates but not reinstall, device migration or backup restore. Apple recommends one key per user account per device. `DCError.Code` values: `featureUnsupported`, `invalidInput`, `invalidKey`, `serverUnavailable` and `unknownSystemFailure`.

- **Bedeutung fürs Design:** Client flow: GET /attest/challenge → `generateKey` → `attestKey(keyId, SHA256(challenge))` → POST {keyId, attestation(base64), challenge} → store keyId in the Keychain. Then for each signing request: GET /challenge → `clientData = JSON(request + challenge)` → `generateAssertion(keyId, SHA256(clientData))` → send the assertion with the request. On `invalidKey`, re-attest.
- **Quelle:** <https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity>

### F36 · Konfidenz: hoch

`isSupported` is false on Mac, including Mac Catalyst and iOS apps running on Apple silicon. `generateKey` fails in most app extensions even when `isSupported` is true. The isSupported page says only watchOS extensions (watchOS 9 and later) are supported; the integrity article says Action, extensible SSO and watchOS extensions are. Share extensions are unsupported according to both.

- **Bedeutung fürs Design:** The Share extension can't attest, so backend calls that require App Attest have to come from the main app (hence the inbox design). The server needs a policy for devices that can't attest: Simulator, Mac and older devices. Whether Action extensions are supported is contradictory in Apple's docs; treat it as unverified.
- **Quelle:** <https://developer.apple.com/documentation/devicecheck/dcappattestservice/issupported>

### F37 · Konfidenz: hoch

App Attest entitlement: `com.apple.developer.devicecheck.appattest-environment`, with value `development` or `production`. Builds distributed through TestFlight or the App Store ignore it and use production. Sandbox keys and production keys don't work in each other's environment. An App ID registered on the developer portal is required.

- **Bedeutung fürs Design:** Put it in the app's entitlements, generated by XcodeGen. The backend has to verify against the matching environment, recognizable from the AAGUID in the attestation.
- **Quelle:** <https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.devicecheck.appattest-environment>

### F38 · Konfidenz: hoch

Swift 6.2 concurrency proposals: SE-0466 (Implemented in Swift 6.2) adds default `@MainActor` isolation inference per module. SE-0461 (Implemented in Swift 6.2, feature flag `NonisolatedNonsendingByDefault`) makes nonisolated async functions run on the caller's actor unless marked `@concurrent`. Xcode build settings: `SWIFT_DEFAULT_ACTOR_ISOLATION` (MainActor or nonisolated); `SWIFT_APPROACHABLE_CONCURRENCY`, which turns on DisableOutwardActorInference, GlobalActorIsolatedTypesUsability, InferIsolatedConformances, InferSendableFromCaptures and NonisolatedNonsendingByDefault; and `SWIFT_STRICT_CONCURRENCY`, which is always 'complete' in Swift 6 mode and reports errors.

- **Bedeutung fürs Design:** With these settings, a plain `func decode(_:) async` called from a SwiftUI view runs on the main thread. CPU-heavy steps (PDF rasterizing, VN\* synchronous perform, image decoding) must be `@concurrent` or live on a dedicated actor. Proposals: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0466-control-default-actor-isolation.md and https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md
- **Quelle:** <https://developer.apple.com/documentation/xcode/build-settings-reference>

### F39 · Konfidenz: mittel

Xcode 26 project templates reportedly default to `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` for new projects, while existing projects stay nonisolated. Sources disagree on whether Approachable Concurrency is also enabled by default.

- **Bedeutung fürs Design:** XcodeGen doesn't apply Xcode's new-project template defaults, so set both settings explicitly in project.yml to get predictable behaviour.
- **Quelle:** <https://www.donnywals.com/setting-default-actor-isolation-in-xcode-26/>

### F40 · Konfidenz: hoch

Sendable status in the current SDK docs. Sendable: UIImage, CGImage, Data, PhotosPickerItem, VNBarcodeSymbology, and all Swift-native Vision requests and observations (DetectBarcodesRequest, BarcodeObservation, RecognizeTextRequest, RecognizeDocumentsRequest, DocumentObservation, ImageRequestHandler), as well as PKAddPassesViewController and AddPassToWalletButton. Not Sendable: VNImageRequestHandler, VNRequest, VNBarcodeObservation (an NSObject without Sendable), RecognizedItem / RecognizedItem.Barcode / RecognizedItem.Text, PKPass and PKPassLibrary. `UIViewControllerRepresentable` is `@MainActor @preconcurrency`.

- **Bedeutung fürs Design:** Only Data, CGImage, UIImage and Codable DTOs should cross actor boundaries. Keep VisionKit items, PKPass, PKPassLibrary and ModelContext on the MainActor. UIImage: https://developer.apple.com/documentation/uikit/uiimage
- **Quelle:** <https://developer.apple.com/documentation/vision/vnimagerequesthandler>

### F41 · Konfidenz: hoch

Observation's `@Observable` macro is iOS 17.

- **Bedeutung fürs Design:** Use `@Observable` view models instead of ObservableObject. Any deployment target of iOS 17 or later allows it.
- **Quelle:** <https://developer.apple.com/documentation/observation/observable()>

### F42 · Konfidenz: hoch

`INFOPLIST_KEY_NSCameraUsageDescription` is a real Xcode build setting, applied when `GENERATE_INFOPLIST_FILE` is enabled. The build system merges an explicit INFOPLIST_FILE with the values it generates.

- **Bedeutung fürs Design:** With XcodeGen, either generate the full Info.plist via `info: properties:` or use INFOPLIST_KEY_\* settings, and pick one. A target-level `info:` block is the more readable choice in YAML.
- **Quelle:** <https://developer.apple.com/documentation/xcode/build-settings-reference>

### F43 · Konfidenz: hoch

XcodeGen: the latest released version is 2.46.0 according to CHANGELOG.md. `options.projectFormat` values go up to `xcode16_3` (default `xcode16_0`). Target keys: `type` (`application`, `app-extension`, `bundle.unit-test`, …), `platform`, `deploymentTarget`, `sources`, `settings`, `dependencies`, `info: {path, properties}` (writes Info.plist and sets INFOPLIST_FILE; generates CFBundleIdentifier, CFBundleVersion and similar), `entitlements: {path, properties}` (writes .entitlements and sets CODE_SIGN_ENTITLEMENTS) and `scheme: {testTargets, gatherCoverageData}`. TEST_HOST is set automatically for unit tests that depend on an app. A `target:` dependency embeds by default in application targets. Code signing is configured only through DEVELOPMENT_TEAM and CODE_SIGN_STYLE. XcodeGen doesn't abstract capabilities; you add entitlements and frameworks yourself.

- **Bedeutung fürs Design:** Generate the .xcodeproj in CI with `xcodegen generate` and don't commit it. Capabilities such as Wallet, App Groups and App Attest go in as `entitlements.properties`, and must also be enabled on the App ID in the developer portal. Changelog and FAQ: https://github.com/yonaskolb/XcodeGen/blob/master/CHANGELOG.md and https://github.com/yonaskolb/XcodeGen/blob/master/Docs/FAQ.md
- **Quelle:** <https://github.com/yonaskolb/XcodeGen/blob/master/Docs/ProjectSpec.md>

### F44 · Konfidenz: hoch

VisionKit also includes `VNDocumentCameraViewController` (paper document scanning UI) and `ImageAnalyzer`/`ImageAnalysisInteraction` (Live Text on still images).

- **Bedeutung fürs Design:** Optionally, offer 'scan paper ticket' through VNDocumentCameraViewController: it produces perspective-corrected pages that can go to DetectBarcodesRequest when a live scan fails on a crumpled printout.
- **Quelle:** <https://developer.apple.com/documentation/visionkit>

## Empfehlungen

### E1

**Empfehlung:** Set the minimum deployment target to iOS 26.0, build with Xcode 27 (iOS 27 SDK), and put iOS 27 APIs behind `if #available(iOS 27, *)`. If market data later demands it, the fallback floor is iOS 18.0, never lower.

**Begründung:** iOS 17 is the absolute minimum because it adds `VNBarcodeObservation.payloadData` (raw bytes for binary UIC 918.3 tickets; before that you need a custom codeword decoder), SwiftData and `@Observable`. iOS 18 adds the Sendable Swift Vision API (DetectBarcodesRequest, BarcodeObservation.payloadData, RecognizeTextRequest, ImageRequestHandler) and SwiftData `#Unique`. iOS 26 adds RecognizeDocumentsRequest (barcodes, text and data detection in one pass), the Swift DataDetector API and PassKit backgroundAddPasses. On reach: 79% of all iPhones ran iOS 26 in June 2026, and iOS 26 and 27 support the same devices (iPhone 11 and later). The only devices you give up are iPhone XS and XR plus people who haven't updated. Choosing iOS 26 also avoids maintaining two pipelines (VN and Swift Vision) under Swift 6 strict concurrency.

### E2

**Empfehlung:** Swift settings in project.yml: `SWIFT_VERSION: 6.0`, `SWIFT_DEFAULT_ACTOR_ISOLATION: MainActor`, `SWIFT_APPROACHABLE_CONCURRENCY: YES`. Mark CPU-heavy functions `@concurrent nonisolated` (PDF rasterizing, image decoding, any VN\* synchronous perform), or put them in an `actor ImagePipeline`.

**Begründung:** With MainActor-by-default and NonisolatedNonsendingByDefault, unannotated async helpers run on the main thread and would freeze the UI during PDF rendering or decoding. Swift 6 mode makes every data-race diagnostic an error. Setting these explicitly makes XcodeGen output behave the same as Xcode 26/27 templates.

### E3

**Empfehlung:** Live scan: write `struct ScannerView: UIViewControllerRepresentable` that builds `DataScannerViewController(recognizedDataTypes: [.barcode(symbologies: [.qr, .aztec, .pdf417, .dataMatrix, .code128, .code39, .code93, .ean13, .ean8, .upce, .itf14, .i2of5, .codabar, .gs1DataBar, .gs1DataBarExpanded, .microQR, .microPDF417])], qualityLevel: .accurate, recognizesMultipleItems: false, isHighFrameRateTrackingEnabled: false, isPinchToZoomEnabled: true, isGuidanceEnabled: true, isHighlightingEnabled: true)`. The Coordinator is an `NSObject, DataScannerViewControllerDelegate`, main-actor isolated. Call `startScanning()` after camera access is granted (catch `ScanningUnavailable`) and `stopScanning()` in `dismantleUIViewController(_:coordinator:)`. In `didTapOn` and in `didAdd`/`didUpdate` (after a stability check), map `.barcode(let b)` to `ScannedCode(symbology: b.observation.symbology.rawValue, payload: b.observation.payloadData, text: b.payloadStringValue)`.

**Begründung:** Every API above is verified for iOS 16 and later. RecognizedItem and VNBarcodeObservation are not Sendable, so copy them into a Sendable DTO inside the MainActor delegate call. `.accurate` raises the resolution, which dense Aztec and PDF417 ticket codes need. Show the scanner only when `isSupported && isAvailable`; otherwise open the import UI.

### E4

**Empfehlung:** Still images, screenshots and PDF pages: `@concurrent func detect(cgImage: CGImage, orientation: CGImagePropertyOrientation) async throws -> [ScannedCode]`, which runs `ImageRequestHandler(cgImage, orientation:).perform(DetectBarcodesRequest(.revision4), RecognizeDocumentsRequest())`. Configure `symbologies` explicitly. Read `payloadData` first. If `payloadString` is nil, or doesn't round-trip to the same bytes in UTF-8 or ISO-8859-1, mark the code `isBinary`. Send `payload` to the backend as base64 together with the symbology.

**Begründung:** Deutsche Bahn and UIC 918.3 Aztec codes are binary, and turning them into a String can corrupt them. Only `payloadData` guarantees the bytes. The backend can then encode them for Wallet, for example as an ISO-8859-1 1:1 byte-to-char `message` with `messageEncoding: "iso-8859-1"`; confirm that in the pass-format research.

### E5

**Empfehlung:** PDF import: open with `PDFDocument(url:)` (or from `Data` for share-extension input) and look at pages 0 to min(pageCount, 5) - 1. For each page, take `bounds(for: .mediaBox)`, scale by s = min(300/72, 4096 / max(width, height)), and render with `UIGraphicsImageRenderer(size: scaled, format: fmt)` where `fmt.scale = 1` and `fmt.opaque = true`. Fill white, flip the CTM, and call `page.draw(with: .mediaBox, to: ctx.cgContext)`. If nothing decodes, try again at 2x or by cropping.

**Begründung:** Vector barcodes in PDFs decode better at high resolution, and the pixel cap keeps memory bounded. Share extensions are especially memory-constrained, though the exact limit isn't documented. Apply page rotation (`PDFPage.rotation`) to the transform.

### E6

**Empfehlung:** Field auto-suggestion: on iOS 26+, use `RecognizeDocumentsRequest` with `textRecognitionOptions.recognitionLanguages = [de-DE, en-US]`, take `document.text.detectedData`, and run `transcript.dataDetectorMatches([.calendarEvent, .flightNumber, .moneyAmount, .postalAddress], options:)` with German language code, Germany region and the Europe/Berlin time zone. Map the results to the pass's relevantDate/expirationDate, organizer name (the largest title text) and member number (the text near the barcode). Always ask the user to confirm.

**Begründung:** All of these APIs are verified for iOS 26. The DataDetector Swift API returns typed CalendarEvent start and end dates. NSDataDetector only needs to remain as a legacy fallback, and Apple warns it drops uncertain matches.

### E7

**Empfehlung:** Import entry points: (1) `PhotosPicker(selection:matching: .images)` loading `Data.self`; (2) `.fileImporter(allowedContentTypes: [.pdf, .image])`, copying into the sandbox while security-scoped access is open; (3) a Share Extension (`com.apple.share-services`, SUBQUERY rule for com.adobe.pdf or public.image, at most 1 attachment) that only writes into the App Group inbox `group.<bundle>.qrcode2wallet/Inbox/` plus a small JSON manifest. The main app imports and processes the inbox on `scenePhase == .active`.

**Begründung:** The Share extension can't use App Attest (generateKey fails in extensions) and can't launch its containing app (NSExtensionContext.open is only for Today and iMessage). Keeping the extension thin also keeps it within its memory limits. PhotosPicker needs no photo-library permission.

### E8

**Empfehlung:** Adding passes: download → check the HTTP 200 status and `application/vnd.apple.pkpass` → `let pass = try PKPass(data:)` on the MainActor → if `PKAddPassesViewController.canAddPasses()`, show `AddPassToWalletButton([pass]) { added in … }`, or call `await library.addPasses([pass])` and present PKAddPassesViewController on `.shouldReviewPasses`. Use `library.containsPass(pass)` for UI state. Enable the Wallet capability with the backend's Pass Type ID (`com.apple.developer.pass-type-identifiers`) so you can call `pass(withPassTypeIdentifier:serialNumber:)` and `replacePass(with:)` for in-place edits. Don't use backgroundAddPasses in v1.

**Begründung:** Adding needs no entitlement, but replacing, reading or removing our own passes does. Our passes are signed with our team's Pass Type ID, so the entitlement covers them. The user should see each pass generated from a third-party ticket before it goes into Wallet.

### E9

**Empfehlung:** Persistence: SwiftData `@Model PassRecord` with `#Unique` on serialNumber and `@Attribute(.externalStorage)` for payload, pkpassData and the source image. Use the default store, not the App Group store, because only the main app writes. Background imports go through a `@ModelActor actor PassStore`, and only `PersistentIdentifier` crosses actors.

**Begründung:** This uses the verified iOS 17/18 APIs and avoids two processes writing to one SwiftData store. The Share extension uses a file inbox instead. ModelContext is not Sendable.

### E10

**Empfehlung:** Networking and attestation: `struct APIClient: Sendable` using `URLSession.shared`. Use `upload(for:from:)` for the JSON (ScannedCode DTO plus pass metadata) and get back either the .pkpass bytes or a pass URL fetched with `data(for:)`. An `actor AttestationManager` stores the keyId in the Keychain, attests once per install and user, and adds an assertion header (base64) on each `/passes` POST, signing SHA256 of the request body plus the server challenge. When `isSupported == false` (Simulator, Mac), the server falls back to stricter rate limits.

**Begründung:** Every App Attest async API is iOS 14 and verified. Keys don't survive reinstall or restore, so handle `invalidKey` by re-attesting. On `serverUnavailable`, retry with the same key and hash.

### E11

**Empfehlung:** Starting project.yml for XcodeGen 2.46: `name: QRCode2Wallet`; `options: {bundleIdPrefix: de.example, deploymentTarget: {iOS: "26.0"}, minimumXcodeGenVersion: "2.46.0", createIntermediateGroups: true}`; `settings: {base: {SWIFT_VERSION: "6.0", SWIFT_DEFAULT_ACTOR_ISOLATION: MainActor, SWIFT_APPROACHABLE_CONCURRENCY: YES, DEVELOPMENT_TEAM: <TEAMID>, CODE_SIGN_STYLE: Automatic, MARKETING_VERSION: "1.0.0", CURRENT_PROJECT_VERSION: "1"}}`. Targets: (1) `QRCode2Wallet: {type: application, platform: iOS, sources: [App], info: {path: App/Info.plist, properties: {CFBundleDisplayName: QRCode2Wallet, UILaunchScreen: {}, NSCameraUsageDescription: "QRCode2Wallet nutzt die Kamera, um Barcodes und QR-Codes von Tickets und Kundenkarten zu scannen."}}, entitlements: {path: App/QRCode2Wallet.entitlements, properties: {com.apple.security.application-groups: [group.de.example.qrcode2wallet], com.apple.developer.devicecheck.appattest-environment: development, com.apple.developer.pass-type-identifiers: ["$(TeamIdentifierPrefix)pass.de.example.qrcode2wallet"]}}, dependencies: [{target: ShareExtension}], scheme: {testTargets: [QRCode2WalletTests], gatherCoverageData: true}}`. (2) `ShareExtension: {type: app-extension, platform: iOS, sources: [ShareExtension], info: {path: ShareExtension/Info.plist, properties: {CFBundleDisplayName: QRCode2Wallet, NSExtension: {NSExtensionPointIdentifier: com.apple.share-services, NSExtensionPrincipalClass: "$(PRODUCT_MODULE_NAME).ShareViewController", NSExtensionAttributes: {NSExtensionActivationRule: "SUBQUERY (extensionItems, $extensionItem, SUBQUERY ($extensionItem.attachments, $attachment, ANY $attachment.registeredTypeIdentifiers UTI-CONFORMS-TO \"com.adobe.pdf\" || ANY $attachment.registeredTypeIdentifiers UTI-CONFORMS-TO \"public.image\").@count == $extensionItem.attachments.@count).@count == 1"}}}}, entitlements: {path: ShareExtension/ShareExtension.entitlements, properties: {com.apple.security.application-groups: [group.de.example.qrcode2wallet]}}}`. (3) `QRCode2WalletTests: {type: bundle.unit-test, platform: iOS, sources: [Tests], dependencies: [{target: QRCode2Wallet}]}`.

**Begründung:** Every key used here is documented in ProjectSpec.md: options, settings.base, info, entitlements, dependencies, scheme.testTargets and bundle.unit-test with an automatic TEST_HOST. App extensions embed by default because the dependency sits on an application target. The `$(TeamIdentifierPrefix)pass.…` value format and the `$(PRODUCT_MODULE_NAME).Class` principal-class pattern are common practice but I couldn't verify them in this research; confirm both by enabling the capability in Xcode once and diffing the result. Capabilities must also be enabled on the App IDs in the developer portal.

## Fallstricke

1. The task's 'iOS 26 / Xcode 26' baseline is out of date: Apple docs and the Xcode support page show Xcode 27, iOS 27 SDK and Swift 6.4 as current (27.1 RC and 27.2 beta are already listed). Docs carry iOS 27-only symbols such as `PKPassLibrary.addPasses(data:)` and `PKAddPassesViewController(passesData:)`, so guard them.
2. Raw bytes: `payloadStringValue` / `payloadString` can be nil or lossy for binary codes such as UIC 918.3 Aztec. `CIBarcodeDescriptor.errorCorrectedPayload` is NOT the decoded payload: it is codewords (Aztec includes stuffed bits, PDF417 uses 16-bit codewords). Use `payloadData` (iOS 17+) only.
3. Naming differs between APIs: VN `payloadStringValue` vs Swift `payloadString`; `coalesceCompositeSymbologies` (VN and RecognizeDocumentsRequest options) vs `coalescesCompositeSymbologies` (DetectBarcodesRequest); `automaticallyDetectsLanguage`/`usesLanguageCorrection` (RecognizeTextRequest) vs `automaticallyDetectLanguage`/`useLanguageCorrection` (RecognizeDocumentsRequest). Swift `BarcodeObservation` has no `barcodeDescriptor`.
4. Deprecated APIs to avoid: `VNDetectBarcodesRequest.supportedSymbologies` (class var, since iOS 15; use the throwing instance method), `VNDetectBarcodesRequestRevision1` and `Revision2` (Revision2 deprecated in iOS 18), `VNRecognizeTextRequestRevision1`/`Revision2`, the capitalized `VNBarcodeSymbology` constants (`.QR`, `.Aztec`, `.PDF417`, …), `PKPass.relevantDate` (use `relevantDates`), and `PKPass.paymentPass`.
5. With `SWIFT_APPROACHABLE_CONCURRENCY` (NonisolatedNonsendingByDefault) plus MainActor default isolation, any unannotated `async` helper runs on the caller's actor, often the main thread. PDF rasterization and VN\* `perform` are synchronous and CPU-heavy, so mark them `@concurrent`.
6. `VNImageRequestHandler`, `VNRequest`, `VNBarcodeObservation`, `RecognizedItem`, `PKPass` and `PKPassLibrary` are not Sendable. Don't keep them in actors or `Task.detached` closures; extract Data and Strings first. `PKPassLibrary` is documented as not thread-safe.
7. `DataScannerViewController` and its delegate are `@MainActor`. Its availability properties are `@MainActor class var`s, so reading them from a nonisolated context fails to compile under Swift 6.
8. `isSupported` only reflects hardware (A12+, false on visionOS); `isAvailable` reflects camera permission and restrictions. Check both. The Simulator has no camera, so expect it to be unsupported there (not explicitly documented) and test on a real device.
9. Wallet can't render every symbology Vision decodes. iOS 27 added Code39, Codabar, EAN13 and I2of5 to QR, PDF417, Aztec and Code128, but Data Matrix, EAN-8, UPC-E, ITF-14, Code 93, GS1 DataBar, microQR and microPDF417 aren't supported. On iOS 26 devices EAN-13 can't render natively, which requires the iOS 27 fallback array. A POS scanner may reject a re-encoded symbology (for example EAN-13 shown as Code128 or QR).
10. `PKPassLibrary.isPassLibraryAvailable()` does not mean passes can be added; use `PKAddPassesViewController.canAddPasses()`. `passes()` and `replacePass(with:)` silently return only entitled passes or false without the Wallet entitlement. `addPasses` can return `.shouldReviewPasses`, and then you MUST present `PKAddPassesViewController`.
11. Share extensions can't use App Attest (`generateKey` fails) and can't open their containing app (`NSExtensionContext.open` works only for Today and iMessage). Any App Store build whose extension contains `TRUEPREDICATE` is rejected.
12. App Attest keys don't survive reinstall, device migration or backup restore, and `isSupported` is false on Macs, including iOS apps on Apple silicon. The server must not hard-fail those clients. Apple asks apps with millions of DAU to ramp up `attestKey` usage gradually.
13. `.fileImporter` URLs are security-scoped, so reading without `startAccessingSecurityScopedResource()` fails. `PDFDocument.page(at:)` raises (an Objective-C exception, which crashes) when the index is out of bounds.
14. Photo orientation: images from PhotosPicker or the camera carry EXIF orientation. Pass the correct `CGImagePropertyOrientation` to `ImageRequestHandler` or `perform(on:orientation:)`, or rotated or small codes may fail to decode.
15. SwiftData across processes: if both the extension and the app open one store in the App Group container, you take on cross-process write coordination. A file inbox avoids that. Don't pass `@Model` instances across actors (ModelContext isn't Sendable), even though the current SDK's macro declaration lists Sendable; use `PersistentIdentifier`.
16. XcodeGen doesn't apply Xcode's new-project template defaults (such as MainActor isolation) and has no capability abstraction. Its `projectFormat` enum stops at `xcode16_3`. Entitlements in project.yml must match the App ID capabilities in the developer portal, or automatic signing fails.
17. PhotosPicker's SwiftUI `Image` Transferable supports only PNG and JPEG; HEIC loses data. Load `Data.self` instead.

## Offene Fragen

1. Does `payloadData` return the exact decoded application bytes for binary Aztec codes (UIC 918.3 / DB tickets, which reportedly start with ASCII '#UT'), including ECI and byte-mode segments? Apple documents it only as 'raw data representation of the barcode's payload'. Test on a device with real DB, ÖBB and SBB tickets and compare against a reference decoder such as ZXing.
2. Is a scan from a PDF render or screenshot reliable enough for dense Aztec and PDF417 codes compared with live scanning? Pick the render DPI and pixel cap from device tests on low-memory devices (iPhone SE 2nd gen, iPhone 11). Also measure the Share Extension's memory ceiling, which isn't documented.
3. Which encoding should the backend use for binary payloads in `barcodes[].message` (ISO-8859-1 1:1 mapping vs others), and does Wallet re-render them byte-identically for Aztec, PDF417 and QR? This belongs to the pass-format research but decides what the client sends.
4. Exact Info.plist and entitlement value formats generated by Xcode 27 for the Wallet capability (`$(TeamIdentifierPrefix)pass.…`) and for the Share extension principal class. Enable each once in Xcode and diff the result to confirm the project.yml values.
5. Product and legal question: App Review position on an app that re-issues third-party tickets and loyalty cards as passes signed under our own Pass Type ID (guidelines 5.2 intellectual property and 4.1 copycats). Also, should we use `backgroundAddPasses` at all, given that each pass comes from user-supplied content?
6. Apple's docs contradict each other on whether App Attest works in Action extensions. The integrity article says yes; the isSupported page says only watchOS extensions. If an Action extension is ever considered instead of a Share extension, verify on a device.
7. Does `DataScannerViewController.RecognizedDataType.barcode()` with the default empty symbology array mean 'all supported symbologies'? Apple's sample uses it that way, but I didn't find it stated explicitly. Pass an explicit list to be safe.
8. Is Approachable Concurrency on by default in Xcode 27 new-project templates? Only secondary sources cover Xcode 26 and they disagree. This doesn't matter if project.yml sets both settings explicitly.

## Faktencheck: alle geprüften Aussagen

### P1 · BESTÄTIGT

**Geprüfte Aussage:** Toolchain: Xcode 27 ships Swift 6.4 and the iOS 27 SDK, supports deployment targets iOS 15 to 27, needs macOS Tahoe 26.6 or later, and installs and runs only on Apple-silicon Macs. Xcode 26 ships Swift 6.2 and the iOS 26 SDK. The release-notes index lists Xcode 27.1 RC and 27.2 beta 2.

**Ergebnis:** All parts check out. The Xcode 27 notes say: 'Xcode 27 includes Swift 6.4 and SDKs for iOS 27 ... requires a Mac running macOS Tahoe 26.6 or later' and, under Intel Deprecation, 'Xcode 27 will only install and run on Apple silicon Macs.' The support table lists Xcode 27 with iOS 15–27 deployment targets and Swift 6.4 (language modes 6, 5, 4.2, 4), and Xcode 26 with Swift 6.2. The index shows 'Xcode 27.2 Beta 2' and 'Xcode 27.1 RC'. One addition: Xcode 27 supports on-device debugging only on iOS 17 and later, even though it can build for an iOS 15 target. Xcode 26.4–26.6 ship Swift 6.3, not 6.2. Cross-check: https://developer.apple.com/support/xcode/

**Quelle:** <https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes>

### P2 · BESTÄTIGT

**Geprüfte Aussage:** Since April 28, 2026, every App Store Connect upload must be built with Xcode 26 or later against the iOS 26 SDK or newer. The rule is about the build SDK, not the deployment target.

**Ergebnis:** Exact text: 'Apps uploaded to App Store Connect must be built with Xcode 26 or later using an SDK for iOS 26, iPadOS 26, tvOS 26, visionOS 26, or watchOS 26.' A separate rule ('Since September 9, 2026') says apps 'must target iOS 13 or later', which shows that SDK and deployment target are handled separately. The page does not yet announce an Xcode 27 or iOS 27 SDK minimum.

**Quelle:** <https://developer.apple.com/news/upcoming-requirements/>

### P3 · BESTÄTIGT

**Geprüfte Aussage:** App Store usage measured June 7, 2026: 79% of all iPhones and 86% of iPhones introduced in the last four years run iOS 26.

**Ergebnis:** Correct, with one precision: the figures are measured 'by devices that transacted on the App Store on June 7, 2026', not across all iPhones. The same page gives iPad figures of 68% (all) and 79% (last four years) on iPadOS 26. These numbers predate the iOS 27 release.

**Quelle:** <https://developer.apple.com/support/app-store/>

### P4 · NICHT VERIFIZIERBAR

**Geprüfte Aussage:** iOS 27 supports the same iPhones as iOS 26 (iPhone 11 and later, iPhone SE 2nd generation and later), all with an A13 or newer chip.

**Ergebnis:** I could not reach apple.com or support.apple.com from this environment. Several secondary outlets (AppleInsider, iClarified, 9to5Mac, Appleosophy) say Apple's list is 'iPhone 11 and later, including iPhone SE (2nd generation and later)' and that no models were dropped. Both iPhone 11 and SE 2 use the A13. Treat this as likely, but confirm on support.apple.com before relying on it.

**Quelle:** <https://appleinsider.com/articles/26/06/08/ios-27-keeps-iphone-11-and-newer-compatibility>

### P5 · BESTÄTIGT

**Geprüfte Aussage:** VisionKit DataScannerViewController: iOS 16.0, '@MainActor @objc class', inherits UIViewController, 7-parameter init (plus the init(recognizedDataTypes:)-only call in Apple's sample), members startScanning/stopScanning/isScanning/recognizedItems/capturePhoto/regionOfInterest/overlayContainerView/zoom/supportedTextRecognitionLanguages, QualityLevel .fast/.balanced/.accurate, nothing deprecated.

**Ergebnis:** Everything matches, and nothing is deprecated. One precision: the initializer has default values, which is why the sample can pass only recognizedDataTypes. Full signature: '@MainActor init(recognizedDataTypes: Set&lt;RecognizedDataType&gt;, qualityLevel: QualityLevel = .balanced, recognizesMultipleItems: Bool = false, isHighFrameRateTrackingEnabled: Bool = true, isPinchToZoomEnabled: Bool = true, isGuidanceEnabled: Bool = true, isHighlightingEnabled: Bool = false)'. Note that isHighlightingEnabled defaults to false. The class is also available on visionOS 1.0 and declared for Mac Catalyst. QualityLevel 'mostly impact[s] the camera resolution'; Apple says to use .accurate for smaller items.

**Quelle:** <https://developer.apple.com/documentation/visionkit/datascannerviewcontroller/init(recognizeddatatypes:qualitylevel:recognizesmultipleitems:ishighframeratetrackingenabled:ispinchtozoomenabled:isguidanceenabled:ishighlightingenabled:)>

### P6 · KORRIGIERT

**Geprüfte Aussage:** isSupported (@MainActor class var) needs A12 Bionic or later and is false in visionOS. isAvailable is true only when the person has granted camera access and no restriction blocks it. startScanning() can throw ScanningUnavailable (.unsupported, .cameraRestricted). UIRequiredDeviceCapabilities can include 'iphone-ipad-minimum-performance-a12'.

**Ergebnis:** The isSupported details (A12, false in visionOS, the a12 capability subkey) and the two ScanningUnavailable cases are correct. ScanningUnavailable conforms to Error and Sendable. Two corrections. (1) Apple's camera-scanning article says isAvailable is true 'If the user doesn't deny your app access to the camera, or there's no other restrictions', so it is also true before the permission prompt (not determined), not only after access is granted. The prompt appears on first camera use, and a denial arrives through dataScanner(_:becameUnavailableWithError:). (2) The startScanning() page shows only '@MainActor func startScanning() throws' and does not document which error is thrown. ScanningUnavailable is documented only as the parameter type of becameUnavailableWithError, so catch any Error, not just ScanningUnavailable.

**Quelle:** <https://developer.apple.com/documentation/visionkit/scanning-data-with-the-camera>

### P7 · BESTÄTIGT

**Geprüfte Aussage:** NSCameraUsageDescription is required (runtime error without it). Don't Allow at first prompt triggers dataScanner(_:becameUnavailableWithError:). Apple's article example uses .text(languages: ["en-US", "fr-FR", "de-DE"]).

**Ergebnis:** Article quotes: 'If you don't add this key, a runtime error occurs when you access the camera' and 'the scanner calls this method when users tap Don't Allow the first time the system prompt appears'. The example is exactly .text(languages: ["en-US", "fr-FR", "de-DE"]). In the design note, AVCaptureDevice.authorizationStatus(for:) and requestAccess(for:) async -&gt; Bool are both iOS 7.0, also confirmed.

**Quelle:** <https://developer.apple.com/documentation/visionkit/scanning-data-with-the-camera>

### P8 · BESTÄTIGT

**Geprüfte Aussage:** RecognizedDataType.barcode(symbologies: [VNBarcodeSymbology] = []) and .text(languages:textContentType:) are iOS 16. DataScannerViewControllerDelegate is '@MainActor protocol ... : AnyObject' with didTapOn, didAdd, didUpdate, didRemove, dataScannerDidZoom and becameUnavailableWithError.

**Ergebnis:** Correct. Both text parameters also have defaults: 'static func text(languages: [String] = [], textContentType: DataScannerViewController.TextContentType? = nil)'. The error parameter of becameUnavailableWithError is typed 'DataScannerViewController.ScanningUnavailable'.

**Quelle:** <https://developer.apple.com/documentation/visionkit/datascannerviewcontrollerdelegate>

### P9 · BESTÄTIGT

**Geprüfte Aussage:** RecognizedItem (iOS 16) is an enum with .barcode(RecognizedItem.Barcode) and .text(RecognizedItem.Text). Barcode has payloadStringValue: String?, bounds, id: UUID and observation: VNBarcodeObservation. All three types conform only to Identifiable (not Sendable).

**Ergebnis:** Correct. The relationships sections list only 'Identifiable' for RecognizedItem, RecognizedItem.Barcode and RecognizedItem.Text. bounds is of type RecognizedItem.Bounds, and Text.observation is a VNRecognizedTextObservation.

**Quelle:** <https://developer.apple.com/documentation/visionkit/recognizeditem/barcode>

### P10 · BESTÄTIGT

**Geprüfte Aussage:** VNDetectBarcodesRequest is iOS 11. Instance method supportedSymbologies() throws (iOS 15); class property deprecated since iOS 15. Revision1 deprecated; Revision2 deprecated in iOS 18 and renamed to Revision3; Revision3 iOS 16; Revision4 iOS 17. Members symbologies, coalesceCompositeSymbologies, results: [VNBarcodeObservation]?.

**Ergebnis:** Correct. Details: Revision1 was introduced in iOS 12 and deprecated in iOS 17 ('Use VNDetectBarcodesRequestRevision3 instead'). Revision2 was introduced in iOS 15, deprecated in iOS 18, and carries the metadata renamed: VNDetectBarcodesRequestRevision3. The class property supportedSymbologies was deprecated in iOS 15 ('Use supportedSymbologies() instead').

**Quelle:** <https://developer.apple.com/documentation/vision/vndetectbarcodesrequest>

### P11 · BESTÄTIGT

**Geprüfte Aussage:** VNBarcodeSymbology lower-case constants (aztec ... upce, 24 listed); upper-case versions deprecated; codabar and microQR iOS 15; the type is Sendable.

**Ergebnis:** The list matches the 'Supported Symbologies' topic exactly, there are 17 deprecated (upper-case) symbols, and the type conforms to Equatable, Hashable, RawRepresentable and Sendable (init(rawValue: String)). Additional detail: msiPlessey is iOS 17. Caveat on the design impact: Apple Wallet renders only a subset of these symbologies (see missing facts), so a Vision-to-Wallet mapping must handle unsupported formats.

**Quelle:** <https://developer.apple.com/documentation/vision/vnbarcodesymbology>

### P12 · BESTÄTIGT

**Geprüfte Aussage:** VNBarcodeObservation has payloadStringValue (iOS 11; string may not be available depending on symbology or payload), payloadData: Data? (iOS 17), supplementalPayloadString, supplementalPayloadData, supplementalCompositeType, isGS1DataCarrier (iOS 17), isColorInverted, symbology, barcodeDescriptor: CIBarcodeDescriptor? (iOS 11).

**Ergebnis:** Correct. payloadData's abstract reads 'The raw data representation of the barcode's payload' (iOS 17.0). isColorInverted and supplementalCompositeType are also iOS 17. barcodeDescriptor's discussion says to 'Use this object to have Core Image regenerate the observed barcode.' The class conforms to NSSecureCoding and NSCopying, not Sendable.

**Quelle:** <https://developer.apple.com/documentation/vision/vnbarcodeobservation>

### P13 · KORRIGIERT

**Geprüfte Aussage:** CIBarcodeDescriptor subclasses (QR, Aztec, PDF417, DataMatrix) expose errorCorrectedPayload as codewords, not decoded bytes (with the per-symbology details given). Extra properties: symbolVersion, maskPattern, errorCorrectionLevel, isCompact, layerCount, dataCodewordCount, rowCount, columnCount.

**Ergebnis:** The codeword semantics are correct. QR: 8-bit codewords from ISO/IEC 18004 §6.4.10. Aztec: 6/8/10/12-bit codewords from ISO/IEC 24778 §7.3.1.2, where 'Clients will need to remove these extra bits'. PDF417: 16-bit codewords 0…928, where the first codeword is a count that includes itself and padding. DataMatrix: 'de-interleaved bits ... at the end of Step 1: Data encodation'. The property list is incomplete: CIDataMatrixCodeDescriptor also has 'eccVersion: CIDataMatrixCodeDescriptor.ECCVersion'. Per class: QR has symbolVersion, maskPattern and errorCorrectionLevel; Aztec has isCompact, layerCount and dataCodewordCount; PDF417 has isCompact, rowCount and columnCount; DataMatrix has rowCount, columnCount and eccVersion.

**Quelle:** <https://developer.apple.com/documentation/coreimage/cidatamatrixcodedescriptor>

### P14 · BESTÄTIGT

**Geprüfte Aussage:** Swift Vision DetectBarcodesRequest (struct, Sendable) is iOS 18.0. It has init(_ revision: Revision?) (only .revision4), symbologies, supportedSymbologies (potentially expensive), coalescesCompositeSymbologies, and perform(on: CGImage|URL|Data|CVPixelBuffer|CMSampleBuffer|CIImage, orientation:) async throws. BarcodeSymbology is CaseIterable, Codable, Sendable with the same case names.

**Ergebnis:** Correct. Precision: the initializer is 'init(_ revision: DetectBarcodesRequest.Revision? = nil)', so DetectBarcodesRequest() compiles. The orientation parameter of perform defaults to nil. BarcodeSymbology has 24 cases matching VNBarcodeSymbology. The API is now also on watchOS 27 (not relevant here).

**Quelle:** <https://developer.apple.com/documentation/vision/detectbarcodesrequest>

### P15 · BESTÄTIGT

**Geprüfte Aussage:** BarcodeObservation (iOS 18, Sendable, Codable) has payloadString, payloadData: Data?, supplementalPayloadString/Data, supplementalCompositeType, symbology: BarcodeSymbology, isGS1DataCarrier, isColorInverted, boundingRegion, plus init(_ observation: VNBarcodeObservation). It has no barcodeDescriptor.

**Ergebnis:** Correct. Precision: 'supplementalCompositeType: BarcodeObservation.CompositeType?' is optional, and boundingRegion is a NormalizedRegion. The documented conformances are Codable (Decodable and Encodable), Sendable, Hashable and VisionObservation.

**Quelle:** <https://developer.apple.com/documentation/vision/barcodeobservation>

### P16 · BESTÄTIGT

**Geprüfte Aussage:** ImageRequestHandler (iOS 18) is a final, Sendable class with inits for CGImage, URL, Data, CIImage, CVPixelBuffer and CMSampleBuffer (orientation:), perform&lt;each T&gt;(repeat each T) async throws -&gt; (repeat (each T).Result), and performAll(_:). VNImageRequestHandler.perform(_:) is synchronous and returns after all requests finish. Neither VNImageRequestHandler nor VNRequest is Sendable.

**Ergebnis:** Correct. There are also CVPixelBuffer and CMSampleBuffer inits with depthData:. performAll returns 'some AsyncSequence&lt;VisionResult, Never&gt;'. VNImageRequestHandler.perform discussion: 'The function returns after all requests have either completed or failed.' VNImageRequestHandler and VNRequest list no Sendable conformance.

**Quelle:** <https://developer.apple.com/documentation/vision/imagerequesthandler>

### P17 · BESTÄTIGT

**Geprüfte Aussage:** RecognizeTextRequest (iOS 18, Sendable) has recognitionLanguages: [Locale.Language], supportedRecognitionLanguages, automaticallyDetectsLanguage, usesLanguageCorrection, customWords, minimumTextHeightFraction and recognitionLevel (.accurate/.fast). The only revision is .revision3. It returns RecognizedTextObservation (transcript, topCandidates(_:), boundingRegion, recognitionLanguages). VNRecognizeTextRequest is iOS 13 with [String] languages and supportedRecognitionLanguages() throws; Revision3 is iOS 16; Revisions 1 and 2 are deprecated.

**Ergebnis:** All confirmed. RecognizedTextObservation also has isTitle, shouldWrapToNextLine and textDirection. Neither page lists the German language, so check supportedRecognitionLanguages at runtime as the researcher suggests.

**Quelle:** <https://developer.apple.com/documentation/vision/recognizetextrequest>

### P18 · BESTÄTIGT

**Geprüfte Aussage:** RecognizeDocumentsRequest (iOS 26.0) returns DocumentObservation. document: Container has text, paragraphs, title, tables, lists and barcodes: [BarcodeObservation]. Text has transcript, lines, words and detectedData: [DataDetectorMatch] (match: DataDetector.Match). Options: barcodeDetectionOptions (enabled, symbologies, coalesceCompositeSymbologies) and textRecognitionOptions (recognitionLanguages, automaticallyDetectLanguage, useLanguageCorrection, customWords, maximumCandidateCount, minimumTextHeightFraction).

**Ergebnis:** Correct, including the naming differences (automaticallyDetectLanguage, useLanguageCorrection, coalesceCompositeSymbologies). Precision: the request produces an array of DocumentObservation. Container.title is optional, Text.words is optional ([RecognizedTextObservation]?), and there is no recognitionLevel option. The request also exposes supportedBarcodeSymbologies and supportedRecognitionLanguages.

**Quelle:** <https://developer.apple.com/documentation/vision/recognizedocumentsrequest>

### P19 · BESTÄTIGT

**Geprüfte Aussage:** Swift DataDetection is iOS 26.0: StringProtocol.dataDetectorMatches(_ types: MatchType = .all, options: Options = .init()) -&gt; some AsyncSequence&lt;DataDetector.Match, Never&gt;. Match types and CalendarEvent fields as listed. Options: documentDate/LanguageCode/Region/TimeZone. Apple warns that NSDataDetector drops uncertain matches and must not be used for validation.

**Ergebnis:** Correct (needs 'import DataDetection'). Apple adds three caveats. (1) Options 'are only hints'; set documentLanguageCode and documentRegion 'only if you know ... with a high degree of confidence'. Their types are Locale.LanguageCode? and Locale.Region?. German date parsing is therefore not guaranteed. (2) The new API also comes with 'Don't use this functionality to validate form inputs'. (3) 'This API can be resource intensive ... avoid blocking the main thread', so with MainActor-default isolation call it from a @concurrent function. NSDataDetector quote: 'NSDataDetector discards potential matches in case of uncertainty.'

**Quelle:** <https://developer.apple.com/documentation/swift/stringprotocol/datadetectormatches(_:options:)>

### P20 · KORRIGIERT

**Geprüfte Aussage:** PhotosPicker (iOS 16) is '@MainActor @preconcurrency struct' with single- and multi-selection inits. PhotosPickerItem is Sendable and Transferable with loadTransferable(type:) async throws -&gt; sending T?. SwiftUI Image loads only PNG and JPEG through Transferable. The picker is out of process, so no photo-library authorization is needed.

**Ergebnis:** Mostly correct: the declaration, the inits, 'func loadTransferable&lt;T&gt;(type: T.Type) async throws -&gt; sending T? where T : Transferable', the PNG/JPEG-only note for Image, and Data conforming to Transferable. The PhotoKit privacy article confirms that PHPickerViewController 'manages its life cycle in a separate process ... doesn't need to explicitly authorize'. Correction: PhotosPickerItem's documented conformances are only Equatable, Hashable and Sendable. Transferable is not in its relationships list, even though the overview text says it 'conforms to Transferable'. Treat it as an item that loads Transferable types, not as a Transferable value.

**Quelle:** <https://developer.apple.com/documentation/photosui/photospickeritem>

### P21 · BESTÄTIGT

**Geprüfte Aussage:** SwiftUI .fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:) is iOS 14 and returns Result&lt;[URL], Error&gt;. URLs are security-scoped and need start/stopAccessingSecurityScopedResource().

**Ergebnis:** Correct. The documentation adds that if the user cancels, onCompletion is not called and isPresented is set to false.

**Quelle:** <https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:allowsmultipleselection:oncompletion:)>

### P22 · BESTÄTIGT

**Geprüfte Aussage:** PDFKit: PDFDocument(url:) and (data:) are failable; pageCount; page(at:) is zero-based and raises an exception out of bounds; bounds(for: .mediaBox) is in page space, so rotation may need a transform; thumbnail(of:for:) -&gt; UIImage and draw(with:to:) are iOS 11; UIGraphicsImageRendererFormat scale and opaque.

**Ergebnis:** Correct. page(at:) returns PDFPage? and 'raises an exception if index is out of bounds'. bounds(for:) says 'coordinates ... are in page space ... transform the points if the page has a rotation', and the result is intersected with the media box. PDFPage.rotation must be a multiple of 90. PDFDocument and PDFPage are not Sendable.

**Quelle:** <https://developer.apple.com/documentation/pdfkit/pdfpage/bounds(for:)>

### P23 · BESTÄTIGT

**Geprüfte Aussage:** Share Extension: NSExtensionPointIdentifier com.apple.share-services; NSExtensionActivationRule is a dictionary or a SUBQUERY predicate string (single-PDF example given). App Review rejects any extension containing TRUEPREDICATE.

**Ergebnis:** Correct. Archive quote: 'If any app extensions in your containing app include the string TRUEPREDICATE, the app will be rejected.' com.apple.share-services is in the current list of NSExtensionPointIdentifier values, and the dictionary keys exist (plus NSExtensionActivationSupportsMovieWithMaxCount, ...Text and ...WebPageWithMaxCount). Note: Apple's sample predicate counts extension items whose attachments all conform. It does not limit the number of attachments, so add '$extensionItem.attachments.@count == 1' if you need exactly one file.

**Quelle:** <https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/ExtensionScenarios.html>

### P24 · BESTÄTIGT

**Geprüfte Aussage:** An extension and its containing app can't reach each other's containers and need an App Group (com.apple.security.application-groups, UserDefaults(suiteName:)). On iOS, NSExtensionContext.open(_:) is supported only by the Today and iMessage extension points, so a Share extension cannot officially open its app. NSItemProvider loadFileRepresentation(for:openInPlace:) and loadDataRepresentation(for:) are iOS 16 with @Sendable handlers.

**Ergebnis:** Correct. open(_:) doc: 'In iOS, the Today and iMessage app extension points support this method.' Both NSItemProvider methods are iOS 16 with '@escaping @Sendable' handlers, and openInPlace defaults to false. Important addition: the temporary file from loadFileRepresentation is deleted when the completion handler returns ('which the system deletes when the completion handler returns', per the legacy variant's docs). Copy it into the App Group inbox synchronously inside the handler.

**Quelle:** <https://developer.apple.com/documentation/foundation/nsextensioncontext/open(_:completionhandler:)>

### P25 · BESTÄTIGT

**Geprüfte Aussage:** PKPass.init(data: Data) throws expects a signed pass. invalidSignature and invalidDataError are thrown; other codes are unsupportedVersionError, notEntitledError and unknownError. PKPass is not Sendable.

**Ergebnis:** Correct. PKPassKitError.Code has exactly these five cases. PKPass lists no Sendable conformance. Related: PKPass.relevantDate was deprecated in iOS 18 ('Use relevantDates', type [PKPassRelevantDate]). On iOS 27 you can skip building a PKPass and add raw Data directly (see missing facts).

**Quelle:** <https://developer.apple.com/documentation/passkit/pkpass/init(data:)>

## Vom Faktenprüfer ergänzte wichtige Fakten

1. Possible blocker – App Review Guideline 1.5 (guidelines last updated June 8, 2026): 'ensure that Wallet passes include valid contact information from the issuer and are signed with a dedicated certificate assigned to the brand or trademark owner of the pass.' QRCode2Wallet would sign passes for third parties (Deutsche Bahn, airlines, gyms, retailers) with its own Pass Type ID. Guideline 3.2.1(iv) adds: 'Wallet passes can be used to make or receive payments, transmit offers, or offer identification (such as movie tickets, coupons, and VIP credentials). Other uses may result in the rejection of the app and the revocation of Wallet credentials.' Guideline 5.2.1 forbids using third-party trademarks without permission. Design impact: default to neutral, user-authored passes (no copied third-party logos or brand names; organizationName and contact info refer to QRCode2Wallet and the user), disclose clearly that the pass is not from the issuer, and get an App Review or legal opinion before building the backend. Source: https://developer.apple.com/app-store/review/guidelines/
2. Wallet barcode formats changed in iOS 27. pass.json 'format' now allows PKBarcodeFormatQR, PDF417, Aztec, Code128, Code39, Codabar, EAN13 and I2of5. Before iOS 27 only QR, PDF417, Aztec and Code128 render. Also new in iOS 27: the 'barcodes' array can hold several barcodes as fallbacks ('if you provide EAN 13 and QR formats ... the EAN 13 barcode renders on devices using iOS 27 and later and the QR code renders for devices using pre iOS 27'). Wallet cannot reproduce DataMatrix, EAN-8, UPC-E, Code 93, ITF-14, GS1 DataBar, MicroQR or MicroPDF417 scans in their original symbology, so the app must warn users that a till or turnstile scanner may not accept a substitute. For a deployment target of iOS 26, EAN-13 loyalty cards need a fallback barcode entry. Source: https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary
3. The researcher's persistence recommendation rests on a wrong assumption. SwiftData ModelConfiguration defaults to 'groupContainer: ModelConfiguration.GroupContainer = .automatic', which 'Tells SwiftData to use the app's primary group container as the root location for the persistent storage.' Because the app has the App Groups entitlement (for the share extension), the 'default store' will be created inside the App Group container. To keep it private, pass 'groupContainer: .none' explicitly, and decide this before the first release, because moving the store later needs a migration. Source: https://developer.apple.com/documentation/swiftdata/modelconfiguration/init(_:schema:isstoredinmemoryonly:allowssave:groupcontainer:cloudkitdatabase:)
4. New PassKit APIs in iOS 27 (put behind if #available(iOS 27, \*)): PKPassLibrary.addPasses(data: [Data]) async -&gt; PKPassLibraryAddPassesStatus, addPasses(fromArchiveData:) and addPasses(fromArchiveAt:) for .pkpasses bundles, and PKAddPassesViewController init?(passesData:), init?(passesArchiveData:) and init?(passesArchiveAt:). These add passes straight from downloaded bytes without building a PKPass first. New in iOS 26: PKPassLibrary.Capability.backgroundAddPasses (currently the only capability), requestAuthorization(for:) async -&gt; AuthorizationStatus and authorizationStatus(for:). If the user grants backgroundAddPasses, addPasses adds silently. Sources: https://developer.apple.com/documentation/passkit/pkpasslibrary/addpasses(data:completion:) , https://developer.apple.com/documentation/passkit/pkpasslibrary/capability
5. 'PKPassLibrary isn't thread-safe. Use instances of this class only on a single thread.' Keep it MainActor-confined. containsPass(_:) works without entitlements. passes() returns only passes the app is entitled to. replacePass(with:) fails unless a pass with the same passTypeIdentifier and serialNumber already exists. The pass-type-identifiers entitlement doc documents '$(TeamIdentifierPrefix)\*' (all of the team's passes), which supports the '$(TeamIdentifierPrefix)pass.…' value format. Sources: https://developer.apple.com/documentation/passkit/pkpasslibrary , https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.pass-type-identifiers
6. iOS 27 SDK build-time requirements (release notes). (a) Apps built with the 27.0 SDK must include a launch screen key (UILaunchStoryboardName, UILaunchStoryboards, UILaunchScreen or UILaunchScreens) 'or are rejected when the App Store begins accepting apps built with the 27.0 SDK'. (b) 'Apps built with the latest SDK must adopt the scene-based life cycle or they fail to launch' (a SwiftUI App is fine). (c) canOpenURL: is deprecated. Source: https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes
7. The iOS 27 release notes support the @concurrent recommendation. SwiftUI moved DocumentReader and DocumentWriter requirements to @concurrent because 'With approachable-concurrency defaults that infer MainActor isolation, an unannotated nonisolated async method runs on the main actor'. SWIFT_APPROACHABLE_CONCURRENCY enables DisableOutwardActorInference, GlobalActorIsolatedTypesUsability, InferIsolatedConformances, InferSendableFromCaptures and NonisolatedNonsendingByDefault. SWIFT_DEFAULT_ACTOR_ISOLATION=MainActor is a documented build setting. Sources: https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes , https://developer.apple.com/documentation/xcode/build-settings-reference
8. App extension memory: 'Memory limits for running app extensions are significantly lower than the memory limits imposed on a foreground app' (no number is given). New in iOS 27: MetricKit's MemoryExceptionDiagnostic 'are available when your app or app extension is terminated for exceeding its memory limit', and a Swift-first MetricManager API replaces MXMetricManager. Use these to tune PDF rasterization caps in the share extension. Sources: https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/ExtensionCreation.html , https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes
9. App Attest details confirmed for the recommendation. 'The generateKey(completionHandler:) method fails when you call it from an app extension, regardless of the value of isSupported.' isSupported is false on Mac, including iOS apps on Apple silicon. Keys 'don't survive app reinstallation, device migration, or restoration of a device from a backup'. On serverUnavailable, 'try attestation again later with the same key'. TestFlight and App Store builds ignore the appattest-environment entitlement and use production. Sources: https://developer.apple.com/documentation/devicecheck/dcappattestservice/issupported , https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity , https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.devicecheck.appattest-environment
10. DataScanner initializer defaults matter if the convenience init is used: qualityLevel .balanced, isHighFrameRateTrackingEnabled true, isHighlightingEnabled false. Also, isAvailable is true before permission is decided, so do not use it as a 'camera granted' check. Use AVCaptureDevice.authorizationStatus(for: .video) for the pre-permission screen. Source: https://developer.apple.com/documentation/visionkit/datascannerviewcontroller/init(recognizeddatatypes:qualitylevel:recognizesmultipleitems:ishighframeratetrackingenabled:ispinchtozoomenabled:isguidanceenabled:ishighlightingenabled:)
11. Unverified, and it affects Deutsche Bahn and other binary Aztec tickets: Apple documents messageEncoding only as 'The IANA character set name of the text encoding to use to convert message from a string representation to a data representation'. No Apple source I found confirms that Wallet's Aztec or PDF417 encoder turns an ISO-8859-1 string back into byte-identical binary symbol data that a UIC 918.3 reader would accept. Confidence is low. Build a test that decodes the Wallet-rendered barcode and compares bytes before committing to the feature. Source: https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary
12. For the PKPass and Wallet side, the June 2026 documentation adds a 'Pass Designer' tool ('Creating a pass with Pass Designer'), new semantic-tag customization for boarding passes, and 'Defining the metadata of your Wallet Pass'. I did not verify these individually, so pass them to the pass-format research. Source: https://developer.apple.com/documentation/updates
13. The researcher's XcodeGen keys check out against ProjectSpec.md: options.minimumXcodeGenVersion, deploymentTarget, createIntermediateGroups, bundleIdPrefix, target info and entitlements (generated plists), target scheme testTargets and gatherCoverageData, the bundle.unit-test and app-extension types, automatic TEST_HOST, and 'embed' defaulting to true for application targets. XcodeGen 2.46.0 is the latest tagged entry in the CHANGELOG. Sources: https://raw.githubusercontent.com/yonaskolb/XcodeGen/master/Docs/ProjectSpec.md , https://raw.githubusercontent.com/yonaskolb/XcodeGen/master/CHANGELOG.md
