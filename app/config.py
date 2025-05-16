import os

# 默认模型路径
WAV2LIP_MODEL_PATH = os.path.join('models', 'wav2lip.pth')

# MuseTalk 配置
MUSETALK_DIR = os.path.join('external', 'MuseTalk')
MUSETALK_VERSION = 'v1.5'  # 可选 'v1.0' 或 'v1.5'

# MuseTalk 更详细配置
MUSETALK_CONFIG = {
    'v1.0': {
        'model_dir': 'models/musetalk',
        'model_file': 'pytorch_model.bin',
        'config_file': 'musetalk.json',
        'version_arg': 'v1'
    },
    'v1.5': {
        'model_dir': 'models/musetalkV15',
        'model_file': 'unet.pth',
        'config_file': 'musetalk.json',
        'version_arg': 'v15'
    }
}

# MuseTalk 推理参数
MUSETALK_INFERENCE = {
    'fps': 25,
    'bbox_shift': 0,  # 嘴部区域调整参数，正值增加嘴部开度，负值减少嘴部开度
    'use_float16': True,  # 是否使用半精度推理以节省显存
}

# 默认输入输出目录
INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

# 其他可扩展配置
