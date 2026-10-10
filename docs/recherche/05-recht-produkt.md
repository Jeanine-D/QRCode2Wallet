# 05 · Recht, Plattform-Richtlinien und Markt

> **Hinweis:** Vollständige Rohfassung der Recherche vom 10.10.2026: KI-Agenten-Recherche gegen Primärquellen, danach von einem unabhängigen Faktenprüfer adversarial gegengeprüft. Die Inhalte stehen in der Originalsprache Englisch. Die deutsche Zusammenfassung mit Bewertung steht in der [Übersicht](README.md). Rechtliche Aussagen sind **keine Rechtsberatung**.

**Recherchierter Umfang:** QRCode2Wallet: legal, platform-policy, and product/market aspects of publishing a consumer iOS app that converts tickets and cards into Apple Wallet passes (focus Germany/EU, as of 2026-10-10). This is a non-binding assessment, not legal advice. A German IT/IP/data-protection lawyer should review it before launch.

**Inhalt:** 60 Fakten (Konfidenz hoch 42, mittel 16, niedrig 2) · 15 Empfehlungen · 15 Fallstricke · 11 offene Fragen · Faktencheck von 25 Kernaussagen: 24 bestätigt, 1 korrigiert, 0 nicht verifizierbar · 21 vom Faktenprüfer ergänzte Fakten

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

- **[KORRIGIERT]** Required-reason codes: UserDefaults CA92.1, 1C8F.1; FileTimestamp DDA9.1, C617.1, 3B52.1; DiskSpace 85F4.1, E174.1; SystemBootTime 35F9.1.
  - **Ergebnis:** Every code listed is correct, but each list is incomplete. Full sets: UserDefaults CA92.1, 1C8F.1, C56D.1 (third-party SDK wrapper only), AC6B.1 (MDM managed config). FileTimestamp DDA9.1 (display only, may not leave the device), C617.1 (files in the app, App Group or CloudKit container), 3B52.1 (user-granted files, e.g. document picker), 0A2A.1 (SDK wrapper only). DiskSpace 85F4.1, E174.1, 7D9E.1 (optional user bug report), B728.1 (health research). SystemBootTime 35F9.1, 8FFB.1 (absolute event timestamps, may be sent off device), 3D61.1 (optional bug report). There is also a category the claim leaves out: NSPrivacyAccessedAPICategoryActiveKeyboards (3EC4.1, 54BD.1).
  - **Quelle:** <https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitype>

## Fakten

### F1 · Konfidenz: hoch

The current Apple Developer Program License Agreement (DPLA) was updated August 18, 2026. Section 1.2 defines 'Pass(es)' as digital passes (e.g. movie tickets, coupons, loyalty reward vouchers, boarding passes, membership cards) 'developed by You under this Agreement, under Your own trademark or brand, and which are signed with Your Pass Type ID'. The date comes from the page marker 'LYL255 / August 18, 2026' and Apple's EU page.

- **Bedeutung fürs Design:** Every generated pass must be issued under QRCode2Wallet's own brand: organizationName is your company or app name, never 'Lidl' or 'Deutsche Bahn'. The pass is a personal digital copy that you issue. It is not the third-party business's pass.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F2 · Konfidenz: hoch

DPLA Attachment 5 §1 (Pass Type ID Usage and Restrictions): the Pass Type ID may be used only to sign 'Your Pass'. Distribution is allowed only 'under Your own trademark or brand, or if You reference a third party's trademark or brand within Your Pass (e.g., a store coupon for a particular good), You represent and warrant that You have any necessary rights.' You may not 'share, provide or transfer Your Pass Type ID to any third party (except for a Service Provider...), nor use Your Pass Type ID to sign a third party's pass.'

- **Bedeutung fürs Design:** This is the core contractual risk. (1) Never offer a B2B or white-label 'we sign passes for your business' service with your Pass Type ID. (2) Third-party brand names should appear only as text the user entered, never as presented official branding. (3) Rights to any brand logo would be your warranty to Apple, so do not supply or encourage brand logos.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F3 · Konfidenz: hoch

DPLA §3.3.9(B) Wallet: 'Your development of Passes, and use of the Pass Type ID and Wallet under this Agreement, must be in accordance with the terms of this Agreement (including the Program Requirements) and Attachment 5.'

- **Bedeutung fürs Design:** Attachment 5 terms are binding Program Requirements. A breach can cost both the Pass Type ID and the developer account.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F4 · Konfidenz: hoch

DPLA Attachment 5 §2.3: 'You agree to state on the Pass the name and address, and the contact information (telephone number; email address) to which any end user questions, complaints, or claims with respect to Your Pass should be directed.' You are solely responsible for support. 'You may not charge any fees to end users in order to use Wallet to access Your Pass.'

- **Bedeutung fürs Design:** Every pass needs a mandatory backFields entry with the legal entity's name, postal address, phone and email. Monetisation must never gate access to an already-issued pass in Wallet: no voiding or expiring passes through webServiceURL updates when a subscription lapses. Charge for app features (recognition, batch, PDF splitting, templates), not for Wallet access.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F5 · Konfidenz: hoch

DPLA Attachment 5 §2.4: by distributing passes, you permit Apple to use screenshots of your pass, 'trademarks and logos associated with Your Pass', and Pass Information for promotional purposes, excluding portions you do not have the right to use and identify to Apple in writing.

- **Bedeutung fürs Design:** You cannot grant Apple rights in Lidl, IKEA or DB logos you do not own. This is another reason to keep third-party logos out of anything you ship, bundle or serve.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F6 · Konfidenz: hoch

DPLA Attachment 5 §3.1: 'You agree to choose the relevant template for Your applicable use (e.g., You will not use the boarding pass template for a movie ticket).' §3.3: pass data may not be linked with other data for targeted advertising or ad measurement, or shared with data brokers.

- **Bedeutung fürs Design:** Map pass styles strictly: boardingPass only for real transit or flight tickets, eventTicket for events, storeCard for loyalty or gift cards, coupon for offers, generic for gym or membership cards. Do not include ad SDKs that touch pass data.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F7 · Konfidenz: hoch

DPLA Attachment 5 §4: Apple may review, approve or reject any pass at any time. Apple 'reserves the right to revoke Your Pass Type ID and reject Your Pass for distribution ... for any reason and at any time in its sole discretion, even if Your Pass meets the Documentation and Program Requirements'.

- **Bedeutung fürs Design:** Revocation is a platform risk outside your control. Design for re-issuing passes (see the certificate facts below).
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F8 · Konfidenz: hoch

Apple Certificates overview, Pass Type ID Certificate (Wallet): 'If your certificate expires, passes that are already installed on users' devices will continue to function normally. However, you'll no longer be able to sign new passes or send updates to existing passes. If your certificate is revoked, your passes will no longer function properly.' Pass Type ID certificates cannot be revoked from the developer account; you must email product-security@apple.com.

- **Bedeutung fürs Design:** If Apple revokes the certificate, every user's passes break. Keep the source data (barcode payload, fields, user images) locally in the app, e.g. in SwiftData, so passes can be regenerated under a new certificate or Pass Type ID. Monitor certificate expiry, and use separate Pass Type IDs for development and production.
- **Quelle:** <https://developer.apple.com/help/account/certificates/certificates-overview/>

### F9 · Konfidenz: hoch

DPLA §5.1: all passes must be signed with an Apple Certificate to be accepted by Wallet. You are 'solely responsible for preventing any unauthorized person or organization from having access to Your Apple Certificates and keys' and must use best efforts to safeguard them.

- **Bedeutung fürs Design:** This confirms the decision to sign on the backend. Keep the Pass Type ID private key in a KMS, HSM or secret store on the FastAPI backend, never in the app or the repository, and restrict access.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F10 · Konfidenz: hoch

DPLA §3.2(4): you warrant that Covered Products (which include Passes) and Pass Information do not infringe third-party trademarks or copyrights. Under §10 you indemnify Apple against claims that a Covered Product or Pass Information infringes third-party IP rights.

- **Bedeutung fürs Design:** Brand-owner claims over logos on passes fall on the developer. Mitigate with ToS warranties and indemnity from users, no logo catalogue, and a takedown process.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F11 · Konfidenz: hoch

DPLA §2.9: you may retain a Service Provider (e.g. to maintain your servers) acting solely on your behalf. You need a binding written agreement with terms at least as protective of Apple, and you remain responsible for the provider's actions.

- **Bedeutung fürs Design:** The hosting provider that holds the signing key needs a written contract, and the GDPR Art. 28 processing agreement (AVV) should cover key custody. Attachment 5 §1 allows sharing the Pass Type ID only with such a Service Provider.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F12 · Konfidenz: hoch

App Store Review Guideline 1.5 (guidelines last updated June 8, 2026): 'ensure that Wallet passes include valid contact information from the issuer and are signed with a dedicated certificate assigned to the brand or trademark owner of the pass.'

- **Bedeutung fürs Design:** This is the main review risk for a 'pass converter'. Position QRCode2Wallet as the issuer and brand owner of the pass container: own organizationName, own contact info on the back, a clear 'personal copy, not an official card of X' disclaimer, and no third-party logos supplied by you. Explain this model in the App Review notes.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F13 · Konfidenz: hoch

Guideline 3.2.1(iv): 'Wallet passes can be used to make or receive payments, transmit offers, or offer identification (such as movie tickets, coupons, and VIP credentials). Other uses may result in the rejection of the app and the revocation of Wallet credentials.'

- **Bedeutung fürs Design:** Limit the scope to tickets, loyalty and membership cards, coupons and boarding passes. Do not market 'put any QR code into Wallet' (Wi-Fi codes, URLs, notes), because those are 'other uses'.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F14 · Konfidenz: hoch

Guideline 4.3(b) Spam: 'Don't submit apps that are indistinguishable from what's already widely available.' Guideline 4.2: apps must offer 'adequate utility' beyond a repackaged website.

- **Bedeutung fürs Design:** The pass-creator category is crowded (Pass2U, NeatPass, Wallet Creator, PassX, PassIt, Walletsio, Barcodes and others), and iOS 27 now has native pass creation. Submit with clear differentiators (PDF and multi-ticket import, automatic field recognition, German transit or flight parsing, batch) and explain them in the review notes.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F15 · Konfidenz: hoch

