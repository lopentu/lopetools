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
import { AiOutlineSend, AiOutlineUndo } from 'react-icons/ai';


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
  const isDemo = true;

  function call_api(text: string, useCwnTools: boolean, useAsbcTools: boolean, usePttTools: boolean) {
    let payload = {
      text: text,
      use_cwn: useCwnTools,
      use_asbc: useAsbcTools,
      use_ptt: usePttTools,
      messages: rawHistory,
      openaiApiKey: openaiApiKey,
    };
    console.log(payload);
    fetch('https://lope.linguistics.ntu.edu.tw/agent/', {
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

  let validate = {}

  if (!isDemo) {
    validate = {
      openaiApiKey: hasLength(51, 'OpenAI API Key must be 51 characters long'),
    }
  }
  const form = useForm({
    initialValues: {
      userInput: '',
      useCwnTools: true,
      useAsbcTools: true,
      usePttTools: true,
      openaiApiKey: openaiApiKey,
    },
    validate: validate
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
          setOpenaiApiKey(values.openaiApiKey);
          call_api(values.userInput, values.useCwnTools, values.useAsbcTools, values.usePttTools);
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
            <Checkbox
              my="md"
              label="Use PTT Tools"
              {...form.getInputProps('usePttTools', { type: 'checkbox' })}
              />
              {/* <Checkbox
              mt="md"
              label="Use ASBC Tools"
              {...form.getInputProps('useAsbcTools', { type: 'checkbox' })}
            /> */}
          </Group>
          {!isDemo && <PasswordInput
            placeholder="OpenAI API Key"
            label="OpenAI API Key"
            size="xs"
            required
            withAsterisk
            {...form.getInputProps('openaiApiKey')}
          />}
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
          <Button leftIcon={<AiOutlineSend size="1rem" />} type="submit">Submit</Button>
          <Button
            onClick={() => {
              setChatHistory([]);
              setRawHistory([]);
            }}
            sx={(theme) => ({
              backgroundColor:
                theme.colorScheme === 'dark' ? theme.colors.lime[9] : theme.colors.lime[5],
            })}
            leftIcon={<AiOutlineUndo size="1rem" />}
          >
            Reset Chat
          </Button>
        </Group>
      </form>
    </Box>
  );
}
