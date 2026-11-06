#!/bin/bash
cd /Users/mac/text2sql
for f in data/train/*.jsonl; do
  echo "== $f"
  .venv/bin/python verify.py --data "$f" 2>&1 | tail -1
done
