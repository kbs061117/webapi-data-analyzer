import pandas as pd
import matplotlib.pyplot as plt

def hist(df, col, outpath, title):
    if col not in df.columns:
        raise KeyError("hist col not found")
    s = pd.to_numeric(df[col], errors="coerce").dropna()
    if len(s) == 0:
        raise ValueError("no numeric values")
    plt.figure()
    plt.hist(s, bins=10)
    plt.title(title)
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def bar(df, col, outpath, title, topk=20):
    if col not in df.columns:
        raise KeyError("bar col not found")
    vc = df[col].astype(str).value_counts(dropna=False).head(topk)
    if len(vc) == 0:
        raise ValueError("no values")
    plt.figure()
    vc.plot(kind="bar")
    plt.title(title)
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
