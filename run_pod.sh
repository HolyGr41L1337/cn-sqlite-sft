#!/bin/bash
# RunPod 上从头跑到尾：装依赖、拉数据、打基线、训练、评测、上传
set -x
exec > >(tee -a /workspace/run.log) 2>&1

cd /workspace
pip install -q --upgrade pip
pip install -q unsloth trl datasets transformers accelerate sentencepiece protobuf
echo "=== deps done"

hf download YukiKaze1337/cn-sqlite-sft --repo-type dataset --local-dir /workspace/data
git clone https://github.com/HolyGr41L1337/cn-sqlite-sft.git /workspace/code || true
cd /workspace/code
cp -r /workspace/data/schemas/* schemas/ 2>/dev/null || true
cp -r /workspace/data/seeds/* seeds/ 2>/dev/null || true

MODEL=Qwen/Qwen3-4B-Instruct-2507

echo "=== baseline library"
python eval.py --model $MODEL --data /workspace/data/test/test_library.jsonl --out /workspace/baseline_lib.json
echo "=== baseline gym"
python eval.py --model $MODEL --data /workspace/data/test/test_gym.jsonl --out /workspace/baseline_gym.json
hf upload YukiKaze1337/cn-sqlite-4b /workspace/baseline_lib.json baseline_lib.json --repo-type model
hf upload YukiKaze1337/cn-sqlite-4b /workspace/baseline_gym.json baseline_gym.json --repo-type model
hf upload YukiKaze1337/cn-sqlite-4b /workspace/run.log run.log --repo-type model

echo "=== train"
python train_unsloth.py --data /workspace/data/train.jsonl --out /workspace/out

echo "=== eval after"
python eval.py --model /workspace/out/merged --data /workspace/data/test/test_library.jsonl --out /workspace/after_lib.json
python eval.py --model /workspace/out/merged --data /workspace/data/test/test_gym.jsonl --out /workspace/after_gym.json

hf upload YukiKaze1337/cn-sqlite-4b /workspace/after_lib.json after_lib.json --repo-type model
hf upload YukiKaze1337/cn-sqlite-4b /workspace/after_gym.json after_gym.json --repo-type model
hf upload YukiKaze1337/cn-sqlite-4b /workspace/run.log run.log --repo-type model
hf upload YukiKaze1337/cn-sqlite-4b /workspace/out/lora lora --repo-type model
echo "=== all done"
