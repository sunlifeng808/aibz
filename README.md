# 玄学AI智能体 🔮

基于传统命理学与现代AI技术的智能预测系统，结合缘分居国学API和DeepSeek大语言模型，为用户提供专业的八字命理分析和人生指导。

## 🌟 项目特色

- **专业八字分析**：集成缘分居国学API，提供准确的八字计算和分析
- **AI智能预测**：使用DeepSeek大语言模型生成个性化的命理解读
- **多维度分析**：支持综合运势、事业发展、感情婚姻等多种预测类型
- **现代化界面**：基于Streamlit构建的美观易用的Web界面
- **数据安全**：完善的数据验证和隐私保护机制

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 稳定的网络连接（用于API调用）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入您的API密钥：
```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com
DEEPSEEK_MODEL_NAME=deepseek-chat

# 缘分居国学API配置
YUANFENJU_API_KEY=your_yuanfenju_api_key_here
YUANFENJU_API_URL=https://api.yuanfenju.com

# LLM配置
LLM_PROVIDER=chatdeepseek  # 支持 chatdeepseek 或 chatopenai
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
LLM_TOP_P=0.9

# 系统提示词配置（可自定义）
SYSTEM_PROMPT_COMPREHENSIVE="你是一位专业的命理学大师..."
SYSTEM_PROMPT_CAREER="你是一位专业的职业规划师..."
SYSTEM_PROMPT_RELATIONSHIP="你是一位专业的情感咨询师..."

# 系统配置
DEBUG=false
LOG_LEVEL=INFO
```

### 启动应用

```bash
streamlit run app.py
```

应用将在 `http://localhost:8501` 启动。

## 📁 项目结构

```
aibz/
├── app.py                 # 主应用文件
├── requirements.txt       # 依赖包列表
├── .env.example          # 环境变量模板
├── README.md             # 项目说明
├── config/               # 配置模块
│   ├── __init__.py
│   └── settings.py       # 系统配置
├── models/               # 数据模型
│   ├── __init__.py
│   ├── user_info.py      # 用户信息模型
│   ├── bazi_data.py      # 八字数据模型
│   └── prediction_result.py # 预测结果模型
├── services/             # 业务服务
│   ├── __init__.py
│   ├── bazi_service.py   # 八字数据服务
│   └── prediction_service.py # 预测服务
├── utils/                # 工具模块
│   ├── __init__.py
│   ├── data_validator.py # 数据验证工具
│   └── logger.py         # 日志工具
├── api_client.py         # API客户端
└── logs/                 # 日志文件目录
```

## ⚙️ 配置说明

### LLM提供商配置

系统支持多种大语言模型提供商，可通过环境变量进行配置：

- **chatdeepseek**：使用DeepSeek API（推荐）
- **chatopenai**：使用OpenAI兼容的API

### LLM参数配置

- `LLM_TEMPERATURE`：控制输出的随机性（0.0-1.0）
- `LLM_MAX_TOKENS`：最大输出token数量
- `LLM_TOP_P`：核采样参数（0.0-1.0）

### 系统提示词自定义

支持自定义三种预测类型的系统提示词：

- `SYSTEM_PROMPT_COMPREHENSIVE`：综合运势分析提示词
- `SYSTEM_PROMPT_CAREER`：事业发展分析提示词
- `SYSTEM_PROMPT_RELATIONSHIP`：感情婚姻分析提示词

提示词支持多行文本，使用`\n`表示换行。

## 🔧 功能模块

### 1. 用户信息管理
- 用户基本信息收集和验证
- 出生时间和地点标准化处理
- 数据安全和隐私保护

### 2. 八字分析服务
- 调用缘分居国学API获取八字数据
- 四柱八字、十神关系、格局分析
- 大运流年、用神喜忌计算

### 3. AI预测服务
- 支持多种LLM提供商（DeepSeek、OpenAI等）
- 可配置的模型参数和系统提示词
- 多种预测类型支持
- 个性化建议和指导

### 4. Web界面
- 响应式设计，支持多设备访问
- 直观的用户交互界面
- 预测结果展示和导出功能

## 🎯 使用指南

### 基本使用流程

1. **填写个人信息**
   - 输入姓名、性别、出生时间和地点
   - 可选择性填写咨询问题

2. **选择预测类型**
   - 综合运势：全面的命理分析
   - 事业发展：职业规划和财运分析
   - 感情婚姻：感情运势和婚姻建议

3. **获取预测结果**
   - 查看八字信息和AI分析
   - 阅读专业建议和指导
   - 导出或分享预测报告

### 高级功能

- **历史记录**：查看之前的预测记录
- **系统状态**：检查API连接和服务状态
- **报告导出**：下载完整的预测报告
- **结果分享**：生成可分享的预测摘要

## 🛡️ 安全特性

- **数据验证**：严格的输入数据验证和清理
- **错误处理**：完善的异常处理和降级机制
- **日志记录**：详细的操作日志和审计跟踪
- **隐私保护**：用户数据脱敏和安全存储

## 🔄 服务监控

系统提供实时服务状态监控，确保服务的稳定性和可用性。

## 📊 监控和日志

- **应用日志**：记录在 `logs/` 目录下
- **API调用日志**：包含请求和响应详情
- **用户操作日志**：记录用户行为（已脱敏）
- **错误日志**：详细的错误信息和堆栈跟踪

## 🚨 故障排除

### 常见问题

1. **API连接失败**
   - 检查网络连接
   - 验证API密钥是否正确
   - 确认API服务是否可用

2. **预测结果异常**
   - 检查输入数据格式
   - 查看日志文件获取详细错误信息
   - 尝试重新提交请求

3. **界面显示问题**
   - 清除浏览器缓存
   - 检查网络连接稳定性
   - 尝试刷新页面

### 调试模式

在 `.env` 文件中设置 `DEBUG=true` 启用调试模式，获取更详细的日志信息。

## 📈 性能优化

- **缓存机制**：八字数据本地缓存，减少API调用
- **异步处理**：优化API请求和响应处理
- **错误重试**：自动重试机制提高成功率
- **资源管理**：合理的内存和连接池管理

## 🔮 未来规划

- [ ] 支持更多命理分析类型（紫微斗数、奇门遁甲等）
- [ ] 增加用户账户系统和历史数据管理
- [ ] 开发移动端应用
- [ ] 集成更多第三方命理API
- [ ] 添加数据分析和统计功能
- [ ] 支持多语言界面

## 📄 许可证

本项目仅供学习和研究使用。预测结果仅供娱乐参考，请理性对待。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 项目Issues：[GitHub Issues]()
- 邮箱：your-email@example.com

---

**免责声明**：本系统预测结果仅供娱乐参考，不构成任何决策建议。请理性对待预测结果，人生的幸福需要通过自己的努力来创造。