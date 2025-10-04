import streamlit as st
import yt_dlp
import os
import time

# Set download folder
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Page config
st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---- Sidebar ----
st.sidebar.image("https://i.imgur.com/OXxV8wN.png", width=150)  # optional logo
st.sidebar.header("Options")
st.sidebar.write("🎯 Simple, safe YouTube Downloader built with Streamlit & yt-dlp")

# ---- Title ----
st.title("🎥 YouTube Downloader")
st.markdown(
    """
    Paste a YouTube URL, choose Video or Audio, pick resolution for video, then click Download.
    """,
    unsafe_allow_html=True
)

# ---- Input Section ----
url = st.text_input("YouTube URL:")

col1, col2 = st.columns(2)
with col1:
    download_type = st.radio("Download type:", ("Video", "Audio (MP3)"))
with col2:
    resolution = st.selectbox("Resolution (video only):", ["best", "720p", "480p", "360p"])

st.markdown("---")

# ---- Download button ----
if st.button("⬇️ Download Now"):
    if not url:
        st.warning("⚠️ Please paste a YouTube URL.")
    else:
        with st.spinner("⏳ Downloading..."):
            # Set yt-dlp options
            ydl_opts = {
                "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
                }
            }

            if download_type == "Audio (MP3)":
                ydl_opts.update({
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                })
            else:
                if resolution == "best":
                    ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
                elif resolution == "720p":
                    ydl_opts["format"] = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/mp4"
                elif resolution == "480p":
                    ydl_opts["format"] = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/mp4"
                elif resolution == "360p":
                    ydl_opts["format"] = "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/mp4"

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    downloaded_file = ydl.prepare_filename(info)
                    if download_type == "Audio (MP3)":
                        downloaded_file = os.path.splitext(downloaded_file)[0] + ".mp3"

                    # wait for file
                    tries = 0
                    while not os.path.exists(downloaded_file) and tries < 10:
                        time.sleep(0.3)
                        tries += 1

                    if not os.path.exists(downloaded_file):
                        st.error("❌ Download finished but file not found.")
                    else:
                        st.success("✅ Download complete!")
                        st.write("File saved at:", downloaded_file)
                        mime_type = "audio/mpeg" if download_type == "Audio (MP3)" else "video/mp4"
                        with open(downloaded_file, "rb") as f:
                            st.download_button(
                                label="💾 Click to download to your computer",
                                data=f,
                                file_name=os.path.basename(downloaded_file),
                                mime=mime_type
                            )
            except Exception as e:
                st.error(f"❌ Error: {e}")
