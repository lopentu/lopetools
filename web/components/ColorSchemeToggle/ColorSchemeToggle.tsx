import { ActionIcon, useMantineColorScheme } from '@mantine/core';
import { IconSun, IconMoonStars } from '@tabler/icons';

export function ColorSchemeToggle({
  counter,
  setCounter,
}: {
  counter: number;
  setCounter: React.Dispatch<React.SetStateAction<number>>;
}) {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  // TODO: show meme modal after 10 clicks

  return (
    <ActionIcon
      onClick={() => {
        toggleColorScheme();
        setCounter(counter + 1);
      }}
      size="lg"
      sx={(theme) => ({
        backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
        color: theme.colorScheme === 'dark' ? theme.colors.yellow[4] : theme.colors.blue[6],
      })}
    >
      {colorScheme === 'dark' ? (
        <IconSun size="1.5rem" stroke={1.5} />
      ) : (
        <IconMoonStars size="1.5rem" stroke={1.5} />
      )}
    </ActionIcon>
  );
}
