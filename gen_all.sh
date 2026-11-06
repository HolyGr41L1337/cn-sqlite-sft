#!/bin/bash
cd /Users/mac/text2sql
for s in school ecommerce hospital company food_delivery cinema bank farm fitness hotel logistics music online_course pet_clinic recruit social storage ticketing; do
  echo "== $s"
  .venv/bin/python teacher.py --schema schemas/$s.sql --n 20 --rounds 5 --out data/train/$s.jsonl 2>/dev/null | tail -1
done
