import ChatHeader from "./components/ChatHeader";
import ChatBody from "./components/ChatBody";
import ChatFooter from "./components/ChatFooter";
import { useEffect, useState } from "react";
import axios from "axios";

export interface MessageProp {
  role: "user" | "model" | "system";
  message: string;
}

function App() {
  const [starting, setStarting] = useState<Boolean>(false)
  const [thinking, setThinking] = useState<Boolean>(false)
  const [chatHistory, setChatHistory] = useState<MessageProp[]>([]);

  useEffect(() => {
    const refresh = async () => {
      setStarting(true);
      try {
        const response = await axios.post<{ reply: string }>("/data/message", { message: "${Restart_Assistant}" });
        console.log(response.data.reply)
        setChatHistory(() => [{ role: "model", message: response.data.reply }]);
      } catch (error) {
        console.error("Error Restarting ChatBot!", error);
      } finally {
        setStarting(false)
      }
    }
    refresh();
  }, [])

  useEffect(() => {
    const handleBeforeUnload = (event: BeforeUnloadEvent) => {
      event.preventDefault();
    };

    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, []);


  return (
    <div id="chat-bot-container">
      <div className="chat-header">
        <ChatHeader />
      </div>
      <div className="chat-body">
        <ChatBody chatHistory={chatHistory} thinking={thinking} starting={starting} />
      </div>
      <div className="chat-footer">
        <ChatFooter setChatHistory={setChatHistory} setThinking={setThinking} />
      </div>
    </div>
  );
}

export default App;