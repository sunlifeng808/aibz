import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

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
    DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"
    DEEPSEEK_API_BASE_URL = os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL_NAME = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")
    
    # 大模型配置
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "chatdeepseek")  # 支持: chatdeepseek, chatopenai
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    LLM_TOP_P = float(os.getenv("LLM_TOP_P", "0.9"))
    
    # 系统提示词配置
    SYSTEM_PROMPT_COMPREHENSIVE = os.getenv("SYSTEM_PROMPT_COMPREHENSIVE", """
你是一位专业的命理学大师，精通八字命理分析。请根据以下信息为用户提供详细的命理分析和人生指导。

请从以下几个方面进行分析：
1. 八字格局分析
2. 性格特点解读
3. 事业发展建议
4. 财运分析
5. 感情婚姻
6. 健康养生
7. 人生建议

要求：
- 语言通俗易懂，避免过于专业的术语
- 分析要有逻辑性和条理性
- 给出具体可行的建议
- 保持积极正面的态度
- 字数控制在800-1200字
- 结合现代生活实际情况
    """)
    
    SYSTEM_PROMPT_CAREER = os.getenv("SYSTEM_PROMPT_CAREER", """
你是一位专业的职业规划师和命理学专家。请根据用户的八字信息，为其提供详细的事业发展分析和建议。

请重点分析：
1. 适合的职业方向和行业
2. 事业发展的最佳时机
3. 职场人际关系处理
4. 创业还是打工的建议
5. 财富积累的方式
6. 需要注意的事业风险

要求：
- 结合八字特点给出具体建议
- 分析要实用可操作
- 语言简洁明了
- 字数控制在600-800字
    """)
    
    SYSTEM_PROMPT_RELATIONSHIP = os.getenv("SYSTEM_PROMPT_RELATIONSHIP", """
你是一位专业的情感咨询师和命理学专家。请根据用户的八字信息，为其提供详细的感情婚姻分析和建议。

请重点分析：
1. 感情性格特点
2. 适合的伴侣类型
3. 恋爱和婚姻运势
4. 最佳结婚时机
5. 感情中需要注意的问题
6. 如何维护长久关系

要求：
- 分析要温和贴心
- 给出实用的感情建议
- 避免过于绝对的判断
- 字数控制在600-800字
    """)
    
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