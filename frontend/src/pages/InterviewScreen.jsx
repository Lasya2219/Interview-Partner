import { useState, useEffect, useRef } from "react";
import api from "../services/api";
import ReactMarkdown from "react-markdown";
import "./InterviewScreen.css";

function InterviewScreen({
  sessionId,
  question,
  duration,
  company
}) {

  const [currentQuestion, setCurrentQuestion] = useState(question);
  const [isFollowup, setIsFollowup] = useState(false);
  const [answer, setAnswer] = useState("");
  const [report, setReport] = useState("");
  const [timeLeft, setTimeLeft] = useState(Number(duration) * 60);
  const [isRecording, setIsRecording] = useState(false);
  const hasSpoken = useRef(false);
  const recognitionRef = useRef(null);

  const handleEndInterview = async () => {

      try {
        if (recognitionRef.current) {
          recognitionRef.current.stop();
        }

        const response = await api.post(
        "/end-interview",
        {
            session_id: sessionId
        }
        );

        setReport(response.data.report);
      
      } catch (error) {
        alert("Error ending interview. Please try again.");
        console.error("Error ending interview:", error);
      }
    };

    const startListening = () => {
        if (
          !window.SpeechRecognition &&
          !window.webkitSpeechRecognition
        ) {
          alert("Speech recognition is not supported in this browser.");
          return;
        }

        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        const recognition =
            new SpeechRecognition();

        recognitionRef.current = recognition;

        recognition.lang = "en-US";

        recognition.onerror = (event) => {
          if (event.error !== "aborted") {
            alert("Unable to access microphone.");
          }
          setIsRecording(false);
        };

        recognition.onresult = (event) => {

            setAnswer(
            event.results[0][0].transcript
            );

        };

        recognition.onend = () => {
          setIsRecording(false);
          recognitionRef.current = null;
        };

        recognition.start();
        setIsRecording(true);
    };

    const stopListening = () => {
        if (recognitionRef.current) {
          recognitionRef.current.stop();
        }
        setIsRecording(false);
    };

    const speakText = (text) => {

        const speech =
            new SpeechSynthesisUtterance(text);

        speech.lang = "en-US";

        window.speechSynthesis.speak(speech);
    };

    useEffect(() => {

        if (!hasSpoken.current) {
            speakText(currentQuestion);
            hasSpoken.current = true;
        }

    }, []);

  useEffect(() => {

    const timer = setInterval(() => {

      setTimeLeft((prev) => {

        if (prev <= 1) {

          clearInterval(timer);

          handleEndInterview();

          return 0;
        }

        return prev - 1;
      });

    }, 1000);

    return () => clearInterval(timer);

  }, []);

  useEffect(() => {
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const handleSubmit = async () => {

    if (!answer.trim()) {
        alert("Please provide an answer.");
        return;
    }
    
    try {

        const response = await api.post(
          "/answer",
          {
            session_id: sessionId,
            question: currentQuestion,
            answer: answer,
            company: company
          }
        );

        const nextQuestion = response.data.question || response.data.followup;
        setCurrentQuestion(nextQuestion);
        setIsFollowup(Boolean(response.data.is_followup));
        speakText(nextQuestion);
        setAnswer("");
    } catch (error) {
        alert("Error submitting answer. Please try again.");
        console.error("Error submitting answer:", error);
      }
    };

  if (report) {
    return (
      <div className="report-container">
        <h1>Interview Report</h1>
        <ReactMarkdown>
            {report}
        </ReactMarkdown>
      </div>
    );
  }

  return (
    <div>

      <h3>
        Time Left: {timeLeft}s
      </h3>

      <h2>{isFollowup ? "Follow-up Question" : "Question"}</h2>

      <p>{currentQuestion}</p>

      <textarea className="answer-textbox"
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />

      <button
        className={isRecording ? "recording-button" : ""}
        onClick={isRecording ? stopListening : startListening}
      >
        {isRecording ? "Stop Recording" : "🎤 Speak Answer"}
      </button>

      <br />

      

      <br />

      <button onClick={handleSubmit}>
        Submit Answer
      </button>

        <br />

      <button onClick={handleEndInterview}>
        End Interview
      </button>

    </div>
  );
}

export default InterviewScreen;
