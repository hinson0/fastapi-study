# import bcrypt

# # 测试 bcrypt 哈希功能
# pwd = b"123123123"
# salt = bcrypt.gensalt()
# hashed = bcrypt.hashpw(pwd, salt)
# print("bcrypt 版本：", bcrypt.__version__)
# print("哈希结果：", hashed)


# %%
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# a = pwd_context.hash("123456")
# a

# %%
# import bcrypt

# # 检查核心属性（无报错则正常）
# print("bcrypt 版本：", bcrypt.__version__)
# print("__about__ 属性：", bcrypt.__about__)  # 4.0+ 版本应有该属性
# print("__about__ 中的版本：", bcrypt.__about__.__version__)

# %%
import pandas as pd
import sys


def read_pandas_csv(file_path: str, sep: str = "|") -> pd.DataFrame:
    """

    python hello.py static/2.psv "|"
        中文术语                        英文翻译                                          场景说明与搭配示例
    0   自主决策  Autonomous Decision-Making  AI领域核心术语，强调无人类干预的独立决策，搭配：autonomous decision-m...
    1  AI智能体                    AI Agent  指能自主感知、决策、执行的AI实体，搭配：intelligent AI agent（智能AI...
    2   环境感知    Environmental Perception  AI获取外部信息的能力，是决策的基础，搭配：real-time environmental ...
    3   决策算法          Decision Algorithm  支撑自主决策的核心技术，搭配：optimized decision algorithm（优化...
    4   自主执行        Autonomous Execution  决策后的落地动作，与自主决策衔接，搭配：autonomous execution of ta...

    ##################################################################
    python hello.py static/1.csv ,
        中文术语                        英文翻译                                          场景说明与搭配示例
    0   自主决策  Autonomous Decision-Making  AI领域核心术语，强调无人类干预的独立决策，搭配：autonomous decision-m...
    1  AI智能体                    AI Agent  指能自主感知、决策、执行的AI实体，搭配：intelligent AI agent（智能AI...
    2   环境感知    Environmental Perception  AI获取外部信息的能力，是决策的基础，搭配：real-time environmental ...
    3   决策算法          Decision Algorithm  支撑自主决策的核心技术，搭配：optimized decision algorithm（优化...
    4   自主执行        Autonomous Execution  决策后的落地动作，与自主决策衔接，搭配：autonomous execution of ta...

    """

    return pd.read_csv(file_path, sep=sep)


if __name__ == "__main__":
    file_path = sys.argv[1]
    sep = sys.argv[2]
    df = read_pandas_csv(file_path, sep=sep)
    print(df.head())
