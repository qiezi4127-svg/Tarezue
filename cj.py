import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import random

# 页面基础设置
st.set_page_config(page_title="期末成绩预测", page_icon="📚", layout="wide")
st.title("📚 期末成绩预测")
st.caption("基于机器学习模型，输入学习信息预测期末成绩")

# ---------------------- 模拟训练数据 & 模型训练 ----------------------
# 模拟学生特征数据：[每周学习时长, 出勤率编码, 补考次数, 作业完成度]
# 出勤率编码：全勤=3, 80%=2, 60%=1, 低于60%=0
X_train = np.array([
    [10, 3, 0, 90], [5, 2, 1, 60], [2, 0, 2, 30], [15, 3, 0, 100],
    [8, 2, 0, 75], [3, 1, 1, 40], [12, 3, 0, 85], [6, 1, 2, 50]
])
# 模拟对应的成绩标签（0-100）
y_train = np.array([85, 62, 35, 98, 73, 42, 92, 55])

# 训练线性回归模型
model = LinearRegression()
model.fit(X_train, y_train)

# ---------------------- 页面交互逻辑 ----------------------
# 表单区域
with st.form(key="score_predict_form"):
    col1, col2 = st.columns(2)
    with col1:
        student_id = st.text_input("学号", placeholder="请输入学号")
        gender = st.selectbox("性别", options=["", "男", "女"])
        major = st.selectbox("专业", options=["", "信息系统", "计算机科学", "软件工程", "大数据"])
    with col2:
        study_time = st.number_input("每周学习时长(小时)", min_value=0, step=1, placeholder="请输入时长")
        class_attend = st.selectbox("上课出勤率", options=["", "全勤", "80%", "60%", "低于60%"])
        exam_times = st.number_input("补考次数", min_value=0, step=1, placeholder="请输入次数")
        homework = st.slider("作业完成度(%)", min_value=0, max_value=100, value=50)

    # 提交按钮
    submit_btn = st.form_submit_button("预测成绩", type="primary")

# 预测结果区域
st.subheader("📊 预测结果")
progress_bar = st.progress(0)
result_placeholder = st.empty()

if submit_btn:
    # 校验表单必填项
    if not all([student_id, gender, major, study_time, class_attend]):
        st.error("请填写所有必填信息！")
    else:
        # 特征编码：将出勤率转换为数值
        attend_map = {"全勤": 3, "80%": 2, "60%": 1, "低于60%": 0}
        attend_encoded = attend_map[class_attend]

        # 构造预测特征数组
        X_predict = np.array([[study_time, attend_encoded, exam_times, homework]])
        # 模型预测成绩（限制在0-100之间）
        score = model.predict(X_predict)[0]
        score = max(0, min(100, score))  # 防止分数超出范围
        score = round(score, 1)  # 保留1位小数

        # 展示进度条和结果
        progress_bar.progress(int(score))
        if score >= 60:
            result_placeholder.success(f"恭喜！预测期末成绩为**{score}分**，顺利通过！")
            # # 预测结果图片占位：替换为通过的图片路径
            # st.image("pass.png", caption=f"预测成绩：{score}分", width=400)
        else:
            result_placeholder.error(f"遗憾！预测期末成绩为**{score}分**，未通过！")
            # # 预测结果图片占位：替换为未通过的图片路径
            # st.image("fail.png", caption=f"预测成绩：{score}分", width=400)
        
        # 生成学习建议
        st.subheader("💡 学习建议")
        if score < 60:
            st.write("- 增加每周学习时长，建议每天至少2小时专注专业课学习")
            st.write("- 保证上课出勤率，及时跟上老师的教学节奏")
            st.write("- 按时完成作业，通过练习巩固知识点")
        elif 60 <= score < 80:
            st.write("- 可针对薄弱章节进行专项复习，提升成绩上限")
            st.write("- 参与学习小组讨论，交流解题思路")
        else:
            st.write("- 保持当前学习状态，可尝试拓展专业相关的进阶知识")
            st.write("- 利用课余时间参与学科竞赛，提升实践能力")
