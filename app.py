import streamlit as st
import os
import json
from datetime import datetime
from typing import Optional
from models.user_info import UserInfo
from services.prediction_service import PredictionService
from config.settings import Settings
from utils.logger import logger
from utils.data_validator import DataValidator

# 页面配置
st.set_page_config(
    page_title="玄学AI智能体",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #1f4e79;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.sub-header {
    text-align: center;
    color: #666;
    font-size: 1.2rem;
    margin-bottom: 3rem;
}

.prediction-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.bazi-info {
    padding: 0.5rem 0;
    margin: 0.5rem 0;
}

.prediction-content {
    padding: 0.5rem 0;
    margin: 0.5rem 0;
    line-height: 1.6;
}

.footer {
    text-align: center;
    color: #999;
    font-size: 0.9rem;
    margin-top: 3rem;
    padding: 2rem;
    border-top: 1px solid #eee;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}
</style>
""", unsafe_allow_html=True)

class AIBaziApp:
    """玄学AI智能体应用"""
    
    def __init__(self):
        self.settings = Settings()
        self.prediction_service = PredictionService()
        self.validator = DataValidator()
        
        # 加载省市数据
        self.load_province_data()
        
        # 初始化session state
        if 'prediction_history' not in st.session_state:
            st.session_state.prediction_history = []
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
        if 'show_result' not in st.session_state:
            st.session_state.show_result = False
        if 'selected_province' not in st.session_state:
            st.session_state.selected_province = None
        if 'selected_city' not in st.session_state:
            st.session_state.selected_city = None
    
    def load_province_data(self):
         """加载省市数据"""
         try:
             with open('province.json', 'r', encoding='utf-8') as f:
                 self.province_data = json.load(f)
         except FileNotFoundError:
             st.error("省市数据文件未找到，请确保 province.json 文件存在")
             self.province_data = {}
         except json.JSONDecodeError:
             st.error("省市数据文件格式错误")
             self.province_data = {}
    
    def run(self):
        """运行应用"""
        self.render_header()
        
        # 侧边栏
        with st.sidebar:
            self.render_sidebar()
        
        # 主内容区
        if st.session_state.show_result and st.session_state.current_user:
            self.render_prediction_result()
        else:
            self.render_input_form()
        
        self.render_footer()
    
    def render_header(self):
        """渲染页面头部"""
        st.markdown('<h1 class="main-header">🔮 玄学AI智能体</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">基于传统命理学与现代AI技术的智能预测系统</p>', unsafe_allow_html=True)
    
    def render_sidebar(self):
        """渲染侧边栏"""
        st.markdown("### 📋 功能菜单")
        
        # 预测类型选择
        prediction_type = st.selectbox(
            "选择预测类型",
            ["综合运势", "事业发展", "感情婚姻"],
            key="prediction_type"
        )
        
        st.markdown("---")
        
        # 历史记录
        st.markdown("### 📚 预测历史")
        if st.session_state.prediction_history:
            for i, record in enumerate(st.session_state.prediction_history[-5:]):
                with st.expander(f"{record['name']} - {record['type']}"):
                    st.write(f"⏰ 时间：{record['time']}")
                    st.write(f"📊 类型：{record['type']}")
                    
                    # 显示八字信息
                    if record.get('bazi_summary'):
                        st.markdown("**📋 八字信息：**")
                        st.text(record['bazi_summary'][:100] + "..." if len(record['bazi_summary']) > 100 else record['bazi_summary'])
                    
                    # 显示AI分析摘要
                    if record.get('prediction_content'):
                        st.markdown("**🤖 AI分析摘要：**")
                        content_preview = record['prediction_content'][:200] + "..." if len(record['prediction_content']) > 200 else record['prediction_content']
                        st.write(content_preview)
                    
                    # 显示建议摘要
                    if record.get('suggestions'):
                        st.markdown("**💡 专业建议：**")
                        suggestions_preview = record['suggestions'][:150] + "..." if len(record['suggestions']) > 150 else record['suggestions']
                        st.write(suggestions_preview)
                    
                    # 操作按钮
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"📖 查看完整报告", key=f"view_full_{i}"):
                            if record.get('result_object'):
                                st.session_state.prediction_result = record['result_object']
                                st.session_state.show_result = True
                                st.rerun()
                    with col2:
                        if st.button(f"🗑️ 删除记录", key=f"delete_{i}"):
                            # 删除对应的历史记录
                            actual_index = len(st.session_state.prediction_history) - 5 + i
                            if 0 <= actual_index < len(st.session_state.prediction_history):
                                del st.session_state.prediction_history[actual_index]
                                st.success("记录已删除")
                                st.rerun()
        else:
            st.write("暂无预测记录")
        
        st.markdown("---")
        
        # 系统信息
        st.markdown("### ⚙️ 系统状态")
        if st.button("检查系统状态"):
            status = self.prediction_service.get_service_status()
            st.json(status)
        
        # 历史记录管理
        if st.button("💾 导出历史记录"):
            self.export_history()
        if st.button("🗂️ 清空历史记录"):
            st.session_state.prediction_history = []
            st.success("历史记录已清空")
            st.rerun()
    
    def render_input_form(self):
        """渲染用户输入表单"""
        st.markdown("### 📝 请填写您的基本信息")
        
        # 省市选择区域 - 独立美化区域
        st.markdown("#### 📍 出生地信息")
        with st.container():
            col_province, col_city = st.columns(2)
            
            with col_province:
                # 省份选择
                provinces = ["请选择省份"] + list(self.province_data.keys())
                selected_province = st.selectbox(
                    "出生省份 *", 
                    provinces,
                    key="province_select",
                    help="请选择您的出生省份"
                )
            
            with col_city:
                # 城市选择
                if selected_province and selected_province != "请选择省份":
                    cities = ["请选择城市"] + self.province_data.get(selected_province, [])
                    selected_city = st.selectbox(
                        "出生城市 *",
                        cities,
                        key="city_select",
                        help="请选择您的出生城市"
                    )
                else:
                    selected_city = st.selectbox(
                        "出生城市 *", 
                        ["请先选择省份"], 
                        disabled=True,
                        help="请先选择省份后再选择城市"
                    )
        
        # 显示选择状态
        if selected_province and selected_province != "请选择省份":
            if selected_city and selected_city != "请选择城市":
                st.success(f"✅ 已选择出生地：{selected_province} {selected_city}")
            else:
                st.warning(f"⚠️ 已选择省份：{selected_province}，请选择城市")
        
        st.markdown("---")  # 分隔线
        
        # 其他表单项放在表单内部
        with st.form("user_info_form"):
            # 基本信息区域
            st.markdown("#### 👤 基本信息")
            col1_form, col2_form = st.columns(2)
            
            with col1_form:
                name = st.text_input(
                    "姓名 *", 
                    placeholder="请输入您的姓名",
                    help="请输入您的真实姓名"
                )
            
            with col2_form:
                gender = st.selectbox(
                    "性别 *", 
                    ["请选择", "男", "女"],
                    help="请选择您的性别"
                )
            
            # 处理省市数据
            if selected_province and selected_province != "请选择省份":
                birth_province = selected_province
                birth_city = selected_city if selected_city != "请选择城市" else ""
            else:
                birth_province = ""
                birth_city = ""
            
            st.markdown("#### 📅 出生时间（请填写公历/阳历时间）")
            
            # 出生日期
            date_col1, date_col2, date_col3 = st.columns(3)
            with date_col1:
                birth_year = st.number_input(
                    "出生年份 *", 
                    min_value=1900, 
                    max_value=datetime.now().year, 
                    value=1990,
                    help="请输入出生年份"
                )
            with date_col2:
                birth_month = st.number_input(
                    "出生月份 *", 
                    min_value=1, 
                    max_value=12, 
                    value=1,
                    help="请输入出生月份"
                )
            with date_col3:
                birth_day = st.number_input(
                    "出生日期 *", 
                    min_value=1, 
                    max_value=31, 
                    value=1,
                    help="请输入出生日期"
                )
            
            # 出生时间
            time_col1, time_col2 = st.columns(2)
            with time_col1:
                birth_hour = st.number_input(
                    "出生小时 *", 
                    min_value=0, 
                    max_value=23, 
                    value=12,
                    help="请输入出生小时（24小时制）"
                )
            with time_col2:
                birth_minute = st.number_input(
                    "出生分钟", 
                    min_value=0, 
                    max_value=59, 
                    value=0,
                    help="请输入出生分钟（可选）"
                )
            
            st.markdown("#### 💭 咨询内容")
            question = st.text_area(
                "咨询问题（可选）",
                placeholder="请描述您想要咨询的具体问题，如事业发展、感情婚姻、财运状况等...",
                height=100,
                help="详细描述您的问题有助于获得更精准的分析"
            )
            
            st.markdown("---")
            submitted = st.form_submit_button(
                "🔮 拜谒祈福", 
                use_container_width=True,
                help="点击开始AI命理分析"
            )
            
            if submitted:
                if not question or question.strip() == "":
                    question = "我今年的运势如何？"
                self.handle_form_submission({
                    'name': name,
                    'gender': gender,
                    'birth_year': birth_year,
                    'birth_month': birth_month,
                    'birth_day': birth_day,
                    'birth_hour': birth_hour,
                    'birth_minute': birth_minute,
                    'birth_province': birth_province,
                    'birth_city': birth_city,
                    'question': question
                })
    
    def handle_form_submission(self, form_data: dict):
        """处理表单提交"""
        # 验证表单数据
        if form_data['gender'] == "请选择":
            form_data['gender'] = ""
        
        validation_errors = self.validator.validate_user_info(form_data)
        
        if validation_errors:
            for error in validation_errors:
                st.error(error)
            return
        
        try:
            # 创建用户信息对象
            user_info = UserInfo(**form_data)
            st.session_state.current_user = user_info
            
            # 记录用户操作
            logger.log_user_action("表单提交", form_data)
            
            # 显示加载状态
            with st.spinner("正在分析您的命理信息，请稍候..."):
                # 根据选择的预测类型进行预测
                prediction_type = st.session_state.get('prediction_type', '综合运势')
                
                if prediction_type == "事业发展":
                    result = self.prediction_service.get_career_prediction(user_info)
                elif prediction_type == "感情婚姻":
                    result = self.prediction_service.get_relationship_prediction(user_info)
                else:
                    result = self.prediction_service.get_comprehensive_prediction(user_info)
                
                st.session_state.prediction_result = result
                st.session_state.show_result = True
                
                # 添加到历史记录
                st.session_state.prediction_history.append({
                    'name': user_info.name,
                    'type': prediction_type,
                    'time': result.get_formatted_time(),
                    'bazi_summary': result.bazi_summary,
                    'prediction_content': result.prediction_content,
                    'suggestions': result.suggestions,
                    'result_object': result  # 保存完整的结果对象
                })
            
            st.rerun()
            
        except Exception as e:
            st.error(f"预测过程中发生错误：{str(e)}")
            logger.error(f"预测失败: {str(e)}")
    
    def render_prediction_result(self):
        """渲染预测结果"""
        result = st.session_state.prediction_result
        
        # 返回按钮
        if st.button("← 返回输入页面"):
            st.session_state.show_result = False
            st.rerun()
        
        st.markdown(f"### 🎯 {result.user_name} 的 {result.prediction_type} 分析报告")
        
        # 预测内容
        st.markdown('<div class="prediction-content">', unsafe_allow_html=True)
        st.write(result.prediction_content)
        
        if result.suggestions:
            st.write(result.suggestions)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 操作按钮
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 导出报告"):
                self.export_report(result)
        
        with col2:
            if st.button("📱 分享结果"):
                self.share_result(result)
        
        with col3:
            if st.button("🔄 重新预测"):
                st.session_state.show_result = False
                st.session_state.current_user = None
                st.rerun()
        
        # 免责声明
        st.markdown("---")
        st.markdown(f"**免责声明：** {result.disclaimer}")
        st.markdown(f"**数据来源：** {result.data_source}")
        st.markdown(f"**预测时间：** {result.get_formatted_time()}")
    
    def export_report(self, result):
        """导出预测报告"""
        try:
            report_content = result.get_export_content()
            
            st.download_button(
                label="下载完整报告",
                data=report_content,
                file_name=f"{result.user_name}_{result.prediction_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
            
            st.success("报告已准备好下载！")
            
        except Exception as e:
            st.error(f"导出报告失败：{str(e)}")
    
    def share_result(self, result):
        """分享预测结果"""
        try:
            share_content = result.get_share_content()
            
            st.text_area(
                "分享内容（复制以下内容分享给朋友）",
                value=share_content,
                height=200
            )
            
            st.success("分享内容已生成，您可以复制分享给朋友！")
            
        except Exception as e:
            st.error(f"生成分享内容失败：{str(e)}")
    
    def export_history(self):
        """导出预测历史记录"""
        try:
            if not st.session_state.prediction_history:
                st.warning("暂无历史记录可导出")
                return
            
            # 构建导出内容
            export_content = "# 玄学AI智能体 - 预测历史记录\n\n"
            export_content += f"导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            export_content += f"总记录数：{len(st.session_state.prediction_history)}\n\n"
            export_content += "=" * 50 + "\n\n"
            
            for i, record in enumerate(st.session_state.prediction_history, 1):
                export_content += f"## 记录 {i}: {record['name']} - {record['type']}\n\n"
                export_content += f"**预测时间：** {record['time']}\n\n"
                
                if record.get('bazi_summary'):
                    export_content += f"**八字信息：**\n{record['bazi_summary']}\n\n"
                
                if record.get('prediction_content'):
                    export_content += f"**AI智能分析：**\n{record['prediction_content']}\n\n"
                
                if record.get('suggestions'):
                    export_content += f"**专业建议：**\n{record['suggestions']}\n\n"
                
                export_content += "-" * 30 + "\n\n"
            
            export_content += "\n\n**免责声明：** 本系统预测结果仅供娱乐参考，请理性对待。\n"
            export_content += "**技术支持：** 玄学AI智能体 - 基于传统命理学与现代AI技术"
            
            # 提供下载
            st.download_button(
                label="📥 下载历史记录",
                data=export_content,
                file_name=f"预测历史记录_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
            
            st.success("历史记录已准备好下载！")
            
        except Exception as e:
            st.error(f"导出历史记录失败：{str(e)}")
    
    def render_footer(self):
        """渲染页面底部"""
        st.markdown('<div class="footer">', unsafe_allow_html=True)
        st.markdown("""
        ---
        **玄学AI智能体** | 基于传统命理学与现代AI技术  
        ⚠️ 本系统预测结果仅供娱乐参考，请理性对待  
        💡 人生的幸福需要通过自己的努力来创造
        """)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """主函数"""
    try:
        # 检查环境配置
        settings = Settings()
        if not settings.validate_config():
            st.error("系统配置不完整，请检查环境变量设置")
            st.stop()
        
        # 启动应用
        app = AIBaziApp()
        app.run()
        
    except Exception as e:
        st.error(f"应用启动失败：{str(e)}")
        logger.error(f"应用启动失败: {str(e)}")

if __name__ == "__main__":
    main()