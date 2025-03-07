import ChatHeader from "./components/ChatHeader";
import ChatBody from "./components/ChatBody";
import ChatFooter from "./components/ChatFooter";
import { useState } from "react";

export interface MessageProp{
  role: "user" | "bot";
  message: string;
}

function App(){
  const [chatHistory, setChatHistory] = useState<MessageProp[]>([{role:"bot",message:"Hey there! How can I help you today?"}]);

  return(
    <div id="chat-bot-container">
      <div className="chat-header">
        <ChatHeader/>
      </div>
      <div className="chat-body">
        <ChatBody chatHistory={chatHistory} />
      </div>
      <div className="chat-footer">
        <ChatFooter setChatHistory={setChatHistory} />
      </div>
    </div>
  );
}

export default App;