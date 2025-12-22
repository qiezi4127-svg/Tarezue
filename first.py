import streamlit as st
import pandas as pd
import numpy as np

# ---------------------- 页面配置 ----------------------
st.set_page_config(
    page_title="南宁美食数据仪表盘",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义样式
st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E2E;
        color: #FFFFFF;
    }
    .stMetric {
        background-color: #2D2D44;
        padding: 10px;
        border-radius: 8px;
    }
    .stDataFrame {
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- 数据准备 ----------------------
# 1. 店铺基础信息（6家）
shops_data = pd.DataFrame({
    "店铺名称": ["南宁老友粉王", "桂小厨·广西菜", "复记老友粉", "舒记老友粉", "粉之都·螺蛳粉", "阿嬷手作"],
    "评分": [4.7, 4.8, 4.6, 4.5, 4.4, 4.9],
    "人均价格": [15, 85, 12, 13, 10, 28],
    "地址": ["南宁市青秀区中山路", "南宁市兴宁区朝阳路", "南宁市兴宁区人民东路", 
             "南宁市青秀区桃源路", "南宁市西乡塘区大学路", "南宁市青秀区万象城"],
    "纬度": [22.8170, 22.8258, 22.8285, 22.8120, 22.8007, 22.8106],
    "经度": [108.3664, 108.3410, 108.3450, 108.3400, 108.2915, 108.3525]
})

# 2. 用餐高峰时段数据（Area Chart）
time_data = pd.DataFrame({
    "时段": ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"],
    "客流量": [50, 80, 200, 60, 70, 250, 180, 100]
}).set_index("时段")

# 3. 12个月价格走势（5家店折线图）
months = pd.date_range(start="2024-01-01", periods=12, freq="M").strftime("%Y-%m")
price_trend_data = pd.DataFrame({
    "月份": months,
    shops_data["店铺名称"][0]: [15,15,16,16,17,17,17,18,18,18,19,19],
    shops_data["店铺名称"][1]: [80,82,83,85,85,88,90,90,92,92,95,95],
    shops_data["店铺名称"][2]: [12,12,13,13,13,14,14,14,15,15,15,16],
    shops_data["店铺名称"][3]: [30,40,50,60,70,50,25,90,33,44,16,24],
    shops_data["店铺名称"][4]: [10,10,10,11,11,11,12,12,12,13,13,13]
}).set_index("月份")

# ---------------------- 页面布局 ----------------------
st.title("🍜 南宁美食数据仪表盘")

# 第一行：地图 + 评分柱状图
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📍 店铺位置分布")
    # Streamlit原生地图
    st.map(shops_data[["纬度", "经度"]].rename(columns={"纬度":"lat", "经度":"lon"}), 
           zoom=12, use_container_width=True)

with col2:
    st.subheader("⭐ 餐厅评分")
    # Streamlit原生柱状图
    bar_data = shops_data.set_index("店铺名称")[["评分"]]
    st.bar_chart(bar_data, height=300, use_container_width=True)

# 第二行：价格走势折线图（5家店）
st.subheader("📈 餐厅12个月价格走势")
st.line_chart(price_trend_data, height=300, use_container_width=True)

# 第三行：用餐高峰时段面积图 + 店铺详情
col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("⏰ 用餐高峰时段")
    # Streamlit原生面积图
    st.area_chart(time_data, height=300, use_container_width=True)

with col4:
    st.subheader("📋 餐厅详情")
    # 店铺详情表格
    st.dataframe(
        shops_data[["店铺名称", "评分", "人均价格", "地址"]],
        hide_index=True,
        use_container_width=True
    )

# 第四行：今日推荐
st.subheader("🍱 今日午餐推荐")
st.markdown("**南宁老友粉王 · 经典老友粉（15元）**")
st.image("https://ts1.tc.mm.bing.net/th/id/R-C.1b5cddc5a949b7bddda62ad84856b1ee?rik=YWNf5dczUf%2fFwA&riu=http%3a%2f%2fcp1.douguo.net%2fupload%2fcaiku%2fd%2fe%2f2%2fyuan_de699d706dad44c820edbe58ec01cf82.jpg&ehk=OseYroWQTztMjKcKgQb%2fbNsBlQMaKljLVuXIMo25hmY%3d&risl=&pid=ImgRaw&r=0", 
         width=300, caption="南宁经典老友粉")
