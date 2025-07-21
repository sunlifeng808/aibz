import requests
import time
from typing import Dict, Any, Optional
from config.settings import Settings
from utils.logger import logger

class YuanFenJuAPIClient:
    """缘分居国学API客户端"""
    
    def __init__(self):
        self.settings = Settings()
        self.base_url = self.settings.YUANFENJU_API_URL
        self.api_key = self.settings.YUANFENJU_API_KEY
        self.session = requests.Session()
        
        # 设置默认headers
        self.session.headers.update({
            'User-Agent': 'AIBZ/1.0'
        })
    
    def _make_request(self, endpoint: str, data: Dict[str, Any], method: str = 'POST') -> Dict[str, Any]:
        """发送API请求"""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.settings.MAX_RETRIES + 1):
            try:
                logger.debug(f"发送API请求: {method} {url}")
                
                if method.upper() == 'POST':
                    response = self.session.post(
                        url,
                        data=data,
                        timeout=self.settings.REQUEST_TIMEOUT
                    )
                else:
                    response = self.session.get(
                        url,
                        params=data,
                        timeout=self.settings.REQUEST_TIMEOUT
                    )
                
                response.raise_for_status()
                result = response.json()
                
                logger.log_api_request(
                    api_name=f"缘分居API-{endpoint}",
                    request_data=data,
                    response_data=result
                )
                
                return result
                
            except requests.exceptions.RequestException as e:
                error_msg = f"API请求失败 (尝试 {attempt + 1}/{self.settings.MAX_RETRIES + 1}): {str(e)}"
                logger.warning(error_msg)
                
                if attempt == self.settings.MAX_RETRIES:
                    logger.log_api_request(
                        api_name=f"缘分居API-{endpoint}",
                        request_data=data,
                        error=error_msg
                    )
                    raise Exception(f"API请求最终失败: {str(e)}")
                
                # 等待后重试
                time.sleep(self.settings.RETRY_DELAY * (attempt + 1))
    
    def get_bazi_analysis(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """获取八字分析"""
        # 构建API请求数据
        api_data = {
            'name': user_data.get('name'),
            'sex': '1' if user_data.get('gender') == '男' else '0',
            'type': '1',  # 公历类型
            'year': str(user_data.get('birth_year')),
            'month': str(user_data.get('birth_month')),
            'day': str(user_data.get('birth_day')),
            'hours': str(user_data.get('birth_hour')),
            'minute': str(user_data.get('birth_minute', 0)),
            'province': user_data.get('birth_province', ''),
            'city': user_data.get('birth_city', ''),
            'api_key': self.api_key
        }
        
        logger.info(f"请求八字分析: {user_data.get('name')}")
        
        try:
            result = self._make_request('index.php/v1/Bazi/paipan', api_data)
            
            # 验证响应数据
            if not self._validate_bazi_response(result):
                logger.error(f"八字分析API响应数据验证失败，实际响应: {result}")
                raise Exception("API返回数据格式不正确")
            
            return result
            
        except Exception as e:
            logger.error(f"八字分析请求失败: {str(e)}")
            # 返回模拟数据作为降级方案
            return self._get_fallback_bazi_data(user_data)
    
    def get_fortune_prediction(self, user_info: Dict[str, Any], prediction_type: str = 'general') -> Dict[str, Any]:
        """获取运势预测"""
        # 根据缘分居API的实际参数格式
        api_data = {
            'name': user_info.get('name', '用户'),
            'sex': '0' if user_info.get('gender') == '女' else '1',
            'type': '1',  # 公历类型
            'year': str(user_info.get('birth_year', 1990)),
            'month': str(user_info.get('birth_month', 1)),
            'day': str(user_info.get('birth_day', 1)),
            'hours': str(user_info.get('birth_hour', 12)),
            'minute': str(user_info.get('birth_minute', 0)),
            'province': user_info.get('birth_province', ''),
            'city': user_info.get('birth_city', ''),
            'api_key': self.api_key
        }
        
        logger.info(f"请求运势预测: {prediction_type}")
        
        try:
            result = self._make_request('index.php/v1/Bazi/jingsuan', api_data)
            return result
            
        except Exception as e:
            logger.error(f"运势预测请求失败: {str(e)}")
            # 返回模拟数据作为降级方案
            return self._get_fallback_fortune_data(prediction_type)
    
    def _validate_bazi_response(self, response: Dict[str, Any]) -> bool:
        """验证八字分析响应数据"""
        if not isinstance(response, dict):
            return False
        
        # 检查缘分居API响应格式
        if 'errcode' not in response:
            return False
        
        if response.get('errcode') != 0:
            return False
        
        # 检查数据字段
        data = response.get('data', {})
        if not isinstance(data, dict):
            return False
        
        # 检查必要的八字信息
        bazi_info = data.get('bazi_info', {})
        if not isinstance(bazi_info, dict):
            return False
        
        # 检查八字数组
        bazi = bazi_info.get('bazi', [])
        if not isinstance(bazi, list) or len(bazi) < 4:
            return False
        
        return True
    

    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            test_data = {'api_key': self.api_key}
            result = self._make_request('index.php/v1/Bazi/paipan', test_data, 'GET')
            return result.get('errcode') == 0
        except Exception as e:
            logger.error(f"API连接测试失败: {str(e)}")
            return False