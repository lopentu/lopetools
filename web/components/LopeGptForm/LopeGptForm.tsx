import {
  Flex,
  Textarea,
  Checkbox,
  Button,
  Group,
  Box,
  PasswordInput,
  Loader,
  ActionIcon,
} from '@mantine/core';
import { useForm, hasLength } from '@mantine/form';
import React, { useEffect, useState } from 'react';
import { GrPowerReset } from 'react-icons/gr';

import { ChatMessageProps } from '../ChatHistory/ChatHistory';

export function LopeGptForm({
  chatHistory,
  setChatHistory,
}: {
  chatHistory: ChatMessageProps[];
  setChatHistory: React.Dispatch<React.SetStateAction<ChatMessageProps[]>>;
}) {
  const [rawHistory, setRawHistory] = useState([]);
  const [openaiApiKey, setOpenaiApiKey] = useState<string>('');

  function call_api(text: string, useCwnTools: boolean, useAsbcTools: boolean) {
    let payload = {
      text: text,
      use_cwn: useCwnTools,
      use_asbc: useAsbcTools,
      messages: rawHistory,
      openaiApiKey: openaiApiKey,
    };
    console.log(payload);
    fetch('http://127.0.0.1:8003/agent/', {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((responseData) => {
        setRawHistory(responseData['raw']);
        setChatHistory(responseData['formatted']);
        console.log(responseData);
      })
      .catch((error) => {
        console.error(error);
      });
  }
  const form = useForm({
    initialValues: {
      userInput: '',
      useCwnTools: true,
      useAsbcTools: true,
      openaiApiKey: openaiApiKey,
    },
    // validate: {
    //   openaiApiKey: hasLength(51, 'OpenAI API Key must be 51 characters long'),
    // },
  });

  return (
    <Box mx="auto">
      <form
        onSubmit={form.onSubmit((values) => {
          let role = 'human';
          let text = values.userInput;
          let idx = chatHistory.length + 1;
          // let time = new Date().getTime();
          let key = `${role}-${text}-${idx}`;
          console.log(values);
          setChatHistory([
            ...chatHistory,
            { role, text, key },
            {
              role: 'ai',
              text: <Loader variant="dots" size="sm" color="white" />,
              key: `${role}-${text}-${idx + 1}`,
            },
          ]);
          // setOpenaiApiKey(values.openaiApiKey);
          call_api(values.userInput, values.useCwnTools, values.useAsbcTools);
          form.reset();
        })}
      >
        <Group position="apart" grow>
          <Group>
            <Checkbox
              my="md"
              label="Use CWN Tools"
              {...form.getInputProps('useCwnTools', { type: 'checkbox' })}
            />
            {/* <Checkbox
              mt="md"
              label="Use ASBC Tools"
              {...form.getInputProps('useAsbcTools', { type: 'checkbox' })}
            /> */}
          </Group>
          <Group position="right">
            <Button
              onClick={() => setChatHistory([])}
              sx={(theme) => ({
                backgroundColor: theme.colorScheme === 'dark' ? theme.colors.lime[9] : theme.colors.lime[5],
              })}
              // color="lime"
              leftIcon={<GrPowerReset size="1rem" />}
            >
              Reset Chat
            </Button>
          </Group>
          {/* <PasswordInput
            placeholder="OpenAI API Key"
            label="OpenAI API Key"
            size="xs"
            required
            withAsterisk
            {...form.getInputProps('openaiApiKey')}
          /> */}
        </Group>
        {/* </Flex> */}
        <Textarea
          withAsterisk
          label="User Input"
          placeholder="Enter your text here"
          autosize
          required
          minRows={5}
          {...form.getInputProps('userInput')}
        />

        <Group position="center" mt="md">
          <Button type="submit">Submit</Button>
        </Group>
      </form>
    </Box>
  );
}
