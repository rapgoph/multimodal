import streamlit as st
import tempfile
import cv2
import os

def analyze_video(video_file):
    # Load the video using OpenCV
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(video_file.read())
        video_path = tmp_file.name

    # Open the video file with OpenCV
    video_capture = cv2.VideoCapture(video_path)

    if video_capture.isOpened():
        st.write("Analyzing video...")
        # Process each frame in the video
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            # Display the frame (optional for showing analysis in Streamlit)
            st.image(frame, channels="BGR")

        st.write("Analysis complete!")
    else:
        st.write("Error: Cannot open video file")

    video_capture.release()

def main():
    st.title("Temporary Video Upload and Analysis")

    # Upload a video file
    video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

    if video_file is not None:
        st.video(video_file)

        # Option to analyze the video
        if st.button("Analyze Video"):
            analyze_video(video_file)

if __name__ == '__main__':
    main()
