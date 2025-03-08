import BotIcon from './BotIcon';
import { MessageProp } from '../App';
import { useEffect } from 'react';

interface Props {
    chatHistory: MessageProp[];
    thinking: Boolean;
    starting: Boolean;
}

function ChatBody({ chatHistory, thinking, starting }: Props) {
    useEffect(() => {
        console.log("Chat History:", chatHistory);
    }, [chatHistory]);

    return (
        <>
            {chatHistory.map((msg, index) => {
                if (msg.role != "system") {
                    return (
                        <div key={index} className={`message ${msg.role}-message`}>
                            {msg.role == "model" && <>
                                <BotIcon size={50} /><p dangerouslySetInnerHTML={{ __html: msg.message }} className="message-text"></p>
                            </>}
                            {msg.role == "user" && <p className="message-text">{msg.message}</p>}

                        </div>
                    );
                }
            }
            )}
            {
                (thinking || starting) && <div className='loading-message message message-text'>
                    <BotIcon size={50} />
                    {thinking && <p>Thinking...</p>}
                    {starting && <p>Starting...</p>}
                </div>
            }
        </>
    );
}

export default ChatBody