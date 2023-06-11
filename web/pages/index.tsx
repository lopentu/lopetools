import { Title, Container } from '@mantine/core';
import { LopeGptForm } from '../components/LopeGptForm/LopeGptForm';
import { ChatHistory } from '../components/ChatHistory/ChatHistory';

export default function HomePage() {
  return (
    <>
      <Container size="sm">
        <Title order={1}>LopeGPT</Title>
        <ChatHistory />
        <LopeGptForm />
      </Container>
    </>
  );
}
