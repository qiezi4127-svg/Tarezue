import streamlit as st   # 导入Streamlit并用st代表它
# 这里为了演示创建了多个标题展示元素

# 创建一个标题展示元素，内容是全英文的，默认锚点为first-title
st.title("first title")

# 创建一个标题展示元素，内容是全中文的
# 如不定义anchor参数，则无锚点
st.title("标题")

# 创建一个标题展示元素，内容是中英文混杂的
# 默认的锚点是英文部分的，即chinese
st.title("这是chinese标题")

# 标题展示元素,并增加了工具提示
st.title('😅这是第五个标题😅', help='工具提示')