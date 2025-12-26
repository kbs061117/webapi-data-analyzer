import argparse
from pathlib import Path
from api_client import getjson
from df_build import todf
from analyze import show, pick
from viz import hist, bar
from utils import sp, outdir, tag

EXU = "https://jsonplaceholder.typicode.com/users"
EXT = "https://jsonplaceholder.typicode.com/todos"

def parser():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group()
    g.add_argument("--url", type=str)
    g.add_argument("--example", choices=["users","todos"])
    p.add_argument("--timeout", type=float, default=10.0)
    p.add_argument("--user-agent", type=str, default="webapi-data-analyzer/1.0")
    p.add_argument("--root-key", type=str, default=None)
    p.add_argument("--outdir", type=str, default="output")
    p.add_argument("--save-csv", action="store_true")
    p.add_argument("--hist", type=str, default=None)
    p.add_argument("--bar", type=str, default=None)
    p.add_argument("--no-plot", action="store_true")
    return p

def urlresolve(a):
    if a.url:
        return a.url.strip()
    if a.example == "users":
        return EXU
    if a.example == "todos":
        return EXT
    print("1) users  2) todos  3) custom")
    c = input("select: ").strip()
    if c == "1": return EXU
    if c == "2": return EXT
    if c == "3":
        u = input("url: ").strip()
        if not u: raise ValueError("empty url")
        return u
    raise ValueError("bad select")

def main():
    a = parser().parse_args()
    u = urlresolve(a)
    o = outdir(Path(a.outdir))

    sp(f"[URL] {u}")
    payload, code, ctype = getjson(u, a.timeout, a.user_agent)
    sp(f"[status] {code}")
    if ctype: sp(f"[type] {ctype}")

    df, meta = todf(payload, a.root_key)
    sp(f"[df] rows={len(df)} cols={len(df.columns)} meta={meta}")

    show(df)

    t = tag()
    if a.save_csv:
        csvp = o / f"data_{t}.csv"
        df.to_csv(csvp, index=False, encoding="utf-8-sig")
        sp(f"[saved] {csvp}")

    if a.no_plot:
        return

    h, b = pick(df, a.hist, a.bar)

    if h:
        img = o / f"hist_{h}_{t}.png"
        hist(df, h, img, f"Histogram: {h}")
        sp(f"[saved] {img}")
    else:
        sp("[warn] no numeric column for histogram")

    if b:
        img = o / f"bar_{b}_{t}.png"
        bar(df, b, img, f"Bar chart: {b}")
        sp(f"[saved] {img}")
    else:
        sp("[warn] no category column for bar")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sp("stopped")
    except Exception as e:
        sp(f"error: {type(e).__name__}: {e}")
