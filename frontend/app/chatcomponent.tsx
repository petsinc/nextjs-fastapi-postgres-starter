"use client";
import { useEffect, useRef, useState } from "react";

type User = {
  userId: string;
};

type Content = {
  content: string;
  is_bot: boolean;
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export function ChatComponent({ userId }: User) {
  const [botMessage, setBotMessage] = useState();
  const [messages, setMessages] = useState<Content[]>([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  const handleInputChange = (event: any) => {
    setInput(event.target.value);
  };

  const handleSendMessage = async () => {
    if (input.trim() === "") return;
    setInput("");

    try {
      const response = await fetch(`${apiUrl}/messages/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: input, user: userId }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setBotMessage(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const Message = ({ content, is_bot }: Content) => {
    return (
      <div>
        <p
          style={{
            display: "flex",
            justifyContent: is_bot ? "flex-end" : "flex-start",
            padding: 10,
          }}
        >
          {content}
        </p>
      </div>
    );
  };

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };
  
  useEffect(() => {
    const getMessages = async () => {
      const response = await fetch(`${apiUrl}/messages/${userId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      setMessages(data);
    };
    console.log("function called");
    getMessages();
    scrollToBottom();
  }, [botMessage]);

  return (
    <>
      <div className="chat-container">
        <div
          style={{ width: "400px" }}
        >
          {messages.length > 0 &&
            messages.map((msg, index) => (
              <Message key={index} content={msg.content} is_bot={msg.is_bot} />
            ))}
              <div ref={messagesEndRef} />
        </div>
        <div
          style={{
            marginTop: 40,
            display: "flex",
            justifyContent: "space-between",
            background: "darkgray",
            padding: 10,
          }}
          className="input-container"
        >
          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={handleInputChange}
            style={{ width: "100%" }}
          />
          <button
            style={{ marginLeft: 30, padding: "0 10px", border: "2px solid" }}
            onClick={handleSendMessage}
          >
            Send
          </button>
        </div>
      </div>
    </>
  );
}
