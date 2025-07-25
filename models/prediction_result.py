from pydantic import BaseModel
from datetime import datetime

class PredictionResult(BaseModel):
    """预测结果数据模型"""
    
    # 基础信息
    user_name: str
    prediction_time: datetime
    
    # AI预测内容
    prediction_content: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }