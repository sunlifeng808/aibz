from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class UserInfo(BaseModel):
    """用户信息数据模型"""
    
    name: str
    gender: str  # "男" 或 "女"
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: int
    birth_minute: int = 0
    birth_province: str
    birth_city: str
    question: Optional[str] = None
    
    def get_birth_datetime_str(self) -> str:
        """获取格式化的出生日期时间字符串"""
        return f"{self.birth_year}-{self.birth_month:02d}-{self.birth_day:02d} {self.birth_hour:02d}:{self.birth_minute:02d}"
    
    def to_api_params(self) -> dict:
        """转换为API调用参数"""
        return {
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "birth_month": self.birth_month,
            "birth_day": self.birth_day,
            "birth_hour": self.birth_hour,
            "birth_minute": self.birth_minute,
            "birth_province": self.birth_province,
            "birth_city": self.birth_city
        }