#!/bin/bash
cd /Users/mac/text2sql
LIST="$1"
for s in $LIST; do
  f="schemas/$s.sql"
  [ -f "$f" ] || f="schemas/extra/$s.sql"
  [ -f "$f" ] || continue
  echo "== $s"
  .venv/bin/python teacher.py --schema "$f" --n 20 --rounds 15 --out data/train/$s.jsonl 2>/dev/null | tail -1
done