Guideline 5.2.1: 'Don't use protected third-party material such as trademarks, copyrighted works, or patented ideas in your app without permission.' Guideline 5.2.2: if the app uses, accesses or displays content from a third-party service, it must be specifically permitted under that service's terms, and authorization must be provided on request.

- **Bedeutung fürs Design:** No bundled or served brand-logo catalogue and no auto-fetching of brand logos. Do not build login-and-import integrations with DB Navigator, Payback, Lidl Plus and similar without written permission. App Store screenshots must use fictional brands.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F16 · Konfidenz: hoch

Guideline 2.3.7: 'don't try to pack any of your metadata with trademarked terms, popular app names ... just to game the system.' Subtitles may not reference other apps.

- **Bedeutung fürs Design:** App Store optimisation cannot rely on 'Lidl', 'IKEA', 'DB', 'Deutschlandticket', 'Payback' or similar as keywords, in the subtitle or in screenshots. Use generic terms instead (Kundenkarte, Ticket, Bordkarte, PDF, Wallet-Karte).
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F17 · Konfidenz: hoch

Guideline 5.1.1: (i) a privacy policy link is required in App Store Connect and inside the app, and must explain collection, third-party sharing, retention and deletion, and consent revocation. (iii) Data minimisation: 'use the out-of-process picker or a share sheet rather than requesting full access to protected resources like Photos'. (v) If the app supports account creation, it must offer in-app account deletion, and an app without significant account-based features must work without login.

- **Bedeutung fürs Design:** Use SwiftUI PhotosPicker (no Photos permission needed), fileImporter and a Share Extension. The camera needs NSCameraUsageDescription. A v1 without accounts avoids the deletion and login rules entirely.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F18 · Konfidenz: hoch

Guideline 5.1.2(i): 'You must clearly disclose where personal data will be shared with third parties, including with third-party AI, and obtain explicit permission before doing so.'

- **Bedeutung fürs Design:** Cloud OCR or LLM field extraction (e.g. a hosted LLM API) would require an explicit consent screen and disclosure. On-device recognition (Vision, VisionKit, Foundation Models) avoids this.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F19 · Konfidenz: hoch

Guideline 4.8 Login Services: if a third-party or social login is used for the primary account, the app must also offer an equivalent login service that limits data to name and email, lets users keep their email private, and does not collect interactions for advertising without consent. This is not required if the app exclusively uses the company's own account system.

- **Bedeutung fürs Design:** With no accounts, nothing applies. If accounts are added later with Google login, Sign in with Apple (or an equivalent) becomes mandatory.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F20 · Konfidenz: hoch

Apple's account deletion guidance (5.1.1(v)): apps that create accounts, including automatically created 'guest' accounts, must let people initiate deletion in the app. Offering only deactivation is insufficient. Apps using Sign in with Apple should revoke tokens through the Sign in with Apple REST API.

- **Bedeutung fürs Design:** A silent backend user record (e.g. for quota tracking) can count as an auto-created account and trigger the deletion requirement. Keep the backend stateless, or provide a deletion endpoint.
- **Quelle:** <https://developer.apple.com/support/offering-account-deletion-in-your-app/>

### F21 · Konfidenz: hoch

Guideline 3.1.1: unlocking features or functionality must use in-app purchase, not license keys or QR codes. Guideline 3.1.2(a): auto-renewable subscriptions 'must provide ongoing value' and last at least seven days.

- **Bedeutung fürs Design:** Use StoreKit 2 only. Reviewers can question a subscription for a one-shot converter. A non-consumable lifetime 'Pro' unlock is easier to defend; a subscription needs genuinely ongoing services (pass updates, sync, new recognisers).
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F22 · Konfidenz: mittel

Guideline 4.10: 'You may not monetize built-in capabilities provided by the hardware or operating system, such as Push Notifications, the camera, or the gyroscope; or Apple services and technologies, such as Apple Music access, iCloud storage, or Screen Time APIs.'

- **Bedeutung fürs Design:** The rule text is verified, but whether it covers Wallet is not stated anywhere. Combined with Attachment 5 §2.3, it is safer to price the conversion intelligence, not the act of adding to Wallet. A basic free conversion path lowers the risk further.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F23 · Konfidenz: mittel

Guideline 5.1.1(ix): apps providing services in highly regulated fields (the list includes 'air travel') or requiring sensitive user information 'should be submitted by a legal entity that provides the services, and not by an individual developer'.

- **Bedeutung fürs Design:** Boarding-pass features could draw this scrutiny. A converter does not provide air travel services, but enrolling as an organisation (UG or GmbH) reduces the risk.
- **Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### F24 · Konfidenz: hoch

App Privacy Details: '"Collect" refers to transmitting data off the device and storing it in a readable form for longer than the time it takes you and/or your third-party partners to service the request ... if data is sent to your servers then immediately discarded after servicing the request, you do not need to disclose this.' Also: 'Data that is processed only on device is not "collected".' and 'You are not responsible for disclosing data collected by Apple.'

- **Bedeutung fürs Design:** Stateless signing, on-device recognition, and no third-party analytics or crash SDK make a 'Data Not Collected' privacy label achievable, which is a strong selling point. This only holds if request payloads are not logged and nothing per user is persisted.
- **Quelle:** <https://developer.apple.com/app-store/app-privacy-details/>

### F25 · Konfidenz: hoch

Privacy manifest: an app bundles PrivacyInfo.xcprivacy with the top-level keys NSPrivacyTracking, NSPrivacyTrackingDomains, NSPrivacyCollectedDataTypes and NSPrivacyAccessedAPITypes. 'Starting May 1, 2024, apps that don't describe their use of required reason API in their privacy manifest file aren't accepted by App Store Connect.'

- **Bedeutung fürs Design:** Include PrivacyInfo.xcprivacy in the app target and in any extension that uses required-reason APIs. Set NSPrivacyTracking=false and leave NSPrivacyCollectedDataTypes empty if the backend is stateless.
- **Quelle:** <https://developer.apple.com/documentation/bundleresources/privacy-manifest-files>

### F26 · Konfidenz: hoch

Required-reason API categories and codes (NSPrivacyAccessedAPIType): NSPrivacyAccessedAPICategoryUserDefaults uses CA92.1 (app-only) and 1C8F.1 (same App Group). NSPrivacyAccessedAPICategoryFileTimestamp uses DDA9.1 (display to user), C617.1 (files in app or App Group container) and 3B52.1 (files the user granted access to, e.g. through a document picker). NSPrivacyAccessedAPICategoryDiskSpace uses 85F4.1 and E174.1. NSPrivacyAccessedAPICategorySystemBootTime uses 35F9.1.

- **Bedeutung fürs Design:** An app plus Share Extension using App Group UserDefaults declares 1C8F.1 (and CA92.1 if it also uses standard defaults). Reading attributes of imported PDFs or images declares 3B52.1 or C617.1. Third-party SDKs bring their own manifests.
- **Quelle:** <https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitype>

### F27 · Konfidenz: hoch

Values for NSPrivacyCollectedDataType include NSPrivacyCollectedDataTypePhotosorVideos, NSPrivacyCollectedDataTypeOtherUserContent, NSPrivacyCollectedDataTypePurchaseHistory, NSPrivacyCollectedDataTypeUserID, NSPrivacyCollectedDataTypeDeviceID, NSPrivacyCollectedDataTypeCrashData and NSPrivacyCollectedDataTypeName. Purposes include NSPrivacyCollectedDataTypePurposeAppFunctionality and NSPrivacyCollectedDataTypePurposeAnalytics.

- **Bedeutung fürs Design:** If the backend persists App Attest public keys or transaction IDs, or a crash SDK is added, declare DeviceID, PurchaseHistory or CrashData with purpose AppFunctionality, and update the App Store Connect label to match.
- **Quelle:** <https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatype>

### F28 · Konfidenz: hoch

Apple upcoming requirements: since April 28, 2026, uploads must be built with Xcode 26 or later and the iOS 26 SDK. Since September 9, 2026, iOS apps must target iOS 13 or later. New age-rating questions had to be answered by January 31, 2026. DSA trader status has been required for EU distribution since February 17, 2025; apps without it are removed from the EU App Store.

- **Bedeutung fürs Design:** Build with Xcode 26 or later. Plan the age-rating questionnaire and the DSA trader declaration before the first submission.
- **Quelle:** <https://developer.apple.com/news/upcoming-requirements/>

### F29 · Konfidenz: hoch

Under DSA Arts. 30 and 31, Apple verifies trader contact information and shows the address, phone number and email on the EU App Store product page. Individual developers must enter an 'Address or P.O. Box'; organisations display the address linked to their D-U-N-S number.

- **Bedeutung fürs Design:** A monetised app makes the publisher a trader. Enrolling as an organisation (UG or GmbH, which needs a free D-U-N-S number) avoids publishing a home address and limits personal liability.
- **Quelle:** <https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements/>

### F30 · Konfidenz: hoch

The Apple Developer Program costs 99 USD per membership year. Apple says 'Prices may vary by region and are listed in local currency during the enrollment process.' Press reports put the German price at 99 EUR per year since 2015; whether that includes VAT is unverified.

- **Bedeutung fürs Design:** Fixed cost of about 99 EUR per year. The Pass Type ID, its certificate, APNs and App Store Server API access are included at no extra charge. The EUR amount is medium confidence: https://www.ifun.de/99e-statt-80e-apple-erhoeht-entwickler-gebuehren-71232/
- **Quelle:** <https://developer.apple.com/programs/enroll/>

### F31 · Konfidenz: mittel

No Apple per-pass fee was found. The DPLA and Attachment 5 describe distribution 'by the web, email, or an Application' with no per-pass charge, and pass signing uses your own certificate.

- **Bedeutung fürs Design:** The marginal cost per pass is backend compute and egress only: a few ms of CMS signing, and a .pkpass from a few KB up to a few hundred KB with images. In hash-only signing mode the request is under 2 KB.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F32 · Konfidenz: hoch

App Store Small Business Program: 15% commission on paid apps and in-app purchases for developers with up to 1 million USD in proceeds in the prior calendar year, and for new developers.

- **Bedeutung fürs Design:** Enrol before launch. Net revenue is 85% of the price excluding VAT.
- **Quelle:** <https://developer.apple.com/app-store/small-business-program/>

