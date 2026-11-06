"""给每个库灌一些假数据，方便验证查询结果是不是有东西。

    python seed.py --schemas schemas --out seeds

按列名猜类型，生成 40 行左右，导出成 INSERT 语句。
"""

import argparse
import random
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent

SURNAMES = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜"
GIVEN = "伟芳娜秀英敏静丽强磊洋艳勇军杰娟涛明超秀霞平刚桂英"
CITIES = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京", "西安", "苏州"]
STATUSES = ["pending", "paid", "shipped", "done", "cancelled", "active", "closed"]
WORDS = ["标准", "豪华", "普通", "高级", "基础", "季度", "年度", "临时"]


def rand_name() -> str:
    return random.choice(SURNAMES) + random.choice(GIVEN) + random.choice(GIVEN)


def rand_date() -> str:
    y = random.choice([2023, 2024, 2025, 2026])
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    if random.random() < 0.4:
        return f"{y}-{m:02d}-{d:02d} {random.randint(0,23):02d}:{random.randint(0,59):02d}:00"
    return f"{y}-{m:02d}-{d:02d}"


def value_for(col: str, table: str, pk_max: dict[str, int], index: int, is_pk: bool):
    c = col.lower()
    if is_pk:
        return index + 1
    if c.endswith("_id"):
        base = c[:-3]
        for t, mx in pk_max.items():
            if t.rstrip("s") in base or base.rstrip("s") in t:
                return random.randint(1, max(1, mx))
        return random.randint(1, 20)
    if "date" in c or "time" in c or c.endswith("_at"):
        return rand_date()
    if c in ("status", "state"):
        return random.choice(STATUSES)
    if "city" in c or "address" in c or "region" in c:
        return random.choice(CITIES)
    if c in ("name", "title", "author", "customer_name", "contact") or c.endswith("_name"):
        return rand_name() if c == "name" else random.choice(WORDS) + rand_name()[:1]
    if "phone" in c or "mobile" in c:
        return "1" + "".join(random.choice("0123456789") for _ in range(10))
    if any(k in c for k in ("amount", "price", "salary", "fee", "cost", "budget", "balance", "revenue", "total")):
        return round(random.uniform(10, 10000), 2)
    if any(k in c for k in ("qty", "quantity", "stock", "count", "number", "num", "age", "hours", "duration", "points", "level", "capacity", "floor", "seat")):
        return random.randint(1, 500)
    if any(k in c for k in ("rate", "rating", "score", "ratio", "percent", "weight", "price")):
        return round(random.uniform(0, 5), 2)
    if c in ("gender", "sex"):
        return random.choice(["男", "女"])
    if "email" in c:
        return f"user{index}@example.com"
    if "category" in c or "type" in c or "kind" in c:
        return random.choice(["A", "B", "C", "通用", "特殊"])
    return random.choice(WORDS) + str(random.randint(1, 99))


def seed_db(sql_path: Path) -> str:
    conn = sqlite3.connect(":memory:")
    conn.executescript(sql_path.read_text(encoding="utf-8"))
    tables = [r[0] for r in conn.execute(
        "select name from sqlite_master where type='table' and name not like 'sqlite_%'"
    )]
    pk_max: dict[str, int] = {}
    inserts: list[str] = []

    for t in tables:
        cols = conn.execute(f"pragma table_info({t})").fetchall()
        rows = 40
        for i in range(rows):
            vals = []
            for c in cols:
                name, typ, pk = c[1], (c[2] or "").upper(), c[5]
                is_pk = bool(pk) and typ == "INTEGER"
                vals.append(value_for(name, t, pk_max, i, is_pk))
            cols_sql = ", ".join(f'"{c[1]}"' for c in cols)
            marks = ", ".join("?" for _ in cols)
            conn.execute(f'insert into "{t}" ({cols_sql}) values ({marks})', vals)
            lit = ", ".join(
                "NULL" if v is None else (f"'{v}'" if isinstance(v, str) else str(v))
                for v in vals
            )
            inserts.append(f'INSERT INTO "{t}" ({cols_sql}) VALUES ({lit});')
        pk_max[t] = rows
    return "\n".join(inserts) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schemas", default="schemas")
    ap.add_argument("--out", default="seeds")
    args = ap.parse_args()

    out = ROOT / args.out
    out.mkdir(exist_ok=True)
    for p in sorted((ROOT / args.schemas).rglob("*.sql")):
        try:
            sql = seed_db(p)
        except Exception as exc:  # noqa: BLE001
            print(f"跳过 {p.name}：{exc}")
            continue
        (out / f"{p.stem}.sql").write_text(sql, encoding="utf-8")
        print(f"{p.stem}: {sql.count('INSERT')} 行")


if __name__ == "__main__":
    main()
