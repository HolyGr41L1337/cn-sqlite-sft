"""出难题：一个 12 张表的零售库，问题要求多表连接、窗口、CTE、反连接这些。

    python teacher_hard.py --n 25 --rounds 4

只留能执行的，语义靠 verify.py 再过一遍。
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).parent
API = "https://api.deepseek.com/chat/completions"

PROMPT = """你在给中文 Text-to-SQLite 数据集出**难题**。

建表语句：

{ddl}

出 {n} 道中文问题，每道配一条 SQLite 查询。这批刻意要难：

- 至少一半的题需要 3 张以上表连接
- 至少三成需要子查询、CTE（WITH）、窗口函数（ROW_NUMBER/RANK/SUM OVER）、或者 NOT EXISTS 反连接
- 要用到日期函数（strftime、date）、HAVING、CASE WHEN、字符串拼接
- 问题用真人说法，可以有歧义、可以有「最近 30 天」「排名前三」「占比多少」这种表达
- 只能 SELECT，一条语句，列名和表名严格照建表语句
- 不要问需要改数据的问题

只输出 JSON：
{{"items": [{{"question": "中文问题", "sql": "SELECT ..."}}]}}"""


def api_key() -> str:
    cfg = json.loads(
        (Path.home() / "Documents/deepseek-harness/default-workspace/qq-bot-stack/data/astrbot/cmd_config.json")
        .read_text(encoding="utf-8-sig")
    )
    for src in cfg.get("provider_sources", []):
        for k in src.get("key") or []:
            if k:
                return k
    raise SystemExit("找不到 key")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", default="schemas/hard_retail.sql")
    ap.add_argument("--n", type=int, default=25)
    ap.add_argument("--rounds", type=int, default=4)
    ap.add_argument("--out", default="data/test_hard.jsonl")
    args = ap.parse_args()

    ddl = (ROOT / args.schema).read_text(encoding="utf-8")
    conn = sqlite3.connect(":memory:")
    conn.executescript(ddl)
    seed = ROOT / "seeds" / f"{Path(args.schema).stem}.sql"
    if seed.exists():
        conn.executescript(seed.read_text(encoding="utf-8"))

    key = api_key()
    out = ROOT / args.out
    kept = 0
    with out.open("a", encoding="utf-8") as f:
        for r in range(args.rounds):
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你只输出 JSON。"},
                    {"role": "user", "content": PROMPT.format(ddl=ddl, n=args.n)},
                ],
                "temperature": 1.1,
                "max_tokens": 6000,
                "response_format": {"type": "json_object"},
            }
            resp = httpx.post(API, json=payload, timeout=300,
                              headers={"Authorization": f"Bearer {key}"})
            resp.raise_for_status()
            raw = resp.json()["choices"][0]["message"]["content"]
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                print("这一轮 JSON 坏了，跳过", file=sys.stderr)
                continue
            for it in data.get("items") or []:
                q, sql = str(it.get("question") or "").strip(), str(it.get("sql") or "").strip()
                if not q or not sql.lower().startswith("select"):
                    continue
                try:
                    conn.execute(sql.rstrip(";")).fetchall()
                except Exception as exc:  # noqa: BLE001
                    print("丢弃", exc, sql[:60], file=sys.stderr)
                    continue
                f.write(json.dumps({"db": "hard_retail", "question": q, "sql": sql.rstrip(";")},
                                   ensure_ascii=False) + "\n")
                kept += 1
            print(f"第 {r+1} 轮，累计 {kept}")
    print("写好了", out, kept, "条")


if __name__ == "__main__":
    main()
