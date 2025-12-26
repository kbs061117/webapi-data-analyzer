import pandas as pd

def _autolist(d):
    for k, v in d.items():
        if isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
            return k, v
    return None, None

def todf(payload, rootkey=None):
    meta = {"mode": None, "rootkey": None}

    if isinstance(payload, list):
        if len(payload) == 0:
            meta["mode"] = "list(empty)"
            return pd.DataFrame(), meta
        if not all(isinstance(x, dict) for x in payload):
            raise TypeError("list must be list[dict]")
        meta["mode"] = "list[dict]"
        return pd.json_normalize(payload), meta

    if isinstance(payload, dict):
        if rootkey:
            if rootkey not in payload:
                raise KeyError("rootkey not found")
            v = payload[rootkey]
            if not (isinstance(v, list) and all(isinstance(x, dict) for x in v)):
                raise TypeError("rootkey must be list[dict]")
            meta["mode"] = "dict(rootkey)"
            meta["rootkey"] = rootkey
            return pd.json_normalize(v), meta

        k, v = _autolist(payload)
        if v is not None:
            meta["mode"] = "dict(auto list)"
            meta["rootkey"] = k
            return pd.json_normalize(v), meta

        meta["mode"] = "dict(single)"
        return pd.json_normalize(payload), meta

    raise TypeError("payload must be list or dict")
