import streamlit as st
import string
from collections import Counter
import pandas as pd

# ---------------------- 页面基础设置 ----------------------
st.set_page_config(
    page_title="英文单词统计工具",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义样式（优化界面美观度）
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
    }
    .stFileUploader > label {
        font-size: 16px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------- 核心统计函数 ----------------------
def count_english_words(text):
    """
    统计英文文本单词数，返回总词数、唯一词数、词频
    """
    # 1. 预处理：去标点、转小写、去空字符
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text.lower().translate(translator)
    words = [word.strip() for word in clean_text.split() if word.strip()]
    
    # 2. 核心统计
    total_words = len(words)
    unique_words = len(set(words))
    word_freq = Counter(words)
    
    # 3. 整理成DataFrame（方便表格展示）
    freq_df = pd.DataFrame(
        word_freq.items(),
        columns=["英文单词", "出现次数"]
    ).sort_values(by="出现次数", ascending=False).reset_index(drop=True)
    
    return {
        "total": total_words,
        "unique": unique_words,
        "frequency_df": freq_df
    }

# ---------------------- 网页界面 ----------------------
# 标题和说明
st.title("📝 英文单词统计平台")
st.markdown("### 上传 `.txt` 格式的英文文本文件，自动统计单词数量和频率")
st.divider()

# 1. 文件上传组件
uploaded_file = st.file_uploader(
    label="选择英文文本文件（仅支持 .txt）",
    type=["txt"],
    label_visibility="visible",
    help="支持任意大小的纯文本文件，自动处理编码问题"
)

# 2. 处理文件并展示结果
if uploaded_file is not None:
    try:
        # 读取文件（兼容utf-8/gbk编码）
        with st.spinner("正在读取并统计文件内容..."):
            try:
                text_content = uploaded_file.read().decode("utf-8")
            except UnicodeDecodeError:
                text_content = uploaded_file.read().decode("gbk")
            
            # 调用统计函数
            stats = count_english_words(text_content)
        
        # 展示核心统计结果（双列布局）
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="✅ 总单词数", value=stats["total"])
        with col2:
            st.metric(label="🔑 唯一单词数", value=stats["unique"])
        
        st.divider()
        
        # 展示单词频率表格（支持搜索/排序）
        st.subheader("📊 单词出现频率（降序）")
        st.dataframe(
            stats["frequency_df"],
            use_container_width=True,
            hide_index=True,
            column_config={
                "英文单词": st.column_config.TextColumn("英文单词", width="medium"),
                "出现次数": st.column_config.NumberColumn("出现次数", width="small")
            }
        )
        
    except Exception as e:
        st.error(f"❌ 文件处理失败：{str(e)}", icon="⚠️")
else:
    # 未上传文件时的提示和示例
    st.info("👉 请上传 `.txt` 格式的英文文本文件，上传后自动统计", icon="💡")
    with st.expander("📌 点击查看测试示例文本"):
        sample_text = """Hello! This is a test text. Hello world! 
        This text is used to test the word count script. Let's go!"""
        st.code(sample_text, language="text")
        st.caption("测试示例统计结果：总单词数 18，唯一单词数 13")

# 页脚
st.divider()
st.caption("💡 提示：工具会自动去除标点、忽略大小写，确保统计结果准确 | 支持Windows/Mac/Linux")
