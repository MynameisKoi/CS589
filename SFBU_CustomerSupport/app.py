#############################################################
# Chat
#
# Step 1: Overview of the workflow for RAG
# Step 2: Load document and create VectorDB
# Step 3: Similarity Search to select relevant chunks (splits)
# Step 4: Create LLM
# Step 5: RetrievalQA Chain
#     Step 5.1: Craete a prompt template
#     Step 5.2: Create QA Chain Prompt from prompt template
#     Step 5.3: Run QA chain from the "QA Chain Prompt"
#           using "Stuff" chain type
# Step 6: ConversationalRetrievalChain
#      Step 6.1: Create Memory
#      Step 6.2: QA with ConversationalRetrievalChain
#      Step 6.3: Test ConversationalRetrievalChain
#          Step 6.3.1: First Question
#          Step 6.3.2: Follow-up Question
# Step 7: Create a chatbot that works on your documents
#      Step 7.1: Create Business Logic
#      Step 7.2: Create a chatbot GUI
#############################################################


#############################################################
# Step 1: Overview of the workflow for
#
#      Retrieval Augmented Generation (RAG)
#
# References: Vectorstores and Embeddings &
#             Vectorstore Retrieval
# 1. Document Loading
# 2. Splitting the content to create chunks (splits)
# 3. Indexing each chunk (split) by embeddings
# 4. Storage - Vectorstore
# 5. Retrieval to select relevant chunks (splits)
#    - Vectorstore Retrieval by Similarity Search
#    - Traditional Retrieval by SVM or TF-IDF
#############################################################

# In[ ]:

print("Step 1: Overview of the workflow for RAG")

#############################################################
# Step 1.1: Set up environment
###########################################
import os
import openai
import sys
sys.path.append('../..')

import panel as pn  # GUI
pn.extension()

from dotenv import load_dotenv, find_dotenv

#############################################################
# Step 1.1.1: OpenAI key setup
#############################################################
import os
import openai
# read local .env file
_ = load_dotenv(find_dotenv())

openai.api_key  = os.environ['OPENAI_API_KEY']

#############################################################
# Step 1.1.2: LLM model selection
#############################################################

# In[ ]:


import datetime
current_date = datetime.datetime.now().date()
if current_date < datetime.date(2023, 9, 2):
    llm_name = "gpt-3.5-turbo-0301"
else:
    llm_name = "gpt-3.5-turbo"
print(llm_name)

# In[ ]:

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

#############################################################
# Step 2: Load document and create VectorDB
#
# Before this step, you must have done
# 1. Document Loading
# 2. Splitting the content to create chunks (splits)
# 3. Indexing each chunk (split) by embeddings
# 4. Storage - Vectorstore
#    - The result is put into the vecstore: docs/chroma/
#
#========================================================
#
# References: Vectorstores and Embeddings &
#             Vectorstore Retrieval
# 1. Document Loading
# 2. Splitting the content to create chunks (splits)
# 3. Indexing each chunk (split) by embeddings
# 4. Storage - Vectorstore
# 5. Retrieval to select relevant chunks (splits)
#    - Vectorstore Retrieval by Similarity Search
#    - Traditional Retrieval by SVM or TF-IDF
#############################################################
print("Step 2: Load document and create VectorDB (i.e., Vectorstore)")

persist_directory = 'docs/chroma/'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embedding)


# In[ ]:


#############################################################
# Step 3: Similarity Search to select relevant chunks (splits)
#
# Vectorstore Retrieval by Similarity Search
#
# References: Vectorstores and Embeddings &
#             Vectorstore Retrieval
# 1. Document Loading
# 2. Splitting the content to create chunks (splits)
# 3. Indexing each chunk (split) by embeddings
# 4. Storage - Vectorstore
# 5. Retrieval to select relevant chunks (splits)
#    - Vectorstore Retrieval by Similarity Search
#    - Traditional Retrieval by SVM or TF-IDF
#############################################################
print("Step 3: Similarity Search to select relevant chunks (splits)")

question = "What are major topics for this class?"
docs = vectordb.similarity_search(question,k=3)
print("len(docs):", len(docs))


# In[ ]:


#############################################################
# Step 4: Create LLM
#############################################################
print("Step 4: Create LLM")

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name=llm_name, temperature=0)
llm.invoke("Hello world!")


# In[ ]:


#############################################################
# Step 5: RetrievalQA Chain
#
# - Use Customer Prompts with Context
# - Does not use Memory
#############################################################
print("Step 5: RetrievalQA Chain - optional")

#############################################################
# Step 5.1: Craete a prompt template
#############################################################
print("Step 5.1: Craete a prompt template")

from langchain.prompts import PromptTemplate

