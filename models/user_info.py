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
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('姓名不能为空')
        if len(v) > 20:
            raise ValueError('姓名长度不能超过20个字符')
        return v.strip()
    
    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['男', '女']:
            raise ValueError('性别必须是"男"或"女"')
        return v
    
    @validator('birth_year')
    def validate_birth_year(cls, v):
        current_year = datetime.now().year
        if v < 1900 or v > current_year:
            raise ValueError(f'出生年份必须在1900-{current_year}之间')
        return v
    
    @validator('birth_month')
    def validate_birth_month(cls, v):
        if v < 1 or v > 12:
            raise ValueError('出生月份必须在1-12之间')
        return v
    
    @validator('birth_day')
    def validate_birth_day(cls, v):
        if v < 1 or v > 31:
            raise ValueError('出生日期必须在1-31之间')
        return v
    
    @validator('birth_hour')
    def validate_birth_hour(cls, v):
        if v < 0 or v > 23:
            raise ValueError('出生小时必须在0-23之间')
        return v
    
    @validator('birth_minute')
    def validate_birth_minute(cls, v):
        if v < 0 or v > 59:
            raise ValueError('出生分钟必须在0-59之间')
        return v
    
    @validator('birth_province')
    def validate_birth_province(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('出生省份不能为空')
        if len(v) > 50:
            raise ValueError('出生省份长度不能超过50个字符')
        return v.strip()
    
    @validator('birth_city')
    def validate_birth_city(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('出生城市不能为空')
        if len(v) > 50:
            raise ValueError('出生城市长度不能超过50个字符')
        return v.strip()
    
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