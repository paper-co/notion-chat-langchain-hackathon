//const PINECONE_INDEX_NAME = 'langchainjsfundamentals';
const PINECONE_INDEX_NAME = process.env.PINECONE_INDEX_NAME;

const PINECONE_NAME_SPACE = 'notion-chatgpt-langchain'; //namespace is optional for your vectors

export { PINECONE_INDEX_NAME, PINECONE_NAME_SPACE };
