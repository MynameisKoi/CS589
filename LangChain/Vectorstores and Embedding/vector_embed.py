import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']


# We just discussed `Document Loading` and `Splitting`.


# In[ ]:


from langchain_community.document_loaders import PyPDFLoader


#############################################################
# 1. Load PDF
#
# References of different loading:
# - PDF
# - Youtube
# - URL
# - Notion DB
#############################################################
loaders = [
    # Duplicate documents on purpose - messy data
    PyPDFLoader("/home/koiisme/CS589/LangChain/Vectorstores and Embedding/2023Catalog.pdf"),
    PyPDFLoader("/home/koiisme/CS589/LangChain/Vectorstores and Embedding/2023Catalog.pdf"),
    PyPDFLoader("/home/koiisme/CS589/LangChain/Vectorstores and Embedding/2024Catalog.pdf"),
    PyPDFLoader("/home/koiisme/CS589/LangChain/Vectorstores and Embedding/SFBU-connection-july-2023.pdf"),
    PyPDFLoader("/home/koiisme/CS589/LangChain/Vectorstores and Embedding/Spring2024RegistrationProcedures.pdf"),
]
docs = []
for loader in loaders:
    docs.extend(loader.load())


# In[ ]:



#############################################################
# 2. Split the content to create chunks
#
# References
# - Document Splitting
#############################################################
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 150
)


# In[ ]:


splits = text_splitter.split_documents(docs)


# In[ ]:


print("len(splits): ", len(splits))


#############################################################
# 3. Create an index for each chunk by embeddings
#
# Let's take our splits and embed them.
#############################################################

# In[ ]:


from langchain_openai import OpenAIEmbeddings
embedding = OpenAIEmbeddings()


# In[ ]:


sentence1 = "i like dogs"
sentence2 = "i like canines"
sentence3 = "the weather is ugly outside"


# In[ ]:


embedding1 = embedding.embed_query(sentence1)
embedding2 = embedding.embed_query(sentence2)
embedding3 = embedding.embed_query(sentence3)


# In[ ]:


import numpy as np


# In[ ]:


# numpy.dot(vector_a, vector_b, out = None)
# returns the dot product of vectors a and b.
print("np.dot(embedding1, embedding2): ", np.dot(embedding1, embedding2))
print("np.dot(embedding1, embedding3): ", np.dot(embedding1, embedding3))
print("np.dot(embedding2, embedding3): ", np.dot(embedding2, embedding3))



#############################################################
# 4. Vectorstores
#############################################################


# In[ ]:


# ! pip install chromadb


# In[ ]:


from langchain_community.vectorstores import Chroma


# In[ ]:


persist_directory = 'docs/chroma/'


# In[ ]:


# remove old database files if any
import subprocess

# Execute the shell command to remove the directory recursively
subprocess.run(['rm', '-rf', './docs/chroma'])



# In[ ]:


vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)


# In[ ]:


print(vectordb._collection.count())



#############################################################
# 5. Similarity Search
#############################################################


# In[ ]:


question = "is there an email i can ask for help"


# In[ ]:


docs = vectordb.similarity_search(question,k=3)


# In[ ]:


print("len(docs): ", len(docs))


# In[ ]:


print(docs[0].page_content)


# Let's save this so we can use it later!


# In[ ]:


print("vectordb.persist(): ", vectordb.persist())



#############################################################
# 6. Edge Case - Failure modes
#
# This seems great, and basic similarity
# search will get you 80% of the way there
# very easily.
#
# But there are some failure modes that can creep up.
#
# Here are some edge cases that can arise - we'll fix
# them in the next class.
#############################################################


# In[ ]:


question = "what did they say about matlab?"


# In[ ]:


docs = vectordb.similarity_search(question,k=5)
print(docs)


#############################################################
# 6.1 Edge Case 1 - Failure modes: Diversity
#
# Notice that we're getting duplicate chunks
# (because of the duplicate
# `MachineLearning-Lecture01.pdf` in the index).
#
# Semantic search fetches all similar documents,
# but does not enforce diversity.
#
# `docs[0]` and `docs[1]` are indentical.
#############################################################

# In[ ]:


print(docs[0])


# In[ ]:


print(docs[1])



#############################################################
# 6.2 Edge Case 2 - Failure modes: Specifity
#
# We can see a new failure mode.
#
# The question below asks a question about
# the third lecture,
# but includes results from other lectures
# as well.
#############################################################


# In[ ]:


question = "what did they say about regression \
  in the third lecture?"


# In[ ]:


docs = vectordb.similarity_search(question,k=5)


# In[ ]:


for doc in docs:
    print(doc.metadata)


# In[ ]:


print(docs[4].page_content)
