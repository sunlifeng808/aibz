from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class PredictionResult(BaseModel):
    """预测结果数据模型"""
    
    # 基础信息
    user_name: str
    prediction_time: datetime
    
    # AI预测内容 - 改为字典格式支持JSON结构化数据
    prediction_content: Dict[str, Any]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }