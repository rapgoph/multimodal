#import streamlit as st
#import tempfile
#import os

#def main():
 #   st.title("Welcome! This is the Multimodal Emotion Recognition App! - Raphael and 명환!")

    # File uploader allows users to upload a video file
  #  video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

   # if video_file is not None:
        # Display the uploaded video
    #    st.video(video_file)

        # Save the uploaded video temporarily
     #   with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
      #      tmp_file.write(video_file.read())
       #     tmp_file_path = tmp_file.name

        # Show some basic info about the video file
        #st.write("### Video Information")
        #st.write(f"**Filename:** {video_file.name}")
        #st.write(f"**File Size:** {os.path.getsize(tmp_file_path)} bytes")

        # Here you could add more analysis or processing on the video file

#if __name__ == '__main__':
 #   main()

import streamlit as st
import whisper_timestamped as whisper
import tempfile
import pandas as pd
import cv2
import os
import base64

def main():
    st.title("Video Transcription App")

    # Option to upload or record a video
    st.header("Upload or Record a Video")
    option = st.radio("Choose an option:", ('Upload Video', 'Record Video'))

    video_file = None
    if option == 'Upload Video':
        video_file = st.file_uploader("Upload your video file", type=["mp4", "mov", "avi"])
    elif option == 'Record Video':
        video_file = record_video_ui()

    if video_file is not None:
        # Display the uploaded or recorded video
        st.video(video_file)

        # Temporary save to disk
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(video_file.read())
            tmp_video_path = tmp_file.name

        # Transcribe the video using Whisper
        st.header("Transcription Results")
        transcribe_video(tmp_video_path)

def record_video_ui():
    st.markdown("""
    <script>
        const startButton = document.createElement("button");
        startButton.textContent = "Start Recording";
        startButton.style.background = "orange";
        startButton.style.color = "white";
        const stopButton = document.createElement("button");
        stopButton.textContent = "Stop Recording";
        stopButton.style.background = "red";
        stopButton.style.color = "white";

        const videoElement = document.createElement("video");
        videoElement.autoplay = true;
        videoElement.style.display = "block";

        let stream = null;
        let recorder = null;
        let recordedChunks = [];

        async function startRecording() {
            stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            recorder = new MediaRecorder(stream, { mimeType: "video/webm" });

            recorder.ondataavailable = (event) => recordedChunks.push(event.data);
            recorder.start();
        }

        function stopRecording() {
            recorder.stop();
            stream.getTracks().forEach(track => track.stop());

            const videoBlob = new Blob(recordedChunks, { type: "video/webm" });
            const reader = new FileReader();
            reader.readAsDataURL(videoBlob);
            reader.onloadend = () => {
                const base64String = reader.result.split(",")[1];
                const videoElement = document.createElement("video");
                videoElement.src = reader.result;
                videoElement.controls = true;
                document.body.appendChild(videoElement);
                window.parent.postMessage({ video: base64String }, "*");
            };
        }

        startButton.onclick = startRecording;
        stopButton.onclick = stopRecording;
        document.body.appendChild(startButton);
        document.body.appendChild(stopButton);
    </script>
    """, unsafe_allow_html=True)

    video_data = st.experimental_get_query_params().get('video')
    if video_data:
        video_bytes = base64.b64decode(video_data[0])
        return video_bytes

    return None

def transcribe_video(video_path):
    audio = whisper.load_audio(video_path)
    model = whisper.load_model("medium", device="cpu")
    result = whisper.transcribe(model, audio)

    # Prepare data for display
    word_texts, word_starts, word_ends, word_confidences = [], [], [], []
    for segment in result['segments']:
        for word in segment['words']:
            word_texts.append(word['text'])
            word_starts.append(word['start'])
            word_ends.append(word['end'])
            word_confidences.append(word['confidence'])

    segments_data = [{'text': seg['text'], 'start': seg['start'], 'end': seg['end'], 'confidence': seg['confidence']}
                     for seg in result['segments']]

    segments_df = pd.DataFrame(segments_data)
    words_df = pd.DataFrame({'text': word_texts, 'start': word_starts, 'end': word_ends, 'confidence': word_confidences})

    # Display the transcription results
    display_transcription(segments_df, words_df)

def display_transcription(segments_df, words_df):
    st.subheader("Segments")
    st.write(segments_df)

    st.subheader("Words")
    st.write(words_df)

    # Option to download results
    st.subheader("Download Transcription")
    excel_file = st.download_button(label="Download Transcription as Excel", data=convert_df_to_excel(segments_df, words_df),
                                    file_name="transcription.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def convert_df_to_excel(segments_df, words_df):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        with pd.ExcelWriter(tmp_file.name) as writer:
            segments_df.to_excel(writer, sheet_name='Segments', index=False)
            words_df.to_excel(writer, sheet_name='Words', index=False)
        tmp_file.seek(0)
        return tmp_file.read()

if __name__ == '__main__':
    main()
