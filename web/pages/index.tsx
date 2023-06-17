import { useState } from 'react';
import { Title, Container } from '@mantine/core';
import { LopeGptForm } from '../components/LopeGptForm/LopeGptForm';
import { ChatHistory, ChatMessageProps } from '../components/ChatHistory/ChatHistory';

export default function HomePage() {
  // let ch = [
  //   {'role': 'human', 'text': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', 'key': 0},
  //   {'role': 'ai', 'text': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', 'key': 1}
  // ]
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
