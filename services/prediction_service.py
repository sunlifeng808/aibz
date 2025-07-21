from typing import Dict, Any, Optional
from datetime import datetime
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from models.user_info import UserInfo
from models.bazi_data import BaziData
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

八字信息：
{{bazi_info}}

运势数据：
{{fortune_data}}

用户咨询：{{question}}

请开始你的分析：
        """
        
        self.comprehensive_prompt = PromptTemplate(
            input_variables=["user_name", "gender", "bazi_info", "fortune_data", "question", "current_time"],
            template=comprehensive_template
        )
        
        # 事业预测提示词模板
        career_template = f"""
{self.settings.SYSTEM_PROMPT_CAREER.strip()}

当前时间：{{current_time}}

用户信息：
姓名：{{user_name}}
性别：{{gender}}

八字信息：
{{bazi_info}}

运势数据：
{{fortune_data}}

请开始你的事业分析：
        """
        
        self.career_prompt = PromptTemplate(
            input_variables=["user_name", "gender", "bazi_info", "fortune_data", "current_time"],
            template=career_template
        )
        
        # 感情预测提示词模板
        relationship_template = f"""
{self.settings.SYSTEM_PROMPT_RELATIONSHIP.strip()}

当前时间：{{current_time}}

用户信息：
姓名：{{user_name}}
性别：{{gender}}

八字信息：
{{bazi_info}}

运势数据：
{{fortune_data}}

