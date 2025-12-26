from utils import sp

def show(df):
    sp("\n=== head ===")
    if df is None or len(df) == 0:
        sp("empty df")
        return
    sp(df.head(5).to_string(index=False))

    sp("\n=== describe ===")
    try:
        sp(df.describe(include="all").to_string())
    except Exception as e:
        sp(f"describe failed: {type(e).__name__}: {e}")

    sp("\n=== dtypes ===")
    sp(df.dtypes.to_string())

def pick(df, hist=None, bar=None):
    cols = list(df.columns)
    h = hist if (hist in cols) else None
    b = bar if (bar in cols) else None

    if h is None:
        nums = df.select_dtypes(include="number").columns.tolist()
        if nums:
            h = nums[0]

    if b is None:
        cats = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
        for c in cats:
            try:
                n = int(df[c].nunique(dropna=True))
                if 2 <= n <= 30:
                    b = c
                    break
            except Exception:
                pass

    return h, b
