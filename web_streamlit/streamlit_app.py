import json
import os
import re
import sys

if "../src/" not in sys.path:
    sys.path.append("../src/lc_tools/")
    sys.path.append("../src/")

from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool, create_csv_agent
from langchain.chains import ConversationChain
from langchain.memory import ConversationTokenBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import messages_from_dict, messages_to_dict
from llama_index.indices.struct_store import GPTPandasIndex
import openai
import pandas as pd
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

UPLOAD_TOOLS = []

pandas_index = None

ASBC_TOOLS = []

BASE = Path(__file__).resolve().parent.parent
load_dotenv(str(BASE / ".env"))
openai.api_key = os.environ["OPENAI_API_KEY"]
# conversation = ConversationChain(memory=memory, llm=llm)

st.title("LOPE Tools")
col1, col2, col3 = st.columns(3)
tool_options = ["CWN Tools", "ASBC Tools"]
# options = st.multiselect("Choose tools", tool_options, help="Choose your tools")

with col1:
    use_cwn_tools = st.checkbox("CWN Tools", value=True)
with col2:
    use_asbc_tools = st.checkbox("ASBC Tools")
with col3:
    use_file = st.empty()

your_data = st.sidebar.file_uploader(
    "Upload your data. Must contain 'Content' column.", type=["csv"]
)

st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("your_data", [])
history = st.session_state["chat_history"]
print("#" * 10, "history", "#" * 10)
print(history)


class LopeAgent:
    # SUFFIX = "不要做額外的分析。在答案前面一定要附上 'Final Answer'"
    SUFFIX = """注意一：'action_input'只輸入字串，不要輸入JSON格式或其他的。
    注意二：在答案前面一定要附上 'Final Answer'。
    注意三：有了答案之後，不要做額外的分析。"""

    def __init__(self, tools):
        self.tools = tools
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            client=None,
            # stop=["Human: "],  # type: ignore
        )
        self.memory = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=3000)
        self.load_messages()
        # if use_file:
        #     self.agent_chain = create_csv_agent(self.llm, st.session_state["your_data"])
        if not tools:
            self.agent_chain = ConversationChain(
                memory=self.memory,
                llm=self.llm,
                verbose=True,
            )
        else:
            self.agent_chain = initialize_agent(
                tools=tools,
                memory=self.memory,
                llm=self.llm,
                agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
            )

    def __call__(self, text):
        try:
            if not self.tools:
                self.agent_chain.predict(input=text)
            else:
                text += self.SUFFIX
                self.agent_chain.run(text)
        except:
            self.memory.chat_memory.add_ai_message("對不起我無法回答您的問題。")
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
    # if use_file:
    #     tools += UPLOAD_TOOLS
    agent = LopeAgent(tools=tools)
    with st.spinner("Thinking..."):
        agent(txt)


with st.container():
    if history:
        formatted_history = format_chat_messages(history)
        print(formatted_history)
        for idx, h in enumerate(formatted_history):
            if h["role"] == "human":
                message(
                    h["text"], key=str(idx), is_user=True, avatar_style="thumbs", seed=3
                )
            else:
                message(
                    h["text"],
                    key=str(idx),
                    is_user=False,
                    avatar_style="bottts",
                    seed=6,
                )
    with st.form("my_form", clear_on_submit=True):
        text_input = st.text_area(
            "Your message",
            height=50,
            key="user_input",
        )
        submitted = st.form_submit_button("Submit", on_click=on_form_submit)
    media_box = st.empty()


def format_tagged(tagged_text: list[dict]):
    return " ".join(
        [
            f"{d['詞']}-{d['SenseID'] if d['SenseID'] != 'NONE' else ''}({d['詞性']})"
            for d in tagged_text
        ]
    )


def process_upload(data):
    global pandas_index
    global UPLOAD_TOOLS
    use_file.checkbox(data.name)
    st.session_state["your_data"] = data
    df = pd.read_csv(data)
    # pandas_index = GPTPandasIndex(df=df)

    # UPLOAD_TOOLS.append(Tool(
    #     name="File Index",
    #     func=lambda q: str(pandas_index.as_query_engine().query(q)),
    #     description="回答關於上傳檔案的資訊",
    # ))
    # content = df['Content'].tolist()
    # tagged = [json.loads(SenseTagTool().run(c)) for c in content]
    # res = []
    # print(tagged)
    # tagged = [format_tagged(t) for t in tagged]
    # df['Content'] = tagged
    media_box.dataframe(df)


if your_data:
    with st.spinner("Processing your data..."):
        process_upload(your_data)
