import { useViewportSize } from '@mantine/hooks';
import { ScrollArea, Mark, Text, ThemeIcon } from '@mantine/core';

import { FaRobot, FaUser, FaUserNinja } from 'react-icons/fa';

export type ChatMessageProps = {
  role: string,
  text: string,
  key: string,
}


function ChatMessage({ role, text: text }: ChatMessageProps) {
  return (
    <>
      {role === 'User' ?
        <Text
          m="md"
          size="md"
          ta="end"
        >
          <Mark
            p="xs"
            color='blue'
            sx={{ borderRadius: '10px' }}
          >{text}
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
          >{text}
          </Mark>
        </Text>
      }
    </>
  )
}

export function ChatHistory({ chatHistory }: { chatHistory: ChatMessageProps[] }) {
  const { height, width } = useViewportSize();
  return (
    <ScrollArea
      h={height / 2}
      type="auto"
    >
      {chatHistory.map((message) => {
        return <ChatMessage
          role={message.role}
          text={message.text}
          key={message.key} />
      })}
    </ScrollArea>
  )
}