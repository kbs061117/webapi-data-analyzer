from pathlib import Path
from datetime import datetime

def sp(x):
    print(str(x))

def outdir(p):
    p.mkdir(parents=True, exist_ok=True)
    return p

def tag():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
