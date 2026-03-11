import streamlit as st
import requests

def stream_remote_video(url):
    """
    Fetches video content from a remote URL and serves it via Streamlit.
    This masks the original URL from the end user.
    """
    try:
        # stream=True is important for large files, though st.video reads bytes
        # For a true proxy, you'd typically stream chunks, but Streamlit's
        # st.video accepts a byte object or a file-like object.
        with requests.get(url, stream=True) as response:
            response.raise_for_status()

            # Read the content into memory
            # Note: Be cautious with very large files
            video_bytes = response.content

            # Display the video using the bytes
            st.video(video_bytes)

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching video: {e}")

st.title("Secure Video Proxy")

# Input for the hidden source URL
# In a real app, this would be hardcoded or fetched from a database
# For demonstration, we use a sample video URL.
DEFAULT_URL = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"

# You can hardcode your target URL here to hide it completely from the UI
target_url = st.text_input("Video Source URL", value=DEFAULT_URL)

if st.button("Play Video"):
    if target_url:
        st.write("Streaming content...")
        stream_remote_video(target_url)
