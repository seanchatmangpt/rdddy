"use client";
import React, { useState } from "react";
import "regenerator-runtime/runtime";

import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

import AceEditor from "react-ace"; // Import AceEditor

import "brace/mode/python"; // Load Python language mode
import "brace/theme/monokai"; // Load a theme (optional)

const Dictaphone = () => {
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  // We declare state variable to save the response from server
  const [serverResponse, setServerResponse] = useState(null);
  const [pythonCode, setPythonCode] = useState(null); // State for the code editor

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser does not support speech recognition.</span>;
  }

  const sendTranscript = async () => {
    const response = await fetch("/receive_transcript", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ transcript }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data.message); // Log the response from your server

      // Set the server response to the state variable
      console.log("Setting message", data.message);
      setServerResponse(data.message);
      setPythonCode(data.message);
    } else {
      console.error("Error sending transcript");
    }
  };

  return (
    <div>
      <p>Microphone: {listening ? "on" : "off"}</p>
      <button onClick={SpeechRecognition.startListening}>Start</button>
      <button onClick={SpeechRecognition.stopListening}>Stop</button>
      <button onClick={resetTranscript}>Reset</button>
      <button onClick={sendTranscript}>Send Transcript</button>
      <p>{transcript}</p>

      {/* Display the server response */}
      {/*{serverResponse && <p>Server response: {serverResponse}</p>}*/}
      {pythonCode && (
        <AceEditor
          mode="python"
          theme="monokai"
          onChange={(newCode) => setPythonCode(newCode)} // Update state on changes
          value={pythonCode}
          name="python-code-editor"
          editorProps={{ $blockScrolling: true }}
          width="100%" // Adjust the width as needed
        />
      )}
    </div>
  );
};
export default Dictaphone;