请开始你的感情分析：
        """
        
        self.relationship_prompt = PromptTemplate(
            input_variables=["user_name", "gender", "bazi_info", "fortune_data", "current_time"],
            template=relationship_template
        )
    
    def get_comprehensive_prediction(self, user_info: UserInfo) -> PredictionResult:
        """获取综合预测"""
        logger.log_user_action("综合预测请求", user_info.dict())
        
        # 获取八字数据
        bazi_data = self.bazi_service.get_bazi_analysis(user_info)
        
        # 获取运势数据
        fortune_data = self.bazi_service.get_fortune_analysis(user_info, 'comprehensive')
        
        # 生成AI预测
        prediction_content = self._generate_prediction(
            user_info, bazi_data, fortune_data, 'comprehensive'
        )
        
        # 创建预测结果
        result = PredictionResult(
            user_name=user_info.name,
            prediction_time=datetime.now(),
            bazi_summary=bazi_data.get_summary(),
            prediction_content=prediction_content,
            prediction_type="综合运势"
        )
        
        logger.log_prediction_request(user_info.name, "综合预测", True)
        return result
    
    def get_career_prediction(self, user_info: UserInfo) -> PredictionResult:
        """获取事业预测"""
        logger.log_user_action("事业预测请求", user_info.dict())
        
        # 获取八字数据
        bazi_data = self.bazi_service.get_bazi_analysis(user_info)
        
        # 获取运势数据
        fortune_data = self.bazi_service.get_fortune_analysis(user_info, 'career')
        
        # 生成AI预测
        prediction_content = self._generate_prediction(
            user_info, bazi_data, fortune_data, 'career'
        )
        
        # 创建预测结果
        result = PredictionResult(
            user_name=user_info.name,
            prediction_time=datetime.now(),
            bazi_summary=bazi_data.get_summary(),
            prediction_content=prediction_content,
            prediction_type="事业运势"
        )
        
        logger.log_prediction_request(user_info.name, "事业预测", True)
        return result
    
    def get_relationship_prediction(self, user_info: UserInfo) -> PredictionResult:
        """获取感情预测"""
        logger.log_user_action("感情预测请求", user_info.dict())
        
        # 获取八字数据
        bazi_data = self.bazi_service.get_bazi_analysis(user_info)
        
        # 获取运势数据
        fortune_data = self.bazi_service.get_fortune_analysis(user_info, 'relationship')
        
        # 生成AI预测
        prediction_content = self._generate_prediction(
            user_info, bazi_data, fortune_data, 'relationship'
        )
        
        # 创建预测结果
        result = PredictionResult(
            user_name=user_info.name,
            prediction_time=datetime.now(),
            bazi_summary=bazi_data.get_summary(),
            prediction_content=prediction_content,
            prediction_type="感情运势"
        )
        
        logger.log_prediction_request(user_info.name, "感情预测", True)
        return result
    
    def _generate_prediction(self, user_info: UserInfo, bazi_data: BaziData, 
                           fortune_data: Dict[str, Any], prediction_type: str) -> str:
        """生成AI预测内容"""
        # 准备输入数据
        bazi_info = self._format_bazi_info(bazi_data)
        fortune_info = self._format_fortune_info(fortune_data)
        current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        
        # 选择合适的提示词模板
        if prediction_type == 'career':
            prompt = self.career_prompt
            chain_input = {
                "user_name": user_info.name,
                "gender": user_info.gender,
                "bazi_info": bazi_info,
                "fortune_data": fortune_info,
                "current_time": current_time
            }
        elif prediction_type == 'relationship':
            prompt = self.relationship_prompt
            chain_input = {
                "user_name": user_info.name,
                "gender": user_info.gender,
                "bazi_info": bazi_info,
                "fortune_data": fortune_info,
                "current_time": current_time
            }
        else:  # comprehensive
            prompt = self.comprehensive_prompt
            chain_input = {
                "user_name": user_info.name,
                "gender": user_info.gender,
                "bazi_info": bazi_info,
                "fortune_data": fortune_info,
                "question": user_info.question or "请为我进行全面的命理分析",
                "current_time": current_time
            }
        
        # 使用LLM生成预测
        chain = prompt | self.llm
        result = chain.invoke(chain_input)
        return result.content.strip() if hasattr(result, 'content') else str(result).strip()
    
    def _format_bazi_info(self, bazi_data: BaziData) -> str:
        """格式化八字信息"""
        info_parts = [
            f"四柱八字：{bazi_data.get_bazi_string()}",
            f"命格：{bazi_data.pattern or '未知'}",
            f"用神：{bazi_data.yongshen or '未知'}",
            f"忌神：{bazi_data.jishen or '未知'}"
        ]
        
        if bazi_data.ten_gods:
            info_parts.append("十神关系：")
            for position, god in bazi_data.ten_gods.items():
                info_parts.append(f"  {position}: {god}")
        
        return "\n".join(info_parts)
    
    def _format_fortune_info(self, fortune_data: Dict[str, Any]) -> str:
        """格式化运势信息"""
        info_parts = []
        
        # 处理缘分居API的运势数据格式
        detail_info = fortune_data.get('detail_info', {})
        yunshi_year_info = detail_info.get('yunshi_year_info', {})
        yunshi_year = yunshi_year_info.get('yunshi_year', {})
        indication = yunshi_year.get('indication', {})
        
        if indication:
            aspect_names = {
                'shiye': '事业运势',
                'caiyun': '财运',
                'yinyuan': '感情运势',
                'jiankang': '健康运势',
                'yunshi': '整体运势',
                'xueye': '学业运势'
            }
            
            for key, name in aspect_names.items():
                if key in indication:
                    info_parts.append(f"{name}：{indication[key]}")
        
        # 如果没有运势信息，提供默认格式
        if not info_parts:
            info_parts = [
                "事业运势：运势平稳，适合稳步发展",
                "财运：财运平稳，理财需谨慎",
                "感情运势：人际关系和谐",
                "健康运势：身体状况良好，注意劳逸结合"
            ]
        
        return "\n".join(info_parts)
    
    def get_service_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        return {
            "service_name": "PredictionService",
            "llm_status": "active",
            "bazi_service_status": self.bazi_service.validate_service_health(),
            "available_predictions": ["综合预测", "事业预测", "感情预测"]
        }