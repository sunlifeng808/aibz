#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试get_comprehensive_prediction接口
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user_info import UserInfo
from services.prediction_service import PredictionService
from config.settings import Settings

def test_comprehensive_prediction():
    """
    测试综合预测功能
    """
    print("=" * 60)
    print("🔮 玄学AI智能体 - 综合预测测试")
    print("=" * 60)
    
    try:
        # 检查配置
        settings = Settings()
        if not settings.validate_config():
            print("❌ 配置验证失败，请检查.env文件中的API密钥设置")
            return
        
        print("✅ 配置验证通过")
        
        # 创建测试用户信息
        test_user = UserInfo(
            name="张三",
            gender="男",
            birth_year=1990,
            birth_month=5,
            birth_day=15,
            birth_hour=14,
            birth_minute=30,
            birth_province="北京市",
            birth_city="北京",
            question="请帮我分析一下我的综合运势，包括事业、财运、感情等方面"
        )
        
        print(f"\n📋 测试用户信息:")
        print(f"   姓名: {test_user.name}")
        print(f"   性别: {test_user.gender}")
        print(f"   出生时间: {test_user.get_birth_datetime_str()}")
        print(f"   出生地点: {test_user.birth_province} {test_user.birth_city}")
        print(f"   咨询问题: {test_user.question}")
        
        # 创建预测服务
        print("\n🚀 初始化预测服务...")
        prediction_service = PredictionService()
        
        # 执行预测
        print("\n🔄 正在获取八字数据并生成AI预测...")
        start_time = datetime.now()
        
        result = prediction_service.get_comprehensive_prediction(test_user)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ 预测完成，耗时: {duration:.2f}秒")
        
        # 输出结果
        print("\n" + "=" * 60)
        print("📊 预测结果")
        print("=" * 60)
        
        print(f"\n👤 用户姓名: {result.user_name}")
        print(f"🕐 预测时间: {result.prediction_time.strftime('%Y年%m月%d日 %H:%M:%S')}")
        print(f"📈 预测类型: 综合运势")
        
        print(f"\n🤖 AI预测分析:")
        print("-" * 40)
        print(result.prediction_content)
        
        print("\n" + "=" * 60)
        print(f"🎉 测试完成！\n共{len(result.prediction_content)}字")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        print("\n详细错误信息:")
        traceback.print_exc()

def main():
    """
    主函数
    """
    print("\n🔮 玄学AI智能体 - API接口测试")
    print("\n请确保已正确配置.env文件中的API密钥:")
    print("- DEEPSEEK_API_KEY: DeepSeek API密钥")
    print("- YUANFENJU_API_KEY: 缘分居API密钥")
    
    input("\n按回车键开始测试...")
    
    test_comprehensive_prediction()

if __name__ == "__main__":
    main()