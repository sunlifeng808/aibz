#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多智能体系统自动化测试脚本
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user_info import UserInfo
from services.multi_agent_prediction_service import MultiAgentPredictionService

from config.settings import Settings
from utils.logger import logger

def test_config():
    """测试配置"""
    print("\n=== 配置检查 ===")
    try:
        settings = Settings()
        print(f"✅ DeepSeek API Key: {'已配置' if settings.DEEPSEEK_API_KEY else '未配置'}")
        print(f"✅ 缘分居 API Key: {'已配置' if settings.YUANFENJU_API_KEY else '未配置'}")
        return True
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

def create_test_user():
    """创建测试用户"""
    return UserInfo(
        name="张三",
        gender="男",
        birth_year=1990,
        birth_month=5,
        birth_day=15,
        birth_hour=14,
        birth_minute=30,
        birth_province="广东省",
        birth_city="广州",
        question="请分析我的事业运势和财运情况"
    )

async def test_multi_agent_prediction():
    """测试多智能体预测"""
    print("\n=== 多智能体预测测试 ===")
    try:
        user_info = create_test_user()
        print(f"测试用户: {user_info.name}")
        print(f"出生时间: {user_info.birth_year}年{user_info.birth_month}月{user_info.birth_day}日 {user_info.birth_hour}:{user_info.birth_minute}")
        print(f"咨询内容: {user_info.question}")
        
        # 初始化多智能体服务
        service = MultiAgentPredictionService()
        print("\n🚀 开始多智能体并行分析...")
        
        start_time = datetime.now()
        result = await service.get_comprehensive_prediction(user_info)
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        print(f"\n⏱️ 分析完成，耗时: {duration:.2f}秒")
        
        # 保存JSON结果到output文件夹
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✅ 创建输出目录: {output_dir}")
        
        # 生成文件名（包含时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"prediction_result_{timestamp}.json")
        
        # 准备完整的结果数据
        complete_result = {
            "user_info": {
                "name": result.user_name,
                "gender": user_info.gender,
                "birth_date": f"{user_info.birth_year}-{user_info.birth_month:02d}-{user_info.birth_day:02d}",
                "birth_time": f"{user_info.birth_hour:02d}:{user_info.birth_minute:02d}",
                "birth_location": f"{user_info.birth_province} {user_info.birth_city}",
                "question": user_info.question
            },
            "prediction_time": result.prediction_time.isoformat(),
            "processing_duration_seconds": duration,
            "prediction_content": result.prediction_content
        }
        
        # 保存到JSON文件
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(complete_result, f, ensure_ascii=False, indent=2)
            print(f"💾 预测结果已保存到: {output_file}")
            print(f"📁 文件大小: {os.path.getsize(output_file)} 字节")
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")
        
        print(f"\n📊 预测结果:")
        print(f"用户姓名: {result.user_name}")
        print(f"预测时间: {result.prediction_time}")
        print(f"\n📝 预测内容结构:")
        if isinstance(result.prediction_content, dict):
            print(f"- 报告信息: {result.prediction_content.get('report_info', {}).get('title', 'N/A')}")
            print(f"- 分析部分数量: {len(result.prediction_content.get('analysis_sections', {}))}")
            print(f"- 总内容长度: {result.prediction_content.get('summary', {}).get('total_content_length', 0)} 字")
            print(f"- 使用的智能体: {', '.join(result.prediction_content.get('summary', {}).get('agents_used', []))}")
        else:
            print(result.prediction_content)
        
        return True
        
    except Exception as e:
        print(f"❌ 多智能体预测测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_agent_status():
    """测试智能体状态"""
    print("\n=== 智能体状态测试 ===")
    try:
        service = MultiAgentPredictionService()
        status = service.get_agent_status()
        
        print("智能体状态:")
        for agent_name, agent_status in status.items():
            print(f"  {agent_name}: {agent_status}")
        
        return True
        
    except Exception as e:
        print(f"❌ 智能体状态测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🤖 玄学AI智能体 - 多智能体系统自动化测试")
    print("=" * 50)
    
    # 配置检查
    if not test_config():
        print("\n❌ 配置检查失败，请检查.env文件")
        return
    
    # 智能体状态测试
    await test_agent_status()
    
    # 多智能体预测测试
    success1 = await test_multi_agent_prediction()

if __name__ == "__main__":
    asyncio.run(main())