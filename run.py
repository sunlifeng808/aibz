#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玄学AI智能体启动脚本

使用方法：
    python run.py
    
或者直接运行：
    streamlit run app.py
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    
    # 检查必要文件
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example'
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ 缺少必要文件: {file}")
            return False
    
    print("✅ 必要文件检查通过")
    
    # 检查.env文件
    if not Path('.env').exists():
        print("⚠️  未找到.env文件，请复制.env.example并配置API密钥")
        print("   运行命令: cp .env.example .env")
        print("   然后编辑.env文件，填入您的API密钥")
        return False
    
    print("✅ 环境配置文件存在")
    return True

def install_dependencies():
    """安装依赖包"""
    print("📦 检查并安装依赖包...")
    
    try:
        # 检查streamlit是否已安装
        import streamlit
        print("✅ Streamlit已安装")
    except ImportError:
        print("📥 正在安装依赖包...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ 依赖包安装完成")

def check_api_config():
    """检查API配置"""
    print("🔑 检查API配置...")
    
    try:
        from config.settings import Settings
        settings = Settings()
        
        if not settings.DEEPSEEK_API_KEY or settings.DEEPSEEK_API_KEY == 'your_deepseek_api_key_here':
            print("⚠️  DeepSeek API密钥未配置")
            return False
        
        if not settings.YUANFENJU_API_KEY or settings.YUANFENJU_API_KEY == 'your_yuanfenju_api_key_here':
            print("⚠️  缘分居API密钥未配置")
            return False
        
        print("✅ API配置检查通过")
        return True
        
    except Exception as e:
        print(f"❌ API配置检查失败: {str(e)}")
        return False

def start_app():
    """启动应用"""
    print("🚀 启动玄学AI智能体...")
    print("📱 应用将在浏览器中打开: http://localhost:8501")
    print("⏹️  按 Ctrl+C 停止应用")
    print("-" * 50)
    
    try:
        # 启动streamlit应用
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")

def main():
    """主函数"""
    print("🔮 玄学AI智能体启动器")
    print("=" * 50)
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请解决上述问题后重试")
        return
    
    # 安装依赖
    try:
        install_dependencies()
    except Exception as e:
        print(f"❌ 依赖安装失败: {str(e)}")
        print("请手动运行: pip install -r requirements.txt")
        return
    
    # 检查API配置
    if not check_api_config():
        print("\n⚠️  API配置不完整，应用将使用降级模式运行")
        print("   建议配置API密钥以获得完整功能")
        
        response = input("\n是否继续启动应用？(y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("👋 启动已取消")
            return
    
    # 启动应用
    start_app()

if __name__ == "__main__":
    main()