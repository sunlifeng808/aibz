from typing import Dict, Any
from datetime import datetime
import json
from langchain.prompts import PromptTemplate
from langchain_deepseek import ChatDeepSeek
from config.settings import Settings
from utils.logger import logger

class BaseAgent:
    """基础Agent类"""
    
    def __init__(self, agent_name: str, prompt_file: str):
        self.agent_name = agent_name
        self.settings = Settings()
        self._setup_llm()
        self._setup_prompt(prompt_file)
    
    def _setup_llm(self):
        """设置大语言模型"""
        self.llm = ChatDeepSeek(
            api_key=self.settings.DEEPSEEK_API_KEY,
            model=self.settings.DEEPSEEK_MODEL_NAME,
            temperature=self.settings.LLM_TEMPERATURE,
            max_tokens=self.settings.LLM_MAX_TOKENS,
            top_p=self.settings.LLM_TOP_P
        )
    
    def _setup_prompt(self, prompt_file: str):
        """设置提示词模板"""
        prompt_content = self._load_combined_prompt(prompt_file)
        self.prompt = PromptTemplate(
            input_variables=["user_name", "gender", "complete_data", "current_time", "question"],
            template=prompt_content
        )
    
    def _load_combined_prompt(self, specific_filename: str) -> str:
        """加载通用提示词和专门提示词并组合"""
        
        # 加载专门提示词
        specific_content = self._load_prompt_from_file(specific_filename)
        
        # 加载通用提示词
        common_content = self._load_prompt_from_file("common_agent_prompt.txt")
        
        # 组合提示词：专门提示词 + 通用提示词
        combined_prompt = f"{specific_content}\n\n{common_content}"
        
        return combined_prompt
    
    def _load_prompt_from_file(self, filename: str) -> str:
        """从文件加载提示词"""
        import os
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'prompts', filename)
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.error(f"提示词文件未找到: {filename}")
            return "请提供详细的分析和建议。"
    
    def _format_complete_data(self, fortune_data: Dict[str, Any]) -> str:
        """格式化完整数据"""
        return f"""完整命理分析数据（JSON格式）：
            {json.dumps(fortune_data, ensure_ascii=False, indent=2)}

            请根据以上JSON数据进行专业分析，数据包含：
            1. 八字信息：四柱、格局、十神、五行等基础命理要素
            2. 运势信息：各方面运势分析和预测
            3. 详细分析：性格特点、发展建议等深度解读

            请综合所有信息进行专业分析，不要在回答中显示原始JSON数据。"""
    
    async def analyze(self, shared_context: Dict[str, Any]) -> str:
        """执行分析"""
        try:
            # 准备输入数据
            chain_input = {
                "user_name": shared_context["user_info"].name,
                "gender": shared_context["user_info"].gender,
                "complete_data": self._format_complete_data(shared_context["fortune_data"]),
                "current_time": shared_context["current_time"],
                "question": shared_context["user_info"].question or "请为我进行全面的命理分析"
            }
            
            # 使用LLM生成分析（异步调用）
            chain = self.prompt | self.llm
            result = await chain.ainvoke(chain_input)
            
            content = result.content.strip() if hasattr(result, 'content') else str(result).strip()
            logger.info(f"{self.agent_name} 分析完成，生成内容长度: {len(content)}")
            return content
            
        except Exception as e:
            logger.error(f"{self.agent_name} 分析失败: {str(e)}")
            return f"{self.agent_name}分析暂时不可用，请稍后重试。"

class FoundationAgent(BaseAgent):
    """八字基础分析Agent"""
    
    def __init__(self):
        super().__init__("八字基础分析", "foundation_agent_prompt.txt")

class YongshenAgent(BaseAgent):
    """用神分析Agent"""
    
    def __init__(self):
        super().__init__("用神分析", "yongshen_agent_prompt.txt")

class FortuneAgent(BaseAgent):
    """大运流年分析Agent"""
    
    def __init__(self):
        super().__init__("大运流年分析", "fortune_agent_prompt.txt")

class LifeAspectsAgent(BaseAgent):
    """人生各方面分析Agent"""
    
    def __init__(self):
        super().__init__("人生各方面分析", "life_aspects_agent_prompt.txt")

class SolutionAgent(BaseAgent):
    """解决方案Agent"""
    
    def __init__(self):
        super().__init__("解决方案", "solution_agent_prompt.txt")

class ConsultationAgent(BaseAgent):
    """咨询回答Agent"""
    
    def __init__(self):
        super().__init__("咨询回答", "consultation_agent_prompt.txt")