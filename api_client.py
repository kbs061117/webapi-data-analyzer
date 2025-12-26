import requests

def getjson(url, timeout, ua):
    if not url or not isinstance(url, str):
        raise ValueError("url empty")
    try:
        r = requests.get(url, headers={"User-Agent": ua}, timeout=timeout)
    except requests.exceptions.Timeout as e:
        raise TimeoutError("timeout") from e
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError("connection error") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError("request error") from e

    code = r.status_code
    ctype = r.headers.get("Content-Type")

    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        t = (r.text or "")[:300].replace("\n", " ")
        raise RuntimeError(f"http {code}: {t}") from e

    try:
        return r.json(), code, ctype
    except ValueError as e:
        t = (r.text or "")[:300].replace("\n", " ")
        raise ValueError(f"not json: {t}") from e
