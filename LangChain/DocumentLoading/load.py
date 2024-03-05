import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']



#############################################################
# 1. PDFs
#
# Let's load a PDF [transcript]
# (https://see.stanford.edu/materials/aimlcs229/
# transcripts/MachineLearning-Lecture01.pdf)
# from Andrew Ng's famous CS229 course!
# - These documents are the result of automated transcription
#   so words and sentences are sometimes split unexpectedly.
#############################################################
print("1. PDFs")

# In[ ]:


# The course will show the pip installs you would need
# to install packages on your own machine.
# These packages are already installed on this
# platform and should not be run again.
#! pip install pypdf

# In[ ]:
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader(
     "/home/koiisme/CS589/LangChain/DocumentLoading/2023Catalog.pdf") # SFBU 2023 Catalog
pages = loader.load()


# Each page is a `Document`.
#
# A `Document` contains
# - text (`page_content`)
# - `metadata`.
len(pages)
page = pages[0]
print(page.page_content[0:500])
page.metadata


#############################################################
# 2. YouTube
#############################################################
print("2. YouTube")

# In[ ]:

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

# In[ ]:

# ! pip install yt_dlp
# ! pip install pydub


# **Note**: This can take several minutes to complete.

# In[ ]:

# url="https://www.youtube.com/watch?v=jGwO_UgTS7I"

# Required tasks - San Francisco Bay University MBA Student Spotlight: John Odebode
url="https://www.youtube.com/watch?v=kuZNIvdwnMc&ab_channel=SanFranciscoBayUniversity"

# Optional
# url1 = "https://www.youtube.com/@sanfranciscobayuniversity" # SFBU videos
# url2 = "https://www.youtube.com/results?search_query=SFBU" # SFBU
# url3 = "https://www.youtube.com/results?search_query=SFBU+DeepPiCar" # SFBU DeepPiCar
url4 = "https://www.youtube.com/watch?v=1gJcCM5G32k&ab_channel=SanFranciscoBayUniversity" # San Francisco Bay University: 10 Bay Area Activities
url5 = "https://www.youtube.com/watch?v=hZE5fT7CVdo&ab_channel=SanFranciscoBayUniversity" # San Francisco Bay University Campus Tour

save_dir="docs/youtube/"
links = [url, url4, url5]

for link in links:
    loader = GenericLoader(
        YoutubeAudioLoader([link],save_dir),
        OpenAIWhisperParser()
    )
    docs = loader.load()
    docs[0].page_content[0:500]


#############################################################
# 3. URLs
#############################################################
print("3. URLs")

# In[ ]:

from langchain_community.document_loaders import WebBaseLoader

# Required - Student Health Insurance
url = "https://www.sfbu.edu/admissions/student-health-insurance"

# Optional
url1 = "https://www.sfbu.edu/about-us" # About us
url2 = "https://www.sfbu.edu/admissions" # Admissions
url3 = "https://www.sfbu.edu/academics" # Academics
url4 = "https://www.sfbu.edu/student-life" # Student life
url5 = "https://www.sfbu.edu/contact-us" # Contact us

links = [url, url1, url2, url3, url4, url5]
for link in links:
    loader = WebBaseLoader(link)
    docs = loader.load()
    print(f"URL: {link}")
    print(docs[0].page_content[:500])

#############################################################
# 4. Notion
#
# - Notion is a really popular store of both personal
#   and company data, and a lot of people have created
#   chatbots talking to their Notion databases.
# - Follow steps [here](https://python.langchain.com/docs/modules/
# data_connection/document_loaders/integrations/notion) for an
# example Notion site such as [this one](https://yolospace.notion.
# site/Blendle-s-Employee-Handbook-
# e31bff7da17346ee99f531087d8b133f):
#
# - Duplicate the page into your own Notion space and
#   export as `Markdown / CSV`.
# - Unzip it and save it as a folder that contains the
#   markdown file for the Notion page.
#############################################################
print("4. Notion")

from langchain_community.document_loaders import NotionDirectoryLoader
loader = NotionDirectoryLoader("/home/koiisme/CS589/LangChain/DocumentLoading/Notion_DB")
docs = loader.load()


print(docs[0].page_content[0:200])
docs[0].metadata

