import { useViewportSize } from '@mantine/hooks';
import { ScrollArea, Mark, Text, ThemeIcon } from '@mantine/core';

import { FaRobot, FaUser, FaUserNinja } from 'react-icons/fa';

function ChatMessage({ role, message }: { role: string, message: string }) {
  return (
    <>
      {role === 'user' ?
        <Text
          m="md"
          size="md"
          ta="end"
        >
          <Mark
            p="xs"
            color='blue'
            sx={{ borderRadius: '10px' }}
          >{message}
          </Mark>
          <ThemeIcon
            variant="light"
            color="blue"
            size="lg"
            radius="xl"
            ml="sm"
          >
            <FaUserNinja />
          </ThemeIcon>
        </Text>
        :
        <Text
          m="md"
          size="md"
          ta="start"
        >
          <ThemeIcon 
            variant="light"
            color="red"
            size="lg"
            radius="xl"
            mr="sm"
          >
            <FaRobot />
          </ThemeIcon>
          <Mark
            p="xs"
            color='red'
            sx={{ borderRadius: '10px' }}
          >{message}
          </Mark>
        </Text>
      }
    </>
  )
}

export function ChatHistory() {
  const { height, width } = useViewportSize();
  let chatHistory = [
    { 'role': 'user', 'text': 'Hello', 'key': 1 },
    { 'role': 'bot', 'text': 'Hello', 'key': 2 },
    { 'role': 'user', 'text': 'Wat', 'key': 3 },
    { 'role': 'bot', 'text': 'Hello', 'key': 4 },
  ]
  return (
    <ScrollArea
      h={height / 2}
      type="auto"
    >
      {chatHistory.map((message) => {
        return <ChatMessage
          role={message.role}
          message={message.text}
          key={message.key} />
      })}
    </ScrollArea>
  )
}