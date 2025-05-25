import React, { useRef, useState } from "react";
import axios from "axios";

function App() {
    const [transcription, setTranscription] = useState("");
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);

            mediaRecorderRef.current.ondataavailable = (event) => {
                audioChunksRef.current.push(event.data);
            };

            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
                const formData = new FormData();
                formData.append("file", audioBlob, "temp.webm");

                try {
                    const response = await axios.post("http://localhost:5000/transcribe", formData, {
                        headers: { "Content-Type": "multipart/form-data" },
                    });
                    setTranscription(response.data.transcription);
                } catch (error) {
                    console.error("Error transcribing audio:", error);
                }

                audioChunksRef.current = [];
            };

            mediaRecorderRef.current.start();
            console.log("Recording started...");

            // Stop recording automatically after 3 seconds
            setTimeout(() => {
                stopRecording();
            }, 2000);

        } catch (error) {
            console.error("Error accessing microphone:", error);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
            mediaRecorderRef.current.stop();
            console.log("Recording stopped.");
        }
    };

    return (
        <div>
            <h1>Audio Transcription App</h1>
            <button onClick={startRecording}>Start Recording</button>
            <p>Transcription: {transcription}</p>
        </div>
    );
}

export default App;
