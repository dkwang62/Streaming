import streamlit as st
import yt_dlp
import os


def download_mp3(youtube_url: str, output_path: str = "audio.mp3") -> str:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "temp_audio.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)

    base, _ = os.path.splitext(filename)
    mp3_file = base + ".mp3"

    return mp3_file


def main():
    st.title("YouTube to MP3 Converter")

    url = st.text_input(
        "Enter YouTube URL",
        "https://www.youtube.com/watch?v=xojJ8tiEJas",
    )

    if st.button("Convert to MP3"):
        if not url:
            st.warning("Please enter a URL")
            return

        with st.spinner("Downloading and converting..."):
            try:
                mp3_file = download_mp3(url)

                with open(mp3_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")

                with open(mp3_file, "rb") as f:
                    st.download_button(
                        label="Download MP3",
                        data=f,
                        file_name="audio.mp3",
                        mime="audio/mpeg",
                    )

            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
