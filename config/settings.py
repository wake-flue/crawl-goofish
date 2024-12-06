import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MongoDB配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'goofish_data')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'search_results')

# 目录配置
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 确保所有必要目录存在
for directory in [RAW_DATA_DIR, OUTPUT_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# 日志配置
LOG_CONFIG = {
    "handlers": [
        {
            "sink": os.path.join(LOGS_DIR, "app.log"),
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            "rotation": "1 day",
            "retention": "7 days",
            "level": "INFO",
            "encoding": "utf-8"
        },
        {
            "sink": lambda msg: print(msg),
            "format": "{time:HH:mm:ss} | {level} | {message}",
            "level": "INFO"
        }
    ]
}