### F33 · Konfidenz: hoch

EU unified business terms (DPLA updated August 18, 2026; effective October 1, 2026): App Store commission for Apple In-App Purchase in the EU is 26%, or 15% for Small Business Program participants and for auto-renewable subscriptions after their first year. The Core Technology Fee was replaced by a 5% Core Technology Commission for distribution outside the App Store. The Initial Acquisition Fee and Store Services Fee were eliminated.

- **Bedeutung fürs Design:** For EU storefronts, model revenue with a 15% commission (Small Business Program). No per-install fee applies while distributing only through the App Store.
- **Quelle:** <https://developer.apple.com/support/dma-and-apps-in-the-eu/>

### F34 · Konfidenz: hoch

StoreKit 2 on the client: AppTransaction (iOS 16.0+) is a JWS-signed record of the app purchase, obtained through AppTransaction.shared. Transaction.currentEntitlements (iOS 15.0+). VerificationResult.jwsRepresentation (iOS 15.0+) is 'The transaction signed by the App Store, in JWS Compact Serialization format'. Transaction.appAccountToken (iOS 15.0+) is an optional UUID linking a transaction to your own user.

- **Bedeutung fürs Design:** For Pro features the app sends the entitlement's jwsRepresentation (or the AppTransaction JWS) with each signing request. The backend verifies it statelessly, with no account system and no stored user table.
- **Quelle:** <https://developer.apple.com/documentation/storekit/verificationresult/jwsrepresentation-21vgo>

### F35 · Konfidenz: hoch

App Store Server API (JWT auth with an In-App Purchase key): Get All Subscription Statuses is GET https://api.storekit.apple.com/inApps/v1/subscriptions/{transactionId}; Get Transaction Info is GET /inApps/v1/transactions/{transactionId}. The sandbox host is api.storekit-sandbox.apple.com. Apple publishes an open-source App Store Server Library in Swift, Java, Python and Node.

- **Bedeutung fürs Design:** Use these endpoints only if you need authoritative subscription status (refunds, revocations). For a one-time unlock, offline JWS verification is enough. Add App Store Server Notifications V2 if you sell subscriptions.
- **Quelle:** <https://developer.apple.com/documentation/appstoreserverapi/get-all-subscription-statuses>

### F36 · Konfidenz: hoch

Python: 'pip install app-store-server-library' (version 3.1.2, released June 1, 2026). SignedDataVerifier(root_certificates, enable_online_checks, environment, bundle_id, app_apple_id) provides verify_and_decode_signed_transaction, verify_and_decode_app_transaction, verify_and_decode_renewal_info and verify_and_decode_notification. AppStoreServerAPIClient(private_key, key_id, issuer_id, bundle_id, environment) provides get_all_subscription_statuses, get_transaction_info, get_transaction_history and others. app_apple_id is required in Production.

- **Bedeutung fürs Design:** The FastAPI entitlement check verifies the JWS chain against Apple root CAs, then checks bundleId, productId, environment, revocationDate and (for subscriptions) expiresDate. It returns 402 or 403 for Pro-only operations, while the basic free path stays open.
- **Quelle:** <https://pypi.org/project/app-store-server-library/>

### F37 · Konfidenz: hoch

DeviceCheck: DCDevice (iOS 11.0+) lets you set and query two bits per device through Apple's server API. Under DPLA §3.3.9(F) you must provide a way for customers to have those values reset, may not use DeviceCheck data as the sole fraud indicator, and may not share the tokens. DCAppAttestService (iOS 14.0+) validates that requests come from a genuine instance of your app.

- **Bedeutung fürs Design:** A free-tier flag (e.g. 'free quota used this month') and abuse protection of the signing endpoint are possible without accounts or device fingerprinting. Note that App Attest requires storing an attested public key per key ID on the server, which may count as Device ID collection for the privacy label.
- **Quelle:** <https://developer.apple.com/documentation/devicecheck/dcdevice>

### F38 · Konfidenz: hoch

DPLA §3.3.3(B): you may not collect user or device data without prior user consent, and then only for a directly relevant service. 'Neither You nor Your Application will use any permanent, device-based identifier, or any data derived therefrom, for purposes of uniquely identifying a device.'

- **Bedeutung fürs Design:** Do not use IDFV or hardware-derived IDs for quotas. Use DeviceCheck bits, App Attest, or StoreKit transactions instead.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F39 · Konfidenz: mittel

iOS 27 Wallet has a native 'Create a Pass' feature (+ &gt; Create a Pass, subtitled 'Tickets, membership cards and more'). It offers a Visual Intelligence scan (an Apple Intelligence feature, reportedly iPhone 15 Pro or newer) and manual creation from three templates: Standard (orange), Membership (blue) and Event (purple). Users can customise colours and background images. Passes are static (no updates), and Wallet does not validate the scanned code. Apple did not announce it on stage, and no developer.apple.com page documents it; the reports are secondary, including a tutorial dated 2026-10-01 describing it as shipping.

- **Bedeutung fürs Design:** This is the largest market risk: the basic 'scan a barcode into Wallet' feature is now free and built in. QRCode2Wallet must win on what the native feature lacks: PDF, screenshot and share-sheet import; multi-ticket PDF splitting; automatic field and date extraction (relevantDates, locations, semantics); German transit and flight ticket understanding; batch; devices without Apple Intelligence; iOS 18–26 users. Other sources: https://appleinsider.com/articles/26/06/09/how-apple-wallets-create-a-pass-works-in-ios-27 and https://www.idownloadblog.com/2026/10/01/create-pass-ios-wallet/
- **Quelle:** <https://www.macrumors.com/how-to/create-a-custom-pass-in-the-wallet-app-on-iphone>

### F40 · Konfidenz: hoch

Pass.Barcodes (iOS 9+): 'In iOS 27 and later, you can provide more than one barcode as a fallback.' Wallet supports PKBarcodeFormatQR, PKBarcodeFormatPDF417, PKBarcodeFormatAztec, PKBarcodeFormatCode128, PKBarcodeFormatCode39, PKBarcodeFormatCodabar, PKBarcodeFormatEAN13 and PKBarcodeFormatI2of5; the formats beyond QR, PDF417, Aztec and Code128 are new in iOS 27.

- **Bedeutung fürs Design:** This fixes a classic complaint about loyalty-card converters: EAN-13 retail cards previously had to be re-encoded as Code128, and some checkout scanners rejected it. Emit the native format plus a fallback for pre-iOS-27 devices.
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary>

### F41 · Konfidenz: hoch

Apple Wallet 'What's new': the Poster Generic pass template and Featured Actions are available in iOS 27 and later. Pass Designer is a macOS 27 app. Pass Builder is a 'Swift on server package' for building and signing passes. Enhanced boarding passes require iOS 26; multi-event tickets require iOS 18.

- **Bedeutung fürs Design:** Apple is lowering the barrier for issuers to adopt Wallet directly, so fewer cards will need conversion over time. Poster templates on iOS 27 are a way to look better than the three native templates. Pass Builder is Swift-only, so the Python backend still needs its own CMS signing.
- **Quelle:** <https://developer.apple.com/wallet/whats-new/>

### F42 · Konfidenz: hoch

Pass keys: organizationName ('The name of the organization'). sharingProhibited (introduced in iOS 11) removes the Share button but 'does not prevent sharing the pass in some other way'. Also voided, expirationDate, relevantDates, and locations (up to 10).

- **Bedeutung fürs Design:** organizationName is your own brand. Set sharingProhibited=true for personalised tickets (Deutschlandticket, rail tickets with a name, boarding passes) to reduce duplication. Set expirationDate so expired tickets disappear (HIG).
- **Quelle:** <https://developer.apple.com/documentation/walletpasses/pass>

### F43 · Konfidenz: hoch

Add to Apple Wallet guidelines: 'Be sure to use the badges provided by Apple. Do not create your own versions.' 'Do not use the Wallet icon alone.' 'Do not imitate Apple communications.' The badge must be secondary to your own identity.

- **Bedeutung fürs Design:** Use the system AddPassToWalletButton (SwiftUI) or PKAddPassButton. Keep the Wallet icon out of the app icon and screenshots. Avoid 'Apple' in the app name; 'Wallet' as a generic word in 'QRCode2Wallet' is lower risk but not verified against Apple's trademark list.
- **Quelle:** <https://developer.apple.com/wallet/add-to-apple-wallet-guidelines/>

### F44 · Konfidenz: hoch

The Foundation Models framework (iOS 26.0+) gives access to the on-device Apple Intelligence model (SystemLanguageModel) for entity extraction and guided generation with @Generable. In iOS 27 it also exposes Private Cloud Compute. Availability depends on device and region support for Apple Intelligence.

- **Bedeutung fürs Design:** Field extraction (event name, date, seat, gate) can run on-device, which keeps personal data off your servers and avoids Guideline 5.1.2(i) third-party-AI consent. A rule-based fallback is needed for non-eligible devices.
- **Quelle:** <https://developer.apple.com/documentation/foundationmodels>

### F45 · Konfidenz: hoch

Custom EULA: under DPLA Schedule 1 §3.2 you may deliver your own EULA for a Licensed Application; it must include Apple's minimum terms. Under §3.3 the EULA 'is solely between You and the end user'.

- **Bedeutung fürs Design:** Put the ToS clauses (lawful holder only, no forging or duplication for others, user rights to any uploaded images, indemnity, issuer rules prevail, no validity guarantee) into a custom EULA in App Store Connect, and show them in the app on first use.
- **Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### F46 · Konfidenz: niedrig

Competitor Pass2U Wallet: free with ads plus a Pro one-time unlock around $2.99 (some sources cite a 5-card free limit). About 4.2 stars from about 2.9K ratings in the US store. Complaints concern ads, purchases that did not unlock adding passes, and restore failures.

- **Bedeutung fürs Design:** Pass2U, a long-running pass-creator app, has stayed on the App Store for years, so Apple tolerates the model in practice. The price anchor is low, and ad-funded apps draw strong complaints. Figures come from aggregators; listing pages were not directly reachable.
- **Quelle:** <https://apps.apple.com/us/app/pass2u-wallet-add-store-card/id1142473931>

### F47 · Konfidenz: mittel

