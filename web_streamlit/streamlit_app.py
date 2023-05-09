import os
import re
import sys

if "../src/" not in sys.path:
    sys.path.append("../src/lc_tools/")
    sys.path.append("../src/")

from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.chains import ConversationChain
from langchain.memory import ConversationTokenBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import messages_from_dict, messages_to_dict
import openai
import streamlit as st
from streamlit_chat import message

from lope_tools import (
    SenseTagTool,
    QuerySenseFromDefinitionTool,
    QuerySenseFromLemmaTool,
    QuerySenseFromExamplesTool,
    QueryAsbcSenseFrequencyTool,
    QueryRelationsFromSenseIdTool,
)

CWN_TOOLS = [
    SenseTagTool(),
    QuerySenseFromDefinitionTool(),
    QuerySenseFromLemmaTool(),
    QuerySenseFromExamplesTool(),
    QueryAsbcSenseFrequencyTool(),
    QueryRelationsFromSenseIdTool(),
]

ASBC_TOOLS = []

BASE = Path(__file__).resolve().parent.parent
load_dotenv(str(BASE / ".env"))
openai.api_key = os.environ["OPENAI_API_KEY"]
# conversation = ConversationChain(memory=memory, llm=llm)

st.title("LOPE Tools")
col1, col2 = st.columns(2)
tool_options = ["CWN Tools", "ASBC Tools"]
# options = st.multiselect("Choose tools", tool_options, help="Choose your tools")

with col1:
    use_cwn_tools = st.checkbox("CWN Tools")
with col2:
    use_asbc_tools = st.checkbox("ASBC Tools")

your_data = st.sidebar.file_uploader("Upload your data", type=["txt", "csv", "xlsx"])

st.session_state.setdefault("chat_history", [])
history = st.session_state["chat_history"]
print("#" * 10, history, "#" * 10)
print(history)


class LopeAgent:
    # SUFFIX = "不要做額外的分析。在答案前面一定要附上 'Final Answer'"
    SUFFIX = "在答案前面一定要附上 'Final Answer'。有了答案之後，不要做額外的分析。"

    def __init__(self, tools):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.memory = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=3000)
        self.load_messages()
        if not tools:
            self.agent_chain = ConversationChain(memory=self.memory, llm=self.llm)
        else:
            self.agent_chain = initialize_agent(
                tools=tools,
                memory=self.memory,
                llm=self.llm,
                agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
            )

    def __call__(self, text):
        if type(self.agent_chain) == ConversationChain:
            self.agent_chain.predict(input=text)
        else:
            text += self.SUFFIX
            self.agent_chain.run(text)
        self.save_messages()

    def save_messages(self):
        messages = messages_to_dict(self.memory.chat_memory.messages)
        st.session_state["chat_history"] = messages

    def load_messages(self):
        messages = st.session_state["chat_history"]
        self.memory.chat_memory.messages = messages_from_dict(messages)


def format_chat_messages(messages) -> list[dict[str, str]]:
    out = []
    for m in messages:
        out.append(
            {
                "role": m["type"],
                "text": re.sub(LopeAgent.SUFFIX, "", m["data"]["content"]),
            }
        )
    return out


def on_form_submit():
    txt = st.session_state["user_input"]
    if not txt:
        return
    tools = []
    if use_cwn_tools:
        tools += CWN_TOOLS
    if use_asbc_tools:
        tools += ASBC_TOOLS
    agent = LopeAgent(tools=tools)
    agent(txt)


with st.container():
    if history:
        formatted_history = format_chat_messages(history)
        print(formatted_history)
        for idx, h in enumerate(formatted_history):
            if h["role"] == "human":
                message(h["text"], key=idx, is_user=True, avatar_style="thumbs", seed=3)
            else:
                message(
                    h["text"], key=idx, is_user=False, avatar_style="bottts", seed=6
                )
    with st.form("my_form", clear_on_submit=True):
        text_input = st.text_area(
            "Your message",
            height=50,
            key="user_input",
        )
        submitted = st.form_submit_button("Submit", on_click=on_form_submit)
