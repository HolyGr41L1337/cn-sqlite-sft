"""在 RunPod 上跑：Qwen3-4B-Instruct-2507 的 LoRA 微调，专做中文→SQLite。

    python train_unsloth.py --data train.jsonl --out /workspace/out

数据格式是 build_sft.py 产出的 messages JSONL。
训完输出 LoRA、合并后的 16bit 模型，以及 Q4_K_M / Q8_0 两个 GGUF。
"""

import argparse
from pathlib import Path

import torch
from datasets import load_dataset
from unsloth import FastLanguageModel
from trl import SFTConfig, SFTTrainer


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="unsloth/Qwen3-4B-Instruct-2507")
    ap.add_argument("--data", default="train.jsonl")
    ap.add_argument("--out", default="/workspace/out")
    ap.add_argument("--epochs", type=float, default=3.0)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--bs", type=int, default=4)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--seq", type=int, default=2048)
    ap.add_argument("--rank", type=int, default=64)
    args = ap.parse_args()

    model, tok = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.seq,
        load_in_4bit=True,
        dtype=torch.bfloat16,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=args.rank,
        lora_alpha=args.rank * 2,
        lora_dropout=0.0,
        bias="none",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        use_gradient_checkpointing="unsloth",
        random_state=42,
    )

    ds = load_dataset("json", data_files=args.data, split="train")
    print(f"样本 {len(ds)} 条", flush=True)

    trainer = SFTTrainer(
        model=model,
        tokenizer=tok,
        train_dataset=ds,
        args=SFTConfig(
            output_dir=args.out,
            per_device_train_batch_size=args.bs,
            gradient_accumulation_steps=args.accum,
            num_train_epochs=args.epochs,
            learning_rate=args.lr,
            lr_scheduler_type="cosine",
            warmup_ratio=0.03,
            logging_steps=10,
            save_strategy="epoch",
            bf16=True,
            optim="adamw_8bit",
            max_seq_length=args.seq,
            packing=True,
            dataset_kwargs={"skip_prepare_dataset": False},
            report_to="none",
        ),
    )
    trainer.train()

    out = Path(args.out)
    model.save_pretrained(str(out / "lora"))
    tok.save_pretrained(str(out / "lora"))
    print("LoRA 存好了", flush=True)

    model.save_pretrained_merged(str(out / "merged"), tok, save_method="merged_16bit")
    print("合并版存好了", flush=True)

    for quant in ("q4_k_m", "q8_0"):
        try:
            model.save_pretrained_gguf(str(out / f"gguf_{quant}"), tok, quantization_method=quant)
            print(f"GGUF {quant} 好了", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"GGUF {quant} 失败：{exc}", flush=True)


if __name__ == "__main__":
    main()
