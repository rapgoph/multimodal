import streamlit as st
import tempfile
import os

def main():
    st.title("Welcome! This is the Multimodal Emotion Recognition App! - Raphael and 명환!")

    # File uploader allows users to upload a video file
    video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

    if video_file is not None:
        # Display the uploaded video
        st.video(video_file)

        # Save the uploaded video temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(video_file.read())
            tmp_file_path = tmp_file.name

        # Show some basic info about the video file
        st.write("### Video Information")
        st.write(f"**Filename:** {video_file.name}")
        st.write(f"**File Size:** {os.path.getsize(tmp_file_path)} bytes")

        # Here you could add more analysis or processing on the video file

if __name__ == '__main__':
    main()
