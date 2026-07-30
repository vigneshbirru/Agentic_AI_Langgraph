from langgraph.graph import StateGraph ,START,END
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated, Literal
from pydantic import BaseModel, Field
from  dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage,BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
import operator
import time

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    

def chat_node(state: ChatState):
    message = state['messages']
    response = llm.invoke(message)
    return {'messages': [response]}

#checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


chatbot = graph.compile(checkpointer=checkpointer)

# for message_chunk, metadata in chatbot.stream(
#     {'messages': [HumanMessage(content='what is recipe to make pasta')]},
#     config ={'configurable': {'thread_id':"thread-1"}},
#     stream_mode = "messages"
# ):

#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)