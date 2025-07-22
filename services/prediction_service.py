from typing import Dict, Any, Optional
from datetime import datetime
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from models.user_info import UserInfo
from models.prediction_result import PredictionResult
from services.bazi_service import BaziService
from config.settings import Settings
from utils.logger import logger
from langchain_deepseek import ChatDeepSeek

class PredictionService:
    """预测服务"""
    
    def __init__(self):
        self.settings = Settings()
        self.bazi_service = BaziService()
        self._setup_llm()
        self._setup_prompts()
    
    def _setup_llm(self):
        """设置大语言模型"""
        self.llm = ChatDeepSeek(
            api_key=self.settings.DEEPSEEK_API_KEY,
            model=self.settings.DEEPSEEK_MODEL_NAME,
            temperature=self.settings.LLM_TEMPERATURE,
            max_tokens=self.settings.LLM_MAX_TOKENS,
            top_p=self.settings.LLM_TOP_P
        )
    
    def _setup_prompts(self):
        """设置提示词模板"""
        # 综合预测提示词模板
        comprehensive_template = f"""
{self.settings.SYSTEM_PROMPT_COMPREHENSIVE.strip()}

当前时间：{{current_time}}

用户信息：
姓名：{{user_name}}
性别：{{gender}}

完整命理数据：
{{complete_data}}

用户咨询：{{question}}

请开始你的分析：
        """
        
        self.comprehensive_prompt = PromptTemplate(
            input_variables=["user_name", "gender", "complete_data", "question", "current_time"],
            template=comprehensive_template
        )
        
        # 事业预测提示词模板
        career_template = f"""
{self.settings.SYSTEM_PROMPT_CAREER.strip()}

当前时间：{{current_time}}

用户信息：
姓名：{{user_name}}
性别：{{gender}}

完整命理数据：
{{complete_data}}

请开始你的事业分析：
        """
        
        self.career_prompt = PromptTemplate(
            input_variables=["user_name", "gender", "complete_data", "current_time"],
            template=career_template
        )
        
        # 感情预测提示词模板
        relationship_template = f"""
{self.settings.SYSTEM_PROMPT_RELATIONSHIP.strip()}

当前时间：{{current_time}}

用户信息：
姓名：{{user_name}}
性别：{{gender}}

完整命理数据：
{{complete_data}}

请开始你的感情分析：
        """
        
        self.relationship_prompt = PromptTemplate(
            input_variables=["user_name", "gender", "complete_data", "current_time"],
            template=relationship_template
        )
    
    def get_comprehensive_prediction(self, user_info: UserInfo) -> PredictionResult:
        """获取综合预测"""
        logger.log_user_action("综合预测请求", user_info.dict())
        
        # 获取运势数据（包含八字信息）
        fortune_data = self.bazi_service.get_fortune_analysis(user_info, 'comprehensive')
        
        # 生成AI预测
        prediction_content = self._generate_prediction(
            user_info, fortune_data, 'comprehensive'
        )
        
        # 创建预测结果
        result = PredictionResult(
            user_name=user_info.name,
            prediction_time=datetime.now(),
            bazi_summary="",  # 不再显示八字摘要
            prediction_content=prediction_content,
            prediction_type="综合运势"
        )
        
        logger.log_prediction_request(user_info.name, "综合预测", True)
        return result
    
    def get_career_prediction(self, user_info: UserInfo) -> PredictionResult:
        """获取事业预测"""
        logger.log_user_action("事业预测请求", user_info.dict())
        
        # 获取运势数据（包含八字信息）
        fortune_data = self.bazi_service.get_fortune_analysis(user_info, 'career')
        
        # 生成AI预测
        prediction_content = self._generate_prediction(
            user_info, fortune_data, 'career'
        )
        
        # 创建预测结果
        result = PredictionResult(
            user_name=user_info.name,
            prediction_time=datetime.now(),
            bazi_summary="",  # 不再显示八字摘要
            prediction_content=prediction_content,
            prediction_type="事业运势"
        )
        
        logger.log_prediction_request(user_info.name, "事业预测", True)
        return result
    
    def get_relationship_prediction(self, user_info: UserInfo) -> PredictionResult:
        """获取感情预测"""
        logger.log_user_action("感情预测请求", user_info.dict())
        
        # 获取运势数据（包含八字信息）
        fortune_data = self.bazi_service.get_fortune_analysis(user_info, 'relationship')
        
        # 生成AI预测
        prediction_content = self._generate_prediction(
            user_info, fortune_data, 'relationship'
        )
        
        # 创建预测结果
        result = PredictionResult(
            user_name=user_info.name,
            prediction_time=datetime.now(),
            bazi_summary="",  # 不再显示八字摘要
            prediction_content=prediction_content,
            prediction_type="感情运势"
        )
        
        logger.log_prediction_request(user_info.name, "感情预测", True)
        return result
    
    def _generate_prediction(self, user_info: UserInfo, fortune_data: Dict[str, Any], prediction_type: str) -> str:
        """生成AI预测内容"""
        # 准备输入数据
        complete_data = self._format_complete_data(fortune_data)
        current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        
        # 选择合适的提示词模板
        if prediction_type == 'career':
            prompt = self.career_prompt
            chain_input = {
                "user_name": user_info.name,
                "gender": user_info.gender,
                "complete_data": complete_data,
                "current_time": current_time
            }
        elif prediction_type == 'relationship':
            prompt = self.relationship_prompt
            chain_input = {
                "user_name": user_info.name,
                "gender": user_info.gender,
                "complete_data": complete_data,
                "current_time": current_time
            }
        else:  # comprehensive
            prompt = self.comprehensive_prompt
            chain_input = {
                "user_name": user_info.name,
                "gender": user_info.gender,
                "complete_data": complete_data,
                "question": user_info.question or "请为我进行全面的命理分析",
                "current_time": current_time
            }
        
        # 使用LLM生成预测
        chain = prompt | self.llm
        result = chain.invoke(chain_input)
        return result.content.strip() if hasattr(result, 'content') else str(result).strip()
    
    def _format_complete_data(self, fortune_data: Dict[str, Any]) -> str:
        """格式化完整数据（包含八字和运势信息）"""
        return f"""完整命理分析数据（JSON格式）：
{json.dumps(fortune_data, ensure_ascii=False, indent=2)}

请根据以上JSON数据进行全面的命理分析，数据包含：
1. 八字信息：四柱、格局、十神、五行等基础命理要素
2. 运势信息：各方面运势分析和预测
3. 详细分析：性格特点、发展建议等深度解读

请综合所有信息进行专业分析，不要在回答中显示原始JSON数据。"""
    
    def get_service_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        return {
            "service_name": "PredictionService",
            "llm_status": "active",
            "bazi_service_status": self.bazi_service.validate_service_health(),
            "available_predictions": ["综合预测", "事业预测", "感情预测"]
        }