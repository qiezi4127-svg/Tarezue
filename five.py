import streamlit as st

# 定义歌曲数据，包含3首歌的信息：歌名、歌手、专辑图片URL、音频URL
songs = [
    {
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "album_cover": "https://ts2.tc.mm.bing.net/th/id/OIP-C.S0xfYxKcDrpRxxhC0epDXQHaHQ?cb=ucfimg2&ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3",
        "audio_url": "https://music.163.com/song/media/outer/url?id=5257138.mp3"
    },
    {
        "title": "Yesterday",
        "artist": "The Beatles",
        "album_cover": "https://pic.baike.soso.com/ugc/baikepic2/5506/20220331205707-2101910652_png_600_600_408620.jpg/300",
        "audio_url": "https://music.163.com/song/media/outer/url?id=22702681.mp3"
    },
    {
        "title": "Hotel California",
        "artist": "Eagles",
        "album_cover": "https://ts1.tc.mm.bing.net/th/id/OIP-C.-9kawyUK6x4Wdrv2lKzEVwAAAA?cb=ucfimg2&ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3",
        "audio_url": "https://music.163.com/song/media/outer/url?id=5257138.mp3"
    }
]

# 初始化会话状态，记录当前播放的歌曲索引
if "current_song_idx" not in st.session_state:
    st.session_state.current_song_idx = 0

# 获取当前歌曲信息
current_song = songs[st.session_state.current_song_idx]

# 页面标题
st.title("简易音乐播放器")

# 布局：专辑图片、歌曲信息、切换按钮
col1, col2 = st.columns([1, 3])
with col1:
    st.image(current_song["album_cover"], width=200)
with col2:
    st.header(current_song["title"])
    st.subheader(f"歌手: {current_song['artist']}")
    # 上一首/下一首按钮
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("上一首"):
            if st.session_state.current_song_idx > 0:
                st.session_state.current_song_idx -= 1
            else:
                st.session_state.current_song_idx = len(songs) - 1  # 循环到最后一首
    with col_btn2:
        if st.button("下一首"):
            if st.session_state.current_song_idx < len(songs) - 1:
                st.session_state.current_song_idx += 1
            else:
                st.session_state.current_song_idx = 0  # 循环到第一首

# 播放当前音频
st.audio(current_song["audio_url"])