"""把生成出来的问答对拼成训练用的 JSONL。

    python build_sft.py

- 合并 data/train/*.jsonl 和老的那几个 data/*.jsonl
- 按 (库, 问题) 去重，问题过短的丢掉
- 用 prompt.py 里的格式包装成 messages
- 顺手统计一下查询类型分布，看看数据偏不偏
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from prompt import build

ROOT = Path(__file__).parent


def schema_path(db: str) -> Path:
    for p in (ROOT / "schemas").rglob(f"{db}.sql"):
        return p
    raise FileNotFoundError(db)


def sql_kind(sql: str) -> str:
    s = sql.lower()
    for key, pat in (
        ("窗口函数", r"\bover\s*\("),
        ("子查询", r"\(\s*select\b"),
        ("CTE", r"\bwith\b"),
        ("多表连接", r"\bjoin\b"),
        ("分组", r"\bgroup by\b"),
        ("排序", r"\border by\b"),
        ("取前几", r"\blimit\b"),
        ("聚合", r"\b(count|sum|avg|max|min)\s*\("),
    ):
        if re.search(pat, s):
            return key
    return "简单筛选"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/sft")
    args = ap.parse_args()

    rows: list[dict] = []
    for p in sorted((ROOT / "data").glob("*.jsonl")) + sorted((ROOT / "data" / "train").glob("*.jsonl")):
        if p.name.startswith("test_"):
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if len(r.get("question", "")) < 4 or not r.get("sql"):
                continue
            rows.append(r)

    seen = set()
    keep = []
    for r in rows:
        key = (r["db"], re.sub(r"\s+", "", r["question"]))
        if key in seen:
            continue
        seen.add(key)
        keep.append(r)

    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    with (out / "train.jsonl").open("w", encoding="utf-8") as f:
        for r in keep:
            ddl = schema_path(r["db"]).read_text(encoding="utf-8")
            msgs = build(ddl, r["question"])
            msgs.append({"role": "assistant", "content": r["sql"].rstrip(";") + ";"})
            f.write(json.dumps({"messages": msgs, "db": r["db"]}, ensure_ascii=False) + "\n")

    kinds = Counter(sql_kind(r["sql"]) for r in keep)
    dbs = Counter(r["db"] for r in keep)
    print(f"写好了 {len(keep)} 条（原始 {len(rows)} 条，去重 {len(rows)-len(keep)}）")
    print("库分布：", dict(sorted(dbs.items(), key=lambda x: -x[1])))
    print("类型分布：", dict(kinds.most_common()))


if __name__ == "__main__":
    main()
