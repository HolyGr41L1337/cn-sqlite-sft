# cn-sqlite-sft

一个只干一件事的模型：把中文问题变成 SQLite 查询。

## 目录

| 文件 | 干什么 |
| --- | --- |
| `schema_gen.py` | 让老师模型造新的 SQLite 库（建表语句） |
| `schemas/` | 手写的 8 个库，`schemas/extra/` 是老师生成的 |
| `seed.py` | 给每个库灌 40 行假数据，空表测不出错 |
| `teacher.py` | 出题：中文问题 + SQL，SQL 先跑一遍能不能执行 |
| `verify.py` | 语义检查：这条 SQL 真的回答了这个问题吗 |
| `build_sft.py` | 去重、套 prompt、拼成训练用的 messages |
| `prompt.py` | 训练和评测共用的 prompt，两边必须一致 |
| `eval.py` | 执行准确率：生成 SQL → 执行 → 和标准 SQL 比结果 |
| `train_unsloth.py` | RunPod 上的 LoRA 训练脚本 |

## 流程

```bash
# 1. 造库（可选，已经生成过就跳过）
python schema_gen.py --n 12

# 2. 灌假数据
python seed.py

# 3. 出题（每个库 100 条）
python teacher.py --schema schemas/school.sql --n 20 --rounds 5 --out data/train/school.jsonl

# 4. 语义过滤
python verify.py --data data/train/school.jsonl

# 5. 拼训练集
python build_sft.py

# 6. 评测
python eval.py --model Qwen/Qwen3-4B-Instruct-2507 --data data/test_library.jsonl
```

## 评测口径

- 只看执行结果，不比 SQL 文本
- 标准 SQL 带 `ORDER BY` 才比顺序，否则按多重集
- 同时报「可执行率」，跑挂的 SQL 算错但单独统计

## 计划

- 训练库和测试库分开，测试库（图书馆、健身房）不出现在训练里
- 之后补 DPO：用基座和第一版模型生成错例，配对偏好数据再训一轮
