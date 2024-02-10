from src.scrapper import ScrapeWebPage
from src.compressed_search import SimilarityCalculator
from src.vector_search import VectorSearch
from src.get_response import ResponseLLM
from src.ollama import OllamaGeneration

import streamlit as st

@st.cache_data()
def scrape_url(url):
    url_scrapper = ScrapeWebPage(url)
    url_list = url_scrapper.get_url()
    content = url_scrapper.get_page_contents(url_list = url_list)
    vector_obj = VectorSearch(data=content, model_name="all-MiniLM-L6-v2")

    return vector_obj


if __name__ == '__main__':
    st.set_page_config(page_title="Interweb Explorer", page_icon="🌐")
    # st.sidebar.image("img/ai.png")
    st.header("`Interweb Explorer`")
    st.info("`I am an AI that can answer questions by exploring, reading, and summarizing web pages."
        "I can be configured to use different modes: public API or private (no data sharing).`")

    # User input 
    url = st.text_input("`Please add a URL: `")
    question = st.text_input("`Ask a question:`")
    
    if url:
        vector_obj=scrape_url(url=url)
        

    if question:
        # Generate answer (w/ citations)
        # Write answer and sources
        answer = st.empty()
        docs, metadatas = vector_obj._split_data()
        data_store = vector_obj._faiss_search()
        result = data_store.similarity_search(question)
        context = result[0].page_content
        answer_response = ResponseLLM(
            context=context,
            question=question,   
        )._generate()
        # answer_response = OllamaGeneration(
        #     context=context,
        #     question=question, 
        #     model="llama2"  
        # )._generate()
        st.write(answer_response)
        # answer.info('`Answer:`\n\n' + result)s
        st.info(f'`Sources:`\n\n {result[0].metadata["source"]}')
    # print(result)


