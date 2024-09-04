import streamlit as st
from webcam import webcam
import whisper_timestamped as whisper
import tempfile
import pandas as pd

def main():
    st.title("Video/Image Transcription App")

    # Option to upload a video or capture an image
    st.header("Upload a video or capture an image")
    option = st.radio("Choose an option:", ('Upload Video', 'Capture Image'))

    if option == 'Upload Video':
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

    elif option == 'Capture Image':
        captured_image = webcam()
        if captured_image is None:
            st.write("Waiting for capture...")
        else:
            st.write("Got an image from the webcam:")
            st.image(captured_image)
            # Save image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                captured_image.save(tmp_file.name)
                tmp_image_path = tmp_file.name
            # You can now process this image or display it further

def transcribe_video(video_path):
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

def convert_df_to_excel(segments_df):
    # Convert dataframe to Excel format for download
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        with pd.ExcelWriter(tmp_file.name) as writer:
            segments_df.to_excel(writer, sheet_name='Segments', index=False)
        tmp_file.seek(0)
        return tmp_file.read()

if __name__ == '__main__':
    main()
