import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from models.user_info import UserInfo

class DataValidator:
    """数据验证工具类"""
    
    @staticmethod
    def validate_user_info(user_info: Dict[str, Any]) -> List[str]:
        """验证用户信息，返回错误列表"""
        errors = []
        
        # 验证姓名
        name = user_info.get('name', '').strip()
        if not name:
            errors.append('姓名不能为空')
        elif len(name) > 20:
            errors.append('姓名长度不能超过20个字符')
        elif not re.match(r'^[\u4e00-\u9fa5a-zA-Z\s]+$', name):
            errors.append('姓名只能包含中文、英文字母和空格')
        
        # 验证性别
        gender = user_info.get('gender', '')
        if gender not in ['男', '女']:
            errors.append('请选择正确的性别')
        
        # 验证出生日期
        try:
            birth_year = int(user_info.get('birth_year', 0))
            birth_month = int(user_info.get('birth_month', 0))
            birth_day = int(user_info.get('birth_day', 0))
            birth_hour = int(user_info.get('birth_hour', 0))
            birth_minute = int(user_info.get('birth_minute', 0))
            
            current_year = datetime.now().year
            if birth_year < 1900 or birth_year > current_year:
                errors.append(f'出生年份必须在1900-{current_year}之间')
            
            if birth_month < 1 or birth_month > 12:
                errors.append('出生月份必须在1-12之间')
            
            if birth_day < 1 or birth_day > 31:
                errors.append('出生日期必须在1-31之间')
            
            if birth_hour < 0 or birth_hour > 23:
                errors.append('出生小时必须在0-23之间')
            
            if birth_minute < 0 or birth_minute > 59:
                errors.append('出生分钟必须在0-59之间')
            
            # 验证日期是否真实存在
            try:
                datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
            except ValueError:
                errors.append('请输入有效的出生日期时间')
                
        except (ValueError, TypeError):
            errors.append('出生日期时间格式不正确')
        
        # 验证出生省份
        birth_province = user_info.get('birth_province', '').strip()
        if not birth_province:
            errors.append('出生省份不能为空')
        elif len(birth_province) > 50:
            errors.append('出生省份长度不能超过50个字符')
        
        # 验证出生城市
        birth_city = user_info.get('birth_city', '').strip()
        if not birth_city:
            errors.append('出生城市不能为空')
        elif len(birth_city) > 50:
            errors.append('出生城市长度不能超过50个字符')
        
        # 验证咨询问题（可选）
        question = user_info.get('question', '')
        if question and len(question) > 500:
            errors.append('咨询问题长度不能超过500个字符')
        
        return errors
    
    @staticmethod
    def validate_api_response(response: Dict[str, Any]) -> bool:
        """验证缘分居API响应数据的完整性"""
        if not isinstance(response, dict):
            return False
        
        # 检查缘分居API的基本字段
        if 'errcode' not in response:
            return False
        
        # errcode为0表示成功
        if response.get('errcode') != 0:
            return False
        
        # 检查数据字段
        data = response.get('data', {})
        if not isinstance(data, dict):
            return False
        
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """清理用户输入，移除潜在的危险字符"""
        if not isinstance(text, str):
            return str(text)
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除特殊字符
        text = re.sub(r'[<>"\'\\\/]', '', text)
        
        # 限制长度
        if len(text) > 1000:
            text = text[:1000]
        
        return text.strip()
    
    @staticmethod
    def validate_bazi_data(bazi_data: Dict[str, Any]) -> List[str]:
        """验证八字数据的完整性"""
        errors = []
        
        # 检查四柱是否完整
        pillars = ['year_pillar', 'month_pillar', 'day_pillar', 'hour_pillar']
        for pillar in pillars:
            if not bazi_data.get(pillar):
                errors.append(f'缺少{pillar}数据')
        
        # 检查格局信息
        if not bazi_data.get('pattern'):
            errors.append('缺少格局分析')
        
        return errors
    
    @staticmethod
    def is_valid_chinese_name(name: str) -> bool:
        """验证是否为有效的中文姓名"""
        if not name or len(name.strip()) == 0:
            return False
        
        name = name.strip()
        
        # 长度检查
        if len(name) < 2 or len(name) > 10:
            return False
        
        # 字符检查（中文字符）
        if not re.match(r'^[\u4e00-\u9fa5]+$', name):
            return False
        
        return True
    
    @staticmethod
    def validate_location(location: str) -> bool:
        """验证地点格式"""
        if not location or len(location.strip()) == 0:
            return False
        
        location = location.strip()
        
        # 长度检查
        if len(location) > 100:
            return False
        
        # 基本格式检查
        if re.search(r'[<>"\'\\\/]', location):
            return False
        
        return True