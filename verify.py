"""用老师再检查一遍：这条 SQL 真的回答了那个问题吗？

执行能通过不等于答对，比如问「每个年级的平均工资」却给个 join 出来的 salary 列表。
这里让模型逐条判断，判错的直接剔掉。

    python verify.py --data data/school.jsonl
"""

import argparse
import json
import re
import sqlite3
from pathlib import Path

import httpx

ROOT = Path(__file__).parent
API = "https://api.deepseek.com/chat/completions"

def find_schema(db: str) -> Path:
    for p in (ROOT / "schemas").rglob(f"{db}.sql"):
        return p
    raise FileNotFoundError(db)


PROMPT = """下面是一组「中文问题 + SQLite 查询」。逐条判断这条 SQL 是否准确回答了问题。

{rows}

判断标准：
- 该查的字段、该做的聚合、该有的过滤条件都在，才算对
- 多查了无关字段但仍是同一件事，算对
- 少条件、聚合错、表连错、语义跑偏，算错
- 问题有歧义时，按最自然的理解判断

只输出 JSON：{{"verdicts": [{{"i": 1, "ok": true, "why": "一句话理由"}}]}}"""


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


def judge(batch: list[dict], ddl: str, key: str) -> dict[int, bool]:
    rows = "\n".join(
        f'{i+1}. 问题：{b["question"]}\n   SQL：{b["sql"]}' for i, b in enumerate(batch)
    )
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你只输出 JSON。"},
            {"role": "user", "content": f"建表语句：\n{ddl}\n\n{PROMPT.format(rows=rows)}"},
        ],
        "temperature": 0.0,
        "max_tokens": 2000,
        "response_format": {"type": "json_object"},
    }
    r = httpx.post(API, json=payload, timeout=180, headers={"Authorization": f"Bearer {key}"})
    r.raise_for_status()
    data = json.loads(r.json()["choices"][0]["message"]["content"])
    out = {}
    for v in data.get("verdicts") or []:
        try:
            out[int(v["i"])] = bool(v.get("ok"))
        except Exception:  # noqa: BLE001
            continue
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--batch", type=int, default=15)
    ap.add_argument("--keep-all", action="store_true")
    args = ap.parse_args()

    path = Path(args.data)
    items = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    key = api_key()
    kept = []
    for start in range(0, len(items), args.batch):
        batch = items[start:start + args.batch]
        ddl = find_schema(batch[0]["db"]).read_text(encoding="utf-8")
        verdict = judge(batch, ddl, key)
        for i, it in enumerate(batch, 1):
            if verdict.get(i, True):
                kept.append(it)
            else:
                print(f"剔除：{it['question']} | {it['sql'][:70]}", flush=True)
        print(f"{min(start+args.batch, len(items))}/{len(items)} 留下 {len(kept)}", flush=True)

    path.write_text("\n".join(json.dumps(k, ensure_ascii=False) for k in kept) + "\n", encoding="utf-8")
    print(f"完成：{len(items)} → {len(kept)}")


if __name__ == "__main__":
    main()
