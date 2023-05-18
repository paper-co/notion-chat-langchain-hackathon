from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
import pinecone
import os
from dotenv import load_dotenv
load_dotenv('../.env')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
markdown_path = "../Notion_DB/Acquire Squad 6877998bca2c4a17acc9868e66704e0e.md"

def initialize_vectorstore():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
    vectorstore = Pinecone.from_existing_index(index_name=PINECONE_INDEX_NAME, embedding=embeddings)
    return vectorstore

# function to test similarity query against Pinecone
def query_vectorstore(query, vectorstore):
    docs = vectorstore.similarity_search(query)
    return docs

def ask_question(query, vectorstore):
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = vectorstore.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)
    return answer


if __name__ == "__main__":
    vectorstore = initialize_vectorstore()
    query = "When is the whole team meeting?"

    # Testing similarity search
    #docs = query_vectorstore(query, vectorstore)
    #print(docs[0].page_content)

    # Testing question answering
    answer = ask_question(query, vectorstore)
    print(answer)
