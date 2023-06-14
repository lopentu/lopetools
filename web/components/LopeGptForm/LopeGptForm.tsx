import { Flex, Textarea, Checkbox, Button, Group, Box } from '@mantine/core';
import { useForm } from '@mantine/form';
import React, { useEffect, useState } from 'react';
import { ChatMessageProps } from '../ChatHistory/ChatHistory';



export function LopeGptForm({ chatHistory, setChatHistory, openaiApiKey }: { chatHistory: ChatMessageProps[], setChatHistory: React.Dispatch<React.SetStateAction<ChatMessageProps[]>>, openaiApiKey: string }) {
  const [rawHistory, setRawHistory] = useState([])

  function call_api(text: string, useCwnTools: boolean, useAsbcTools: boolean) {
    let payload = {
      text: text,
      use_cwn: useCwnTools,
      use_asbc: useAsbcTools,
      messages: rawHistory,
      openai_api_key: openaiApiKey
    }
    fetch('http://localhost:3002/', {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(responseData => {
      console.log(responseData)
    })
    .catch(error => {
      console.error(error)
    });
  }
  const form = useForm({
    initialValues: {
      userInput: '',
      useCwnTools: true,
      useAsbcTools: true,
    }
  });


  return (
    <Box mx="auto">
      <form onSubmit={form.onSubmit((values) => {
        let role = 'User';
        let text = values.userInput;
        let key = `${role}-${text}`
        console.log(values)
        setChatHistory([...chatHistory, { role, text, key }])
        call_api(values.userInput, values.useCwnTools, values.useAsbcTools)
        form.reset();
      })}>
        <Flex
          gap="md"
          justify="flex-start"
          align="center"
          direction="row"
          wrap="wrap"
          rowGap="lg"
          mb="lg"
        >
          <Checkbox
            mt="md"
            label="Use CWN Tools"
            {...form.getInputProps('useCwnTools', { type: 'checkbox' })}
          />
          <Checkbox
            mt="md"
            label="Use ASBC Tools"
            {...form.getInputProps('useAsbcTools', { type: 'checkbox' })}
          />
        </Flex>
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
  )
}