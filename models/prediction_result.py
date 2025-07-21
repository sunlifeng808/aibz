from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PredictionResult(BaseModel):
    """预测结果数据模型"""
    
    # 基础信息
    user_name: str
    prediction_time: datetime
    
    # 八字信息
    bazi_summary: str
    
    # AI预测内容
    prediction_content: str
    
    # 建议和指导
    suggestions: Optional[str] = None
    
    # 免责声明
    disclaimer: str = "本预测仅供娱乐参考，不构成任何决策建议。请理性对待预测结果，人生的幸福需要通过自己的努力来创造。"
    
    # 数据来源
    data_source: str = "缘分居国学API + DeepSeek AI"
    
    # 预测类型
    prediction_type: Optional[str] = "综合运势"
    
    def get_formatted_time(self) -> str:
        """获取格式化的预测时间"""
        return self.prediction_time.strftime('%Y年%m月%d日 %H:%M:%S')
    
    def get_export_content(self) -> str:
        """获取可导出的完整内容"""
        content_parts = [
            f"=== {self.user_name} 的命理预测报告 ===",
            f"预测时间：{self.get_formatted_time()}",
            f"预测类型：{self.prediction_type}",
            "",
            "=== 八字信息 ===",
            self.bazi_summary,
            "",
            "=== AI预测分析 ===",
            self.prediction_content,
        ]
        
        if self.suggestions:
            content_parts.extend([
                "",
                "=== 建议指导 ===",
                self.suggestions
            ])
        
        content_parts.extend([
            "",
            "=== 数据来源 ===",
            self.data_source,
            "",
            "=== 免责声明 ===",
            self.disclaimer
        ])
        
        return "\n".join(content_parts)
    
    def get_share_content(self) -> str:
        """获取可分享的简化内容"""
        return f"""
🔮 {self.user_name} 的命理预测

📊 八字信息：
{self.bazi_summary}

🤖 AI分析：
{self.prediction_content[:200]}...

⚠️ 本预测仅供娱乐参考
        """.strip()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }