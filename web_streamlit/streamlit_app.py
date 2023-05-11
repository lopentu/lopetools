import base64
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
from langchain.schema import messages_from_dict, messages_to_dict
from llama_index import Document, GPTVectorStoreIndex
import openai
import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_chat import message

from lope_tools import (
    SenseTagTool,
    QuerySenseFromDefinitionTool,
    QuerySenseFromLemmaTool,
    QuerySenseFromExamplesTool,
    QueryAsbcSenseFrequencyTool,
    QueryRelationsFromSenseIdTool,
    QuerySimilarSenseFromCwnTool,
)

CWN_TOOLS = [
    SenseTagTool(return_direct=True),
    QuerySenseFromDefinitionTool(),
    QuerySenseFromLemmaTool(),
    QuerySenseFromExamplesTool(),
    QueryAsbcSenseFrequencyTool(),
    QueryRelationsFromSenseIdTool(),
    QuerySimilarSenseFromCwnTool(return_direct=True),
]

UPLOAD_TOOLS = []

upload_index = None

ASBC_TOOLS = []

os.environ["TIKTOKEN_CACHE_DIR"] = ""
BASE = Path(__file__).resolve().parent.parent
load_dotenv(str(BASE / ".env"))
openai.api_key = os.environ["OPENAI_API_KEY"]
sheep = Image.open("./static/羊.png")


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
        img_to_bytes(img_path)
    )
    return img_html


st.set_page_config("LopeGPT", page_icon=sheep, layout="wide")
col1, col2, col3 = st.columns(3)
tool_options = ["CWN Tools", "ASBC Tools"]
# options = st.multiselect("Choose tools", tool_options, help="Choose your tools")

with col1:
    st.markdown(
        "<h1 style='text-align: center;'>CWN</h1>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        "<p style='text-align: center; color: black;'>"
        + img_to_html("./static/羊.png")
        + "</p>",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        "<h1 style='text-align: center;'>GPT</h1>",
        unsafe_allow_html=True,
    )

with st.sidebar:
    your_data = st.file_uploader(
        "Upload your data. Must contain 'Content' column.", type=["csv"]
    )
    use_cwn_tools = st.checkbox("CWN Tools", value=True)
    # use_asbc_tools = st.checkbox("ASBC Tools")
    use_asbc_tools = False
    use_file = st.empty()

st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("upload_data", [])
history = st.session_state["chat_history"]
print("#" * 10, "history", "#" * 10)
print(history)


class LopeAgent:
    SUFFIX = """注意一：'action_input'只輸入字串，不要輸入JSON格式或其他的格式。
    注意二：有了答案之後，不要做額外的分析。"""
    # SUFFIX = """注意一：'action_input'只輸入字串，不要輸入JSON格式或其他的格式。
    # 注意二：每個答復的前面一定要附上['Question: ', 'Thought: ', 'Action: ', 'Final Answer: '] 的其中之一。
    # 注意二：在最終答案前面一定要附上 'Final Answer'。
    # 注意三：有了答案之後，不要做額外的分析。"""

    def __init__(self, tools):
        self.tools = tools
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            client=None,
            # stop=["Human: "],  # type: ignore
        )
        self.memory = ConversationTokenBufferMemory(
            llm=self.llm,
            max_token_limit=3000,
            return_messages=True,
            memory_key="chat_history",
        )
        self.load_messages()
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
                # agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                verbose=True,
                max_iterations=5
            )

    def __call__(self, text):
        try:
            if not self.tools:
                self.agent_chain.predict(input=text)
            else:
                text += self.SUFFIX
                self.agent_chain.run(input=text)
        except Exception as e:
            print("########## EXCEPTION ##########")
            print(e)
            self.memory.chat_memory.add_user_message(text)
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
                # "text": re.sub(LopeAgent.SUFFIX, "", m["data"]["content"]),
                "text": m["data"]["content"].replace(LopeAgent.SUFFIX, "").strip(),
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
    if use_file:
        tools += UPLOAD_TOOLS
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


def process_upload(data, limit_docs=1):
    global upload_index
    global UPLOAD_TOOLS
    use_file.checkbox(data.name, value=True)
    st.session_state["your_data"] = data
    df = pd.read_csv(data)
    if limit_docs:
        documents = [Document(doc) for doc in df["Content"].tolist()[:limit_docs]]
    else:
        documents = [Document(doc) for doc in df["Content"].tolist()]
    upload_index = GPTVectorStoreIndex.from_documents(documents=documents)

    UPLOAD_TOOLS.append(
        Tool(
            name="Document Index",
            func=lambda q: str(upload_index.as_query_engine().query(q)),
            # description="提供使用者個人資料索引功能。沒有提供額外的metadata。",
            description="索引使用者的文件的內容。沒有提供額外的metadata。",
            # description="useful for answering questions about the user's data",
            return_direct=True,
        )
    )
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
