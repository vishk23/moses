import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from src.config import INPUT_DIR

BASE_URL = "https://bcsb.identifi.net"
SEARCH_URL = f"{BASE_URL}/api/documents/kwyk-search"
DOC_URL_TMPL = f"{BASE_URL}/api/document/{{storage_type_id}}/{{pkid}}"

# Basic security: require HTTPS
if not BASE_URL.lower().startswith("https://"):
    raise RuntimeError(f"Insecure BASE_URL detected: {BASE_URL}. Use HTTPS.")

# Load environment variables from local .env next to this file
_ENV_PATH = Path(__file__).parent / ".env"
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)

# Set your API key and header name from environment
# IDENTIFI_API_KEY: required
# IDENTIFI_KEY_HEADER_NAME: defaults to x-api-key; set to Authorization if Bearer
# IDENTIFI_USE_BEARER: "true" to prefix with Bearer
API_KEY = os.getenv("IDENTIFI_API_KEY", "")
KEY_HEADER_NAME = os.getenv("IDENTIFI_KEY_HEADER_NAME", "x-api-key")
USE_BEARER = os.getenv("IDENTIFI_USE_BEARER", "false").lower() == "true"

# Optional headers sometimes required by the service
_REFERER = os.getenv("IDENTIFI_REFERER")
_ORIGIN = os.getenv("IDENTIFI_ORIGIN")
_UA = os.getenv(
    "IDENTIFI_UA",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
)

def _auth_headers():
    if KEY_HEADER_NAME.lower() == "authorization":
        token = f"Bearer {API_KEY}" if USE_BEARER and not str(API_KEY).lower().startswith("bearer ") else API_KEY
        return {"Authorization": token}
    return {KEY_HEADER_NAME: API_KEY}

def _dbg(msg: str):
    print(f"[api_call] {msg}")

def get_latest_document(criteria_value: str = "CO_VSUS", results_limit: int = 100) -> dict | None:
    # Build the JSON payload exactly like DevTools shows under Request Payload
    payload = {
        "criteria": [
            {
                "values": [{"comparisonOperator": 1, "value1": criteria_value}],
                "attributeInternalName": "DocumentTypeDisplayName",
                "displayName": "Document Type",
                "dataType": 1,
            }
        ],
        "sortBy": "StorageDate",
        "sortDirection": 1,
        "resultsLimit": results_limit,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": _UA,
        "disable-global-loading-indicator": "true",
        **_auth_headers(),
    }
    if _REFERER:
        headers["Referer"] = _REFERER
    if _ORIGIN:
        headers["Origin"] = _ORIGIN

    _dbg(f"SEARCH begin -> url={SEARCH_URL}")
    _dbg(f"SEARCH headers keys: {list(headers.keys())}")
    _dbg(f"SEARCH criteria={criteria_value} sortBy=StorageDate sortDirection=1 limit={results_limit}")
    with requests.Session() as s:
        if not API_KEY:
            raise RuntimeError("IDENTIFI_API_KEY is not set. Provide it in .env next to api_call.py or as an environment variable.")
        r = s.post(SEARCH_URL, json=payload, headers=headers, timeout=30)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            # Helpful debug if 401/403/etc.
            raise RuntimeError(f"Search failed: {r.status_code} {r.text[:500]}")

        _dbg(f"SEARCH response: status={r.status_code} ctype={r.headers.get('Content-Type')} len={len(r.content)}")
        data = r.json()
        # results are already descending by StorageDate based on sort; take the first
        results = data.get("results", [])
        _dbg(f"SEARCH results count={len(results)}")
        if not results:
            return None
        doc = results[0]
        pkid = doc.get("PKID")
        _dbg(f"PKID: {pkid}")
        # Some APIs include a downloadUrl in the `info` array; log presence
        has_download_url = any((info or {}).get("downloadUrl") for info in (doc.get("info") or []))
        _dbg(f"SEARCH first doc has downloadUrl={has_download_url}")
        return doc

