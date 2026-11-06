#!/bin/bash
# RunPod 上一次性装好依赖、把数据拉下来
set -e
pip install -q --upgrade pip
pip install -q unsloth trl datasets transformers accelerate sentencepiece protobuf
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download("YukiKaze1337/cn-sqlite-sft", repo_type="dataset", local_dir="/workspace/cn-sqlite")
print("数据到位")
PY
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
