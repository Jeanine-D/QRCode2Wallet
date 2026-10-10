"""FastAPI signing service sketch (stateless). Run: uvicorn app:app"""
from __future__ import annotations
import logging, secrets, uuid
from functools import lru_cache
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field, SecretBytes, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.middleware.body_limit import RequestBodyLimitMiddleware   # Starlette >= 1.6.0

from images import icon_set, logo_set
from pkpass import PKPASS_MEDIA_TYPE, PassSigner, build_pkpass

log = logging.getLogger("pkpass")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="Q2W_", env_file=".env", secrets_dir="/run/secrets")
    pass_p12_b64: SecretStr                 # or load from KMS/Secret Manager at startup
    pass_p12_password: SecretStr
    wwdr_pem: str
    max_body_bytes: int = 256 * 1024
    organization_name: str = "QRCode2Wallet"

@lru_cache
def settings() -> Settings:
    return Settings()

@lru_cache
def signer() -> PassSigner:
    import base64
    s = settings()
    return PassSigner.from_p12(base64.b64decode(s.pass_p12_b64.get_secret_value()),
                               s.pass_p12_password.get_secret_value().encode(), s.wwdr_pem.encode())

BarcodeFormat = Literal["PKBarcodeFormatQR", "PKBarcodeFormatPDF417", "PKBarcodeFormatAztec", "PKBarcodeFormatCode128"]

class Barcode(BaseModel):
    model_config = ConfigDict(extra="forbid")
    format: BarcodeFormat
    message: Annotated[str, Field(min_length=1, max_length=2048)]
    messageEncoding: Literal["iso-8859-1", "utf-8"] = "iso-8859-1"
    altText: Annotated[str | None, Field(max_length=64)] = None

class FieldIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    key: Annotated[str, Field(pattern=r"^[A-Za-z0-9_]{1,32}$")]
    label: Annotated[str | None, Field(max_length=40)] = None
    value: Annotated[str, Field(max_length=120)]

class PassRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    style: Literal["generic", "storeCard", "eventTicket", "coupon", "boardingPass"] = "generic"
    description: Annotated[str, Field(min_length=1, max_length=80)]
    logoText: Annotated[str | None, Field(max_length=30)] = None
    backgroundColor: Annotated[str | None, Field(pattern=r"^rgb\(\d{1,3}, ?\d{1,3}, ?\d{1,3}\)$")] = None
    foregroundColor: Annotated[str | None, Field(pattern=r"^rgb\(\d{1,3}, ?\d{1,3}, ?\d{1,3}\)$")] = None
    barcode: Barcode
    primary: Annotated[list[FieldIn], Field(max_length=1)] = []
    secondary: Annotated[list[FieldIn], Field(max_length=4)] = []
    back: Annotated[list[FieldIn], Field(max_length=10)] = []

app = FastAPI(title="QRCode2Wallet signer", docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(RequestBodyLimitMiddleware, max_body_size=256 * 1024)

@app.post("/v1/passes", response_class=Response,
          responses={200: {"content": {PKPASS_MEDIA_TYPE: {}}}})
def create_pass(req: PassRequest, s: Annotated[PassSigner, Depends(signer)]) -> Response:
    serial = uuid.uuid4().hex                                   # server-chosen; never client-chosen
    pj = {
        "formatVersion": 1, "serialNumber": serial, "description": req.description,
        "organizationName": settings().organization_name,
        "sharingProhibited": False,
        "barcodes": [req.barcode.model_dump(exclude_none=True)],
        req.style: {"primaryFields": [f.model_dump(exclude_none=True) for f in req.primary],
                    "secondaryFields": [f.model_dump(exclude_none=True) for f in req.secondary],
                    "backFields": [f.model_dump(exclude_none=True) for f in req.back]},
    }
    if req.style == "boardingPass":
        pj[req.style]["transitType"] = "PKTransitTypeGeneric"
    for k in ("logoText", "backgroundColor", "foregroundColor"):
        if getattr(req, k):
            pj[k] = getattr(req, k)
    files = icon_set((req.logoText or req.description)[:2]) | logo_set(req.logoText or "")
    data = build_pkpass(s, pj, files)
    log.info("pass_signed", extra={"serial": serial, "style": req.style, "bytes": len(data)})  # no PII / no barcode content
    return Response(content=data, media_type=PKPASS_MEDIA_TYPE,
                    headers={"Content-Disposition": f'attachment; filename="{serial}.pkpass"',
                             "Cache-Control": "no-store"})
