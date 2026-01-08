import streamlit as st
import string
from collections import Counter
import pandas as pd

# 页面基础设置
st.set_page_config(
    page_title="英文单词统计工具（多文件版）",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义样式
st.markdown("""
    <style>
    .stMetric {background-color: #f0f2f6; padding: 15px; border-radius: 8px;}
    .stFileUploader > label {font-size: 16px; font-weight: 500;}
    </style>
    """, unsafe_allow_html=True)

# 核心统计函数
def count_english_words(text):
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text.lower().translate(translator)
    words = [word.strip() for word in clean_text.split() if word.strip()]
    
    total = len(words)
    unique = len(set(words))
    freq = Counter(words)
    freq_df = pd.DataFrame(freq.items(), columns=["英文单词", "出现次数"]).sort_values(by="出现次数", ascending=False).reset_index(drop=True)
    
    return {"total": total, "unique": unique, "frequency_df": freq_df}

# 网页界面
st.title("📝 英文单词统计平台（多文件批量版）")
st.markdown("### 上传多个 `.txt` 英文文件，自动统计每个文件的单词数")
st.divider()

# 多文件上传组件
uploaded_files = st.file_uploader(
    "选择多个英文文本文件（仅支持 .txt）",
    type=["txt"],
    accept_multiple_files=True,  # 开启多文件上传
    help="可同时选择多个.txt文件，自动批量统计"
)

if uploaded_files:
    # 存储所有文件的统计结果
    all_results = []
    total_all_files = 0  # 所有文件总单词数
    unique_all_files = set()  # 所有文件的唯一单词集合

    with st.spinner("正在批量统计所有文件..."):
        for file in uploaded_files:
            try:
                # 读取文件
                try:
                    text = file.read().decode("utf-8")
                except UnicodeDecodeError:
                    text = file.read().decode("gbk")
                
                # 统计当前文件
                stats = count_english_words(text)
                total_all_files += stats["total"]
                unique_all_files.update(stats["frequency_df"]["英文单词"].tolist())
                
                # 记录当前文件结果
                all_results.append({
                    "文件名": file.name,
                    "总单词数": stats["total"],
                    "唯一单词数": stats["unique"]
                })

                # 展示单个文件的详细结果
                st.subheader(f"📄 文件：{file.name}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("总单词数", stats["total"])
                with col2:
                    st.metric("唯一单词数", stats["unique"])
                st.dataframe(
                    stats["frequency_df"],
                    use_container_width=True,
                    hide_index=True,
                    column_config={"英文单词": st.column_config.TextColumn(width="medium")}
                )
                st.divider()

            except Exception as e:
                st.error(f"文件 {file.name} 处理失败：{str(e)}", icon="⚠️")

        # 展示所有文件的汇总结果
        st.subheader("📊 所有文件汇总统计")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("所有文件总单词数", total_all_files)
        with col_b:
            st.metric("所有文件唯一单词数", len(unique_all_files))
        
        # 展示各文件统计表格
        st.dataframe(
            pd.DataFrame(all_results),
            use_container_width=True,
            hide_index=True,
            column_config={
                "文件名": st.column_config.TextColumn(width="medium"),
                "总单词数": st.column_config.NumberColumn(),
                "唯一单词数": st.column_config.NumberColumn()
            }
        )

else:
    st.info("👉 可同时选择多个.txt文件上传，自动批量统计", icon="💡")
