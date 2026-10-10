import os, sys, base64, pathlib, io, zipfile, json
T = pathlib.Path(sys.argv[1]); sys.path.insert(0, str(pathlib.Path(__file__).parent))
os.environ["Q2W_PASS_P12_B64"] = base64.b64encode((T/"pass.p12").read_bytes()).decode()
os.environ["Q2W_PASS_P12_PASSWORD"] = "testpw"
os.environ["Q2W_WWDR_PEM"] = (T/"wwdr.pem").read_text()
from fastapi.testclient import TestClient
from app import app
c = TestClient(app)
body = {"description": "Fitnessstudio Mitgliedskarte", "logoText": "FitX", "style": "storeCard",
        "backgroundColor": "rgb(20, 20, 20)", "foregroundColor": "rgb(255,255,255)",
        "barcode": {"format": "PKBarcodeFormatCode128", "message": "123456789"},
        "primary": [{"key": "member", "label": "Mitglied", "value": "Erika Mustermann"}]}
r = c.post("/v1/passes", json=body)
print(r.status_code, r.headers["content-type"], r.headers["content-disposition"], len(r.content))
z = zipfile.ZipFile(io.BytesIO(r.content)); print(sorted(z.namelist()))
(T/"api.pkpass").write_bytes(r.content); z.extractall(T/"api_out")
print(json.loads(z.read("pass.json"))["passTypeIdentifier"])
r2 = c.post("/v1/passes", json=body | {"passTypeIdentifier": "pass.evil"}); print("extra field ->", r2.status_code)
r3 = c.post("/v1/passes", content=b"{" + b" " * (300 * 1024) + b"}", headers={"content-type": "application/json"}); print("oversize ->", r3.status_code)
