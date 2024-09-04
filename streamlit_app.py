import streamlit as st
import whisper_timestamped as whisper
import tempfile
import pandas as pd
import subprocess

def main():
    # Application Header
    st.title("Business & Process Analytics Lab: Multimodal Emotion Recognition System")

    # Section: Video Upload
    st.header("Upload a Video for Transcription")
    video_file = st.file_uploader("Upload your video file", type=["mp4", "mov", "avi"])

    if video_file is not None:
        # Display the uploaded video
        st.video(video_file)
        
        # Save the uploaded video temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(video_file.read())
            tmp_video_path = tmp_file.name
        
        # Transcribe the video using Whisper
        st.header("Transcription Results")
        transcribe_video(tmp_video_path)

def transcribe_video(video_path):
    try:
        # Load the audio from the video
        audio = whisper.load_audio(video_path)
        
        # Load the Whisper model
        model = whisper.load_model("medium", device="cpu")
        
        # Transcribe the video/audio
        result = whisper.transcribe(model, audio)
        
        # Prepare data for display
        segments_data = [{'text': seg['text'], 'start': seg['start'], 'end': seg['end'], 'confidence': seg['confidence']}
                         for seg in result['segments']]

        segments_df = pd.DataFrame(segments_data)
        st.write(segments_df)

        # Option to download transcription as Excel
        excel_file = convert_df_to_excel(segments_df)
        st.download_button(label="Download Transcription as Excel", data=excel_file, file_name="transcription.xlsx")
    except subprocess.CalledProcessError as e:
        st.error("An error occurred while processing the audio. Please ensure FFmpeg is installed and accessible.")
        st.error(f"Error details: {e}")

def convert_df_to_excel(segments_df):
    # Convert dataframe to Excel format for download
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        with pd.ExcelWriter(tmp_file.name) as writer:
            segments_df.to_excel(writer, sheet_name='Segments', index=False)
        tmp_file.seek(0)
        return tmp_file.read()

if __name__ == '__main__':
    main()
