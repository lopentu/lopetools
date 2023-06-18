import { useState } from 'react';
import { Title, Container } from '@mantine/core';
import { LopeGptForm } from '../components/LopeGptForm/LopeGptForm';
import { ChatHistory, ChatMessageProps } from '../components/ChatHistory/ChatHistory';
import { ColorSchemeCounterContext } from '../components/ColorSchemeToggle/ColorSchemeCounterContext';

export default function HomePage() {
  const [chatHistory, setChatHistory] = useState<ChatMessageProps[]>([]);

  return (
    <>
      <Container size="sm">
        <ChatHistory chatHistory={chatHistory} setChatHistory={setChatHistory} />
        <LopeGptForm chatHistory={chatHistory} setChatHistory={setChatHistory} />
      </Container>
    </>
  );
}
