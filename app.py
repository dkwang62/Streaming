import streamlit as st
import requests


def is_likely_direct_video_url(url: str) -> bool:
    url = url.lower()
    return any(ext in url for ext in [".mp4", ".webm", ".ogg", ".m3u8"])


def stream_remote_video(video_url: str) -> None:
    try:
        response = requests.get(video_url, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()
        if "video" not in content_type and "application/vnd.apple.mpegurl" not in content_type:
            st.error(
                f"This URL did not return video data. Content-Type was: {content_type or 'unknown'}"
            )
            return

        st.video(response.content)

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching video: {e}")


def main() -> None:
    st.set_page_config(page_title="Remote Video Player", layout="centered")
    st.title("Remote Video Player")

    st.write("Paste a direct video file URL, not a webpage URL.")

    default_url = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
    video_url = st.text_input("Direct video URL", value=default_url)

    if st.button("Play Video"):
        video_url = video_url.strip()

        if not video_url:
            st.warning("Please enter a URL.")
            return

        if not is_likely_direct_video_url(video_url):
            st.error("This does not look like a direct video URL. Use a direct .mp4 or similar media link.")
            return

        stream_remote_video(video_url)


if __name__ == "__main__":
    main()
