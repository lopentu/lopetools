import base64
import json
import os
import re
import sys


from pathlib import Path
# BASE = Path(__file__).resolve().parent.parent
# sys.path.append(str(BASE / "src"))

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chains import ConversationChain
from langchain.memory import ConversationTokenBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict


from src.lc_tools.lope_tools import (
    SenseTagTool,
    QuerySenseFromDefinitionTool,
    QuerySenseFromLemmaTool,
    QuerySenseFromExamplesTool,
    QueryAsbcSenseFrequencyTool,
    QueryRelationsFromSenseIdTool,
    QuerySimilarSenseFromCwnTool,
    # QueryAsbcFullTextTool
)


os.environ["TIKTOKEN_CACHE_DIR"] = ""
BASE = Path(__file__).resolve().parent.parent
load_dotenv(str(BASE / ".env"))
# openai.api_key = os.environ["OPENAI_API_KEY"]


CWN_TOOLS = [
    SenseTagTool(return_direct=True),
    QuerySenseFromDefinitionTool(),
    QuerySenseFromLemmaTool(),
    QuerySenseFromExamplesTool(),
    QueryAsbcSenseFrequencyTool(),
    QueryRelationsFromSenseIdTool(),
    QuerySimilarSenseFromCwnTool(return_direct=True),
    # QueryAsbcFullTextTool(return_direct=True),
]

ASBC_TOOLS = []


class LOPEAgent:
    SUFFIX = """注意一：'action_input'只輸入字串，不要輸入JSON格式或其他的格式。
    注意二：有了答案之後，不要做額外的分析。"""
    # SUFFIX = """注意一：'action_input'只輸入字串，不要輸入JSON格式或其他的格式。
    # 注意二：每個答復的前面一定要附上['Question: ', 'Thought: ', 'Action: ', 'Final Answer: '] 的其中之一。
    # 注意二：在最終答案前面一定要附上 'Final Answer'。
    # 注意三：有了答案之後，不要做額外的分析。"""

    def __init__(self, use_cwn, use_asbc, openai_api_key, messages=None):
        self.tools = []
        if use_cwn:
            self.tools = CWN_TOOLS
        if use_asbc:
            self.tools += ASBC_TOOLS
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            client=None,
            openai_api_key=openai_api_key,
            # stop=["Human: "],  # type: ignore
        )
        self.memory = ConversationTokenBufferMemory(
            llm=self.llm,
            max_token_limit=4000,
            return_messages=True,
            memory_key="chat_history",
            ai_prefix="Assistant",
            human_prefix="User",
        )
        if messages:
            self.load_messages(messages)
        if not self.tools:
            self.agent_chain = ConversationChain(
                memory=self.memory,
                llm=self.llm,
                verbose=True,
                max_iterations=8,
            )
        else:
            self.agent_chain = initialize_agent(
                tools=self.tools,
                memory=self.memory,
                llm=self.llm,
                # agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                verbose=True,
                max_iterations=8,
            )

    def __call__(self, text):
        try:
            if not self.tools:
                self.agent_chain.predict(input=text)
            else:
                text += self.SUFFIX
                self.agent_chain.run(input=text)
                # output = json.loads(self.agent_chain.run(input=text))
        except Exception as e:
            print("########## EXCEPTION ##########")
            print(e)
            self.memory.chat_memory.add_user_message(text)
            self.memory.chat_memory.add_ai_message("對不起我無法回答您的問題。")
        return self.export_messages()

    def export_messages(self):
        raw = messages_to_dict(self.memory.chat_memory.messages)
        formatted = self.format_chat_messages(raw)
        return {"formatted": formatted, "raw": raw}

    def load_messages(self, messages):
        self.memory.chat_memory.messages = messages_from_dict(messages)

    def format_chat_messages(self, messages) -> list[dict[str, str]]:
        out = []
        for m in messages:
            out.append(
                {
                    "role": m["type"],
                    "text": m["data"]["content"].replace(self.SUFFIX, "").strip(),
                }
            )
        return out
