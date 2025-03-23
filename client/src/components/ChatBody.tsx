import BotIcon from './BotIcon';
import { MessageProp } from '../App';
import { useEffect, useRef } from 'react';

interface Props {
    chatHistory: MessageProp[];
    thinking: Boolean;
    starting: Boolean;
}

function ChatBody({ chatHistory, thinking, starting }: Props) {
    const lastMsgRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        console.log("Chat History:", chatHistory);
        if (lastMsgRef.current){
            lastMsgRef.current.scrollIntoView({behavior: "smooth"})
        }
    }, [chatHistory]);

    return (
        <>
            {chatHistory.map((msg, index) => {
                if (msg.role != "system") {
                    return (
                        <div key={index} className={`message ${msg.role}-message`}>
                            {msg.role == "model" && <>
                                <BotIcon size={55} /><p dangerouslySetInnerHTML={{ __html: msg.message }} className="message-text"></p>
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
            <div ref={lastMsgRef} className="scroll-ref"></div>
        </>
    );
}

export default ChatBody