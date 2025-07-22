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
    

    
    def get_fortune_prediction(self, user_info: Dict[str, Any], prediction_type: str = 'general') -> Dict[str, Any]:
        """获取运势预测"""
        # 根据缘分居API的实际参数格式
        api_data = {
            'api_key': self.api_key,
            'name': user_info.get('name', '用户'),
            'sex': '0' if user_info.get('gender') == '女' else '1',
            'type': '1',  # 公历类型
            'year': str(user_info.get('birth_year', 1990)),
            'month': str(user_info.get('birth_month', 1)),
            'day': str(user_info.get('birth_day', 1)),
            'hours': str(user_info.get('birth_hour', 12)),
            'minute': str(user_info.get('birth_minute', 0)),
            'zhen': '1',
            'province': user_info.get('birth_province', ''),
            'city': user_info.get('birth_city', '')
        }
        
        logger.info(f"请求运势预测: {prediction_type}")
        
        result = self._make_request('index.php/v1/Bazi/cesuan', api_data)
        return result


    

    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            test_data = {'api_key': self.api_key}
            result = self._make_request('index.php/v1/Bazi/jingsuan', test_data, 'GET')
            return result.get('errcode') == 0
        except Exception as e:
            logger.error(f"API连接测试失败: {str(e)}")
            return False