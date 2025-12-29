import streamlit as st
import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

# ====================== 核心函数：训练模型 ======================
def train_insurance_model(data_path):
    """
    读取CSV数据并训练随机森林模型
    :param data_path: CSV文件路径
    :return: 训练好的模型 + 特征列名（用于预测时匹配格式）
    """
    # 1. 读取CSV数据（中文编码用gbk，若报错可换utf-8）
    try:
        df = pd.read_csv(data_path, encoding='gbk')
    except:
        df = pd.read_csv(data_path, encoding='utf-8')
    
    # 检查关键列是否存在（请根据你的CSV实际列名修改！）
    # 请确认：你的CSV列名是以下这些，若不是，替换成实际列名
    required_cols = ['年龄', '性别', 'BMI', '子女数量', '是否吸烟', '区域', '医疗费用']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"CSV文件缺少必要列：{missing_cols}，请检查列名！")
        return None, None
    
    # 2. 数据预处理（独热编码类别特征）
    X = df.drop('医疗费用', axis=1)  # 特征
    y = df['医疗费用']               # 目标变量（预测的医疗费用）
    
    # 对类别特征（性别、是否吸烟、区域）做独热编码
    categorical_cols = ['性别', '是否吸烟', '区域']
    encoder = OneHotEncoder(sparse_output=False, drop=None)
    encoded_cats = encoder.fit_transform(X[categorical_cols])
    encoded_df = pd.DataFrame(encoded_cats, columns=encoder.get_feature_names_out(categorical_cols))
    
    # 合并数值特征（年龄、BMI、子女数量）和编码后的类别特征
    numeric_cols = ['年龄', 'BMI', '子女数量']
    X_processed = pd.concat([X[numeric_cols].reset_index(drop=True), 
                             encoded_df.reset_index(drop=True)], axis=1)
    
    # 3. 训练随机森林模型
    rfr_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rfr_model.fit(X_processed, y)
    
    return rfr_model, X_processed.columns.tolist()

# ====================== 页面函数：简介 ======================
def introduce_page():
    st.write("# 欢迎使用医疗费用预测系统！")
    st.sidebar.success("单击 预测医疗费用")
    st.markdown("""
    # 医疗费用预测应用
    这个应用利用机器学习模型（随机森林），基于被保险人的个人信息预测医疗费用，为保险定价提供参考。
    
    ## 背景介绍
    - 开发目标：帮助保险公司合理定价保险产品，控制风险。
    - 模型算法：随机森林回归（基于insurance-chinese.csv数据训练）。
    
    ## 使用指南
    - 输入准确的被保险人信息，可得到更精准的费用预测。
    - 预测结果仅作参考，实际定价需结合更多业务因素。
    
    技术支持:email:: support@example.com
    """)

# ====================== 页面函数：预测 ======================
def predict_page():
    st.markdown("""
    ## 医疗费用预测
    输入被保险人的以下信息，点击「预测费用」即可得到医疗费用预测结果。
    """)
    
    # 1. 获取CSV文件路径（和脚本同目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'insurance-chinese.csv')
    
    # 检查CSV文件是否存在
    if not os.path.exists(csv_path):
        st.error(f"找不到数据源文件：{csv_path}，请确认文件在脚本同目录下！")
        return
    
    # 2. 训练模型（每次预测前自动训练，无需单独保存.pkl）
    rfr_model, feature_names = train_insurance_model(csv_path)
    if rfr_model is None:
        return  # 若训练失败，直接返回
    
    # 3. 用户输入表单
    with st.form('user_inputs'):
        age = st.number_input('年龄', min_value=0, max_value=120, value=30)
        sex = st.radio('性别', options=['男性', '女性'])
        bmi = st.number_input('BMI值', min_value=0.0, max_value=100.0, value=24.0, step=0.1)
        children = st.number_input("子女数量", step=1, min_value=0, max_value=10, value=0)
        smoke = st.radio("是否吸烟", ("是", "否"))
        region = st.selectbox('所在区域', ('东南部', '西南部', '东北部', '西北部'))
        submitted = st.form_submit_button('预测费用')
    
    # 4. 提交后处理预测逻辑
    if submitted:
        # 初始化独热编码后的特征值（和训练时格式一致）
        feature_values = {
            '年龄': age,
            'BMI': bmi,
            '子女数量': children,
            '性别_女性': 1 if sex == '女性' else 0,
            '性别_男性': 1 if sex == '男性' else 0,
            '是否吸烟_否': 1 if smoke == '否' else 0,
            '是否吸烟_是': 1 if smoke == '是' else 0,
            '区域_东北部': 1 if region == '东北部' else 0,
            '区域_东南部': 1 if region == '东南部' else 0,
            '区域_西北部': 1 if region == '西北部' else 0,
            '区域_西南部': 1 if region == '西南部' else 0
        }
        
        # 按训练时的特征顺序组装数据（关键：顺序必须一致）
        format_data = [feature_values[col] for col in feature_names]
        
        # 转为DataFrame（匹配模型输入格式）
        format_data_df = pd.DataFrame([format_data], columns=feature_names)
        
        # 预测并输出结果
        predict_result = rfr_model.predict(format_data_df)[0]
        st.success(f'✅ 预测该客户的医疗费用为：{round(predict_result, 2)} 元')
        st.write("技术支持:email:: support@example.com")

# ====================== 主程序 ======================
# 设置页面配置
st.set_page_config(
    page_title="医疗费用预测",
    page_icon="🏥",
    layout="wide"
)

# 侧边栏导航
nav = st.sidebar.radio("导航菜单", ["简介", "预测医疗费用"])

# 根据导航选择展示对应页面
if nav == "简介":
    introduce_page()
else:
    predict_page()
