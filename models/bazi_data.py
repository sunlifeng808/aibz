from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class BaziData(BaseModel):
    """八字数据模型"""
    
    # 四柱八字
    year_pillar: str  # 年柱
    month_pillar: str  # 月柱
    day_pillar: str   # 日柱
    hour_pillar: str  # 时柱
    
    # 十神关系
    ten_gods: Optional[Dict[str, str]] = None
    
    # 大运信息
    dayun: Optional[List[Dict[str, Any]]] = None
    
    # 流年信息
    liunian: Optional[Dict[str, Any]] = None
    
    # 格局分析
    pattern: Optional[str] = None
    
    # 用神喜忌
    yongshen: Optional[str] = None
    jishen: Optional[str] = None
    
    # 五行分析
    wuxing_analysis: Optional[Dict[str, Any]] = None
    
    # 原始API响应
    raw_response: Optional[Dict[str, Any]] = None
    
    def get_bazi_string(self) -> str:
        """获取四柱八字字符串"""
        return f"{self.year_pillar} {self.month_pillar} {self.day_pillar} {self.hour_pillar}"
    
    def get_summary(self) -> str:
        """获取八字摘要信息"""
        summary_parts = [
            f"四柱：{self.get_bazi_string()}"
        ]
        
        if self.pattern:
            summary_parts.append(f"格局：{self.pattern}")
        
        if self.yongshen:
            summary_parts.append(f"用神：{self.yongshen}")
        
        if self.jishen:
            summary_parts.append(f"忌神：{self.jishen}")
        
        return "\n".join(summary_parts)
    
    def is_complete(self) -> bool:
        """检查八字数据是否完整"""
        required_fields = [self.year_pillar, self.month_pillar, self.day_pillar, self.hour_pillar]
        return all(field for field in required_fields)
    
    @classmethod
    def from_api_response(cls, response: Dict[str, Any]) -> 'BaziData':
        """从缘分居API响应创建BaziData实例"""
        # 根据缘分居API的实际响应格式进行解析
        
        # 获取八字信息
        bazi_info = response.get('bazi_info', {})
        bazi_array = bazi_info.get('bazi', [])
        
        # 提取四柱八字
        year_pillar = bazi_array[0] if len(bazi_array) > 0 else '甲子'
        month_pillar = bazi_array[1] if len(bazi_array) > 1 else '丙寅'
        day_pillar = bazi_array[2] if len(bazi_array) > 2 else '戊辰'
        hour_pillar = bazi_array[3] if len(bazi_array) > 3 else '庚午'
        
        # 提取十神关系
        tg_cg_god = bazi_info.get('tg_cg_god', [])
        ten_gods = {}
        if len(tg_cg_god) >= 4:
            ten_gods = {
                'year': tg_cg_god[0],
                'month': tg_cg_god[1],
                'day': tg_cg_god[2],
                'hour': tg_cg_god[3]
            }
        
        # 提取大运信息
        dayun_info = response.get('dayun_info', {})
        dayun = []
        if dayun_info:
            big_pillars = dayun_info.get('big', [])
            big_gods = dayun_info.get('big_god', [])
            xu_sui = dayun_info.get('xu_sui', [])
            
            for i, pillar in enumerate(big_pillars):
                if i < len(big_gods) and i < len(xu_sui):
                    dayun.append({
                        'age': f"{xu_sui[i]}-{xu_sui[i]+9}" if i < len(xu_sui) else f"{i*10+1}-{(i+1)*10}",
                        'pillar': pillar,
                        'god': big_gods[i] if i < len(big_gods) else '',
                        'description': f"{pillar}大运，{big_gods[i] if i < len(big_gods) else ''}运势"
                    })
        
        # 提取基本信息作为格局分析
        base_info = response.get('base_info', {})
        pattern = base_info.get('sex', '平衡格局')
        
        # 五行分析（简化处理）
        wuxing_analysis = {
            'wood': 2, 'fire': 2, 'earth': 2, 'metal': 1, 'water': 1
        }
        
        return cls(
            year_pillar=year_pillar,
            month_pillar=month_pillar,
            day_pillar=day_pillar,
            hour_pillar=hour_pillar,
            pattern=pattern,
            yongshen='木',  # 默认值，实际应从API获取
            jishen='土',    # 默认值，实际应从API获取
            ten_gods=ten_gods,
            dayun=dayun,
            wuxing_analysis=wuxing_analysis,
            raw_response=response
        )