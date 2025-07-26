from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

# Load .env variables for secure config management
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-8b-8192")

# Prompt template for two-line meme captions
prompt = PromptTemplate(
    input_variables=["error_log"],
    template="""Given this error log:
{error_log}
Write ONLY a witty meme caption in exactly two lines. Output ONLY two lines: the first line for the top text, and the second line for the bottom text. Do not return any explanation, quotes, or extra information."""
)
error_to_caption_chain = LLMChain(llm=groq_llm, prompt=prompt)

# Import FAISS utilities for modular search
from faiss_utils import load_template_tags, load_index, load_embedder, query_template

def load_faiss_resources(index_path="faiss_template.index", meta_path="templates/template_meta.json", model_name='all-MiniLM-L6-v2'):
    """Load all resources needed for error→template retrieval."""
    texts, filenames = load_template_tags(meta_path)
    embedder = load_embedder(model_name)
    index = load_index(index_path)
    return embedder, index, filenames

def select_template(error_log, embedder, index, filenames):
    """Given an error_log, select the best meme template filename."""
    return query_template(error_log, embedder, index, filenames)

# Uncomment below for quick standalone test
# if __name__ == "__main__":
#     embedder, index, filenames = load_faiss_resources()
#     test_log = "ValueError: Cannot convert string to float"
#     print(select_template(test_log, embedder, index, filenames))
#     print(error_to_caption_chain.run(error_log=test_log))
