import streamlit as st
import requests


def stream_remote_video(video_url: str) -> None:
    """
    Fetch a video from a direct, authorized video URL and display it in Streamlit.
    """
    try:
        response = requests.get(video_url, timeout=30)
        response.raise_for_status()
        st.video(response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching video: {e}")


def main() -> None:
    st.set_page_config(page_title="Remote Video Player", layout="centered")
    st.title("Remote Video Player")

    st.write("Enter a direct video URL you are authorized to use.")

    default_url = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
    video_url = st.text_input("Direct video URL", value=default_url)

    if st.button("Play Video"):
        if not video_url.strip():
            st.warning("Please enter a video URL.")
            return
        stream_remote_video(video_url.strip())


if __name__ == "__main__":
    main()