template = """Use the following pieces of \
   context to answer \
   the question at the end. If you don't know \
   the answer, \
   just say that you don't know, don't try \
   to make up an \
   answer. Use three sentences maximum. \
   Keep the answer as \
   concise as possible. Always say \
   "thanks for asking!" \
   at the end of the answer.
{context}
Question: {question}
Helpful Answer:"""

#############################################################
# Step 5.2: Create QA Chain Prompt from prompt template
#############################################################
print("Step 5.2: Create QA Chain Prompt from prompt template")

QA_CHAIN_PROMPT = PromptTemplate(
     input_variables=["context", "question"],
     template=template,)

#############################################################
# Step 5.3: Run QA chain from the "QA Chain Prompt"
#           using "Stuff" chain type
#############################################################
print("Step 5.3: Run QA chain from the 'QA Chain Prompt' # using 'Stuff' chain type")

from langchain.chains import RetrievalQA

question = "Is probability a class topic?"
qa_chain = RetrievalQA.from_chain_type(llm,
   retriever=vectordb.as_retriever(),
   return_source_documents=True,
   chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})


result = qa_chain({"query": question})
print('result["result"]:', result["result"])

#############################################################
# Step 6: ConversationalRetrievalChain
#
# - Use Memory
#############################################################
print("Step 6: ConversationalRetrievalChain")

#############################################################
# Step 6.1: Create Memory
#############################################################
print("Step 6.1: Create Memory")

# In[ ]:


from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    # Set return messages equal true
    # - Return the chat history as a  list of messages
    #   as opposed to a single string.
    # - This is  the simplest type of memory.
    #   + For a more in-depth look at memory, go back to
    #     the first class that I taught with Andrew.
    return_messages=True
)


# In[ ]:

#############################################################
# Step 6.2: QA with ConversationalRetrievalChain
#############################################################
print("Step 6.2: QA with ConversationalRetrievalChain")

from langchain.chains import ConversationalRetrievalChain

retriever=vectordb.as_retriever()
qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory
)


# In[ ]:

#############################################################
# Step 6.3: Test ConversationalRetrievalChain
#############################################################
print("Step 6.3: Test ConversationalRetrievalChain")

#############################################################
# Step 6.3.1: First Question
#############################################################
print("Step 6.3.1: First Question")
question = "Is probability a class topic?"
result = qa({"question": question})

# In[ ]:

print("result['answer']:", result['answer'])


# In[ ]:


#############################################################
# Step 6.3.2: Follow-up Question
#############################################################
print("Step 6.3.2: Follow-up Question")

question = "why are those prerequesites needed?"
result = qa({"question": question})

# In[ ]:

print("result['answer']:", result['answer'])

#############################################################
# Step 7: Create a chatbot that works on your documents
#############################################################
print("Step 7: Create a chatbot that works on your documents")

# In[ ]:


from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader


# The chatbot code has been updated a bit
# since filming. The GUI
# appearance also varies depending on the
# platform it is running on.


# In[ ]:

#############################################################
# Step 7.1: Create a chatbot that works on your documents
#
# - Create Business logic
#############################################################
print("Step 7.1: Create Business Logic")

#############################################################
# Step 7.1.1: load_db function
#############################################################
def load_db(file, chain_type, k):
    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split documents
    text_splitter = RecursiveCharacterTextSplitter(
           chunk_size=1000,
           chunk_overlap=150)
    docs1 = text_splitter.split_documents(documents)
    # define embedding
    embeddings = OpenAIEmbeddings()
    # create vector database from data
    db = DocArrayInMemorySearch.from_documents(docs1,
           embeddings)
    # define retriever
    retriever = db.as_retriever(search_type="similarity",
           search_kwargs={"k": k})
    # create a chatbot chain. Memory is managed externally.
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_name, temperature=0),
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )
    return qa


# In[ ]:


import panel as pn
import param

