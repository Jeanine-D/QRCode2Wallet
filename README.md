# QRCode2Wallet (Arbeitstitel)

Native iOS-App, die vorhandene **Tickets, Kundenkarten, Bordkarten, Coupons und Mitgliedskarten** in **Apple-Wallet-Pässe** umwandelt. Als Quelle dienen Foto, Screenshot, PDF oder Live-Kamera.

## Status

> **Übergabe und Wiedereinstieg:** siehe [HANDOFF.md](HANDOFF.md)

| Phase | Stand |
|---|---|
| Grundsatzentscheidungen | ✅ getroffen (siehe unten) |
| Recherche | ✅ abgeschlossen, gegengeprüft: [docs/recherche/](docs/recherche/README.md) |
| Konzept | ⏸️ wartet auf Freigabe und die [offenen Entscheidungen](docs/recherche/README.md#5-offene-entscheidungen-für-den-product-owner) |
| MVP (iOS-App + Backend) | ⏸️ wartet auf Freigabe |

## Grundsatzentscheidungen (10.10.2026)

| Frage | Entscheidung |
|---|---|
| Wallet-Plattform | **Nur Apple Wallet** |
| App-Form | **Native Mobile-App**: iOS mit SwiftUI, weil nur Apple Wallet unterstützt wird |
| Zielgruppe | **Öffentliches Produkt** (App Store) |
| Lieferumfang | **Konzept + lauffähiges MVP** |
| Signierung | **Python-Backend (FastAPI)**: Der private Signierschlüssel darf nie in die App |

## Geplante Struktur

```
docs/        Recherche, Konzept, API-Vertrag, Apple-Setup-Anleitung
backend/     Python/FastAPI-Signierdienst (.pkpass-Erzeugung)
ios/         SwiftUI-App (XcodeGen-Projekt)
```

## Wichtigste Erkenntnisse aus der Recherche

Die Details mit Quellen stehen in der [Recherche-Übersicht](docs/recherche/README.md).

- **Technisch machbar.** Die Signierung in Python ist verifiziert, und iOS bringt alle nötigen Frameworks mit.
- **iOS 27 kann in Wallet selbst Pässe erstellen.** Das Produkt muss sich deshalb klar abheben: PDF- und Mehrfach-Tickets, Bahn- und Flugtickets, automatische Felderkennung, ältere iOS-Versionen, Datenschutz.
- **Apples Lizenzvertrag und Review-Richtlinien** verlangen ein **Issuer-Modell**: Jeder Pass erscheint unter der eigenen Marke als „persönliche digitale Kopie“, ohne Fremdlogos und mit Kontaktdaten des Ausstellers.
- **Der Signierdienst ist das wichtigste Gut.** Nötig sind App Attest, Quoten und ein Schlüssel im KMS/HSM in einer EU-Region.
