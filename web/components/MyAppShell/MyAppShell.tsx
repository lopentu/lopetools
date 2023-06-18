import React, {
  JSXElementConstructor,
  ReactElement,
  ReactFragment,
  ReactPortal,
  useState,
} from 'react';
import {
  AppShell,
  Anchor,
  Center,
  Flex,
  Group,
  Navbar,
  Header,
  Footer,
  Aside,
  Text,
  Image,
  ThemeIcon,
  MediaQuery,
  Burger,
  useMantineTheme,
} from '@mantine/core';

import { GiGoat } from 'react-icons/gi';

import { ColorSchemeToggle } from '../ColorSchemeToggle/ColorSchemeToggle';

export function MyAppShell(props: {
  children:
    | string
    | number
    | boolean
    | ReactElement<any, string | JSXElementConstructor<any>>
    | ReactFragment
    | ReactPortal
    | null
    | undefined;
  counter: number;
  setCounter: React.Dispatch<React.SetStateAction<number>>;
}) {
  const theme = useMantineTheme();
  const [opened, setOpened] = useState(false);
  return (
    <AppShell
      padding="md"
      styles={{
        main: {
          background: theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0],
        },
      }}
      navbarOffsetBreakpoint="sm"
      asideOffsetBreakpoint="sm"
      // navbar={
      //   <Navbar p="md" hiddenBreakpoint="sm" hidden={!opened} width={{ sm: 200, lg: 300 }}>
      //     <Text>Application navbar</Text>
      //   </Navbar>
      // }
      //   aside={
      //     <MediaQuery smallerThan="sm" styles={{ display: 'none' }}>
      //       <Aside p="md" hiddenBreakpoint="sm" width={{ sm: 200, lg: 300 }}>
      //         <Text>Application sidebar</Text>
      //       </Aside>
      //     </MediaQuery>
      //   }
      footer={
        <Footer height={60} p="md">
          <Anchor
            href="https://lope.linguistics.ntu.edu.tw"
            target="_blank"
            color="dimmed"
            weight="bold"
          >
            LOPE Lab
          </Anchor>
        </Footer>
      }
      header={
        // https://github.com/mantinedev/mantine/blob/master/src/mantine-demos/src/demos/core/AppShell/AppShell.demo.usage.tsx
        <Header height={60} p="xs">
          {/* <div style={{ alignItems: "center", alignContent: "center", height: '100%' }}> */}
          <Group sx={{ height: '100%' }} px={20} position="apart">
            <Group>
              <ThemeIcon variant="filled" size="lg" radius="xl">
                <GiGoat />
              </ThemeIcon>
              <Text fz="xl" fw={700}>
                LopeGPT
              </Text>
            </Group>
            <ColorSchemeToggle counter={props.counter} setCounter={props.setCounter} />
          </Group>
          {/* <MediaQuery largerThan="sm" styles={{ display: 'none' }}>
              <Burger
                opened={opened}
                onClick={() => setOpened((o) => !o)}
                size="sm"
                color={theme.colors.gray[6]}
                mr="xl"
              />
            </MediaQuery> */}
          {/* </div> */}
        </Header>
      }
    >
      {props.children}
    </AppShell>
  );
}
