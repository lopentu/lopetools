import { useState } from 'react';
import { Title, Container } from '@mantine/core';
import { LopeGptForm } from '../components/LopeGptForm/LopeGptForm';
import { ChatHistory, ChatMessageProps } from '../components/ChatHistory/ChatHistory';

export default function HomePage() {
  const [chatHistory, setChatHistory] = useState<ChatMessageProps[]>([])
  const [openaiApiKey, setOpenaiApiKey] = useState<string>('')

  return (
    <>
      <Container size="sm">
        <Title order={1}>LopeGPT</Title>
        <ChatHistory chatHistory={chatHistory} />
        <LopeGptForm openaiApiKey={openaiApiKey} chatHistory={chatHistory} setChatHistory={setChatHistory} />
      </Container>
    </>
  );
}