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
        self._cache = {}  # 简单的内存缓存
    
    def get_fortune_analysis(self, user_info: UserInfo, prediction_type: str = 'general') -> Dict[str, Any]:
        """获取运势分析（包含完整的八字和运势信息）"""
        # 生成缓存键
        cache_key = self._generate_cache_key(user_info, prediction_type)
        
        # 检查缓存
        if cache_key in self._cache:
            logger.info(f"从缓存获取运势数据: {user_info.name}")
            return self._cache[cache_key]
        
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
        
        # 缓存结果
        self._cache[cache_key] = fortune_data
        
        logger.info(f"运势分析获取成功: {user_info.name}")
        return fortune_data
    

    
    def _generate_cache_key(self, user_info: UserInfo, prediction_type: str = 'general') -> str:
        """生成缓存键"""
        return f"{user_info.name}_{user_info.birth_year}_{user_info.birth_month}_{user_info.birth_day}_{user_info.birth_hour}_{user_info.birth_minute}_{prediction_type}"
    

    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        logger.info("八字数据缓存已清空")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息"""
        return {
            "cache_size": len(self._cache),
            "cached_users": list(self._cache.keys())
        }
    
    def validate_service_health(self) -> Dict[str, Any]:
        """验证服务健康状态"""
        health_status = {
            "service_name": "BaziService",
            "status": "healthy",
            "api_connection": False,
            "cache_status": "active",
            "errors": []
        }
        
        try:
            # 测试API连接
            health_status["api_connection"] = self.api_client.test_connection()
            
            if not health_status["api_connection"]:
                health_status["errors"].append("API连接失败")
                health_status["status"] = "degraded"
            
        except Exception as e:
            health_status["errors"].append(f"健康检查失败: {str(e)}")
            health_status["status"] = "unhealthy"
        
        return health_status