# 玄学AI智能体项目设计文档

## 技术架构

### 前端技术栈

- **框架**: Streamlit 1.28+
- **特点**: 
  - 快速开发和部署的Python Web框架
  - 原生支持Python生态和数据科学库
  - 丰富的内置组件和自定义CSS支持
  - 响应式设计和现代化UI组件
  - 会话状态管理和实时交互

### 后端技术栈

- **AI模型**: DeepSeek Chat API
- **第三方API**: 缘分居国学API
- **数据处理**: Python标准库 + 自定义模块
- **特点**:
  - 直接API调用，无需复杂框架
  - 灵活的提示词配置和管理
  - 多LLM提供商支持（DeepSeek、OpenAI等）
  - 专业的八字数据API集成

### 系统架构设计

```
用户界面层 (Streamlit App)
       ↓
    app.py (主应用)
       ↓
预测服务层 (prediction_service.py)
       ↓
    ┌─────────────────┬─────────────────┐
    ↓                 ↓                 ↓
八字数据服务      AI预测调用        数据模型层
(bazi_service)   (直接API调用)     (models/)
    ↓                 ↓                 ↓
缘分居API客户端    DeepSeek API     用户信息模型
(api_client.py)      ↓              八字数据模型
    ↓            HTTP请求           预测结果模型
缘分居国学API
```

## 技术实现方案

### 项目结构

```
aibz/
├── app.py                 # Streamlit主应用文件
├── api_client.py          # 缘分居国学API客户端
├── run.py                 # 应用启动脚本
├── test_app.py            # 应用测试文件
├── province.json          # 省市数据文件
├── requirements.txt       # 项目依赖
├── .env.example          # 环境变量模板
├── .gitignore            # Git忽略文件
├── LICENSE               # 项目许可证
├── README.md             # 项目说明
├── requirements_document.md # 需求文档
├── design_document.md    # 设计文档
├── project_execution_plan.md # 项目执行计划
├── config/               # 配置模块
│   ├── __init__.py
│   ├── settings.py       # 系统配置
│   └── prompts/          # 提示词配置
│       ├── comprehensive_prompt.txt # 综合运势提示词
│       ├── career_prompt.txt        # 事业发展提示词
│       ├── relationship_prompt.txt  # 感情婚姻提示词
│       └── business_prompt.txt      # 商业运势提示词
├── services/             # 业务服务层
│   ├── __init__.py
│   ├── bazi_service.py   # 八字数据服务
│   └── prediction_service.py # 预测服务
├── models/               # 数据模型层
│   ├── __init__.py
│   ├── user_info.py      # 用户信息数据模型
│   ├── bazi_data.py      # 八字数据模型
│   └── prediction_result.py # 预测结果模型
├── utils/                # 工具模块
│   ├── __init__.py
│   ├── data_validator.py # 数据验证工具
│   └── logger.py         # 日志工具
├── logs/                 # 日志文件目录
├── .vercel/              # Vercel部署配置
│   └── project.json
└── 八字分析系统*.docx    # 项目文档
```

### 核心模块设计

1. **主应用模块 (app.py)**
   - Streamlit Web应用的主入口
   - 用户界面渲染和交互逻辑
   - 会话状态管理和数据流控制
   - 省市联动选择和表单验证
   - 预测结果展示和历史记录管理

2. **缘分居API客户端 (api_client.py)**
   - 封装缘分居国学API的调用接口
   - 处理API认证和请求管理
   - 实现请求重试和错误处理机制
   - 提供统一的八字数据获取方法
   - 支持多种API端点和参数配置

3. **八字数据服务 (bazi_service.py)**
   - 协调用户信息收集和API调用
   - 管理八字数据的获取和处理
   - 提供标准化的八字数据接口
   - 处理API响应数据的验证和转换
   - 实现数据缓存和性能优化

4. **预测服务层 (prediction_service.py)**
   - 整合八字数据和AI预测功能
   - 管理完整的预测流程
   - 协调多个服务模块的交互
   - 提供统一的预测服务接口
   - 支持多种预测类型和LLM提供商

5. **数据模型层 (models/)**
   - **用户信息模型 (user_info.py)**：标准化用户输入数据结构
   - **八字数据模型 (bazi_data.py)**：定义API返回的八字数据结构
   - **预测结果模型 (prediction_result.py)**：规范化预测输出格式

6. **配置管理模块 (config/)**
   - **系统配置 (settings.py)**：环境变量和系统参数管理
   - **提示词配置 (prompts/)**：分类存储的提示词模板文件
     - comprehensive_prompt.txt：综合运势分析提示词
     - career_prompt.txt：事业发展分析提示词
     - relationship_prompt.txt：感情婚姻分析提示词
     - business_prompt.txt：商业运势分析提示词

7. **工具模块 (utils/)**
   - **数据验证器 (data_validator.py)**：验证用户输入和API响应
   - **日志工具 (logger.py)**：统一的日志记录和管理

8. **数据文件**
   - **省市数据 (province.json)**：中国省份和城市的分级数据
   - **环境配置 (.env.example)**：环境变量配置模板

