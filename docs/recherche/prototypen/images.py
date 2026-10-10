"""Default pass images with Pillow (sizes in points; Apple Pass Builder 2026: icon 38x38 required, logo max 160x50)."""
import io
from PIL import Image, ImageDraw, ImageFont

def _png(img: Image.Image) -> bytes:
    b = io.BytesIO(); img.save(b, format="PNG", optimize=True); return b.getvalue()

def _hex(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#"); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))

def icon_set(initials: str, bg: str = "#1F6FEB", fg: str = "#FFFFFF", pt: int = 38) -> dict[str, bytes]:
    out = {}
    for scale, suffix in ((1, ""), (2, "@2x"), (3, "@3x")):
        s = pt * scale
        img = Image.new("RGB", (s, s), _hex(bg))           # square, opaque; system rounds corners
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default(size=int(s * 0.45))  # Pillow >= 10.1 (FreeType default font)
        d.text((s / 2, s / 2), initials[:2].upper(), font=font, fill=_hex(fg), anchor="mm")
        out[f"icon{suffix}.png"] = _png(img)
    return out

def logo_set(text: str, fg: str = "#FFFFFF", max_w: int = 160, h: int = 50) -> dict[str, bytes]:
    out = {}
    for scale, suffix in ((1, ""), (2, "@2x"), (3, "@3x")):
        H = h * scale
        font = ImageFont.load_default(size=int(H * 0.5))
        w = min(int(font.getlength(text)) + 4 * scale, max_w * scale)
        img = Image.new("RGBA", (max(w, 50 * scale), H), (0, 0, 0, 0))  # transparent
        ImageDraw.Draw(img).text((0, H / 2), text, font=font, fill=_hex(fg) + (255,), anchor="lm")
        out[f"logo{suffix}.png"] = _png(img)
    return out

def normalize_user_image(data: bytes, box_pt: tuple[int, int], max_pixels: int = 40_000_000) -> dict[str, bytes]:
    """Re-encode untrusted uploads: decompression-bomb guard, strip metadata/EXIF, fit to box at @1x/@2x/@3x."""
    Image.MAX_IMAGE_PIXELS = max_pixels                     # Pillow raises DecompressionBombError above 2x this
    with Image.open(io.BytesIO(data)) as im:
        im.verify()
    with Image.open(io.BytesIO(data)) as im:
        im = im.convert("RGBA")
        out = {}
        for scale, suffix in ((1, ""), (2, "@2x"), (3, "@3x")):
            c = im.copy(); c.thumbnail((box_pt[0] * scale, box_pt[1] * scale), Image.Resampling.LANCZOS)
            out[suffix] = _png(c)
        return out
