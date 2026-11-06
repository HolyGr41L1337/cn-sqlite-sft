"""让老师批量生成新的 SQLite 库建表语句，扩充训练集的表结构多样性。

    python schema_gen.py --n 12 --out schemas/extra
"""

import argparse
import json
import re
from pathlib import Path

import httpx

ROOT = Path(__file__).parent
API = "https://api.deepseek.com/chat/completions"

PROMPT = """生成 {n} 个互不相同的 SQLite 业务数据库设计，每个库 3 到 5 张表。

要求：
- 领域要杂：可以是物流、酒店、银行、在线课程、健身、招聘、票务、宠物医院、农场、仓储、社交、音乐平台、租房、保险、图书电商、快递柜、停车场、咖啡店、律所、实验室……
- 每个库用一个英文小写单词或下划线短语做库名，表名也用英文
- 字段类型只用 INTEGER / TEXT / REAL，主键用 INTEGER PRIMARY KEY
- 字段名要具体，别用 col1 这种；金额用 REAL，日期用 TEXT
- 表之间要有外键关系（外键字段可以不加 FOREIGN KEY 约束）
- 至少有一张表带状态字段（如 status），至少有一个金额字段，至少有一个日期字段

只输出 JSON：{{"databases": [{{"name": "logistics", "ddl": "CREATE TABLE ...;\\nCREATE TABLE ...;"}}]}}"""


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
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--out", default="schemas/extra")
    args = ap.parse_args()

    key = api_key()
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你只输出 JSON。"},
            {"role": "user", "content": PROMPT.format(n=args.n)},
        ],
        "temperature": 1.0,
        "max_tokens": 8000,
        "response_format": {"type": "json_object"},
    }
    r = httpx.post(API, json=payload, timeout=300, headers={"Authorization": f"Bearer {key}"})
    r.raise_for_status()
    data = json.loads(r.json()["choices"][0]["message"]["content"])

    n = 0
    for db in data.get("databases") or []:
        name = re.sub(r"[^a-z0-9_]", "", str(db.get("name") or "").lower())
        ddl = str(db.get("ddl") or "").strip()
        if not name or "create table" not in ddl.lower():
            continue
        (out / f"{name}.sql").write_text(ddl + "\n", encoding="utf-8")
        n += 1
        print("写入", name)
    print(f"共 {n} 个库 → {out}")


if __name__ == "__main__":
    main()
