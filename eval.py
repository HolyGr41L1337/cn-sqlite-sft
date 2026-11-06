"""执行准确率评测：模型生成的 SQL 和标准 SQL 在同一个 SQLite 上比结果。

    python eval.py --model Qwen/Qwen3-4B-Instruct-2507 --data data/test_library.jsonl

只比结果，不比 SQL 文本；标准 SQL 带 ORDER BY 时才算顺序，否则按多重集比较。
"""

import argparse
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent
SELECT_RE = re.compile(r"(?is)\bselect\b.*?(?:;|$)")

TEMPERATURE = 0.0


def extract_sql(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:sql)?|```$", "", text, flags=re.M).strip()
    m = SELECT_RE.search(text)
    if not m:
        return ""
    sql = m.group(0).strip().rstrip(";")
    # 只要第一条语句
    return sql.split(";")[0].strip()


def rows_of(conn: sqlite3.Connection, sql: str):
    return conn.execute(sql).fetchall()


def same_result(gold, pred, ordered: bool) -> bool:
    if len(gold) != len(pred):
        return False
    if ordered:
        return gold == pred
    return sorted(map(tuple, gold)) == sorted(map(tuple, pred))


def prompt_for(ddl: str, question: str) -> str:
    return (
        "你是 SQLite 查询助手。根据建表语句，把中文问题写成一条 SQLite 查询。\n"
        "只输出 SQL，不要解释，不要 markdown。\n\n"
        f"建表语句：\n{ddl}\n\n问题：{question}\nSQL："
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default="")
    ap.add_argument("--max-new-tokens", type=int, default=200)
    args = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto", trust_remote_code=True,
    )
    model.eval()

    items = [json.loads(l) for l in Path(args.data).read_text(encoding="utf-8").splitlines() if l.strip()]
    if args.limit:
        items = items[: args.limit]

    ok = valid = 0
    records = []
    for i, it in enumerate(items, 1):
        ddl = next((ROOT / "schemas").rglob(f"{it['db']}.sql")).read_text(encoding="utf-8")
        conn = sqlite3.connect(":memory:")
        conn.executescript(ddl)

        msgs = [{"role": "user", "content": prompt_for(ddl, it["question"])}]
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        inputs = tok(text, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=args.max_new_tokens,
                                 do_sample=False, temperature=None, top_p=None,
                                 pad_token_id=tok.eos_token_id)
        pred_text = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        pred = extract_sql(pred_text)

        gold_rows = rows_of(conn, it["sql"])
        hit = False
        if pred:
            try:
                pred_rows = rows_of(conn, pred)
                valid += 1
                hit = same_result(gold_rows, pred_rows, ordered="order by" in it["sql"].lower())
            except Exception:  # noqa: BLE001
                hit = False
        ok += int(hit)
        records.append({"db": it["db"], "question": it["question"], "gold": it["sql"],
                        "pred": pred, "hit": hit})

        if i % 10 == 0:
            print(f"{i}/{len(items)} 有效 {valid} 正确 {ok} 准确率 {ok/i:.3f}", flush=True)

    n = len(items)
    print(f"\n总数 {n}｜可执行 {valid}（{valid/n:.1%}）｜执行准确率 {ok/n:.1%}")
    if args.out:
        Path(args.out).write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
        print("明细写到", args.out)


if __name__ == "__main__":
    main()
