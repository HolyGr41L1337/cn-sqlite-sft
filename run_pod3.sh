#!/bin/bash
# 全程不依赖 SSH：自己跑完自己关机，日志随时传 HF
REPO=YukiKaze1337/cn-sqlite-4b
LOG=/workspace/run.log
: > $LOG
exec > >(tee -a $LOG) 2>&1

beat() { hf upload $REPO "$LOG" run.log --repo-type model >/dev/null 2>&1 || true; }
step() { echo "=== $(date -u +%H:%M:%S) $*"; beat; }

( while true; do sleep 300; beat; done ) &

cd /workspace
step "start"
pip install -q --upgrade pip
pip install -q "transformers==4.57.1" peft "trl==0.25.2" datasets accelerate sentencepiece protobuf "huggingface_hub[cli]"
step "deps"
hf download YukiKaze1337/cn-sqlite-sft --repo-type dataset --local-dir /workspace/data
step "data"
git clone -q https://github.com/HolyGr41L1337/cn-sqlite-sft.git /workspace/code
cd /workspace/code
cp -r /workspace/data/schemas/* schemas/ 2>/dev/null
cp -r /workspace/data/seeds/* seeds/ 2>/dev/null
step "code"

python train_peft.py --data /workspace/data/train.jsonl --out /workspace/out --smoke 20
step "smoke ok"

python train_peft.py --data /workspace/data/train.jsonl --out /workspace/out
step "train done"

MODEL=/workspace/out/merged
python eval.py --model $MODEL --data /workspace/data/test/test_library.jsonl --out /workspace/after_lib.json
step "eval lib"
python eval.py --model $MODEL --data /workspace/data/test/test_gym.jsonl --out /workspace/after_gym.json
step "eval gym"

hf upload $REPO /workspace/after_lib.json after_lib.json --repo-type model >/dev/null 2>&1
hf upload $REPO /workspace/after_gym.json after_gym.json --repo-type model >/dev/null 2>&1
hf upload $REPO /workspace/baseline_lib.json baseline_lib.json --repo-type model >/dev/null 2>&1 || true
hf upload $REPO /workspace/out/lora lora --repo-type model >/dev/null 2>&1
step "uploaded"

curl -s -X POST "https://rest.runpod.io/v1/pods/$RUNPOD_POD_ID/stop" -H "Authorization: Bearer $RUNPOD_API_KEY" >/dev/null
step "ALL DONE"
