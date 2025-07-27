from typing import Dict, Any, List
from datetime import datetime
import asyncio
import json

from models.user_info import UserInfo
from models.prediction_result import PredictionResult
from services.bazi_service import BaziService
from services.agents import (
    FoundationAgent,
    YongshenAgent,
    FortuneAgent,
    LifeAspectsAgent,
    SolutionAgent,
    ConsultationAgent
)
from utils.logger import logger

class MultiAgentPredictionService:
    """多智能体预测服务"""
    
    def __init__(self):
        self.bazi_service = BaziService()
        self._initialize_agents()
    
    def _initialize_agents(self):
        """初始化所有智能体"""
        self.agents = {
            "foundation": FoundationAgent(),
            "yongshen": YongshenAgent(),
            "fortune": FortuneAgent(),
            "life_aspects": LifeAspectsAgent(),
            "solution": SolutionAgent(),
            "consultation": ConsultationAgent()
        }
        logger.info(f"初始化了 {len(self.agents)} 个专业智能体")
    
    async def get_comprehensive_prediction(self, user_info: UserInfo) -> PredictionResult:
        """获取综合预测（并行模式）"""
        logger.log_user_action("多智能体综合预测请求", user_info.dict())
        
        try:
            # 获取八字数据
            logger.info("正在获取八字数据...")
            fortune_data = self.bazi_service.get_fortune_analysis(user_info, 'comprehensive')
            
            # 准备共享上下文
            shared_context = {
                "user_info": user_info,
                "fortune_data": fortune_data,
                "current_time": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            }
            
            # 并行执行所有智能体分析
            logger.info("开始并行执行智能体分析...")
            start_time = datetime.now()
            
            analysis_results = await self._parallel_analysis(shared_context)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"并行分析完成，耗时: {duration:.2f}秒")
            
            # 聚合结果
            prediction_content = self._merge_results(analysis_results)
            
            # 创建预测结果
            result = PredictionResult(
                user_name=user_info.name,
                prediction_time=datetime.now(),
                prediction_content=prediction_content
            )
            
            logger.log_prediction_request(user_info.name, "多智能体综合预测", True)
            total_length = prediction_content.get("summary", {}).get("total_content_length", 0)
            logger.info(f"预测完成，生成JSON结构化结果，总内容长度: {total_length}字")
            
            return result
            
        except Exception as e:
            logger.error(f"多智能体预测失败: {str(e)}")
            logger.log_prediction_request(user_info.name, "多智能体综合预测", False, str(e))
            raise
    
    async def _parallel_analysis(self, shared_context: Dict[str, Any]) -> Dict[str, str]:
        """并行执行所有智能体分析"""
        # 创建并行任务
        tasks = {
            agent_name: agent.analyze(shared_context)
            for agent_name, agent in self.agents.items()
        }
        
        # 记录并发开始时间
        start_time = datetime.now()
        logger.info(f"🚀 开始并发执行 {len(tasks)} 个智能体任务，时间: {start_time.strftime('%H:%M:%S.%f')[:-3]}")
        for agent_name in tasks.keys():
            logger.info(f"📋 智能体 {agent_name} 任务已创建")
        
        # 并行执行
        try:
            results = await asyncio.gather(*tasks.values(), return_exceptions=True)
            
            # 记录并发完成时间
            end_time = datetime.now()
            total_duration = (end_time - start_time).total_seconds()
            logger.info(f"⚡ 所有智能体任务完成，总耗时: {total_duration:.2f}秒，完成时间: {end_time.strftime('%H:%M:%S.%f')[:-3]}")
            
            # 处理结果
            analysis_results = {}
            for i, (agent_name, result) in enumerate(zip(tasks.keys(), results)):
                current_time = datetime.now()
                if isinstance(result, Exception):
                    logger.error(f"❌ {agent_name} 智能体分析失败: {str(result)}")
                    analysis_results[agent_name] = f"{agent_name}分析暂时不可用，请稍后重试。"
                else:
                    analysis_results[agent_name] = result
                    logger.info(f"✅ {agent_name} 智能体分析成功，内容长度: {len(result)}，处理时间: {current_time.strftime('%H:%M:%S.%f')[:-3]}")
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"并行分析执行失败: {str(e)}")
            raise
    
    def _merge_results(self, analysis_results: Dict[str, str]) -> Dict[str, Any]:
        """聚合所有智能体的分析结果为JSON对象"""
        # 构建结构化的JSON结果
        merged_result = {
            "report_info": {
                "title": "玄学AI智能体 - 综合命理分析报告",
                "generated_time": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
                "service_provider": "玄学AI智能体服务",
                "description": "本分析报告由多个专业智能体协同生成，为您提供全方位的命理指导。"
            },
            "analysis_sections": {
                "foundation_analysis": {
                    "title": "八字基础分析",
                    "content": analysis_results.get("foundation", "").strip(),
                    "agent": "foundation"
                },
                "yongshen_analysis": {
                    "title": "用神喜忌分析",
                    "content": analysis_results.get("yongshen", "").strip(),
                    "agent": "yongshen"
                },
                "fortune_prediction": {
                    "title": "大运流年预测",
                    "content": analysis_results.get("fortune", "").strip(),
                    "agent": "fortune"
                },
                "life_aspects": {
                    "title": "人生各方面详解",
                    "content": analysis_results.get("life_aspects", "").strip(),
                    "agent": "life_aspects"
                },
                "solutions": {
                    "title": "专业解决方案",
                    "content": analysis_results.get("solution", "").strip(),
                    "agent": "solution"
                },
                "consultation": {
                    "title": "咨询问题回答",
                    "content": analysis_results.get("consultation", "").strip(),
                    "agent": "consultation"
                }
            },
            "summary": {
                "total_sections": len([k for k, v in analysis_results.items() if v and v.strip()]),
                "total_content_length": sum(len(v) for v in analysis_results.values() if v),
                "agents_used": list(analysis_results.keys())
            }
        }
        
        # 移除空内容的分析部分
        merged_result["analysis_sections"] = {
            k: v for k, v in merged_result["analysis_sections"].items() 
            if v["content"]
        }
        
        total_content_length = sum(
            len(section["content"]) 
            for section in merged_result["analysis_sections"].values()
        )
        
        logger.info(f"结果聚合完成，生成JSON对象包含 {len(merged_result['analysis_sections'])} 个分析部分，总内容长度: {total_content_length}字")
        
        return merged_result
    
    def get_agent_status(self) -> Dict[str, Any]:
        """获取所有智能体状态"""
        status = {
            "total_agents": len(self.agents),
            "agents": {
                agent_name: {
                    "name": agent.agent_name,
                    "status": "ready"
                }
                for agent_name, agent in self.agents.items()
            },
            "service_status": "ready"
        }
        return status
    
    async def test_agents(self, user_info: UserInfo) -> Dict[str, Any]:
        """测试所有智能体（用于调试）"""
        try:
            # 获取测试数据
            fortune_data = self.bazi_service.get_fortune_analysis(user_info, 'comprehensive')
            
            shared_context = {
                "user_info": user_info,
                "fortune_data": fortune_data,
                "current_time": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            }
            
            # 测试每个智能体
            test_results = {}
            for agent_name, agent in self.agents.items():
                try:
                    start_time = datetime.now()
                    result = await agent.analyze(shared_context)
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    
                    test_results[agent_name] = {
                        "status": "success",
                        "duration": duration,
                        "content_length": len(result),
                        "content_preview": result[:100] + "..." if len(result) > 100 else result
                    }
                except Exception as e:
                    test_results[agent_name] = {
                        "status": "failed",
                        "error": str(e)
                    }
            
            return test_results
            
        except Exception as e:
            logger.error(f"智能体测试失败: {str(e)}")
            return {"error": str(e)}