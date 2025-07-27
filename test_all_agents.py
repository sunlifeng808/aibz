#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
所有智能体统一测试脚本
"""

import sys
import os
import asyncio
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user_info import UserInfo
from services.bazi_service import BaziService
from services.agents import (
    FoundationAgent,
    YongshenAgent,
    FortuneAgent,
    LifeAspectsAgent,
    SolutionAgent,
    ConsultationAgent
)
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
        name="测试用户",
        gender="男",
        birth_year=1990,
        birth_month=5,
        birth_day=15,
        birth_hour=14,
        birth_minute=30,
        birth_province="广东省",
        birth_city="广州",
        question="请为我进行全面的命理分析"
    )

async def test_single_agent(agent_class, agent_display_name, shared_context):
    """测试单个智能体"""
    try:
        print(f"\n{'='*60}")
        print(f"🤖 测试智能体: {agent_display_name}")
        print(f"{'='*60}")
        
        # 初始化智能体
        agent = agent_class()
        print(f"智能体名称: {agent.agent_name}")
        print("🚀 开始分析...")
        
        start_time = datetime.now()
        result = await agent.analyze(shared_context)
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        print(f"⏱️ 分析完成，耗时: {duration:.2f}秒")
        print(f"📝 分析结果长度: {len(result)} 字")
        
        # 输出分析结果（截取前200字符作为预览）
        preview = result[:200] + "..." if len(result) > 200 else result
        print(f"\n📖 分析结果预览:\n{preview}")
        
        return True, result, duration
        
    except Exception as e:
        print(f"❌ {agent_display_name} 测试失败: {e}")
        return False, str(e), 0

async def test_all_agents():
    """测试所有智能体"""
    print("\n=== 所有智能体测试 ===")
    
    try:
        user_info = create_test_user()
        print(f"测试用户: {user_info.name}")
        print(f"出生时间: {user_info.birth_year}年{user_info.birth_month}月{user_info.birth_day}日 {user_info.birth_hour}:{user_info.birth_minute}")
        print(f"咨询内容: {user_info.question}")
        
        # 获取八字数据
        print("\n📊 获取八字数据...")
        bazi_service = BaziService()
        fortune_data = bazi_service.get_fortune_analysis(user_info, 'comprehensive')
        
        # 准备共享上下文
        shared_context = {
            "user_info": user_info,
            "fortune_data": fortune_data,
            "current_time": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        }
        
        # 定义所有智能体
        agents_to_test = [
            (FoundationAgent, "八字基础分析智能体"),
            (YongshenAgent, "用神分析智能体"),
            (FortuneAgent, "大运流年分析智能体"),
            (LifeAspectsAgent, "人生各方面分析智能体"),
            (SolutionAgent, "解决方案智能体"),
            (ConsultationAgent, "咨询回答智能体")
        ]
        
        # 测试结果统计
        test_results = []
        total_start_time = datetime.now()
        
        # 逐个测试智能体
        for agent_class, agent_name in agents_to_test:
            success, result, duration = await test_single_agent(agent_class, agent_name, shared_context)
            test_results.append({
                'name': agent_name,
                'success': success,
                'result': result,
                'duration': duration
            })
        
        total_end_time = datetime.now()
        total_duration = (total_end_time - total_start_time).total_seconds()
        
        # 输出测试总结
        print(f"\n{'='*80}")
        print("📊 测试总结")
        print(f"{'='*80}")
        
        successful_tests = sum(1 for r in test_results if r['success'])
        total_tests = len(test_results)
        total_content_length = sum(len(r['result']) for r in test_results if r['success'])
        
        print(f"✅ 成功测试: {successful_tests}/{total_tests} 个智能体")
        print(f"⏱️ 总耗时: {total_duration:.2f}秒")
        print(f"📝 总内容长度: {total_content_length} 字")
        print(f"⚡ 平均每个智能体耗时: {total_duration/total_tests:.2f}秒")
        
        print("\n📋 详细结果:")
        for i, result in enumerate(test_results, 1):
            status = "✅" if result['success'] else "❌"
            print(f"{i}. {status} {result['name']} - {result['duration']:.2f}秒")
        
        if successful_tests == total_tests:
            print("\n🎉 所有智能体测试通过！")
        else:
            print(f"\n⚠️ {total_tests - successful_tests} 个智能体测试失败")
        
        return successful_tests == total_tests
        
    except Exception as e:
        print(f"❌ 智能体测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主测试函数"""
    print("🤖 玄学AI智能体 - 所有智能体统一测试")
    print("=" * 80)
    
    # 配置检查
    if not test_config():
        print("\n❌ 配置检查失败，请检查.env文件")
        return
    
    # 智能体测试
    success = await test_all_agents()
    
    if success:
        print("\n✅ 所有测试完成")
    else:
        print("\n❌ 部分测试失败")

if __name__ == "__main__":
    asyncio.run(main())