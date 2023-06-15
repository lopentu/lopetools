import { useState } from 'react';
import { Title, Container } from '@mantine/core';
import { LopeGptForm } from '../components/LopeGptForm/LopeGptForm';
import { ChatHistory, ChatMessageProps } from '../components/ChatHistory/ChatHistory';

export default function HomePage() {
  const [chatHistory, setChatHistory] = useState<ChatMessageProps[]>([]);

  return (
    <>
      <Container size="sm">
        <ChatHistory chatHistory={chatHistory} />
        <LopeGptForm chatHistory={chatHistory} setChatHistory={setChatHistory} />
      </Container>
    </>
  );
}
