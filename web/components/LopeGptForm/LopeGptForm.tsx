import { Flex, Textarea, Checkbox, Button, Group, Box } from '@mantine/core';
import { useForm } from '@mantine/form';


export function LopeGptForm() {
  const form = useForm({
    initialValues: {
      userInput: '',
      useCwnTools: true,
      useAsbcTools: true,
    }
  });

  return (
    <Box mx="auto">
      <form onSubmit={form.onSubmit((values) => console.log(values))}>
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
          {...form.getInputProps('userInput')}
        />

        <Group position="center" mt="md">
          <Button type="submit">Submit</Button>
        </Group>
      </form>
    </Box>
  )
}