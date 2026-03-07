import json
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据保存文件
DATA_FILE = BASE_DIR / "test_data.json"


def load_data():
    """
    读取保存的数据
    """
    if DATA_FILE.exists():
        # 检查文件是否为空
        if DATA_FILE.stat().st_size == 0:  # 文件大小为0
            return {}
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # 文件内容不是有效的JSON时，返回空字典
            print(f"警告: {DATA_FILE} 内容不是有效的JSON，返回空字典")
            return {}

    return {}


def save_data(data: dict):
    """
    保存数据
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)