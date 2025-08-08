import os
from pathlib import Path
import requests
from dotenv import load_dotenv

BASE_URL = "https://randomorg.identifi.net"
SEARCH_URL = f"{BASE_URL}/api/documents/kwyk-search"
DOC_URL_TMPL = f"{BASE_URL}/api/document/{{storage_type_id}}/{{pkid}}"

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

def _auth_headers():
    if KEY_HEADER_NAME.lower() == "authorization":
        token = f"Bearer {API_KEY}" if USE_BEARER and not str(API_KEY).lower().startswith("bearer ") else API_KEY
        return {"Authorization": token}
    return {KEY_HEADER_NAME: API_KEY}

def kwyk_search_first_pkid(criteria_value="CO_VSUS", results_limit=100):
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
        **_auth_headers(),
    }
    if _REFERER:
        headers["Referer"] = _REFERER
    if _ORIGIN:
        headers["Origin"] = _ORIGIN

    with requests.Session() as s:
        if not API_KEY:
            raise RuntimeError("IDENTIFI_API_KEY is not set. Provide it in .env next to api_call.py or as an environment variable.")
        r = s.post(SEARCH_URL, json=payload, headers=headers, timeout=30)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            # Helpful debug if 401/403/etc.
            raise RuntimeError(f"Search failed: {r.status_code} {r.text[:500]}")

        data = r.json()
        results = data.get("results", [])
        if not results:
            return None, []
        first_pkid = results[0].get("PKID")
        return first_pkid, results

def download_document(pkid, dest_path, storage_type_id=1):
    if not pkid:
        raise ValueError("pkid is required")

    url = DOC_URL_TMPL.format(storage_type_id=storage_type_id, pkid=pkid)
    headers = {
        "Accept": "*/*",
        **_auth_headers(),
    }

    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    with requests.Session() as s:
        with s.get(url, headers=headers, stream=True, timeout=60) as r:
            try:
                r.raise_for_status()
            except requests.HTTPError:
                raise RuntimeError(f"Download failed: {r.status_code} {r.text[:500]}")
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 64):
                    if chunk:
                        f.write(chunk)
    return dest

# --- Example notebook cells ---
# 1) Find the latest PKID for CO_VSUS
first_pkid, results = kwyk_search_first_pkid("CO_VSUS", results_limit=100)
print("First PKID:", first_pkid)
print("Total results:", len(results))

# 2) Download that document (PDF or similar) to a file
if first_pkid:
    out_file = download_document(first_pkid, "/tmp/CO_VSUS_latest.pdf", storage_type_id=1)
    print("Saved to:", out_file)