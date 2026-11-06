"""bf16 LoRA 训练，不依赖 unsloth 和 bitsandbytes。

    python train_peft.py --data train.jsonl --out /workspace/out
"""

import argparse
import os
from pathlib import Path

import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3-4B-Instruct-2507")
    ap.add_argument("--data", default="train.jsonl")
    ap.add_argument("--out", default="/workspace/out")
    ap.add_argument("--epochs", type=float, default=3.0)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--bs", type=int, default=2)
    ap.add_argument("--accum", type=int, default=8)
    ap.add_argument("--seq", type=int, default=1536)
    ap.add_argument("--rank", type=int, default=32)
    ap.add_argument("--smoke", type=int, default=0, help="只跑这么多步，用来验流程")
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.bfloat16, device_map="cuda"
    )
    model.gradient_checkpointing_enable()
    model = get_peft_model(model, LoraConfig(
        r=args.rank, lora_alpha=args.rank * 2, lora_dropout=0.0, bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    ))
    model.print_trainable_parameters()

    ds = load_dataset("json", data_files=args.data, split="train")
    print("样本", len(ds), flush=True)

    cfg = SFTConfig(
        output_dir=args.out,
        per_device_train_batch_size=args.bs,
        gradient_accumulation_steps=args.accum,
        num_train_epochs=args.epochs,
        max_steps=args.smoke if args.smoke else -1,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=10,
        save_strategy="no",
        bf16=True,
        optim="adamw_torch",
        max_length=args.seq,
        packing=True,
        dataset_kwargs={"skip_prepare_dataset": False},
        report_to="none",
    )
    trainer = SFTTrainer(model=model, train_dataset=ds, args=cfg, processing_class=tok)
    trainer.train()

    out = Path(args.out)
    model.save_pretrained(str(out / "lora"))
    tok.save_pretrained(str(out / "lora"))
    print("LoRA 存好了", flush=True)

    merged = model.merge_and_unload()
    merged.save_pretrained(str(out / "merged"), safe_serialization=True)
    tok.save_pretrained(str(out / "merged"))
    print("合并版存好了", flush=True)


if __name__ == "__main__":
    main()
