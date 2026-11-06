#!/bin/bash
# v2：每一步都往 HF 传状态，挂了也看得出挂在哪
REPO=YukiKaze1337/cn-sqlite-4b
LOG=/workspace/run.log
: > $LOG

beat() {
  hf upload $REPO "$LOG" run.log --repo-type model >/dev/null 2>&1 || true
}
step() {
  echo "=== $(date -u +%H:%M:%S) $*" | tee -a $LOG
  beat
}

(
  while true; do sleep 180; beat; done
) &
BEAT_PID=$!

cd /workspace
step "start"
pip install -q --upgrade pip 2>&1 | tail -1
step "install deps"
pip install -q unsloth trl datasets transformers accelerate sentencepiece protobuf "huggingface_hub[cli]" 2>&1 | tail -5
step "deps done"

hf download YukiKaze1337/cn-sqlite-sft --repo-type dataset --local-dir /workspace/data 2>&1 | tail -2
step "data ready"

git clone https://github.com/HolyGr41L1337/cn-sqlite-sft.git /workspace/code 2>&1 | tail -1
cd /workspace/code
cp -r /workspace/data/schemas/* schemas/ 2>/dev/null
cp -r /workspace/data/seeds/* seeds/ 2>/dev/null
step "code ready"

MODEL=Qwen/Qwen3-4B-Instruct-2507
python eval.py --model $MODEL --data /workspace/data/test/test_library.jsonl --out /workspace/baseline_lib.json 2>&1 | tail -3
step "baseline library done"
python eval.py --model $MODEL --data /workspace/data/test/test_gym.jsonl --out /workspace/baseline_gym.json 2>&1 | tail -3
step "baseline gym done"
hf upload $REPO /workspace/baseline_lib.json baseline_lib.json --repo-type model >/dev/null 2>&1
hf upload $REPO /workspace/baseline_gym.json baseline_gym.json --repo-type model >/dev/null 2>&1
step "baseline uploaded"

python train_unsloth.py --data /workspace/data/train.jsonl --out /workspace/out 2>&1 | tail -8
step "train done"

python eval.py --model /workspace/out/merged --data /workspace/data/test/test_library.jsonl --out /workspace/after_lib.json 2>&1 | tail -3
step "after library done"
python eval.py --model /workspace/out/merged --data /workspace/data/test/test_gym.jsonl --out /workspace/after_gym.json 2>&1 | tail -3
step "after gym done"

hf upload $REPO /workspace/after_lib.json after_lib.json --repo-type model >/dev/null 2>&1
hf upload $REPO /workspace/after_gym.json after_gym.json --repo-type model >/dev/null 2>&1
hf upload $REPO /workspace/out/lora lora --repo-type model >/dev/null 2>&1
step "ALL DONE"
kill $BEAT_PID 2>/dev/null
