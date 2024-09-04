import streamlit as st
from fer import FER
import pandas as pd
from moviepy.editor import VideoFileClip
import tempfile

def main():
    st.title("Emotion Probability Detection")

    # Upload video file
    video_file = st.file_uploader("Upload your video file", type=["mp4", "mov", "avi"])

    if video_file is not None:
        # Display the uploaded video
        st.video(video_file)

        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(video_file.read())
            video_path = tmp_file.name

        # Button to start facial emotion recognition
        if st.button("Facial Emotion Recognition"):
            with st.spinner("Processing... Please wait."):
                # Process the video to get emotion probabilities
                emotions_df = process_video(video_path)

            # Display the emotion probabilities
            if emotions_df is not None:
                st.header("Emotion Probability Scores")
                st.dataframe(emotions_df)
                st.download_button(
                    label="Download Emotion Data as CSV",
                    data=emotions_df.to_csv(index=False),
                    file_name="emotion_probabilities.csv",
                    mime="text/csv",
                )

def process_video(video_path):
    # Load the video using MoviePy
    video_clip = VideoFileClip(video_path)

    # Initialize the face detection detector
    face_detector = FER(mtcnn=True)

    # Initialize DataFrame to store emotions and time
    emotions_data = []

    # Process each frame in the video
    for frame_number, frame in enumerate(video_clip.iter_frames()):
        # Calculate the time in seconds
        time_seconds = frame_number / video_clip.fps

        # Detect emotions in the frame
        result = face_detector.detect_emotions(frame)

        for face in result:
            emotions = face["emotions"]
            emotions["Time (s)"] = time_seconds  # Add time information to emotions
            emotions_data.append(emotions)

    # Create DataFrame from emotions data
    if emotions_data:
        emotions_df = pd.DataFrame(emotions_data)

        # Rearrange columns so that "Time (s)" is the first column
        columns = ["Time (s)"] + [col for col in emotions_df.columns if col != "Time (s)"]
        emotions_df = emotions_df[columns]

        return emotions_df
    else:
        st.error("No faces detected in the video.")
        return None

if __name__ == '__main__':
    main()
