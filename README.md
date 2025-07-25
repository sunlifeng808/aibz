# 玄学AI智能体 - API接口

基于传统命理学与现代AI技术的综合预测API接口。

## 功能特性

- 🔮 综合命理预测分析
- 🤖 基于DeepSeek大模型的智能分析
- 📊 集成缘分居国学API获取八字数据
- 🎯 专业的命理学提示词优化

## 核心接口

### `get_comprehensive_prediction(user_info: UserInfo) -> PredictionResult`

获取用户的综合命理预测分析。

**输入参数：**
- `user_info`: UserInfo对象，包含用户基本信息和出生数据

**返回结果：**
- `PredictionResult`: 包含完整的预测分析结果

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 缘分居API配置
YUANFENJU_API_KEY=your_yuanfenju_api_key_here
```

### 3. 运行测试

```bash
python test_prediction.py
```

## 使用示例

```python
from models.user_info import UserInfo
from services.prediction_service import PredictionService

# 创建用户信息
user_info = UserInfo(
    name="张三",
    gender="男",
    birth_year=1990,
    birth_month=5,
    birth_day=15,
    birth_hour=14,
    birth_minute=30,
    birth_province="北京市",
    birth_city="北京市",
    question="请帮我分析一下我的综合运势"
)

# 创建预测服务
prediction_service = PredictionService()

# 获取预测结果
result = prediction_service.get_comprehensive_prediction(user_info)

# 输出结果
print(f"用户: {result.user_name}")
print(f"预测内容: {result.prediction_content}")
```

## 项目结构

```
├── models/                 # 数据模型
│   ├── user_info.py       # 用户信息模型
│   └── prediction_result.py # 预测结果模型
├── services/              # 服务层
│   ├── prediction_service.py # 预测服务
│   └── bazi_service.py    # 八字数据服务
├── config/                # 配置文件
│   ├── settings.py        # 系统配置
│   └── prompts/           # 提示词模板
├── utils/                 # 工具类
│   ├── logger.py          # 日志工具
│   └── data_validator.py  # 数据验证
├── api_client.py          # API客户端
├── province.json          # 省市数据
├── test_prediction.py     # 测试脚本
└── requirements.txt       # 依赖包
```

## API密钥获取

1. **DeepSeek API**: 访问 [DeepSeek官网](https://platform.deepseek.com/) 注册并获取API密钥
2. **缘分居API**: 访问 [缘分居官网](https://www.yuanfenju.com/) 注册并获取API密钥

## 注意事项

- 确保网络连接正常，API调用需要访问外部服务
- 预测结果仅供娱乐参考，请理性对待
- 请妥善保管API密钥，避免泄露

## 许可证

本项目仅供学习和研究使用。