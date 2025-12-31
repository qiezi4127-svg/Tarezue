import streamlit as st

# 定义视频数据：标题、集数、视频URL
video_data = {
    "视频1": {
        "title": "还珠格格第一部",
        "episode": "第1集",
        "url": "https://www.w3school.com.cn/example/html5/mov_bbb.mp4"
    },
    "视频2": {
        "title": "还珠格格第一部",
        "episode": "第2集",
        "url": "https://www.w3schools.com/html/movie.mp4"
    },
    "视频3": {
        "title": "还珠格格第一部",
        "episode": "第3集",
        "url": "https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/05/90/34884749005/34884749005-1-192.mp4?e=ig8euxZM2rNcNbNM7bdVhwdlhbKjhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&nbs=1&oi=771356656&platform=html5&trid=d9db3cc868514b7196482b01bcfc628h&mid=0&gen=playurlv3&os=cosovbv&og=ali&deadline=1766565426&uipk=5&upsig=8f4f5c6b22fb9b90574392b00fc3d407&uparams=e,nbs,oi,platform,trid,mid,gen,os,og,deadline,uipk&bvc=vod&nettype=0&bw=1976427&agrr=1&buvid=&build=0&dl=0&f=h_0_0&orderid=0,1"
    }
}

# 页面标题与布局
st.set_page_config(page_title="视频播放站", layout="wide")
st.markdown(f"<h1 style='text-align: center;'>{list(video_data.values())[0]['title']}</h1>", unsafe_allow_html=True)

# 选择视频（集数切换）
selected_video = st.selectbox(
    "选择集数",
    options=list(video_data.keys()),
    format_func=lambda x: video_data[x]["episode"],
    key="episode_selector",
    label_visibility="collapsed"
)

# 展示选中的视频
current_video = video_data[selected_video]
st.video(current_video["url"])

# 显示集数信息
st.markdown(f"<h3 style='text-align: center;'>{current_video['episode']}</h3>", unsafe_allow_html=True)
