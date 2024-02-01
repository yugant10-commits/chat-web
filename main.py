from src.scrapper import ScrapeWebPage
from src.compressed_search import SimilarityCalculator
from src.vector_search import VectorSearch

if __name__ == '__main__':
    query="give me more information about sharad rai"
    url = "https://tai.com.np/"
    url_scrapper = ScrapeWebPage(url)
    url_list = url_scrapper.get_url()
    content = url_scrapper.get_page_contents(url_list = url_list)
    # print(content)
    # obj = SimilarityCalculator(context_list=content, query=query)
    # final_compute = obj._compute_distance()
    # results = obj.get_k_closest_result(k=2)
    # print(results)
    # print(results)
    vector_obj = VectorSearch(data=content, model_name="all-MiniLM-L6-v2")
    docs, metadatas = vector_obj._split_data()
    data_store = vector_obj._faiss_search()
    result = data_store.similarity_search(query)
    print(result)
    
    
    