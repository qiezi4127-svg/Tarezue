import streamlit as st
from PIL import Image
import io

class ResumeGeneratorStreamlit:
    def __init__(self):
        st.set_page_config(page_title="个人简历生成器", layout="wide", page_icon="📄")
        self._setup_ui()
    
    def _setup_ui(self):
        st.title("个人简历生成器")
        
        # 创建两列布局
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("个人信息表单")
            
            # 创建表单
            self.name = st.text_input("姓名", key="name")
            self.job = st.text_input("职业", key="job")
            
            # 创建两列用于性别选择
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                self.gender = st.radio("性别", ["男", "女"], horizontal=True, key="gender")
            
            self.edu = st.text_input("学历", key="edu")
            self.phone = st.text_input("电话", key="phone")
            self.email = st.text_input("邮箱", key="email")
            self.birth = st.text_input("出生日期", key="birth")
            self.work_years = st.text_input("工作经验(年)", key="work_years")
            self.salary = st.text_input("期望薪资", key="salary")
            self.contact_year = st.text_input("期望联系时间", key="contact_year")
            self.language = st.text_input("语言能力", key="language")
            self.tags = st.text_input("专业技能Tag(逗号分隔)", key="tags")
            self.intro = st.text_area("个人简介", height=150, key="intro")
            
            # 头像上传
            self.avatar_file = st.file_uploader("上传头像", type=["png", "jpg", "jpeg"], key="avatar")
            self.avatar_image = None
            if self.avatar_file:
                img = Image.open(self.avatar_file)
                # 调整图片大小
                img = img.resize((100, 120))
                self.avatar_image = img
        
        with col2:
            st.header("简历实时预览")
            
            # 预览区域
            preview_container = st.container()
            with preview_container:
                # 使用列布局展示头像和基本信息
                col2_1, col2_2 = st.columns([1, 2])
                
                with col2_1:
                    if self.avatar_image:
                        st.image(self.avatar_image, width=100)
                    else:
                        st.info("暂无头像")
                
                with col2_2:
                    # 解析Tag
                    tags_list = [tag.strip() for tag in (self.tags or "").split(",") if tag.strip()]
                    tag_str = " | ".join(tags_list) if tags_list else "无"
                    
                    # 显示预览信息
                    st.markdown("### 基本信息")
                    st.markdown(f"**姓名**: {self.name or '未填写'}")
                    st.markdown(f"**性别**: {self.gender} | **学历**: {self.edu or '未填写'}")
                    st.markdown(f"**职业**: {self.job or '未填写'} | **工作经验**: {self.work_years or '0'}年")
                    st.markdown(f"**期望薪资**: {self.salary or '未填写'} | **期望联系时间**: {self.contact_year or '未填写'}")
                    st.markdown(f"**电话**: {self.phone or '未填写'} | **邮箱**: {self.email or '未填写'}")
                    st.markdown(f"**出生日期**: {self.birth or '未填写'} | **语言能力**: {self.language or '未填写'}")
                    
                    st.markdown("---")
                    
                    st.markdown("### 个人简介")
                    st.markdown(self.intro or "暂无简介")
                    
                    st.markdown("### 专业技能")
                    st.markdown(tag_str)
                

def main():
    app = ResumeGeneratorStreamlit()

if __name__ == "__main__":
    main()
