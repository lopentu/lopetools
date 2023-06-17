import { useViewportSize } from '@mantine/hooks';
import { ScrollArea, Mark, Text, ThemeIcon, useMantineTheme, Group, Flex } from '@mantine/core';

import { FaRobot, FaUser, FaUserNinja } from 'react-icons/fa';

export type ChatMessageProps = {
  role: string;
  text: string;
  key: string;
};

function ChatMessage({ role, text: text }: ChatMessageProps) {
  const theme = useMantineTheme();
  return (
    <>
      {role === 'human' ? (
        <Flex justify="flex-end">
          <Text
            sx={{ 
              backgroundColor: theme.colorScheme === 'dark' ? theme.colors.blue[9] : theme.colors.blue[3], 
              padding: '0.5em', borderRadius: '10px' }}
            m="md"
            size="md"
            ta="end"
          >
            {text}
          </Text>
          <ThemeIcon variant="filled" color="blue" size="lg" radius="xl">
            <FaUserNinja />
          </ThemeIcon>
        </Flex>
      ) : (
        <Flex justify="flex-start">
          <ThemeIcon variant="filled" color="grape" size="lg" radius="xl" mr="sm">
            <FaRobot />
          </ThemeIcon>
          <Text
            sx={{ 
              backgroundColor: theme.colorScheme === 'dark'? theme.colors.grape[9] : theme.colors.grape[3], 
              padding: '10px', borderRadius: '10px' }}
            m="xs"
            size="md"
            ta="start"
          >
            {text}
          </Text>
        </Flex>
      )}
    </>
  );
}

export function ChatHistory({ chatHistory }: { chatHistory: ChatMessageProps[] }) {
  const { height, width } = useViewportSize();
  return (
    <ScrollArea mih={height / 2} type="auto">
      {chatHistory.map((message) => {
        return <ChatMessage role={message.role} text={message.text} key={message.key} />;
      })}
    </ScrollArea>
  );
}
