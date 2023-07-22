import { useContext } from 'react';
import { useViewportSize } from '@mantine/hooks';
import Image from 'next/image';
import { ScrollArea, Mark, Text, ThemeIcon, useMantineTheme, Flex } from '@mantine/core';

import { FaRobot, FaUser, FaUserNinja } from 'react-icons/fa';

import shukai from '../../public/images/shukai-horse.png';
import { ColorSchemeCounterContext } from '../ColorSchemeToggle/ColorSchemeCounterContext';

export type ChatMessageProps = {
  role: string;
  text: string | JSX.Element;
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
              backgroundColor:
                theme.colorScheme === 'dark' ? theme.colors.cyan[9] : theme.colors.cyan[3],
              padding: '0.5em',
              borderRadius: '10px',
            }}
            m="md"
            size="md"
            ta="end"
          >
            {text}
          </Text>
          <ThemeIcon variant="filled" color="cyan" size="lg" radius="xl">
            <FaUserNinja />
          </ThemeIcon>
        </Flex>
      ) : (
        <Flex justify="flex-start">
          <ThemeIcon variant="filled" color="pink" size="lg" radius="xl" mr="sm">
            <FaRobot />
          </ThemeIcon>
          <Text
            sx={{
              backgroundColor:
                theme.colorScheme === 'dark' ? theme.colors.pink[9] : theme.colors.pink[3],
              padding: '10px',
              borderRadius: '10px',
            }}
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

export function ChatHistory({
  chatHistory,
  setChatHistory,
}: {
  chatHistory: ChatMessageProps[];
  setChatHistory: React.Dispatch<React.SetStateAction<ChatMessageProps[]>>;
}) {
  const { height, width } = useViewportSize();
  const counter = useContext(ColorSchemeCounterContext);
  return (
    <>
      {counter !== 0 && counter % 5 === 0 && <Image src={shukai} fill={true} alt="shukai" />}
      <ScrollArea h={height / 1.75} type="auto">
        {chatHistory.map((message) => {
          return <ChatMessage role={message.role} text={message.text} key={message.key} />;
        })}
      </ScrollArea>
    </>
  );
}
