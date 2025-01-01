import streamlit as st
from typing import List, Optional
import os
import time
from report import report
from categories import get_available_categories, get_category_manager

# Set page config
st.set_page_config(
    page_title="AI市场洞察报告生成器",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .reportgen-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="reportgen-header">AI市场洞察报告生成器</p>', unsafe_allow_html=True)

# Sidebar for category selection
with st.sidebar:
    st.header("类目选择")
    categories = get_available_categories()
    selected_category = st.selectbox(
        "选择产品类目",
        categories,
        format_func=lambda x: get_category_manager(x).get_name()
    )

    # Get available sections for the selected category
    category_manager = get_category_manager(selected_category)
    
    # Define ordered sections like v2
    ordered_sections = [
        'hot_trends',          # 热点趋势和话题分析
        'emotional_analysis',   # 情感分析
        'trend_prediction',    # 趋势预测
        'audience_analysis',   # 受众画像和圈层分析
        'user_segmentation',   # 用户群体聚类与联动机会
        'market_data',         # 竞品和市场数据分析
        'differentiation',     # 差异化分析
        'design_prompt'        # Midjourney提示词生成
    ]
    
    # Filter available sections based on category's prompts
    available_prompts = category_manager.get_prompts()
    available_sections = [s for s in ordered_sections if s in available_prompts]
    
    st.header("分析维度")
    selected_sections = st.multiselect(
        "选择需要分析的维度",
        available_sections,
        default=available_sections,
        format_func=lambda x: category_manager.get_section_name(x)
    )

# Main content area
topic = st.text_input("请输入分析主题", placeholder="例如：Hello Kitty、迪士尼、宝可梦等")

if st.button("生成报告", type="primary"):
    if not topic:
        st.error("请输入分析主题")
    else:
        with st.spinner("正在生成报告，请稍候..."):
            try:
                # Show progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.1)
                    progress_bar.progress(i + 1)
                
                # Generate report
                output_file = report(
                    topic=topic,
                    category=selected_category,
                    sections=selected_sections
                )
                
                # Display success message and download button
                if os.path.exists(output_file):
                    with open(output_file, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                    
                    st.success("报告生成成功！")
                    st.download_button(
                        label="下载PDF报告",
                        data=pdf_bytes,
                        file_name=output_file,
                        mime="application/pdf"
                    )
                else:
                    st.error("报告生成失败，请重试")
            
            except Exception as e:
                st.error(f"生成报告时发生错误: {str(e)}")
                st.exception(e)
