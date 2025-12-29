import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# 设置页面的标题、图标和布局
st.set_page_config(
    page_title="企鹅分类器",
    page_icon=":penguin:",
    layout='wide'
)

# ---------------------- 修复1：加载训练模型（适配中文CSV列名） ----------------------
def load_and_train_model(csv_path):
    """读取中文列名CSV，预处理并训练随机森林模型"""
    # 读取CSV文件（中文列名直接保留）
    df = pd.read_csv(csv_path, encoding='gbk')  
    
    # 查看CSV实际列名（可选，用于调试）
    # st.write("CSV列名：", df.columns.tolist())
    
    # 缺失值处理（数值列用中位数填充，性别用UNKNOWN填充）
    numeric_cols = ['喙的长度', '喙的深度', '翅膀的长度', '身体质量']
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df['性别'] = df['性别'].fillna('UNKNOWN')
    
    # 特征和标签分离（标签列是“企鹅的种类”，而非英文species）
    X = df.drop('企鹅的种类', axis=1)
    y = df['企鹅的种类']
    
    # 分类特征独热编码（中文列名：岛屿、性别）
    cat_features = ['企鹅栖息的岛屿', '性别']
    encoder = OneHotEncoder(sparse_output=False, drop='first')
    cat_encoded = encoder.fit_transform(X[cat_features])
    cat_df = pd.DataFrame(cat_encoded, columns=encoder.get_feature_names_out(cat_features))
    
    # 合并数值特征和编码后的分类特征
    num_features = X.drop(cat_features, axis=1)
    X_processed = pd.concat([num_features.reset_index(drop=True), cat_df.reset_index(drop=True)], axis=1)
    
    # 修复2：train_test_split参数错误（缺少y参数，修正参数顺序）
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, train_size=0.8, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    # 返回模型、编码器、特征名、物种列表
    return model, encoder, X_processed.columns, y.unique()

# ---------------------- 修复3：用户输入预处理（删除重复参数+适配中文特征） ----------------------
# 移除重复的flipper_length和冗余的body参数，参数顺序与表单输入一致
def preprocess_user_input(island, sex, bill_length, bill_depth, flipper_length, body_mass, encoder):
    """将用户输入转换为模型可接受的格式（适配中文列名）"""
    # 构造用户输入的DataFrame（列名与CSV一致，均为中文）
    user_input = pd.DataFrame({
        '企鹅栖息的岛屿': [island],
        '性别': [sex],
        '喙的长度': [bill_length],
        '喙的深度': [bill_depth],
        '翅膀的长度': [flipper_length],
        '身体质量': [body_mass]
    })
    
    # 对分类特征编码（使用训练好的编码器）
    cat_features = ['企鹅栖息的岛屿', '性别']
    cat_encoded = encoder.transform(user_input[cat_features])
    cat_df = pd.DataFrame(cat_encoded, columns=encoder.get_feature_names_out(cat_features))
    
    # 合并数值特征和编码后的分类特征
    num_features = user_input.drop(cat_features, axis=1)
    input_processed = pd.concat([num_features.reset_index(drop=True), cat_df.reset_index(drop=True)], axis=1)
    
    return input_processed

# ---------------------- 页面逻辑（优化交互体验） ----------------------
with st.sidebar:
    # 图片路径若不存在可注释
    st.image('images/right_logo.png', width=100)
    st.title('请选择页面')
    page = st.selectbox("请选择页面", ["简介页面", "预测分类页面"], label_visibility='collapsed')

if page == "简介页面":
    st.title("企鹅分类器:penguin:")
    st.header('数据集介绍')
    st.markdown("""帕尔默群岛企鹅数据集是用于数据探索和机器学习入门的优秀数据集，由Gorman等收集并发布。
该数据集包含344条观测记录，涵盖3种南极企鹅：**阿德利企鹅**、**巴布亚企鹅**和**帽带企鹅**，记录了它们的栖息岛屿、性别、身体测量数据等信息。""")
    st.header('三种企鹅的卡通图像')
    # 图片路径若不存在可注释
    st.image('images/penguins.png')

elif page == "预测分类页面":
    st.header("预测企鹅分类")
    st.markdown("基于帕尔默群岛企鹅数据集的随机森林模型，输入以下6项信息即可预测企鹅物种！")
    
    # 列布局
    col_form, col, col_logo = st.columns([3, 1, 2])
    
    with col_form:
        # 表单输入（优化：增加默认值，岛屿选项适配中文CSV）
        with st.form('user_inputs'):
            # 修复4：岛屿选项与CSV一致（中文岛屿名）
            island = st.selectbox('企鹅栖息的岛屿', options=['托尔森岛', '比斯科群岛', '德里姆岛'])
            sex = st.selectbox('性别', options=['雄性', '雌性', 'UNKNOWN'])  # 包含UNKNOWN，匹配数据预处理
            # 数值输入增加默认值和合理范围，提升体验
            bill_length = st.number_input('喙的长度（毫米）', min_value=10.0, max_value=60.0, value=38.0)
            bill_depth = st.number_input('喙的深度（毫米）', min_value=10.0, max_value=30.0, value=17.0)
            flipper_length = st.number_input('翅膀的长度（毫米）', min_value=150.0, max_value=250.0, value=190.0)
            body_mass = st.number_input('身体质量（克）', min_value=2500.0, max_value=7000.0, value=3800.0)
            submitted = st.form_submit_button('预测分类')
        
        # 加载模型（处理文件不存在的异常）
        try:
            model, encoder, feature_names, species_list = load_and_train_model('penguins-chinese.csv')
        except FileNotFoundError:
            st.error("❌ 未找到penguins-chinese.csv文件，请将CSV文件放在代码同级目录！")
            st.stop()
        
        # 预测逻辑
        if submitted:
            # 预处理用户输入（参数数量与函数定义一致）
            input_data = preprocess_user_input(island, sex, bill_length, bill_depth, flipper_length, body_mass, encoder)
            
            # 补全特征（防止编码后特征数不匹配）
            for col in feature_names:
                if col not in input_data.columns:
                    input_data[col] = 0
            input_data = input_data[feature_names]
            
            # 预测并显示结果
            predict_result = model.predict(input_data)[0]
            st.success(f'🎉 预测结果：该企鹅的物种是 **{predict_result}**')
    
    with col_logo:
        if not submitted:
            # 替换为本地图片路径，若无则注释
            st.image('images/right_logo.png', width=300)
            st.write("请输入信息并点击预测按钮")
        else:
            # 可根据预测结果显示对应企鹅图片，若无则注释
            st.image(f'images/{predict_result}.png', width=300)
            st.write(f"预测物种：{predict_result}")
