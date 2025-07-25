import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def load_prompt_from_file(filename: str) -> str:
    """从文件加载提示词"""
    prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', filename)
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        # 如果文件不存在，返回默认提示词
        return "请提供详细的分析和建议。"

class Settings:
    """系统配置类"""
    
    # API配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    YUANFENJU_API_KEY = os.getenv("YUANFENJU_API_KEY", "")
    YUANFENJU_API_URL = os.getenv("YUANFENJU_API_URL", "https://api.yuanfenju.com")
    
    # 系统配置
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API限制
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "1"))
    
    # DeepSeek API配置
    DEEPSEEK_API_BASE_URL = os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL_NAME = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")
    
    # 大模型配置
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "chatdeepseek")  # 支持: chatdeepseek, chatopenai
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    LLM_TOP_P = float(os.getenv("LLM_TOP_P", "0.9"))
    
    # 系统提示词配置
    SYSTEM_PROMPT_COMPREHENSIVE = load_prompt_from_file('comprehensive_prompt.txt')
    
    # 缓存配置
    CACHE_TTL = 3600  # 1小时
    
    @classmethod
    def validate_config(cls):
        """验证配置是否完整"""
        missing_configs = []
        
        if not cls.DEEPSEEK_API_KEY:
            missing_configs.append("DEEPSEEK_API_KEY")
        
        if not cls.YUANFENJU_API_KEY:
            missing_configs.append("YUANFENJU_API_KEY")
        
        if missing_configs:
            raise ValueError(f"缺少必要的配置项: {', '.join(missing_configs)}")
        
        return True

# 创建全局配置实例
settings = Settings()