## 用户体验设计

### 界面布局

1. **主页面**
   - 顶部：项目标题和简介
   - 左侧：用户信息输入区域
   - 右侧：预测结果显示区域
   - 底部：操作按钮区域

2. **输入区域**
   - 表单式布局，逐步引导用户输入
   - 实时验证和提示
   - 清晰的字段标签和说明

3. **结果区域**
   - 卡片式展示预测结果
   - 支持展开/折叠详细内容
   - 提供复制和导出功能

### 交互流程

1. **用户信息收集阶段**
   - 用户访问系统首页
   - 填写姓名、性别等基本信息
   - 选择出生日期（年月日时）
   - 输入出生地点信息
   - 描述具体咨询问题

2. **API数据获取阶段**
   - 系统验证用户输入数据
   - 调用缘分居国学API获取八字数据
   - 接收完整的命理分析结果
   - 解析和验证API返回数据
   - 显示八字基础信息

3. **数据处理阶段**
   - 将API数据转换为标准化格式
   - 提取关键命理信息
   - 构建AI模型输入数据
   - 系统显示数据处理进度

4. **AI预测生成阶段**
   - 基于API返回的八字数据构建提示词
   - 结合用户问题调用DeepSeek R1模型
   - 生成个性化的预测和建议
   - 系统显示AI处理状态

5. **结果展示阶段**
   - 展示缘分居API提供的八字分析
   - 显示AI生成的个性化预测内容
   - 提供通俗易懂的解释和建议
   - 用户可保存、分享或重新咨询

## 接口设计与实现

### 缘分居国学API接口

#### 1. API基本信息
- **API端点**: `https://api.yuanfenju.com`
- **认证方式**: API Key认证
- **请求方法**: POST
- **数据格式**: JSON

#### 2. 八字分析接口
```python
# 请求参数格式
{
    "api_key": "your_api_key",
    "name": "用户姓名",
    "gender": "男" | "女",
    "birth_year": 1990,
    "birth_month": 1,
    "birth_day": 1,
    "birth_hour": 12,
    "birth_minute": 0,
    "province": "北京市",
    "city": "朝阳区"
}

# 响应数据格式
{
    "status": "success",
    "data": {
        "bazi_info": {
            "year_pillar": "庚午",
            "month_pillar": "戊子",
            "day_pillar": "甲申",
            "hour_pillar": "丙午"
        },
        "wuxing_analysis": {
            "metal": 2,
            "wood": 1,
            "water": 1,
            "fire": 2,
            "earth": 2
        },
        "detailed_analysis": "详细的八字分析内容..."
    }
}
```

### DeepSeek AI接口

#### 1. API基本信息
- **API端点**: `https://api.deepseek.com/v1/chat/completions`
- **认证方式**: Bearer Token
- **请求方法**: POST
- **数据格式**: JSON

#### 2. 聊天完成接口
```python
# 请求参数格式
{
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "system",
            "content": "系统提示词内容..."
        },
        {
            "role": "user",
            "content": "用户问题和八字数据..."
        }
    ],
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 0.9
}

# 响应数据格式
{
    "id": "chatcmpl-xxx",
    "object": "chat.completion",
    "created": 1677652288,
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "AI生成的预测内容..."
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 100,
        "completion_tokens": 200,
        "total_tokens": 300
    }
}
```

## 数据传递格式

### 用户输入数据格式
```python
class UserInfo:
    name: str              # 用户姓名
    gender: str            # 性别 ("男" | "女")
    birth_year: int        # 出生年份
    birth_month: int       # 出生月份 (1-12)
    birth_day: int         # 出生日期 (1-31)
    birth_hour: int        # 出生小时 (0-23)
    birth_minute: int      # 出生分钟 (0-59)
    birth_province: str    # 出生省份
    birth_city: str        # 出生城市
    question: str          # 咨询问题 (可选)
```

### 八字数据格式
```python
class BaziData:
    year_pillar: str       # 年柱
    month_pillar: str      # 月柱
    day_pillar: str        # 日柱
    hour_pillar: str       # 时柱
    wuxing_analysis: dict  # 五行分析
    detailed_analysis: str # 详细分析
    dayun_info: list      # 大运信息
    liunian_info: list    # 流年信息
```

### 预测结果格式
```python
class PredictionResult:
    user_info: UserInfo    # 用户信息
    bazi_data: BaziData   # 八字数据
    prediction_type: str   # 预测类型
    ai_analysis: str      # AI分析内容
    suggestions: str      # 专业建议
    timestamp: datetime   # 预测时间
```

## 参数和提示词配置

### 环境变量配置
```bash
# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_BASE=https://api.deepseek.com
DEEPSEEK_MODEL_NAME=deepseek-chat

# 缘分居API配置
YUANFENJU_API_KEY=your_yuanfenju_api_key
YUANFENJU_API_URL=https://api.yuanfenju.com

# LLM参数配置
LLM_PROVIDER=chatdeepseek
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
LLM_TOP_P=0.9

# 系统配置
DEBUG=false
LOG_LEVEL=INFO
```