def fetch_latest_to_input(criteria_value: str = "CO_VSUS", storage_type_id: int = 1,
                          filename_template: str = "CO_VSUS_{pkid}.txt") -> Path | None:
    """Search for latest PKID and download the document into INPUT_DIR as .txt.

    Returns the destination Path if downloaded, else None.
    """
    _dbg("FETCH latest -> start")
    doc = get_latest_document(criteria_value=criteria_value)
    if not doc:
        _dbg("FETCH latest -> no documents found")
        return None
    pkid = doc.get("PKID")
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = INPUT_DIR / filename_template.format(pkid=pkid)
    _dbg(f"FETCH latest -> destination={dest}")
    # Prefer explicit downloadUrl if provided by API
    download_url = None
    for info in (doc.get("info") or []):
        if info and info.get("downloadUrl"):
            download_url = info["downloadUrl"]
            break
    _dbg(f"FETCH latest -> using override_url={bool(download_url)}")
    download_document(pkid, dest, storage_type_id=storage_type_id, override_url=download_url)
    return dest

def download_document(pkid, dest_path, storage_type_id=1, override_url: str | None = None):
    if not pkid:
        raise ValueError("pkid is required")

    # Candidate URLs to try until we get non-JSON content
    candidates = []
    if override_url:
        candidates.append(override_url if override_url.startswith("http") else f"{BASE_URL}{override_url}")
    candidates.extend([
        DOC_URL_TMPL.format(storage_type_id=storage_type_id, pkid=pkid),
        f"{BASE_URL}/api/document/{storage_type_id}/{pkid}/file",
        f"{BASE_URL}/api/document/{storage_type_id}/{pkid}/content",
        f"{BASE_URL}/api/document/{storage_type_id}/{pkid}?download=true",
    ])
    _dbg(f"DOWNLOAD pkid={pkid} -> candidates={candidates}")

    headers = {
        # Site reports mimeType "text/report" for PRN; prefer that
        "Accept": "text/report, application/octet-stream, */*",
        "User-Agent": _UA,
        "disable-global-loading-indicator": "true",
        **_auth_headers(),
    }
    if _REFERER:
        headers["Referer"] = _REFERER
    if _ORIGIN:
        headers["Origin"] = _ORIGIN

    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    last_error = None
    with requests.Session() as s:
        for url in candidates:
            try:
                with s.get(url, headers=headers, stream=True, timeout=60) as r:
                    try:
                        r.raise_for_status()
                    except requests.HTTPError as e:
                        last_error = f"{r.status_code} {r.text[:300]}"
                        _dbg(f"DOWNLOAD try url={url} -> HTTPError {last_error}")
                        continue
                    ctype = (r.headers.get("Content-Type") or "").lower()
                    _dbg(f"DOWNLOAD try url={url} -> status={r.status_code} ctype={ctype}")
                    if "json" in ctype:
                        # JSON likely means metadata or error; try next candidate
                        try:
                            last_error = r.json()
                        except Exception:
                            last_error = r.text[:300]
                        _dbg(f"DOWNLOAD try url={url} -> got JSON, skipping. Preview={str(last_error)[:180]}")
                        continue
                    with open(dest, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024 * 64):
                            if chunk:
                                f.write(chunk)
                    _dbg(f"DOWNLOAD success -> wrote bytes={dest.stat().st_size} to {dest}")
                    return dest
            except requests.RequestException as e:
                last_error = str(e)
                _dbg(f"DOWNLOAD try url={url} -> RequestException {last_error}")
                continue
    _dbg(f"DOWNLOAD failed -> tried={len(candidates)} last_error={last_error}")
    raise RuntimeError(f"Download failed for pkid={pkid}. Tried {len(candidates)} URLs. Last response: {last_error}")
    return dest

# No top-level execution in this module