Competitor NeatPass – PDF ins Wallet (German listing): one free conversion, then a €4.99 one-time unlock with no subscription. It runs on-device ML and claims 'only a cryptographic fingerprint is sent for Wallet signing'. It splits multi-ticket PDFs, requires iOS 18.1+, and publishes German content about DB tickets. Ratings reported around 3.9 from 15 on the DE store.

- **Bedeutung fürs Design:** A direct competitor already holds the 'privacy-first, PDF, German, one-time €4.99' position. Differentiation must go further: auto-recognition quality, batch, transit and flight parsing, pass design, Apple Watch, and support. Also see https://www.appgefahren.de/tag/neatpass
- **Quelle:** <https://apps.apple.com/de/app/neatpass-pdf-ins-wallet/id6756032474>

### F48 · Konfidenz: mittel

Other converters and their pricing (US listings via search): Barcodes: Loyalty Card Wallet (3 cards free; $1.99/month, $7.99/year, $14.99 lifetime). Loyalty Cards: Add to Wallet (weekly $1.99–$5.99, yearly up to $49.99, with ads). Pass – Loyalty Card Wallet (WalletLab Pro $4.49/week). Wallet Creator: Digital Passes (Astrum Computing, free plus IAP). Also PassX, PassIt and Walletsio. Aggregated reviews report paywalls that block basic functions.

- **Bedeutung fürs Design:** Many apps use aggressive weekly subscriptions, and users resent that. Transparent pricing (generous free tier plus a fair one-time Pro) is a credible differentiator, especially in Germany.
- **Quelle:** <https://apps.apple.com/us/app/barcodes-loyalty-card-wallet/id1610894014>

### F49 · Konfidenz: mittel

WalletWallet is a free, browser-based tool that creates .pkpass files from scanned, uploaded or typed barcodes, with no registration. Its operator also offers an API for businesses, advertised as needing no Apple developer account or certificate.

- **Bedeutung fürs Design:** A free web alternative sets a €0 price anchor for simple loyalty cards. Its B2B API model, signing passes for other businesses, is exactly what DPLA Attachment 5 §1 forbids, so do not copy it.
- **Quelle:** <https://www.mobiflip.de/walletwallet-macht-fast-jede-kundenkarte-iphone-tauglich/>

### F50 · Konfidenz: mittel

Klarna acquired Stocard (2021) and rebranded it (2022). The standalone Stocard app was shut down and card management moved into the Klarna app, which requires a Klarna account. German media point displaced users to account-free alternatives such as SuperCards.

- **Bedeutung fürs Design:** There is German demand for account-free, ad-free, privacy-friendly card storage. Offering 'no account, no tracking, cards live in your Wallet' is a positioning opportunity.
- **Quelle:** <https://www.iphone-ticker.de/kundenkarten-apps-supercards-als-alternative-zu-stocard-245162/>

### F51 · Konfidenz: mittel

DB and Deutschlandticket: DB Navigator offers no Wallet export for the Deutschlandticket, and sources conflict on whether a Wallet button still exists for long-distance tickets. The official Deutschlandticket app and some transit operators (BVG, HVV, Bogestra) offer native Wallet support.

- **Bedeutung fürs Design:** DB support is a real German demand signal. Prefer guiding users to official Wallet exports where they exist, and support PDF Online-Tickets (Aztec barcodes) as the main DB use case. Also see https://neatpass.app/learn/deutsche-bahn-apple-wallet
- **Quelle:** <https://www.macwelt.de/article/1812791/deutschland-ticket-apple-wallet-iphone.html>

### F52 · Konfidenz: mittel

German transit issuers (e.g. NAH.SH, BVG) state that copies or screenshots of mobile tickets (Handytickets) are not valid; digital tickets are valid only in the official app on a working device. One report cites a Berlin court decision allowing a printed Deutschlandticket, which is an individual case.

- **Bedeutung fürs Design:** A Wallet copy of an app-only Handyticket may be rejected at inspection, giving the user a fare penalty and a bad review. Detect and warn (or block) for app-only transit tickets, and never claim validity. Also see https://www.deskmodder.de/blog/2025/09/12/handy-ticket-screenshot-reicht-bei-kontrolle-nicht-aus/
- **Quelle:** <https://www.nah.sh/de/fahrkarten/deutschlandticket/nutzung/>

### F53 · Konfidenz: mittel

The Deutschlandticket barcode (VDV-KA) carries the holder's name, shortened by a rule, and date of birth. At inspection these are compared with an official photo ID. The ticket is personal and non-transferable.

- **Bedeutung fürs Design:** Ticket barcodes are personal data under GDPR Art. 4(1), and copying them does not make them more valid. Never persist or log the barcode payload on the server.
- **Quelle:** <https://www.kcd-nrw.de/fileadmin/user_upload/Technische_Anforderung_Deutschlandticket_V1.5.pdf>

### F54 · Konfidenz: niedrig

IATA BCBP boarding-pass barcodes can contain passenger name, booking reference (PNR), flight, seat and sometimes the frequent-flyer number. Many are not digitally signed.

- **Bedeutung fürs Design:** Treat boarding passes as sensitive: no server logging, sharingProhibited=true, and boardingPass style only for real boarding passes. The source is secondary; check against the IATA BCBP specification.
- **Quelle:** <https://kiledjian.com/2024/10/21/unveiling-the-hidden-risks-in.html>

### F55 · Konfidenz: hoch

GDPR (Regulation (EU) 2016/679): Art. 5(1)(c) data minimisation and 5(1)(e) storage limitation. Art. 6(1)(b) (necessary for a contract the data subject requested) and 6(1)(f) (legitimate interests). Art. 9(1) special categories include data revealing religious beliefs, trade-union membership and health data. Art. 13 information duties; Art. 17 erasure; Art. 25 data protection by design and default; Art. 28 processor contracts; Art. 30 records of processing; Art. 32 security; Art. 33 72-hour breach notification; Art. 35 DPIA (mandatory for large-scale processing of Art. 9 data); Arts. 44 ff. international transfers.

- **Bedeutung fürs Design:** Users will convert union, church, health-insurance, disability or patient cards, which are Art. 9 data. If such content reaches the server, you need explicit consent (Art. 9(2)(a)) and possibly a DPIA. Hash-only signing, where the server never sees pass content, removes the issue. Use Art. 6(1)(b) as the basis for the conversion service and Art. 6(1)(f) for short-lived security logs. Article text was not fetchable in this session; confidence rests on well-established law.
- **Quelle:** <https://eur-lex.europa.eu/eli/reg/2016/679/oj>

### F56 · Konfidenz: mittel

The EU-US Data Privacy Framework adequacy decision (2023) was upheld by the EU General Court on September 3, 2025 (T-553/23 Latombe). An appeal (C-703/25 P) has been pending at the Court of Justice since October 31, 2025.

- **Bedeutung fürs Design:** US-cloud hosting relies on an adequacy decision that may be invalidated, as Schrems II did with Privacy Shield. Hosting the signing backend with an EU-headquartered provider in an EU region avoids Chapter V transfer risk and supports the privacy positioning.
- **Quelle:** <https://www.wilmerhale.com/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20251201-european-court-of-justice-to-review-challenge-to-eu-us-data-privacy-framework>

### F57 · Konfidenz: mittel

Germany: §25 TDDDG (formerly TTDSG, renamed May 14, 2024) requires consent to store or read information on the user's device unless strictly necessary for a service the user explicitly requested. The Impressum obligation moved from §5 TMG to §5 DDG on May 14, 2024; violations can be pursued under §3a UWG and fined under §33 DDG.

- **Bedeutung fürs Design:** Third-party analytics or crash SDKs need opt-in consent, or should be avoided. An Impressum must be reachable in the app (e.g. Settings &gt; Impressum, within two taps) and on the website and support URL.
- **Quelle:** <https://www.datenschutz-notizen.de/websitebetreiber-aufgepasst-abloesung-des-tmg-und-ttdsg-4648163/>

### F58 · Konfidenz: mittel

EU Trade Mark Regulation (EU) 2017/1001: Art. 9 gives the proprietor rights against use of a sign 'in the course of trade'. Art. 14(1)(c) permits using a trade mark to identify or refer to goods or services as those of the proprietor, in accordance with honest practices. German equivalents are §14 and §23 MarkenG.

- **Bedeutung fürs Design:** A user privately typing 'Lidl Plus' or adding their own image is low risk. The risk lies in your commercial use: logo catalogues, brand-named templates, marketing screenshots, ASO keywords, or 'official' claims. Plain text references to the card issuer are defensible nominative use.
- **Quelle:** <https://eur-lex.europa.eu/eli/reg/2017/1001/oj>

### F59 · Konfidenz: mittel

Digital Services Act (EU) 2022/2065: Art. 6 hosting liability exemption. Art. 16 requires hosting services to provide a notice-and-action mechanism. Arts. 11 and 12 require single points of contact for all intermediary services. Some transparency obligations (e.g. Art. 15) do not apply to micro and small enterprises.

- **Bedeutung fürs Design:** Stateless signing that stores nothing is arguably not 'hosting'. If you add hosted share links, pass update web services or cloud backup, you become a hosting service: implement a notice form (IP or abuse) and a statement-of-reasons flow.
- **Quelle:** <https://eur-lex.europa.eu/eli/reg/2022/2065/oj>

### F60 · Konfidenz: mittel

German criminal law relevant to user misuse: §265a StGB (fare evasion, 'Erschleichen von Leistungen'), §267 StGB (forgery of documents), §263 StGB (fraud).

- **Bedeutung fürs Design:** If users share copied tickets with others, the users commit the offence, but app positioning matters. Do not market 'share tickets' or 'duplicate'. Do not allow editing of scanned ticket payloads (manual entry only for loyalty-card numbers). The ToS should forbid creating passes for tickets you do not lawfully hold. How these offences apply to a converter app is an assessment, not established case law.
- **Quelle:** <https://www.gesetze-im-internet.de/stgb/__265a.html>

## Empfehlungen

### E1

**Empfehlung:** Publish through a legal entity (UG (haftungsbeschränkt) or GmbH) enrolled in the Apple Developer Program as an Organization with a D-U-N-S number. Declare DSA trader status, and enrol in the Small Business Program before the first paid sale.

