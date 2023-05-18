import glob
import pinecone
import os
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from decouple import AutoConfig

config = AutoConfig(search_path='../')


OPENAI_API_KEY = config('OPENAI_API_KEY')
PINECONE_API_KEY = config('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = config('PINECONE_ENVIRONMENT')
PINECONE_INDEX_NAME = config("PINECONE_INDEX_NAME")


def get_texts_from_markdown():
    for i in glob.glob("../Notion_DB/*.md"):
        loader = UnstructuredMarkdownLoader(i)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(data)
        print (f'We have {len(texts)} documents in our dataset.')
    return texts


def embed_and_store_texts(texts, index_name):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # initialize pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
    vectorstore = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=PINECONE_INDEX_NAME)
    print(f'Indexed {len(texts)} documents in Pinecone.')




if __name__ == "__main__":
    texts = get_texts_from_markdown()
    embed_and_store_texts(texts, PINECONE_INDEX_NAME)
