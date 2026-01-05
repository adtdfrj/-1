import streamlit as st
import pandas as pd
import os

# 1. 网页基础设置
st.set_page_config(page_title="成果查询系统", layout="wide")

# 2. 读取数据的函数
@st.cache_data
def load_data(file_path):
    try:
        # 尝试使用 utf-8 读取，如果失败则尝试 gbk
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='gbk')
            
        # 填充一下空值，防止报错
        df = df.fillna("")
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"读取数据出错: {e}")
        return None

# 3. 页面主要内容
# 加载数据逻辑
# 侧边栏：简单统计
with st.sidebar:
    st.header("关于系统 (About)")
    st.write("这是一个本地离线查询系统。")
    st.markdown("---")
    language = st.radio("语言选择 (Language)", ["中文", "English"])

# 根据语言选择加载不同的数据文件
# 统一使用合并后的文件
current_file = "data_merged.csv"

# 加载数据
df = load_data(current_file)

if language == "English":
    main_title = "🔎 Achievement Query System"
    search_placeholder = "Please enter keywords... e.g. Radar, Robot"
    result_text = "✅ Found {} related results:"
    no_result_text = "❌ No results found for '{}', please try other keywords."
    info_text = "👆 Please enter keywords above. Here are some latest results:"
    link_text = "👉 Click for details"
    time_text = "Date/Index: {}"
    # 英文模式下使用 title_en 列
    search_col = 'title_en'
    display_col = 'title_en'
    
    # 检查是否有英文数据列
    if df is not None and 'title_en' not in df.columns:
        st.error("English data column (title_en) is missing in data_merged.csv.")
        st.stop()
else:
    main_title = "🔎 成果查询系统"
    search_placeholder = "请输入关键字进行搜索... 例如：雷达、机器人、芯片"
    result_text = "✅ 找到 {} 条相关结果："
    no_result_text = "❌ 没有找到包含“{}”的成果，请尝试其他关键词。"
    info_text = "👆 请在上方输入关键字开始检索。以下是部分最新成果预览："
    link_text = "👉 点击查看详情"
    time_text = "数据索引号/时间: {}"
    # 中文模式下使用 title 列
    search_col = 'title'
    display_col = 'title'

if df is not None:
    with st.sidebar:
        st.success(f"当前已收录数据：{len(df)} 条")

    st.title(main_title)

    # 顶部搜索框
    col1, col2 = st.columns([3, 1])
    with col1:
        keyword = st.text_input("Search", placeholder=search_placeholder, label_visibility="collapsed")
    
    st.markdown("---")

    # 筛选逻辑
    if keyword:
        # 模糊搜索
        # 使用对应的语言列进行搜索
        result = df[df[search_col].astype(str).str.contains(keyword, case=False, na=False)]
        
        if not result.empty:
            st.subheader(result_text.format(len(result)))
            
            # 遍历显示结果
            for index, row in result.iterrows():
                # 使用卡片样式展示
                with st.container():
                    # 标题作为链接，显示对应语言的标题
                    st.markdown(f"### 📄 [{row[display_col]}]({row['link']})")
                    
                    # 如果有时间字段，显示时间
                    if 'create_time' in row and row['create_time']:
                        st.caption(time_text.format(row['create_time']))
                    
                    st.divider()
        else:
            st.warning(no_result_text.format(keyword))
    else:
        # 如果没输入关键字，显示前5条作为示例
        st.info(info_text)
        
        # 显示前5条，使用可点击的链接
        for index, row in df.head(5).iterrows():
            with st.container():
                # 标题作为链接，显示对应语言的标题
                st.markdown(f"##### 📄 [{row[display_col]}]({row['link']})")
                # 显示时间
                if 'create_time' in row and row['create_time']:
                    st.caption(time_text.format(row['create_time']))
                st.divider()

else:
    st.error(f"找不到 {current_file} 文件！请确保该文件在同一目录下。")