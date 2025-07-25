from typing import Dict, Any, Optional
from models.user_info import UserInfo
from api_client import YuanFenJuAPIClient
from utils.logger import logger
from utils.data_validator import DataValidator

class BaziService:
    """八字数据服务"""
    
    def __init__(self):
        self.api_client = YuanFenJuAPIClient()
        self.validator = DataValidator()
    
    def get_fortune_analysis(self, user_info: UserInfo, prediction_type: str = 'general') -> Dict[str, Any]:
        """获取运势分析（包含完整的八字和运势信息）"""
        # 验证用户信息
        user_data = user_info.dict()
        validation_errors = self.validator.validate_user_info(user_data)
        if validation_errors:
            raise ValueError(f"用户信息验证失败: {', '.join(validation_errors)}")
        
        # 调用API获取运势分析（包含八字信息）
        logger.info(f"开始获取运势分析: {user_info.name}, 类型: {prediction_type}")
        api_response = self.api_client.get_fortune_prediction(
            user_info.to_api_params(),
            prediction_type
        )
        
        # 验证API响应
        if not self.validator.validate_api_response(api_response):
            raise ValueError("API响应数据格式不正确")
        
        # 直接返回API响应的data部分
        fortune_data = api_response.get('data', {})
        
        logger.info(f"运势分析获取成功: {user_info.name}")
        return fortune_data