"""让老师模型照着建表语句造 (中文问题, SQLite 查询) 对。

    python teacher.py --schema schemas/school.sql --n 20

生成的 SQL 会真的丢进内存 SQLite 跑一遍，跑不过的直接扔掉；
只留单条 SELECT，DDL/DML 一律不要。
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).parent
API = "https://api.deepseek.com/chat/completions"

PROMPT = """你在给一个中文 Text-to-SQLite 数据集出题。

下面是数据库的建表语句：

{ddl}

出 {n} 道中文问题，并为每题写一条 SQLite 查询。要求：

- 问题要像真人问的，口语化，可以有「上个月」「最多的前五个」这种自然表达
- 覆盖不同难度：简单筛选、聚合、分组、多表连接、子查询、排序取前几
- 只能用 SELECT，一条语句，不要解释、不要分号结尾以外的多余内容
- 表名和列名必须严格使用上面出现过的
- 不要问需要 INSERT/UPDATE/DELETE 的问题
- 大约五分之一的题要牵涉 CTE（WITH）、窗口函数或者日期计算，别全是简单查询
- 日期字段是 TEXT，格式 'YYYY-MM-DD' 或 'YYYY-MM-DD HH:MM:SS'，用 SQLite 的 date()/strftime()

只输出 JSON，格式：
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


def ask(ddl: str, n: int, key: str) -> list[dict]:
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你只输出 JSON。"},
            {"role": "user", "content": PROMPT.format(ddl=ddl, n=n)},
        ],
        "temperature": 1.0,
        "max_tokens": 4000,
        "response_format": {"type": "json_object"},
    }
    r = httpx.post(
        API, json=payload, timeout=180,
        headers={"Authorization": f"Bearer {key}"},
    )
    r.raise_for_status()
    data = r.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content).get("items") or []


def check(sql: str, conn: sqlite3.Connection) -> tuple[bool, str]:
    s = sql.strip().rstrip(";")
    if not s.lower().startswith("select"):
        return False, "不是 select"
    if ";" in s:
        return False, "多条语句"
    try:
        conn.execute(s).fetchall()
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    schema_path = ROOT / args.schema if not Path(args.schema).is_absolute() else Path(args.schema)
    ddl = schema_path.read_text(encoding="utf-8")
    dbname = schema_path.stem
    conn = sqlite3.connect(":memory:")
    conn.executescript(ddl)
    seed = ROOT / "seeds" / f"{dbname}.sql"
    if seed.exists():
        conn.executescript(seed.read_text(encoding="utf-8"))

    key = api_key()
    out_path = Path(args.out) if args.out else ROOT / "data" / f"{dbname}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    kept = bad = 0
    with out_path.open("a", encoding="utf-8") as f:
        for r in range(args.rounds):
            items = ask(ddl, args.n, key)
            for it in items:
                q = str(it.get("question") or "").strip()
                sql = str(it.get("sql") or "").strip()
                if not q or not sql:
                    continue
                ok, err = check(sql, conn)
                if not ok:
                    bad += 1
                    print(f"丢弃（{err[:60]}）：{sql[:80]}", file=sys.stderr)
                    continue
                f.write(json.dumps({"db": dbname, "question": q, "sql": sql.rstrip(";")},
                                   ensure_ascii=False) + "\n")
                kept += 1
            print(f"第 {r+1} 轮：累计保留 {kept}，丢弃 {bad}", flush=True)

    print(f"完成：{out_path}，保留 {kept} 条，丢弃 {bad} 条")


if __name__ == "__main__":
    main()
