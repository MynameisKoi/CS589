import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import warnings
warnings.filterwarnings("ignore")


# Note: LLM's do not always produce the same results. When
# executing the code in your notebook, you may get slightly
# different answers that those in the video.

# In[ ]:


# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be
# set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"


##############################################################
# Built-in LangChain tools
###############################################################

# In[ ]:


#!pip install -U wikipedia


# In[ ]:


from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain_openai import ChatOpenAI


# In[ ]:


llm = ChatOpenAI(temperature=0, model=llm_model)


# In[ ]:


tools = load_tools(["llm-math","wikipedia"], llm=llm)


# In[ ]:


agent= initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)


# In[ ]:


agent("What is the 25% of 300?")


##############################################################
# Wikipedia example
# - Showcase of the agent's interaction with Wikipedia.
# - Example involves asking the agent about Tom
#   M. Mitchell, an American computer scientist.
# - Demonstration of the agent's ability to leverage
#   tools to retrieve accurate and contextually
#   appropriate answers.
###############################################################

# In[ ]:


question = "Tom M. Mitchell is an American computer scientist \
and the Founders University Professor at Carnegie \
Mellon University (CMU)\
what book did he write?"

result = agent(question)


##############################################################
# Python Agent
###############################################################

# In[ ]:


agent = create_python_agent(
    llm,
    tool=PythonREPLTool(),
    verbose=True
)


# In[ ]:


customer_list = [["Harrison", "Chase"],
                 ["Lang", "Chain"],
                 ["Dolly", "Too"],
                 ["Elle", "Elem"],
                 ["Geoff","Fusion"],
                 ["Trance","Former"],
                 ["Jen","Ayai"]
                ]


# In[ ]:


agent.run(f"""Sort these customers by \
last name and then first name \
and print the output: {customer_list}""")


##############################################################
# View detailed outputs of the chains
###############################################################

# In[ ]:


import langchain

langchain.debug=True
agent.run(f"""Sort these customers by \
last name and then first name \
and print the output: {customer_list}""")

langchain.debug=False


##############################################################
# Define your own tool
# - Guidance on crafting a custom tool using a "time"
#   function as an example.
# - Introduction of the "tool decorator" for defining
#   a function as a tool for LangChain.
# - Emphasis on the importance of clear docstrings
#   in guiding the agent's use of the tool.
###############################################################

# In[ ]:


#!pip install DateTime


# In[ ]:


from langchain.agents import tool
from datetime import date


# In[ ]:


@tool
def time(text: str) -> str:
    """Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this function will always return todays \
    date - any date mathmatics should occur \
    outside this function."""
    return str(date.today())


# In[ ]:

##############################################################
# Integrating Custom Tool with an Agent
# - Instructions on integrating a custom tool
#   with an agent.
# - Process involves adding the custom tool to
#   the list of existing tools used by the agent.
# - Example includes using a tool that returns
#   the current date.
# - Explanation of how the agent recognizes the
#   need to use the custom tool and interacts with
#   it to provide the requested information.
##############################################################
agent= initialize_agent(
    tools + [time],
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)


# **Note**:
#
# The agent will sometimes come to the wrong
# conclusion (agents are a work in progress!).
#
# If it does, please try running it again.

# In[ ]:


try:
    result = agent("whats the date today?")
except:
    print("exception on external access")