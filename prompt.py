"""训练和推理共用的一套 prompt，两边必须一模一样，不然分数都是假的。"""

SYSTEM = (
    "你是 SQLite 查询专家。用户会给你建表语句和一句中文问题，"
    "你要写出一条能回答它的 SQLite 查询。只输出 SQL，不要解释。"
)

USER = """建表语句：
{ddl}

问题：{question}"""


def build(ddl: str, question: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": USER.format(ddl=ddl.strip(), question=question.strip())},
    ]