**Begründung:** This limits personal liability for indemnities to Apple (DPLA §10) and for brand claims. It keeps a home address off the EU product page (DSA trader display), lowers 5.1.1(ix) scrutiny for boarding-pass features, and halves the commission (15% vs 26% in the EU).

### E2

**Empfehlung:** Use an issuer model: every pass is a QRCode2Wallet-issued 'personal digital copy'. organizationName is your brand. logoText or header carries the user-entered card name as text only. The default logo and icon are your own neutral artwork. A mandatory backFields block reads, in German and English: 'Persönliche digitale Kopie, erstellt mit QRCode2Wallet. Keine offizielle Karte von &lt;Name&gt;. Es gelten die Bedingungen des ursprünglichen Ausstellers. Herausgeber des Passes: &lt;Firma&gt;, &lt;Anschrift&gt;, &lt;Telefon&gt;, &lt;E-Mail&gt;.' (English: 'Personal digital copy created with QRCode2Wallet. Not an official card of &lt;Name&gt;. The original issuer's terms apply. Pass issued by: &lt;company&gt;, &lt;address&gt;, &lt;phone&gt;, &lt;email&gt;.')

**Begründung:** This satisfies DPLA Definition 'Pass' ('under Your own trademark or brand'), Attachment 5 §1 (no signing of a third party's pass) and §2.3 (contact info on every pass), and Guideline 1.5 (issuer contact; certificate belongs to the pass's brand owner, which is you). It is the defensible reading that existing converters rely on.

### E3

**Empfehlung:** Do not provide brand logos or a logo catalogue, and do not auto-fetch logos from logo APIs or websites. Allow optional user-supplied images, processed on-device. Include a ToS/EULA warranty that the user owns or may use any image, plus indemnity. Publish an abuse and IP contact (and a DSA Art. 16 form if anything is hosted). App Store screenshots and keywords use only fictional brands such as 'Musterladen'.

**Begründung:** Guideline 5.2.1 and 2.3.7, DPLA §3.2(4) warranty, §10 indemnity and Attachment 5 §2.4 (you license pass logos to Apple). Commercial use of a mark 'in the course of trade' (EUTMR Art. 9) is your risk; private user choices are much lower risk.

### E4

**Empfehlung:** Privacy architecture: run all recognition on-device (Vision barcode and document recognition, VisionKit DataScannerViewController, Foundation Models where available, with a rule-based fallback). The backend signs in 'hash-only' mode: the app builds pass.json, images and manifest.json, sends only manifest.json (file names and SHA-1 hashes) plus an App Attest assertion, and the FastAPI service returns the detached PKCS#7 signature. Persist nothing. Log only status codes and timing, never request bodies. Keep IP logs for at most 7 days, under Art. 6(1)(f).

**Begründung:** Ticket barcodes contain name, date of birth, PNR and booking codes, and many cards are Art. 9 data (union, church, health, disability). If the server never sees content, there is no Art. 9 consent, no DPIA, minimal Art. 28 scope, and a 'Data Not Collected' label is possible under Apple's definition of 'collect'. This is the main differentiator against cloud-based converters. A content-seeing signer that does not moderate adds little control, because Apple holds you responsible for signed passes either way.

### E5

**Empfehlung:** Host the signing backend and its key with an EU-headquartered provider in an EU or German region, under an Art. 28 AVV. Keep the Pass Type ID private key in a KMS/HSM or encrypted secret store, with access limited to the signing service, rotation documented, and certificate-expiry monitoring.

**Begründung:** DPLA §5.1 key safeguarding and §2.9 Service Provider contract. The DPF adequacy decision is under CJEU appeal (C-703/25 P). EU hosting is also a German marketing point.

### E6

**Empfehlung:** Ship v1 without user accounts. Gate Pro features by sending the StoreKit 2 entitlement JWS (VerificationResult.jwsRepresentation or AppTransaction) with each signing request, verified server-side with app_store_server_library SignedDataVerifier.verify_and_decode_signed_transaction or verify_and_decode_app_transaction (check bundleId, productId, environment, revocationDate). Enforce the free-tier quota with DeviceCheck two-bit flags plus App Attest. Provide 'Restore Purchases'.

**Begründung:** No accounts means no Guideline 4.8, no 5.1.1(v) deletion flow and no user database, so verification stays stateless. DPLA §3.3.3(B) forbids device-ID fingerprinting, and DeviceCheck is the sanctioned mechanism. You must offer a reset contact (DPLA §3.3.9(F)).

### E7

**Empfehlung:** Monetise with a generous free tier (unlimited manual and loyalty-card passes, or N conversions per month) plus a one-time non-consumable 'Pro' unlock, suggested €5.99–9.99. Pro covers PDF and multi-ticket import, batch import, automatic field and date recognition, poster templates, and Apple Watch-optimised layouts. Add an optional yearly subscription only if ongoing server features exist, such as pass updates or backup. No weekly plans. Never void, expire or degrade passes already issued when a purchase is refunded or lapses.

**Begründung:** Attachment 5 §2.3 forbids charging users 'to use Wallet to access Your Pass', and Guideline 4.10 bans monetising Apple services. Guideline 3.1.2(a) requires ongoing value for subscriptions. Competitors' weekly plans draw complaints, NeatPass sets a €4.99 one-time anchor, and iOS 27's native feature makes basic conversion free.

### E8

**Empfehlung:** Map pass styles strictly by document type: boardingPass for flights and rail with a transitType; eventTicket; storeCard; coupon; generic for memberships and gyms. Set expirationDate and relevantDates. Set sharingProhibited=true for personalised tickets.

**Begründung:** Attachment 5 §3.1 (correct template), Guideline 3.2.1(iv) (permitted uses only). The HIG says to set expiration and relevance. sharingProhibited reduces easy duplication of personal tickets.

### E9

**Empfehlung:** Add a ticket-integrity policy in product and ToS. (a) Never let users edit a scanned barcode payload for ticket types; manual entry only for loyalty-card numbers. (b) Detect signed transit barcodes (e.g. UIC 918.3 '#UT' header, VDV-KA) and Deutschlandticket or Verbund Handytickets, then show an issuer-rules warning ('Kopien von Handytickets werden von vielen Verkehrsunternehmen nicht anerkannt', i.e. many transit operators do not accept copies of mobile tickets). (c) Wording: 'QRCode2Wallet übernimmt den Barcode unverändert. Gültigkeit und Kontrolle liegen ausschließlich beim Aussteller.' (The barcode is carried over unchanged; validity and inspection rest solely with the issuer.) (d) The ToS forbids creating passes for tickets the user does not lawfully hold and passing copies to others. (e) Do not advertise sharing or duplicating tickets.

**Begründung:** Transit issuers declare screenshots and copies invalid, the Deutschlandticket is personal with name and date of birth, and §265a and §267 StGB apply to misuse. Re-wrapping does not create validity (signed barcodes, first-scan-wins), but positioning protects against facilitation claims and one-star reviews.

### E10

**Empfehlung:** Build for business continuity: store each pass's source model (payload, format, fields, user images) locally in SwiftData, plus optional CloudKit private database or iCloud sync, so any pass can be regenerated and re-signed under a new certificate or Pass Type ID.

**Begründung:** Apple can revoke the Pass Type ID at any time for any reason (Attachment 5 §4), and a revoked certificate means installed passes 'will no longer function properly' (Apple Certificates overview).

### E11

**Empfehlung:** Position against iOS 27's native 'Create a Pass': import from PDF, screenshot, Photos, Files, Mail or the share sheet; split multi-ticket PDFs; batch import; extract date, time, seat, gate, platform and venue automatically into relevantDates, locations and semantics; parse German rail and flight tickets for display fields; emit iOS 27 multi-barcode fallbacks (e.g. EAN13 plus Code128 or QR); support iOS 18–26 devices and devices without Apple Intelligence; German-language UI and support; no account and 'Data Not Collected'.

**Begründung:** Native Wallet now covers the trivial 'scan one code' case for free on supported devices. Differentiation must target what it reportedly lacks (PDF and batch input, auto-extraction without Apple Intelligence, older OS versions) and what competitors do poorly (aggressive paywalls, ads, privacy).

### E12

**Empfehlung:** Privacy manifest and label: create PrivacyInfo.xcprivacy for the app and any extension, with NSPrivacyTracking=false and NSPrivacyAccessedAPITypes such as UserDefaults 1C8F.1 (App Group) and CA92.1, and FileTimestamp 3B52.1 or C617.1 if used. Leave NSPrivacyCollectedDataTypes empty only if the backend truly persists nothing. If App Attest keys are stored server-side, declare NSPrivacyCollectedDataTypeDeviceID with purpose AppFunctionality, not linked and not tracking. Avoid third-party analytics or crash SDKs in v1, and use Apple's App Analytics and crash reports instead.

**Begründung:** App Store Connect rejects undeclared required-reason API use (since May 1, 2024). Data Apple collects need not be disclosed. TDDDG §25 consent would otherwise be needed for third-party SDKs.

### E13

**Empfehlung:** Prepare the legal documents: a German Datenschutzerklärung (privacy policy, Art. 13) linked in App Store Connect and in the app; Impressum (§5 DDG) in the app and on the website; a custom EULA/ToS in App Store Connect (DPLA Schedule 1 §3.2); records of processing (Art. 30); technical and organisational measures (Art. 32); an AVV with the hosting provider; an abuse and IP contact process. Have a German IT lawyer sign off.

**Begründung:** These are required by Guideline 5.1.1(i), GDPR, DDG and DSA. All legal positions here are non-binding assessments.

### E14

**Empfehlung:** For App Review, use review notes explaining: passes are issued under the developer's own brand and Pass Type ID as a user's personal copy; issuer contact info is on every pass; no third-party logos are provided; barcode data stays on-device; signing is stateless. Provide demo material with fictional brands, and avoid the words 'official' and 'Deutsche Bahn approved'.

**Begründung:** This pre-empts Guideline 1.5, 4.3(b) and 5.2.1 objections. Reviewers judge the presentation of an app whose legality rests on the issuer model.

### E15

**Empfehlung:** Do not build credentialed integrations (DB account, Payback, Lidl Plus or airline account scraping) or pull tickets from third-party APIs without written permission. Import only what the user already has (files, images, camera).

**Begründung:** Guideline 5.2.2 (a third-party service's terms must permit access) and the platforms' ToS. This also reduces the data you handle.

## Fallstricke

1. Mistaking Pass2U's longevity for permission: Guideline 1.5 ('signed with a dedicated certificate assigned to the brand or trademark owner of the pass') and Attachment 5 §1 ('nor use Your Pass Type ID to sign a third party's pass') are on the books. Enforcement against converters is discretionary, and no public revocation case was found (low-confidence absence of evidence).
2. Showing third-party branding as the pass's identity (organizationName 'Lidl', a bundled IKEA logo, DB red with the DB logo) turns your pass into an apparent 'third party's pass' and creates trademark exposure plus an indemnity duty to Apple.
3. Gating already-issued passes behind payment, e.g. voiding passes through webServiceURL when a subscription ends, conflicts with Attachment 5 §2.3 ('may not charge any fees to end users in order to use Wallet to access Your Pass') and likely Guideline 4.10.
4. Silently creating backend 'guest' user records for quotas triggers the account-deletion requirement and privacy-label disclosures. Persisting App Attest keys is device-linked data that must be declared.
5. Logging request bodies or saving uploaded images or PDFs 'for debugging' destroys the 'Data Not Collected' label and the Art. 9 risk position. Under Apple's definition, retention beyond servicing the request counts as collection.
6. Using a cloud OCR or LLM (US provider) without explicit consent violates Guideline 5.1.2(i) (third-party AI) and creates GDPR Chapter V transfer issues.
7. Using the boardingPass style for non-transport items, or marketing generic 'put any QR code (Wi-Fi, URL) into Wallet' features, breaks Attachment 5 §3.1 and Guideline 3.2.1(iv), and Apple warns this can cost the Wallet credentials.
8. Advertising 'works with Deutschlandticket or DB Navigator tickets': issuers state copies and screenshots of Handytickets are invalid, so users can be fined and blame the app. Trademarked names in metadata also breach Guideline 2.3.7.
9. Weekly subscriptions and paywall-after-scan flows match the most-cited user complaints about this category, and Guideline 3.1.2(a) requires ongoing value for subscriptions.
10. Revocation is a single point of failure: a revoked Pass Type ID certificate breaks every installed pass. Without locally stored source data you cannot re-issue. Pass Type ID certificates can only be revoked through product-security@apple.com, so plan for key compromise too.
11. Enrolling as an individual developer publishes your address (or P.O. box), phone and email on the EU App Store page (DSA trader rules) and leaves personal liability unshielded.
12. Hash-only signing means you cannot see or moderate pass content. Abuse (phishing passes impersonating banks) must be limited by App Attest, rate limits and in-app guardrails, because Apple still attributes every signed pass to your Pass Type ID.
13. Building without the iOS 26 SDK or Xcode 26 is rejected at upload (since April 28, 2026). Missing required-reason declarations are also rejected (since May 1, 2024).
14. Assuming iOS 27 users still need a converter for simple loyalty cards: native 'Create a Pass' covers that case for free on Apple Intelligence devices. Positioning on that use case alone invites a Guideline 4.3(b) 'not meaningfully different' rejection and weak conversion.
15. Assuming German law treats the Wallet copy as harmless: personalised tickets (Deutschlandticket with name and date of birth, rail tickets bound to an ID) are non-transferable, and pass sharing would facilitate fare evasion (§265a StGB). Set sharingProhibited=true and avoid share or duplicate features.

## Offene Fragen

1. Will Apple App Review accept the issuer model under Guideline 1.5 for a new 2026/2027 submission, given native 'Create a Pass' in iOS 27? Consider a pre-submission inquiry through App Review contact, or a TestFlight external-review trial early.
2. Does Apple interpret Attachment 5 §2.3 ('may not charge any fees to end users in order to use Wallet to access Your Pass') as also covering a per-pass purchase or a creation quota? No official clarification was found, so a lawyer or Apple contact should confirm before pricing per pass.
3. What exactly does iOS 27 'Create a Pass' support in the shipping build (photo or screenshot import, PDF, region availability in Germany, device requirements)? It was verified only through secondary press and tutorials, because apple.com and support.apple.com were unreachable from this session.
4. Hash-only signing or content-aware signing? This trades GDPR Art. 9 minimisation and privacy-label benefits against the ability to enforce content rules (no logos, correct style) server-side. The product owner should decide, ideally with a data-protection lawyer.
5. Should Deutschlandticket and Verbund app-only Handytickets be blocked outright rather than warned about? This needs review of current Tarifbestimmungen (DB, VDV, major Verbünde) and possibly direct contact with issuers.
6. Is a pass-signing backend that stores nothing an 'intermediary service' or 'hosting service' under the DSA? This decides whether Art. 16 notice-and-action and Art. 11/12 contact points are formally required.
7. Exact current App Store listing data for competitors (prices in EUR, ratings, review texts for Pass2U, NeatPass, Wallet Creator and others) could not be fetched directly (apps.apple.com unreachable). Validate manually in the German App Store before final pricing.
8. Does the App Store's 'Data Not Collected' label remain accurate if App Attest public keys and counters are stored server-side for assertion verification? Apple's guidance suggests this is Device ID collection for App Functionality.
9. Pass Type ID certificate validity period and renewal cadence were not found on the reachable Apple pages. Verify in Certificates, Identifiers & Profiles when the certificate is created, and set monitoring accordingly.
10. Copyright treatment of user-uploaded store logos (UrhG; private copying under §53 UrhG versus the company's involvement in signing the pass) was not verified with primary sources. A German IP lawyer should assess this, together with the ToS indemnity wording.
11. Does the EU Accessibility Act / German BFSG (in force since June 28, 2025) apply to this app, given that in-app sales are made by Apple as commissionaire (DPLA Schedule 2)? There is a microenterprise exemption for services; this was not verified.

## Faktencheck: alle geprüften Aussagen

### P1 · BESTÄTIGT

**Geprüfte Aussage:** The current DPLA was updated August 18, 2026 (page marker 'LYL255 / August 18, 2026'). Section 1.2 defines 'Pass(es)' as digital passes 'developed by You under this Agreement, under Your own trademark or brand, and which are signed with Your Pass Type ID'.

**Ergebnis:** Confirmed: the page shows 'LYL255 / August 18, 2026' and the footer reads 'Developer Program License Agreement, including its Schedule 1 last updated August 18, 2026; Exhibits to Schedule 2 & 3 last updated August 27, 2026'. The quote is cut short, though. The full definition continues '...signed with Your Pass Type ID, or otherwise developed by You in accordance with the Documentation.' Attachment 5 §1 still limits signing to 'Your Pass', so the design impact stands.

**Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### P2 · BESTÄTIGT

**Geprüfte Aussage:** DPLA Attachment 5 §1: the Pass Type ID may be used only to sign 'Your Pass'. Distribution only under Your own trademark or brand, or if you reference a third party's brand you warrant the necessary rights. You may not share or transfer the Pass Type ID (except to a Service Provider) nor use it to sign a third party's pass.

**Ergebnis:** The quote is verbatim. DPLA §5.1 says the same thing independently: 'You will not use Your Apple Certificates to sign any third party's application, pass, extension...'.

**Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### P3 · BESTÄTIGT

**Geprüfte Aussage:** DPLA §3.3.9(B) Wallet: 'Your development of Passes, and use of the Pass Type ID and Wallet under this Agreement, must be in accordance with the terms of this Agreement (including the Program Requirements) and Attachment 5.'

**Ergebnis:** The text is verbatim. It sits under §3.3.9 'Transactions and Passes', item B 'Wallet', and continues '(Additional Terms for Passes)'.

**Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### P4 · BESTÄTIGT

**Geprüfte Aussage:** DPLA Attachment 5 §2.3: state on the Pass the name, address and contact information (telephone; email) for end-user questions, complaints or claims. You are solely responsible for support. 'You may not charge any fees to end users in order to use Wallet to access Your Pass.'

**Ergebnis:** Verbatim. §2.3 also says you are 'responsible for attaching or otherwise including, at Your discretion, any relevant end user usage terms with Your Pass', so a short ToS reference on the back of each pass is supported.

**Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### P5 · BESTÄTIGT

**Geprüfte Aussage:** DPLA Attachment 5 §3.1: choose the relevant template (e.g. not boarding pass for a movie ticket). §3.3: pass data may not be linked with other data for targeted advertising or ad measurement, or shared with data brokers.

**Ergebnis:** Verbatim. Two details were left out. §3.3 allows sharing user or device data between the Pass and your app 'with prior user consent' when it is directly relevant to the Pass or app. §3.1 adds that if you enable a template that shows smart recommendations, Apple may use Pass Information for recommendations (navigation, weather, music), which belongs in the privacy policy.

**Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### P6 · BESTÄTIGT

**Geprüfte Aussage:** Certificates overview, Pass Type ID Certificate: if it expires, installed passes keep working, but you can't sign new passes or send updates; if revoked, passes no longer function properly. Pass Type ID certificates cannot be revoked from the developer account; email product-security@apple.com.

**Ergebnis:** The quote is verbatim on the Certificates overview. The 'cannot revoke from the account' part comes from a different page, Reference &gt; Revoking privileges (https://developer.apple.com/help/account/reference/revoking-privileges/): 'You can't revoke Developer ID or Pass Type ID certificates using your developer account. Instead, send a request to Apple at product-security@apple.com'. The overview adds that after a compromise you can keep distributing passes by requesting an additional certificate, and that 'Apple can revoke digital certificates at any time at its sole discretion.'

**Quelle:** <https://developer.apple.com/help/account/certificates/certificates-overview/>

### P7 · BESTÄTIGT

**Geprüfte Aussage:** DPLA §5.1: all passes must be signed with an Apple Certificate to be accepted by Wallet; you are solely responsible for preventing unauthorized access to your Apple Certificates and keys and must use best efforts to safeguard them.

**Ergebnis:** Verbatim. §5.1 also requires you to 'immediately notify Apple in writing' if you suspect a compromise. Certificates may go to a Service Provider only when it uses them on your behalf. A KMS or hosting provider therefore needs a binding written contract 'at least as restrictive and protective of Apple' (DPLA §2.9).

**Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

### P8 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 1.5 (guidelines last updated June 8, 2026): 'ensure that Wallet passes include valid contact information from the issuer and are signed with a dedicated certificate assigned to the brand or trademark owner of the pass.'

**Ergebnis:** Verbatim, under '1.5 Developer Information'. The page footer reads 'Last Updated: June 8, 2026'. Treating QRCode2Wallet as the 'brand owner of the pass' is the researcher's reading; Apple has not published any confirmation of it.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P9 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 3.2.1(iv): 'Wallet passes can be used to make or receive payments, transmit offers, or offer identification (such as movie tickets, coupons, and VIP credentials). Other uses may result in the rejection of the app and the revocation of Wallet credentials.'

**Ergebnis:** Verbatim, under 3.2.1 'Acceptable'.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P10 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 4.3(b) Spam: 'Don't submit apps that are indistinguishable from what's already widely available.' Guideline 4.2: apps must offer 'adequate utility' beyond a repackaged website.

**Ergebnis:** Both texts are verbatim. The design impact says iOS 27 has native pass creation. That is supported at medium confidence: Apple's newsroom (June 2026) and Apple Support 'Create passes in Wallet on iPhone' describe Wallet &gt; Add Card &gt; Create a Pass, with Standard, Membership and Event templates, manual creation, and photo/screenshot creation with Apple Intelligence. The search engine surfaced these pages, but support.apple.com and apple.com could not be fetched directly in this session.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P11 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 5.2.1: don't use protected third-party trademarks or copyrighted works without permission. Guideline 5.2.2: if the app uses, accesses or displays third-party service content, it must be specifically permitted by that service's terms; authorization on request.

**Ergebnis:** Verbatim. 5.2.2 also covers apps that 'monetize access to' third-party content. 5.2.1 adds: 'Apps should be submitted by the person or legal entity that owns or has licensed the intellectual property and other relevant rights.'

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P12 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 2.3.7: don't pack metadata with trademarked terms, popular app names, etc. Subtitles may not reference other apps.

**Ergebnis:** Verbatim. 2.3.7 also caps app names at 30 characters. Related rules: 2.3.9 makes you responsible for rights to everything in icons, screenshots and previews, and asks for fictional account data. 4.1(c) bars using another developer's icon, brand or product name in your app's icon or name without approval.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P13 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 5.1.1: (i) privacy policy link in App Store Connect and in-app; (iii) use out-of-process picker or share sheet rather than full Photos access; (v) account creation requires in-app deletion; apps without significant account-based features must work without login.

**Ergebnis:** Confirmed, with one wording difference. On third parties, 5.1.1(i) requires the policy to 'confirm that any third party with whom an app shares user data ... will provide the same or equal protection'. It does not ask the policy to 'explain third-party sharing'. 5.1.1(ii) also requires consent for collecting user or usage data 'even if such data is considered to be anonymous'. GDPR legitimate interest is allowed if you comply fully with GDPR.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P14 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 5.1.2(i): 'You must clearly disclose where personal data will be shared with third parties, including with third-party AI, and obtain explicit permission before doing so.'

**Ergebnis:** Verbatim.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P15 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 4.8: an app using a third-party or social login for the primary account must also offer an equivalent login service (name+email only, private email option, no ad-interaction collection without consent); not required if the app exclusively uses the company's own account system.

**Ergebnis:** Verbatim. The claim lists only one exemption. The guideline also exempts alternative marketplaces, education/enterprise accounts, government or industry eIDs, and clients for a specific third-party service. Sign in with Apple is not mandated by name; any login service with these properties qualifies.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P16 · BESTÄTIGT

**Geprüfte Aussage:** Account deletion guidance: apps that create accounts, including automatically created 'guest' accounts, must let people initiate deletion in-app; deactivation alone insufficient; Sign in with Apple apps should revoke tokens via the SIWA REST API.

**Ergebnis:** Verbatim, including the FAQ: 'People should have the option to delete automatically generated accounts (sometimes called "guest" accounts)'.

**Quelle:** <https://developer.apple.com/support/offering-account-deletion-in-your-app/>

### P17 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 3.1.1: unlocking features must use IAP, not license keys or QR codes. 3.1.2(a): auto-renewable subscriptions must provide ongoing value and last at least seven days.

**Ergebnis:** The quotes are verbatim. 3.1.2(a) also requires subscriptions to 'be available across all of the user's devices'. 'StoreKit 2 only' is a design choice; no guideline requires it. Two exceptions were missed. On the United States storefront, apps may include buttons, external links or other calls to action to other purchase methods without an entitlement (3.1.1(a)). In the EU, DPLA Attachment 14 (effective Oct 1, 2026) allows Alternative Payment Processing and Out-of-App Offers.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P18 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 4.10: you may not monetize built-in hardware/OS capabilities (Push Notifications, camera, gyroscope) or Apple services (Apple Music access, iCloud storage, Screen Time APIs). Whether it covers Wallet is not stated.

**Ergebnis:** Verbatim. The examples do not mention Wallet. The researcher's medium confidence on applying it to Wallet is appropriate.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P19 · BESTÄTIGT

**Geprüfte Aussage:** Guideline 5.1.1(ix): apps providing services in highly regulated fields (list includes 'air travel') or requiring sensitive user information 'should be submitted by a legal entity that provides the services, and not by an individual developer'.

**Ergebnis:** Verbatim. The list reads 'banking and financial services, healthcare, gambling, legal cannabis use, air travel and crypto exchanges'.

**Quelle:** <https://developer.apple.com/app-store/review/guidelines/>

### P20 · BESTÄTIGT

**Geprüfte Aussage:** App Privacy Details: 'Collect' = transmitting off device and storing in readable form longer than needed to service the request; data sent to your servers and immediately discarded need not be disclosed; on-device-only data is not collected; you are not responsible for disclosing data collected by Apple.

**Ergebnis:** All three quotes are verbatim. The same page also says: 'You collect and store IP address from your users. Declare the relevant data types based on how you use IP address, such as precise location, coarse location, device ID, or diagnostics.' Any retained IP logs or server-stored per-device keys therefore cancel the 'Data Not Collected' label.

**Quelle:** <https://developer.apple.com/app-store/app-privacy-details/>

### P21 · BESTÄTIGT

**Geprüfte Aussage:** Privacy manifest PrivacyInfo.xcprivacy with top-level keys NSPrivacyTracking, NSPrivacyTrackingDomains, NSPrivacyCollectedDataTypes, NSPrivacyAccessedAPITypes. 'Starting May 1, 2024, apps that don't describe their use of required reason API in their privacy manifest file aren't accepted by App Store Connect.'

**Ergebnis:** The keys are verified on the privacy-manifest-files page. The May 1, 2024 sentence is on 'Describing use of required reason API' (https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api). That page also says each executable or dynamic library that uses a required-reason API needs a manifest in its own bundle, so extensions need their own.

**Quelle:** <https://developer.apple.com/documentation/bundleresources/privacy-manifest-files>

### P22 · KORRIGIERT

**Geprüfte Aussage:** Required-reason codes: UserDefaults CA92.1, 1C8F.1; FileTimestamp DDA9.1, C617.1, 3B52.1; DiskSpace 85F4.1, E174.1; SystemBootTime 35F9.1.

**Ergebnis:** Every code listed is correct, but each list is incomplete. Full sets: UserDefaults CA92.1, 1C8F.1, C56D.1 (third-party SDK wrapper only), AC6B.1 (MDM managed config). FileTimestamp DDA9.1 (display only, may not leave the device), C617.1 (files in the app, App Group or CloudKit container), 3B52.1 (user-granted files, e.g. document picker), 0A2A.1 (SDK wrapper only). DiskSpace 85F4.1, E174.1, 7D9E.1 (optional user bug report), B728.1 (health research). SystemBootTime 35F9.1, 8FFB.1 (absolute event timestamps, may be sent off device), 3D61.1 (optional bug report). There is also a category the claim leaves out: NSPrivacyAccessedAPICategoryActiveKeyboards (3EC4.1, 54BD.1).

**Quelle:** <https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitype>

### P23 · BESTÄTIGT

**Geprüfte Aussage:** Since April 28, 2026 uploads must use Xcode 26+ and iOS 26 SDK; since September 9, 2026 iOS apps must target iOS 13+; age-rating questions due January 31, 2026; DSA trader status required for EU since February 17, 2025, otherwise removed from EU App Store.

**Ergebnis:** All four items appear verbatim on the Upcoming Requirements page. DSA trader status has also been required for app updates in the EU since February 18, 2025, per an earlier entry on the same page.

**Quelle:** <https://developer.apple.com/news/upcoming-requirements/>

### P24 · BESTÄTIGT

**Geprüfte Aussage:** Under DSA Arts. 30 and 31 Apple verifies and displays trader address, phone and email on the EU product page. Individuals enter an 'Address or P.O. Box'; organisations display the D-U-N-S address.

**Ergebnis:** Confirmed. The design impact needs fixing. An individual may show a P.O. Box (with documents proving the association). An organisation cannot choose: the D-U-N-S address is displayed automatically, and for a small UG that is often the founder's home. Enrolling as an organisation therefore does not by itself keep a home address off the product page. A German Impressum (§5 DDG) also needs a summonable postal address ('ladungsfähige Anschrift') regardless; that is general German law, not verified in this session.

**Quelle:** <https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements/>

### P25 · BESTÄTIGT

**Geprüfte Aussage:** No Apple per-pass fee; DPLA/Attachment 5 describe distribution 'by the web, email, or an Application' with no per-pass charge; signing uses your own certificate.

**Ergebnis:** Attachment 5 §2.1 allows distribution 'by the web, email, or an Application'. The only fee Attachment 5 mentions bans you from charging end users to access a pass in Wallet; there is no fee payable to Apple. The real prerequisite is the paid Developer Program membership: if it expires, you lose access to Certificates, Identifiers & Profiles (https://developer.apple.com/help/account/membership/renewal/). The per-pass compute and size figures in the design impact were not verified.

**Quelle:** <https://developer.apple.com/support/terms/apple-developer-program-license-agreement/>

## Vom Faktenprüfer ergänzte wichtige Fakten

1. WRONG SECTION IN A RECOMMENDATION: the DeviceCheck reset-contact duty is DPLA §3.3.7(F) 'DeviceCheck APIs' (under 3.3.7 Infrastructure Technologies), not §3.3.9(F). It also says 'You may not rely on the DeviceCheck Data as a single identifier of fraudulent conduct' and Apple may delete DeviceCheck data at any time. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
2. DESIGN CONTRADICTION, App Attest vs 'persist nothing / stateless'. Apple's App Attest server guide requires you to 'Store the verified public key ... on your server and associate it with the user for the specific device', and on every assertion to check the counter is 'greater than the value from the previous assertion' and then 'Store counter'. App Attest assertions therefore cannot be verified without per-device state on the server. That state is server-side collected data (likely NSPrivacyCollectedDataTypeDeviceID, purpose NSPrivacyCollectedDataTypePurposeAppFunctionality), so the 'Data Not Collected' label is incompatible with App Attest-gated signing. Source: https://developer.apple.com/documentation/devicecheck/validating-apps-that-connect-to-your-server
3. DESIGN CONTRADICTION, 7-day IP logs vs 'Data Not Collected'. Apple's App Privacy FAQ: 'You collect and store IP address from your users. Declare the relevant data types based on how you use IP address, such as precise location, coarse location, device ID, or diagnostics.' Only an IP address that is 'sent on a server call and not retained' is exempt. Keeping IP logs for 7 days means declaring a data type, e.g. Other Diagnostic Data. Source: https://developer.apple.com/app-store/app-privacy-details/
4. DESIGN CONTRADICTION, the optional subscription 'pass updates or backup'. Pass updates via webServiceURL require the server to store per-device registrations and push tokens, which is collected Device ID data and cancels 'Data Not Collected'. DPLA Attachment 1 §1.2 also requires you to 'disclose to Apple any use of the APN as part of the submission process'. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
5. HASH-ONLY SIGNING CREATES A SIGNING ORACLE. If the backend signs any manifest.json without seeing pass.json, a modified client that gets past App Attest can have arbitrary passes signed with your Pass Type ID, including passes that impersonate brands. That collides with three rules: DPLA §5.1 ('solely responsible for preventing any unauthorized person or organization from having access to Your Apple Certificates and keys'; must not sign third-party passes); Attachment 5 §1; and Guideline 3.2.1(iv), which allows 'revocation of Wallet credentials'. The server also cannot enforce the mandatory issuer contact block (Attachment 5 §2.3, Guideline 1.5) or the correct template (Attachment 5 §3.1). Attachment 5 §4 adds that Apple may review any Pass 'already in use' and 'If requested by Apple, You agree to promptly provide such Pass'. Consider sending pass.json, which is small, to the server for schema and policy validation (passTypeIdentifier, teamIdentifier, organizationName, required backFields, allowed style), then discarding it, while images stay hash-only. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
6. DPLA Attachment 5 §2.4: by distributing passes you 'permit Apple to use (i) screenshots of Your Pass; (ii) trademarks and logos associated with Your Pass; and (iii) Pass Information, for promotional purposes ... excluding those portions which You do not have the right to use for promotional purposes and which You identify in writing to Apple.' DPLA §10(iv) makes you indemnify Apple for its permitted use of your Pass and Pass Information. User-generated passes contain third-party marks and personal data, so send Apple a written exclusion notice. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
7. DPLA §3.2: you will not use Apple Software or Services 'to develop any Covered Product ... which would commit or facilitate the commission of a crime, or other tortious, unlawful or illegal act'. This is the Apple-side contractual basis for the ticket-integrity policy against ticket duplication and fare evasion. The same section has a 'Pass Information' non-infringement warranty ('to the best of Your knowledge and belief'), which covers content users provide (DPLA definition of 'Pass Information'). Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
8. Attachment 5 §2.1: passes 'can be removed or transferred by such users at any time'. The Pass reference for sharingProhibited (iOS 11+) says it 'removes the button' (Share) and does not 'prevent sharing the pass in some other way'. Treat it as a UX hint, not a control. Sources: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/ and https://developer.apple.com/documentation/walletpasses/pass
9. NFC is out of scope without Apple approval. Attachment 5 §3.4: using NFC with a Pass requires requesting a separate Apple Certificate; Apple 'may provide You with a separate agreement' and 'reserves the right to not provide' it. Cards that work only by NFC (many transit and some loyalty cards) cannot be converted; the product must say it handles barcode and QR cards only. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
10. Barcode formats (product scope, verified): Pass.Barcodes docs say 'In iOS 27 and later, you can provide more than one barcode as a fallback' and Wallet supports QR, PDF 417, Aztec, Code 128, Code 39, Codabar, EAN 13 and ITF. Before iOS 27 only QR, PDF417, Aztec and Code128 render. EAN-13 loyalty cards need a QR or Code128 fallback for iOS 26 and earlier, and scanner acceptance of a re-encoded barcode is not guaranteed. Source: https://developer.apple.com/documentation/walletpasses/pass/barcodes-data.dictionary
11. EU monetisation terms changed: DPLA Attachment 14 'Additional Terms for Apps in the European Union' takes effect October 1, 2026 and replaces the earlier EU Alternative Terms and External Purchase Link addenda. Rates: IAP commission 26%, or 15% for Small Business Program members (§3.5(B)). Alternative Payment Processing 20%/10% (§3.5(A)). Out-of-App Offers 15%/10% store services commission (§3.5(C)). The researcher's '15% vs 26%' is correct for IAP under this attachment. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
12. EULA citation fix: once the app sells In-App Purchases, it falls under DPLA Schedule 2 (fee-based apps; Apple acts as agent or commissionaire). A custom EULA goes under Schedule 2 §4.2 and must contain the minimum terms in Exhibit D. Schedule 1 §3.2 applies to free apps only. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
13. Organisation enrollment has more prerequisites than a D-U-N-S number. Apple requires a legal entity ('We don't accept DBAs, fictitious businesses, trade names, or branches'). The organisation 'must be publicly available and functional' on a website 'and its domain name must be associated with your organization'. Enrollment includes a binding-authority check. An individual's 'personal legal name will be listed as the seller'. Source: https://developer.apple.com/help/account/membership/program-enrollment/
14. APP NAME RISK, 'QRCode2Wallet' (medium/low confidence, secondary sources only; qrcode.com and EUIPO were unreachable). The word 'QR Code' is reported as a registered trademark of DENSO WAVE INCORPORATED in Japan and other countries, with an EU registration reported. The name also uses 'Wallet', Apple's app name. The Add to Apple Wallet guidelines say Wallet messaging 'cannot be used in any manner that falsely suggests an association with Apple', 'Do not use the Wallet icon alone', and in apps you should 'use the PKAddPassButton class'. Guideline 5.2.5 bars apps that look confusingly similar to an Apple app. A name built on 'QR code to Wallet' also suggests 'any QR code', which conflicts with Guideline 3.2.1(iv)'s limit on permitted pass uses. Get a trademark clearance (DPMA/EUIPO) before branding. Sources: https://developer.apple.com/wallet/add-to-apple-wallet-guidelines/ , https://developer.apple.com/app-store/review/guidelines/ , https://www.jpo.go.jp/e/news/koho/innovation/01_qrcode_e.html
15. iOS 27 native pass creation (medium confidence; Apple pages seen only via search snippets). The newsroom (June 2026) and Apple Support 'Create passes in Wallet on iPhone' describe Wallet &gt; Add Card &gt; Create a Pass with Standard, Membership and Event templates and a 'Create Pass Manually' path. Creating from a photo or screenshot requires Apple Intelligence, and a Siri Mode support article names iPhone 15 Pro or later. Press reports say only predefined field areas can be edited. Apple also shipped Pass Designer (macOS 27) and 'Pass Builder', a Swift-on-server package for building and signing passes, which is a first-party alternative to a Python signer. Sources: https://developer.apple.com/wallet/whats-new/ , https://support.apple.com/guide/iphone/create-passes-el8l5r9jnhyv/ios , https://www.macrumors.com/2026/06/08/ios-27-wallet-create-pass
16. DPLA §3.3.3(B): 'may not collect user or device data without prior user consent ... and then only to provide a service or function that is directly relevant'. This is stricter on its face than GDPR Art. 6(1)(f). Guideline 5.1.1(ii) accepts GDPR legitimate interest if the law is fully complied with, but any server-side retention (IP logs, App Attest keys) should be disclosed in-app and in the privacy policy. DPLA §3.3.3(C) also requires notifying users of a breach involving data collected from the app. Source: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
17. Foundation Models: DPLA §3.3.11(A) binds you to the 'Foundation Models Framework Acceptable Use Requirements', for example no use that 'Infringes or violates the intellectual property, publicity, or privacy rights of another' or that 'Engages in any kind of fraud, deception'. On-device field extraction from tickets is not prohibited, but keep reasonable guardrails. Source: https://developer.apple.com/apple-intelligence/acceptable-use-requirements-for-the-foundation-models-framework/
18. Monetisation options the researcher did not mention. Guideline 3.1.1 allows non-subscription apps a free time-based trial through a Non-Consumable IAP 'at Price Tier 0' named 'XX-day Trial', which must disclose its duration and the later charges. Credits bought via IAP 'may not expire', and you need a restore mechanism. Source: https://developer.apple.com/app-store/review/guidelines/
19. Export compliance at submission: add ITSAppUsesNonExemptEncryption to Info.plist and set it to NO if the app only uses OS-provided encryption such as HTTPS via URLSession. Apple notes exempt apps 'might alternatively be required to submit a year-end self-classification report to the U.S. government'. Schedule 2 §2.3 makes you certify export compliance. Source: https://developer.apple.com/documentation/security/complying-with-encryption-export-regulations
20. Trademark exception (not verified in this session; EUR-Lex unreachable): Art. 14(1)(c) EUTMR (Reg. 2017/1001) and §23 MarkenG allow using a mark 'for the purpose of identifying or referring to goods or services as those of the proprietor', but only 'in accordance with honest practices'. This supports showing a user-entered store name as plain text to identify the card. It does not cover logos or trade dress. Low confidence; needs a German IT/IP lawyer.
21. Accessibility (low confidence): App Store Accessibility Nutrition Labels are currently voluntary (App Store Connect Help). The EU Accessibility Act / German BFSG has exemptions for microenterprises, and this was not verified for an IAP-only app. Source: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels
