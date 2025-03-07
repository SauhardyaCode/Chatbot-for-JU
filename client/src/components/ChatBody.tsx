import BotIcon from './BotIcon';
import { MessageProp } from '../App';
import { useEffect } from 'react';

interface Props {
    chatHistory: MessageProp[];
}

function ChatBody({chatHistory}: Props) {
    useEffect(() => {
        console.log("Chat History:", chatHistory);
      }, [chatHistory]);

    return (
        <>
            {chatHistory.map((msg, index) => {
                return(
                <div key={index} className={`message ${msg.role}-message`}>
                    {msg.role=="bot" && <BotIcon size={50}/>}
                    <p className="message-text">{msg.message}</p>
                </div>);
            }
            )}
        </>
    );
}

export default ChatBody