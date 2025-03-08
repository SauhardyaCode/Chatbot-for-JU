import { useRef } from 'react';
import send_icon from '../pictures/send.png'
import { MessageProp } from '../App'
import axios from 'axios';

interface Props {
    setChatHistory: React.Dispatch<React.SetStateAction<MessageProp[]>>;
    setThinking: React.Dispatch<React.SetStateAction<Boolean>>;
}

function ChatFooter({setChatHistory, setThinking}:Props) {
    const inputRef = useRef<HTMLInputElement>(null);

    const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const query = inputRef.current!.value.trim();
        // ! tells TypeScript => Don't worry I promise it's not null here
        inputRef.current!.value = "";
        if (!query) return;

        setChatHistory((prevHistory) => [...prevHistory,{role:"user", message: query}])
        setThinking(true);
        try{
            const response = await axios.post<{reply:string}>("/data/message", {message: query});
            setChatHistory((prevHistory) => [...prevHistory,{role:"model", message: response.data.reply}])
        } catch (error){
            console.error("Error Sending Message!", error)
        } finally {
            setThinking(false);
        }
    }

    return (
        <>
            <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
                <input ref={inputRef} type="text" id="message-input" placeholder="Ask Anything" autoComplete='off' required />
                <button id='send-message' type='submit'><img src={send_icon} alt="send" width="20em" /></button>
            </form>
        </>
    );
}

export default ChatFooter;