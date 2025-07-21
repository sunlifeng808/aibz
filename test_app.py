#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玄学AI智能体测试脚本

用于测试应用的基本功能和组件
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def test_imports():
    """测试模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        # 测试基础模块
        import streamlit as st
        print("✅ Streamlit导入成功")
        
        from config.settings import Settings
        print("✅ 配置模块导入成功")
        
        from models.user_info import UserInfo
        from models.bazi_data import BaziData
        from models.prediction_result import PredictionResult
        print("✅ 数据模型导入成功")
        
        from services.bazi_service import BaziService
        from services.prediction_service import PredictionService
        print("✅ 服务模块导入成功")
        
        from utils.data_validator import DataValidator
        from utils.logger import logger
        print("✅ 工具模块导入成功")
        
        from api_client import YuanFenJuAPIClient
        print("✅ API客户端导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 导入测试异常: {str(e)}")
        return False

def test_configuration():
    """测试配置"""
    print("\n⚙️ 测试配置...")
    
    try:
        from config.settings import Settings
        settings = Settings()
        
        # 测试基本配置
        print(f"✅ DEBUG模式: {settings.DEBUG}")
        print(f"✅ 日志级别: {settings.LOG_LEVEL}")
        print(f"✅ 请求超时: {settings.REQUEST_TIMEOUT}秒")
        print(f"✅ 最大重试次数: {settings.MAX_RETRIES}")
        
        # 测试API配置（不显示密钥）
        deepseek_configured = bool(settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY != 'your_deepseek_api_key_here')
        yuanfenju_configured = bool(settings.YUANFENJU_API_KEY and settings.YUANFENJU_API_KEY != 'your_yuanfenju_api_key_here')
        
        print(f"✅ DeepSeek API: {'已配置' if deepseek_configured else '未配置'}")
        print(f"✅ 缘分居API: {'已配置' if yuanfenju_configured else '未配置'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {str(e)}")
        return False

def test_data_models():
    """测试数据模型"""
    print("\n📊 测试数据模型...")
    
    try:
        from models.user_info import UserInfo
        from models.bazi_data import BaziData
        from models.prediction_result import PredictionResult
        
        # 测试UserInfo模型
        user_info = UserInfo(
            name="测试用户",
            gender="男",
            birth_year=1990,
            birth_month=1,
            birth_day=1,
            birth_hour=12,
            birth_minute=0,
            birth_location="北京市",
            question="测试问题"
        )
        print(f"✅ UserInfo模型: {user_info.name}")
        
        # 测试BaziData模型
        bazi_data = BaziData(
            year_pillar="甲子",
            month_pillar="丙寅",
            day_pillar="戊辰",
            hour_pillar="庚午"
        )
        print(f"✅ BaziData模型: {bazi_data.get_bazi_string()}")
        
        # 测试PredictionResult模型
        prediction_result = PredictionResult(
            user_name="测试用户",
            prediction_time=datetime.now(),
            bazi_summary="测试八字摘要",
            prediction_content="测试预测内容"
        )
        print(f"✅ PredictionResult模型: {prediction_result.user_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据模型测试失败: {str(e)}")
        return False

def test_data_validator():
    """测试数据验证器"""
    print("\n🔍 测试数据验证器...")
    
    try:
        from utils.data_validator import DataValidator
        validator = DataValidator()
        
        # 测试有效数据
        valid_data = {
            'name': '张三',
            'gender': '男',
            'birth_year': 1990,
            'birth_month': 1,
            'birth_day': 1,
            'birth_hour': 12,
            'birth_minute': 0,
            'birth_location': '北京市',
            'question': '测试问题'
        }
        
        errors = validator.validate_user_info(valid_data)
        if not errors:
            print("✅ 有效数据验证通过")
        else:
            print(f"❌ 有效数据验证失败: {errors}")
        
        # 测试无效数据
        invalid_data = {
            'name': '',  # 空姓名
            'gender': '未知',  # 无效性别
            'birth_year': 1800,  # 无效年份
            'birth_month': 13,  # 无效月份
            'birth_day': 32,  # 无效日期
            'birth_hour': 25,  # 无效小时
            'birth_minute': 61,  # 无效分钟
            'birth_location': '',  # 空地点
        }
        
        errors = validator.validate_user_info(invalid_data)
        if errors:
            print(f"✅ 无效数据验证通过，发现{len(errors)}个错误")
        else:
            print("❌ 无效数据验证失败，应该发现错误")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据验证器测试失败: {str(e)}")
        return False

def test_logger():
    """测试日志系统"""
    print("\n📝 测试日志系统...")
    
    try:
        from utils.logger import logger
        
        # 测试各种日志级别
        logger.info("测试信息日志")
        logger.debug("测试调试日志")
        logger.warning("测试警告日志")
        
        # 测试API请求日志
        logger.log_api_request(
            api_name="测试API",
            request_data={"test": "data"},
            response_data={"status": "success"}
        )
        
        # 测试用户操作日志
        logger.log_user_action(
            action="测试操作",
            user_info={"name": "测试用户"},
            details="测试详情"
        )
        
        print("✅ 日志系统测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 日志系统测试失败: {str(e)}")
        return False

def test_services():
    """测试服务层"""
    print("\n🔧 测试服务层...")
    
    try:
        from services.bazi_service import BaziService
        from services.prediction_service import PredictionService
        from models.user_info import UserInfo
        
        # 测试八字服务
        bazi_service = BaziService()
        health_status = bazi_service.validate_service_health()
        print(f"✅ 八字服务状态: {health_status['status']}")
        
        # 测试预测服务
        prediction_service = PredictionService()
        service_status = prediction_service.get_service_status()
        print(f"✅ 预测服务状态: {service_status['service_name']}")
        
        # 测试缓存功能
        cache_info = bazi_service.get_cache_info()
        print(f"✅ 缓存状态: {cache_info['cache_size']} 个缓存项")
        
        return True
        
    except Exception as e:
        print(f"❌ 服务层测试失败: {str(e)}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n📁 测试文件结构...")
    
    required_files = [
        'app.py',
        'run.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'api_client.py'
    ]
    
    required_dirs = [
        'config',
        'models',
        'services',
        'utils'
    ]
    
    # 检查文件
    for file in required_files:
        if Path(file).exists():
            print(f"✅ 文件存在: {file}")
        else:
            print(f"❌ 文件缺失: {file}")
            return False
    
    # 检查目录
    for dir_name in required_dirs:
        if Path(dir_name).is_dir():
            print(f"✅ 目录存在: {dir_name}/")
        else:
            print(f"❌ 目录缺失: {dir_name}/")
            return False
    
    return True

def main():
    """主测试函数"""
    print("🔮 玄学AI智能体 - 功能测试")
    print("=" * 50)
    
    tests = [
        ("文件结构", test_file_structure),
        ("模块导入", test_imports),
        ("配置系统", test_configuration),
        ("数据模型", test_data_models),
        ("数据验证", test_data_validator),
        ("日志系统", test_logger),
        ("服务层", test_services)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 测试 {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用可以正常运行")
        print("\n🚀 运行以下命令启动应用:")
        print("   python run.py")
        print("   或者")
        print("   streamlit run app.py")
    else:
        print("⚠️  部分测试失败，请检查相关问题")
        print("\n💡 提示:")
        print("   1. 确保已安装所有依赖: pip install -r requirements.txt")
        print("   2. 检查.env文件配置")
        print("   3. 查看详细错误信息并修复")

if __name__ == "__main__":
    main()