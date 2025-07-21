import logging
import os
from datetime import datetime
from typing import Optional
from config.settings import Settings

class Logger:
    """日志工具类"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """设置日志配置"""
        settings = Settings()
        
        # 创建日志目录
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建logger
        self._logger = logging.getLogger('aibz')
        self._logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
        
        # 避免重复添加handler
        if not self._logger.handlers:
            # 文件handler
            log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            # 控制台handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
            
            # 格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加handler
            self._logger.addHandler(file_handler)
            self._logger.addHandler(console_handler)
    
    def info(self, message: str, extra: Optional[dict] = None):
        """记录信息日志"""
        self._logger.info(message, extra=extra)
    
    def debug(self, message: str, extra: Optional[dict] = None):
        """记录调试日志"""
        self._logger.debug(message, extra=extra)
    
    def warning(self, message: str, extra: Optional[dict] = None):
        """记录警告日志"""
        self._logger.warning(message, extra=extra)
    
    def error(self, message: str, extra: Optional[dict] = None):
        """记录错误日志"""
        self._logger.error(message, extra=extra)
    
    def critical(self, message: str, extra: Optional[dict] = None):
        """记录严重错误日志"""
        self._logger.critical(message, extra=extra)
    
    def log_api_request(self, api_name: str, request_data: dict, response_data: dict = None, error: str = None):
        """记录API请求日志"""
        log_data = {
            'api_name': api_name,
            'request_time': datetime.now().isoformat(),
            'request_data': request_data,
        }
        
        if response_data:
            log_data['response_data'] = response_data
            self.info(f"API请求成功: {api_name}", extra=log_data)
        
        if error:
            log_data['error'] = error
            self.error(f"API请求失败: {api_name} - {error}", extra=log_data)
    
    def log_user_action(self, action: str, user_info: dict = None, details: str = None):
        """记录用户操作日志"""
        log_data = {
            'action': action,
            'timestamp': datetime.now().isoformat(),
        }
        
        if user_info:
            # 脱敏处理
            safe_user_info = {
                'name': user_info.get('name', '').replace(user_info.get('name', '')[1:-1], '*' * len(user_info.get('name', '')[1:-1])) if len(user_info.get('name', '')) > 2 else user_info.get('name', ''),
                'gender': user_info.get('gender', ''),
                'birth_year': user_info.get('birth_year', ''),
                'location': user_info.get('birth_location', '')[:2] + '***' if len(user_info.get('birth_location', '')) > 2 else user_info.get('birth_location', '')
            }
            log_data['user_info'] = safe_user_info
        
        if details:
            log_data['details'] = details
        
        self.info(f"用户操作: {action}", extra=log_data)
    
    def log_prediction_request(self, user_name: str, prediction_type: str, success: bool = True, error: str = None):
        """记录预测请求日志"""
        log_data = {
            'user_name': user_name[:1] + '*' * (len(user_name) - 2) + user_name[-1:] if len(user_name) > 2 else user_name,
            'prediction_type': prediction_type,
            'timestamp': datetime.now().isoformat(),
            'success': success
        }
        
        if error:
            log_data['error'] = error
            self.error(f"预测请求失败: {user_name} - {error}", extra=log_data)
        else:
            self.info(f"预测请求成功: {user_name}", extra=log_data)

# 创建全局logger实例
logger = Logger()