#############################################################
# Step 7.1.2: cbfs class
#############################################################
class cbfs(param.Parameterized):
    chat_history = param.List([])
    answer = param.String("")
    db_query  = param.String("")
    db_response = param.List([])

    #########################################################
    # Step 7.1.2.1: init function
    #########################################################
    def __init__(self,  **params):
        super(cbfs, self).__init__( **params)
        self.panels = []
        self.loaded_file = "/home/koiisme/CS589/SFBU_CustomerSupport/2024Catalog.pdf"
        self.qa = load_db(self.loaded_file,"stuff", 4)

    #########################################################
    # Step 7.1.2.2: call_load_db function
    #########################################################
    def call_load_db(self, count):
        # init or no file specified :
        if count == 0 or file_input.value is None:
            return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")
        else:
            file_input.save("temp.pdf")  # local copy
            self.loaded_file = file_input.filename
            button_load.button_style="outline"
            self.qa = load_db("temp.pdf", "stuff", 4)
            button_load.button_style="solid"
        self.clr_history()
        return pn.pane.Markdown(
            f"Loaded File: {self.loaded_file}")

    #########################################################
    # Step 7.1.2.3: convchain(self, query) function
    #########################################################
    def convchain(self, query):
        if not query:
            return pn.WidgetBox(pn.Row('User:',
               pn.pane.Markdown("", width=600)), scroll=True)
        result = self.qa({"question": query,
                          "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        self.db_query = result["generated_question"]
        self.db_response = result["source_documents"]
        self.answer = result['answer']
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query, width=600)),
            pn.Row('ChatBot:', pn.pane.Markdown(self.answer,
               width=600,
               style={'background-color': '#F6F6F6'}))
        ])
        inp.value = ''  #clears loading indicator when cleared
        return pn.WidgetBox(*self.panels,scroll=True)

    #########################################################
    # Step 7.1.2.4: get_lquest(self) function
    #########################################################
    @param.depends('db_query ', )
    def get_lquest(self):
        if not self.db_query :
            return pn.Column(
                pn.Row(pn.pane.Markdown(f"Last question to DB:",
            styles={'background-color': '#F6F6F6'})),
                pn.Row(pn.pane.Str("no DB accesses so far"))
            )
        return pn.Column(
            pn.Row(pn.pane.Markdown(f"DB query:",
            styles={'background-color': '#F6F6F6'})),
            pn.pane.Str(self.db_query )
        )

    #########################################################
    # Step 7.1.2.5: get_sources function
    #########################################################
    @param.depends('db_response', )
    def get_sources(self):
        if not self.db_response:
            return
        rlist=[pn.Row(pn.pane.Markdown(f"Result of DB lookup:",
            styles={'background-color': '#F6F6F6'}))]
        for doc in self.db_response:
            rlist.append(pn.Row(pn.pane.Str(doc)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    #########################################################
    # Step 7.1.2.6: get_chats function
    #########################################################
    @param.depends('convchain', 'clr_history')
    def get_chats(self):
        if not self.chat_history:
            return pn.WidgetBox(
                  pn.Row(pn.pane.Str("No History Yet")),
                   width=600, scroll=True)
        rlist=[pn.Row(pn.pane.Markdown(
            f"Current Chat History variable",
            styles={'background-color': '#F6F6F6'}))]
        for exchange in self.chat_history:
            rlist.append(pn.Row(pn.pane.Str(exchange)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    #########################################################
    # Step 7.1.2.7: clr_history function
    #########################################################
    def clr_history(self,count=0):
        self.chat_history = []
        return


#############################################################
# Step 7.2: Create a chatbot that works on your documents
#
# -  Create a chatbot GUI
#############################################################
print("Step 7.2: Create a chatbot GUI")

# In[ ]:


# Integrate Business Logic and GUI
cb = cbfs()

#############################################################
# Step 7.2.1: Create File input
#############################################################
file_input = pn.widgets.FileInput(accept='.pdf')


#############################################################
# Step 7.2.2: Create buttons
#############################################################
button_load = pn.widgets.Button(name="Load DB",
      button_type='primary')
button_clearhistory = pn.widgets.Button(name="Clear History",
        button_type='warning')
button_clearhistory.on_click(cb.clr_history)
inp = pn.widgets.TextInput( placeholder='Enter text here…')
bound_button_load = pn.bind(cb.call_load_db,
         button_load.param.clicks)

#############################################################
# Step 7.2.3: Create conversation
#############################################################
conversation = pn.bind(cb.convchain, inp)

#############################################################
# Step 7.2.4: Create jpg_pane
#############################################################
jpg_pane = pn.pane.Image( '/home/koiisme/CS589/SFBU_CustomerSupport/BayleyBayhawk.jpg')

#############################################################
# Step 7.2.5: Create tables
#############################################################
tab1 = pn.Column(
    pn.Row(inp),
    pn.layout.Divider(),
    pn.panel(conversation, loading_indicator=True, height=300),
    pn.layout.Divider(),
)
tab2 = pn.Column(
    pn.panel(cb.get_lquest),
    pn.layout.Divider(),
    pn.panel(cb.get_sources),
)
tab3= pn.Column(
    pn.panel(cb.get_chats),
    pn.layout.Divider(),
)
tab4=pn.Column(
    pn.Row( file_input, button_load, bound_button_load),
    pn.Row( button_clearhistory, pn.pane.Markdown(
        "Clears chat history. Can use to start a new topic" )),
    pn.layout.Divider(),
    pn.Row(jpg_pane.clone(width=400))
)

#############################################################
# Step 7.2.6: Create dashboard
#############################################################
dashboard = pn.Column(
    pn.Row(pn.pane.Markdown('# ChatWithYourData_Bot')),
    pn.Tabs(('Conversation', tab1), ('Database', tab2),
        ('Chat History', tab3),('Configure', tab4))
)

# print(dashboard)
dashboard.servable()
