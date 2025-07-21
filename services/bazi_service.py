from typing import Dict, Any, Optional
from models.user_info import UserInfo
from models.bazi_data import BaziData
from api_client import YuanFenJuAPIClient
from utils.logger import logger
from utils.data_validator import DataValidator

class BaziService:
    """八字数据服务"""
    
    def __init__(self):
        self.api_client = YuanFenJuAPIClient()
        self.validator = DataValidator()
        self._cache = {}  # 简单的内存缓存
    
    def get_bazi_analysis(self, user_info: UserInfo) -> BaziData:
        """获取八字分析数据"""
        # 生成缓存键
        cache_key = self._generate_cache_key(user_info)
        
        # 检查缓存
        if cache_key in self._cache:
            logger.info(f"从缓存获取八字数据: {user_info.name}")
            return self._cache[cache_key]
        
        # 验证用户信息
        user_data = user_info.dict()
        validation_errors = self.validator.validate_user_info(user_data)
        if validation_errors:
            raise ValueError(f"用户信息验证失败: {', '.join(validation_errors)}")
        
        # 调用API获取八字分析
        logger.info(f"开始获取八字分析: {user_info.name}")
        api_response = self.api_client.get_bazi_analysis(user_data)
        
        # 验证API响应
        if not self.validator.validate_api_response(api_response):
            raise ValueError("API响应数据格式不正确")
        
        # 转换为BaziData对象
        bazi_data = BaziData.from_api_response(api_response.get('data', {}))
        
        # 验证八字数据完整性
        bazi_validation_errors = self.validator.validate_bazi_data(bazi_data.dict())
        if bazi_validation_errors:
            logger.warning(f"八字数据不完整: {', '.join(bazi_validation_errors)}")
        
        # 缓存结果
        self._cache[cache_key] = bazi_data
        
        logger.info(f"八字分析获取成功: {user_info.name}")
        return bazi_data
    
    def get_fortune_analysis(self, user_info: UserInfo, prediction_type: str = 'general') -> Dict[str, Any]:
        """获取运势分析"""
        logger.info(f"开始获取运势分析: {prediction_type}")
        
        # 调用API获取运势预测
        api_response = self.api_client.get_fortune_prediction(
            user_info.to_api_params(),
            prediction_type
        )
        
        if not self.validator.validate_api_response(api_response):
            raise ValueError("运势分析API响应数据格式不正确")
        
        logger.info(f"运势分析获取成功: {prediction_type}")
        return api_response.get('data', {})
    
    def _generate_cache_key(self, user_info: UserInfo) -> str:
        """生成缓存键"""
        return f"{user_info.name}_{user_info.birth_year}_{user_info.birth_month}_{user_info.birth_day}_{user_info.birth_hour}_{user_info.birth_minute}"
    

    
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