"""把训练数据、建表语句、假数据打包到 dist/，方便传 HF。"""

import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"

def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "schemas").mkdir(parents=True)
    (DIST / "seeds").mkdir()
    (DIST / "test").mkdir()

    for p in (ROOT / "schemas").rglob("*.sql"):
        shutil.copy2(p, DIST / "schemas" / p.name)
    for p in (ROOT / "seeds").glob("*.sql"):
        shutil.copy2(p, DIST / "seeds" / p.name)
    for p in (ROOT / "data").glob("test_*.jsonl"):
        shutil.copy2(p, DIST / "test" / p.name)
    shutil.copy2(ROOT / "data" / "sft" / "train.jsonl", DIST / "train.jsonl")
    print("dist 好了：", len(list(DIST.rglob('*'))), "个文件")

if __name__ == "__main__":
    main()
