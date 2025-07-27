#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人生各方面分析智能体单独测试脚本
"""

import sys
import os
import asyncio
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user_info import UserInfo
from services.bazi_service import BaziService
from services.agents import LifeAspectsAgent
from config.settings import Settings
from utils.logger import logger

def test_config():
    """测试配置"""
    print("\n=== 配置检查 ===")
    try:
        settings = Settings()
        print(f"✅ DeepSeek API Key: {'已配置' if settings.DEEPSEEK_API_KEY else '未配置'}")
        return True
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

def create_test_user():
    """创建测试用户"""
    return UserInfo(
        name="孙七",
        gender="男",
        birth_year=1995,
        birth_month=6,
        birth_day=25,
        birth_hour=9,
        birth_minute=30,
        birth_province="湖北省",
        birth_city="武汉",
        question="请分析我人生各方面的情况"
    )

async def test_life_aspects_agent():
    """测试人生各方面分析智能体"""
    print("\n=== 人生各方面分析智能体测试 ===")
    try:
        user_info = create_test_user()
        print(f"测试用户: {user_info.name}")
        print(f"出生时间: {user_info.birth_year}年{user_info.birth_month}月{user_info.birth_day}日 {user_info.birth_hour}:{user_info.birth_minute}")
        print(f"咨询内容: {user_info.question}")
        
        # 获取八字数据
        bazi_service = BaziService()
        fortune_data = bazi_service.get_fortune_analysis(user_info, 'comprehensive')
        
        # 准备共享上下文
        shared_context = {
            "user_info": user_info,
            "fortune_data": fortune_data,
            "current_time": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        }
        
        # 初始化智能体
        agent = LifeAspectsAgent()
        print(f"\n🤖 智能体名称: {agent.agent_name}")
        print("🚀 开始分析...")
        
        start_time = datetime.now()
        result = await agent.analyze(shared_context)
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        print(f"\n⏱️ 分析完成，耗时: {duration:.2f}秒")
        print(f"📝 分析结果长度: {len(result)} 字")
        
        # 输出分析结果
        print("\n" + "=" * 80)
        print("🔮 人生各方面分析结果")
        print("=" * 80)
        print(result)
        print("\n" + "=" * 80)
        
        return True
        
    except Exception as e:
        print(f"❌ 人生各方面分析智能体测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主测试函数"""
    print("🤖 人生各方面分析智能体 - 单独测试")
    print("=" * 50)
    
    # 配置检查
    if not test_config():
        print("\n❌ 配置检查失败，请检查.env文件")
        return
    
    # 智能体测试
    success = await test_life_aspects_agent()
    
    if success:
        print("\n✅ 测试完成")
    else:
        print("\n❌ 测试失败")

if __name__ == "__main__":
    asyncio.run(main())