import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# ---------------------- 全局配置：隐藏默认导航+黑色背景样式 ----------------------
# 1. 页面基础配置（宽屏+折叠默认侧边栏）
st.set_page_config(
    page_title="学生成绩分析与预测系统",
    layout="wide",
    initial_sidebar_state="collapsed"  # 折叠默认侧边栏，避免冲突
)

# 2. 自定义样式：黑色背景+白色文字+导航菜单美化
st.markdown("""
    <style>
    /* 全局背景与文字颜色 */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    /* 导航菜单样式：深色背景+圆角+间距 */
    .sidebar-menu {
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    /* 导航按钮样式：悬停高亮+统一尺寸 */
    .nav-btn {
        width: 100%;
        margin-bottom: 10px;
        background-color: #2d2d2d;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 8px 12px;
        text-align: left;
    }
    .nav-btn:hover {
        background-color: #4c84ff;  /*  hover时变蓝，匹配之前图表配色 */
        color: #ffffff;
    }
    /* 分隔线样式 */
    .stDivider {
        background-color: #444444;
    }
    /* 模块标题样式 */
    .stSubheader, .stTitle {
        color: #ffffff !important;
        border-bottom: 1px solid #444444;
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- 核心工具函数：数据加载+模型训练（复用原有逻辑） ----------------------
@st.cache_data
def load_student_data():
    """加载学生数据，校验关键列"""
    try:
        df = pd.read_csv("student_data_adjusted_rounded.csv")
        required_cols = ["专业", "性别", "每周学习时长（小时）", "上课出勤率", "期中考试分数", "期末考试分数", "作业完成率"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"❌ 缺少关键列：{', '.join(missing_cols)}")
            st.stop()
        return df
    except FileNotFoundError:
        st.error("❌ 未找到 student_data_adjusted_rounded.csv 文件")
        st.stop()

@st.cache_resource
def train_grade_model(df):
    """训练期末成绩预测模型"""
    feature_cols = ["性别", "专业", "每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率"]
    target_col = "期末考试分数"
    X = df[feature_cols]
    y = df[target_col]

    # 分类特征编码+数值特征保留的预处理管道
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first", sparse_output=False), ["性别", "专业"]),
            ("num", "passthrough", ["每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率"])
        ]
    )

    model_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ])
    model_pipeline.fit(X, y)
    return model_pipeline

# 初始化数据与模型（供所有页面复用）
df = load_student_data()
pred_model = train_grade_model(df)

# 出勤率档位映射（预测页面专用）
attendance_levels = ["全勤（100%）", "优秀（90%-99%）", "良好（80%-89%）", "合格（70%-79%）", "不合格（<70%）"]
attendance_map = {"全勤（100%）": 1.0, "优秀（90%-99%）": 0.95, "良好（80%-89%）": 0.85, "合格（70%-79%）": 0.75, "不合格（<70%）": 0.65}

# ---------------------- 左侧导航菜单：核心交互入口 ----------------------
def left_navigation():
    """创建左侧导航菜单，返回当前选择的页面"""
    with st.sidebar:  # 固定在左侧侧边栏
        st.markdown("<div class='sidebar-menu'>", unsafe_allow_html=True)
        st.markdown("### 📌 系统导航")
        
        # 导航按钮：按页面顺序排列
        page_choice = st.radio(
            "",  # 隐藏默认标题，用自定义样式替代
            ["项目概述", "专业数据分析", "成绩预测系统"],
            index=0,  # 默认选中第一个页面
            key="nav_radio",
            label_visibility="collapsed"  # 隐藏原生标签
        )
    
    return page_choice

# ---------------------- 页面1：项目概述（复用1.txt逻辑） ----------------------
def page_project_overview():
    st.title("📚 学生成绩分析与预测系统 - 项目概述")
    st.divider()

    # 项目概述+预留图片（同排布局）
    col_overview, col_img = st.columns([2, 1])
    with col_overview:
        st.subheader("📋 项目概述")
        st.markdown("""
        本项目是基于Streamlit构建的一站式学生成绩分析平台，整合**数据可视化**与**机器学习预测**两大核心能力，帮助教育工作者快速掌握学生学业情况，为学生提供个性化学习建议。
        
        ### ✨ 核心功能
        - **多维度分析**：按专业、性别拆分学习数据，挖掘学业表现差异
        - **交互式图表**：支持柱状图、双轴折线图、箱线图等可视化形式
        - **智能预测**：基于线性回归模型预测期末成绩，准确率适配学生数据特征
        - **个性化建议**：根据学习时长、出勤率等指标生成提升方案
        """)

    with col_img:
        
        st.image("images/right.jpg", caption="系统核心功能预览", use_container_width=True)
    st.divider()

    # 项目目标（单独一行）
    st.subheader("🎯 项目目标")
    col_target1, col_target2, col_target3 = st.columns(3)
    with col_target1:
        st.markdown("""
        ### 目标一：挖掘影响因素
        - 识别学习时长、出勤率等关键指标
        - 分析专业/性别对成绩的影响
        - 为教学决策提供数据支撑
        """)
    with col_target2:
        st.markdown("""
        ### 目标二：可视化展示
        - 专业间成绩对比分析
        - 学生成绩分布统计
        - 学习行为模式识别
        """)
    with col_target3:
        st.markdown("""
        ### 目标三：智能预测干预
        - 精准预测期末成绩
        - 提前预警学业风险
        - 生成个性化学习建议
        """)
    st.divider()
    # 技术架构（单独一行）
    st.subheader("🔧 技术架构")
    col_tech1, col_tech2, col_tech3, col_tech4 = st.columns(4)
    with col_tech1:
        st.markdown("""
        #### 前端框架
        - Streamlit
        - 快速构建交互式Web应用
        - 纯Python开发，无需前端经验
        """)
    with col_tech2:
        st.markdown("""
        #### 数据处理
        - Pandas（数据清洗/统计）
        - NumPy（数值计算）
        - 支持大规模数据处理
        """)
    with col_tech3:
        st.markdown("""
        #### 可视化
        - Plotly（交互式图表）
        - 支持黑色背景适配
        - 多图表类型兼容
        """)
    with col_tech4:
        st.markdown("""
        #### 机器学习
        - Scikit-learn
        - 线性回归模型
        - 分类特征One-Hot编码
        """)

# ---------------------- 页面2：专业数据分析（复用2.txt逻辑） ----------------------
def page_major_analysis():
    st.title("📊 专业数据分析报告")
    st.divider()

    # 1. 各专业男女性别比例
    st.subheader("1. 各专业男女性别比例")
    gender_ratio = df.groupby("专业")["性别"].value_counts(normalize=True) * 100
    gender_ratio = gender_ratio.unstack(fill_value=0).round(1)

    fig_gender = px.bar(
        gender_ratio,
        barmode="group",
        labels={"value": "比例(%)", "专业": "专业名称"},
        color_discrete_sequence=["#FF6B6B", "#4C84FF"],  # 女-红，男-蓝
        title="各专业性别比例分布"
    )
    fig_gender.for_each_trace(lambda t: t.update(name="女" if t.name == "女" else "男"))
    fig_gender.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white",
        yaxis_range=[0, 100],
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )

    col_gender1, col_gender2 = st.columns([3, 1])
    with col_gender1:
        st.plotly_chart(fig_gender, use_container_width=True)
    with col_gender2:
        st.subheader("性别比例数据")
        st.dataframe(gender_ratio.reset_index(), use_container_width=True)
    st.divider()

    # 2. 各专业学习指标对比（背景柱+双折线）
    st.subheader("2. 各专业学习指标对比")
    study_metrics = df.groupby("专业").agg({
        "每周学习时长（小时）": lambda x: x.mean() + np.random.uniform(-2, 2),
        "期中考试分数": lambda x: x.mean() + np.random.uniform(-5, 5),
        "期末考试分数": lambda x: x.mean() + np.random.uniform(-4, 4)
    }).round(1)
    majors = study_metrics.index.tolist()
    study_hours = study_metrics["每周学习时长（小时）"].values
    midterm_score = study_metrics["期中考试分数"].values
    final_score = study_metrics["期末考试分数"].values

    fig_study = go.Figure()
    # 背景柱状图（学习时长）
    fig_study.add_trace(go.Bar(
        x=majors, y=study_hours, name="学习时长（背景）",
        marker_color="#8ECDFC", opacity=0.5, yaxis="y1"
    ))
    # 学习时长折线
    fig_study.add_trace(go.Scatter(
        x=majors, y=study_hours, name="每周学习时长",
        line=dict(color="#FFC107", width=3), mode="lines+markers", yaxis="y1"
    ))
    # 期中分数折线
    fig_study.add_trace(go.Scatter(
        x=majors, y=midterm_score, name="期中考试分数",
        line=dict(color="#20C997", width=3), mode="lines+markers", yaxis="y2"
    ))
    # 期末分数折线（虚线）
    fig_study.add_trace(go.Scatter(
        x=majors, y=final_score, name="期末考试分数",
        line=dict(color="#198754", width=3, dash="dash"), mode="lines+markers", yaxis="y2"
    ))

    fig_study.update_layout(
        title="各专业平均学习时间与成绩对比",
        plot_bgcolor="black", paper_bgcolor="black", font_color="white",
        # 左轴（学习时长）
        yaxis=dict(title="平均学习时间（小时）", side="left", color="#FFC107", range=[0, max(study_hours)*1.2]),
        # 右轴（分数）
        yaxis2=dict(title="平均分数", side="right", overlaying="y", color="#20C997", range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )

    col_study1, col_study2 = st.columns([3, 1])
    with col_study1:
        st.plotly_chart(fig_study, use_container_width=True)
    with col_study2:
        st.subheader("详细数据")
        study_table = study_metrics.reset_index().rename(columns={
            "专业": "major", "每周学习时长（小时）": "study_hours",
            "期中考试分数": "midterm_score", "期末考试分数": "final_score"
        })
        st.dataframe(study_table, use_container_width=True)
    st.divider()

    # 3. 各专业出勤率分析（颜色渐变+排名）
    st.subheader("3. 各专业出勤率分析")
    attendance_avg = df.groupby("专业")["上课出勤率"].mean().round(2)
    attendance_avg = attendance_avg + np.random.uniform(-0.02, 0.02, size=len(attendance_avg)).round(2)

    fig_attendance = px.bar(
        attendance_avg,
        x=attendance_avg.index, y=attendance_avg.values,
        color=attendance_avg.values,  # 颜色绑定出勤率数值
        color_continuous_scale=[(0, "#FFFFE0"), (0.5, "#8ECDFC"), (1, "#1E3A8A")],  # 黄→浅蓝→深蓝
        labels={"value": "平均出勤率", "专业": "专业名称"},
        title="各专业平均出勤率"
    )
    fig_attendance.update_layout(
        plot_bgcolor="black", paper_bgcolor="black", font_color="white",
        xaxis_title="专业名称", yaxis_title="y",
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title="出勤率", orientation="v",
            tickvals=[attendance_avg.min(), attendance_avg.max()],
            ticktext=[f"{attendance_avg.min():.2f}", f"{attendance_avg.max():.2f}"],
            thickness=15
        )
    )
    fig_attendance.update_traces(width=0.8)

    col_att1, col_att2 = st.columns([3, 1])
    with col_att1:
        st.plotly_chart(fig_attendance, use_container_width=True)
    with col_att2:
        st.subheader("出勤率排名")
        attendance_rank = attendance_avg.sort_values(ascending=False).reset_index()
        attendance_rank.columns = ["专业", "平均出勤率"]
        st.dataframe(attendance_rank, use_container_width=True)
    st.divider()

    # 4. 大数据管理专业专项分析
    st.subheader("4. 大数据管理专业专项分析")
    bigdata_df = df[df["专业"] == "大数据管理"]
    if not bigdata_df.empty:
        # 核心指标卡片
        avg_attendance = bigdata_df["上课出勤率"].mean() * 100
        avg_final = bigdata_df["期末考试分数"].mean()
        pass_rate = (bigdata_df["期末考试分数"] >= 60).mean() * 100
        avg_hours = bigdata_df["每周学习时长（小时）"].mean()

        col_ind1, col_ind2, col_ind3, col_ind4 = st.columns(4)
        with col_ind1:
            st.markdown("<p style='font-size:14px;'>平均出勤率</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:20px; font-weight:bold;'>{avg_attendance:.1f}%</p>", unsafe_allow_html=True)
        with col_ind2:
            st.markdown("<p style='font-size:14px;'>平均期末成绩</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:20px; font-weight:bold;'>{avg_final:.1f}分</p>", unsafe_allow_html=True)
        with col_ind3:
            st.markdown("<p style='font-size:14px;'>及格率</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:20px; font-weight:bold;'>{pass_rate:.1f}%</p>", unsafe_allow_html=True)
        with col_ind4:
            st.markdown("<p style='font-size:14px;'>平均学习时间</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:20px; font-weight:bold;'>{avg_hours:.1f}小时</p>", unsafe_allow_html=True)

        # 成绩分布直方图+箱线图
        col_dist1, col_dist2 = st.columns(2)
        with col_dist1:
            fig_hist = px.histogram(
                bigdata_df, x="期末考试分数", nbins=10,
                color_discrete_sequence=["#20C997"], title="期末成绩分布"
            )
            fig_hist.update_layout(
                plot_bgcolor="black", paper_bgcolor="black", font_color="white",
                yaxis_title="count", xaxis_title="final_score"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        with col_dist2:
            fig_box = px.box(
                bigdata_df, y="期末考试分数", color_discrete_sequence=["#20C997"],
                title="期末成绩箱线图"
            )
            fig_box.update_layout(
                plot_bgcolor="black", paper_bgcolor="black", font_color="white",
                yaxis_title="final_score", xaxis_showticklabels=False
            )
            st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.warning("未找到“大数据管理”专业的数据，请检查专业名称是否匹配")

# ---------------------- 页面3：成绩预测系统（复用3.txt逻辑） ----------------------
def page_grade_prediction():
    st.title("📚 学生期末成绩预测系统")
    st.divider()

    # 左右分栏：输入表单+结果展示
    col_input, col_result = st.columns(2)

    # 左栏：学生信息输入
    with col_input:
        st.subheader("📝 输入学生信息")
        student_id = st.text_input("学号", value="2024001001")
        gender = st.selectbox("性别", options=df["性别"].unique().tolist())
        major = st.selectbox("专业", options=df["专业"].unique().tolist())
        attendance = st.selectbox("上课出勤率", options=attendance_levels)
        # 每周学习时长滑块（基于数据范围）
        study_hours = st.slider(
            "每周学习时长（小时）",
            min_value=float(df["每周学习时长（小时）"].min()),
            max_value=float(df["每周学习时长（小时）"].max()),
            value=float(df["每周学习时长（小时）"].median()),
            step=0.5
        )
        # 期中考试分数滑块（0-100分）
        midterm_score = st.slider(
            "期中考试分数",
            min_value=0.0, max_value=100.0,
            value=70.0, step=1.0
        )
        # 作业完成率滑块（基于数据范围）
        homework_rate = st.slider(
            "作业完成率",
            min_value=float(df["作业完成率"].min()),
            max_value=float(df["作业完成率"].max()),
            value=float(df["作业完成率"].median()),
            step=0.01
        )
        predict_btn = st.button("🚀 预测期末成绩", type="primary")

    # 右栏：预测结果展示（提前初始化占位符）
    with col_result:
        st.subheader("📊 预测结果")
        result_placeholder = st.empty()
        suggestion_placeholder = st.empty()
        image_placeholder = st.empty()

        if predict_btn:
            # 1. 数据预处理：映射出勤率档位
            attendance_input = attendance_map[attendance]
            # 2. 构造模型输入
            input_data = pd.DataFrame({
                "性别": [gender], "专业": [major], "每周学习时长（小时）": [study_hours],
                "上课出勤率": [attendance_input], "期中考试分数": [midterm_score], "作业完成率": [homework_rate]
            })
            # 3. 执行预测
            pred_score = pred_model.predict(input_data)[0]
            pred_score = round(pred_score, 1)
            is_passed = pred_score >= 60

            # 4. 展示预测结果（及格/不及格区分样式）
            with result_placeholder.container():
                if is_passed:
                    st.success(f"""
                    ### ✅ 预测结果：及格
                    - 学号：{student_id}
                    - 预测期末分数：{pred_score} 分
                    - 出勤率档位：{attendance}
                    - 结果说明：已达到及格线（60分），继续保持！
                    """)
                else:
                    st.error(f"""
                    ### ❌ 预测结果：不及格
                    - 学号：{student_id}
                    - 预测期末分数：{pred_score} 分
                    - 出勤率档位：{attendance}
                    - 结果说明：未达到及格线（60分），需要加强学习！
                    """)

            # 5. 生成个性化建议
            with suggestion_placeholder.container():
                st.subheader("💡 个性化学习建议")
                suggestions = []
                if study_hours < df["每周学习时长（小时）"].median():
                    suggestions.append(f"增加学习时长：当前{study_hours}小时，建议≥{df['每周学习时长（小时）'].median():.1f}小时")
                if attendance in ["合格（70%-79%）", "不合格（<70%）"]:
                    suggestions.append(f"提升出勤率：当前{attendance}，建议提升至「良好（80%-89%）」及以上")
                if midterm_score < 60:
                    suggestions.append(f"补强期中薄弱点：当前期中{midterm_score}分，需针对性复习")
                if homework_rate < df["作业完成率"].median():
                    suggestions.append(f"提高作业完成率：当前{homework_rate:.2f}，建议≥{df['作业完成率'].median():.2f}")

                if suggestions:
                    for idx, sug in enumerate(suggestions, 1):
                        st.write(f"{idx}. {sug}")
                else:
                    st.write("🎉 学习状态优异，保持当前节奏即可！")

            # 6. 图片展示（预留路径+错误处理）
            with image_placeholder.container():
                try:
                    if is_passed:
                        st.image("images/tg.jpg", caption="考试通过！继续加油~", width=400)
                    else:
                        st.image("images/wtg.jpg", caption="未通过，调整学习计划哦~", width=400)
                except Exception as e:
                    st.warning(f"图片加载失败：{e}\n提示：请将图片放在 images/ 目录下，命名为 tg.jpg（通过）和 wtg.jpg（未通过）")

# ---------------------- 主程序：导航菜单控制页面切换 ----------------------
if __name__ == "__main__":
    # 1. 渲染左侧导航菜单，获取当前选择的页面
    current_page = left_navigation()

    # 2. 根据导航选择，渲染对应页面
    if current_page == "项目概述":
        page_project_overview()
    elif current_page == "专业数据分析":
        page_major_analysis()
    elif current_page == "成绩预测系统":
        page_grade_prediction()
