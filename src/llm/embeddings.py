import os
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search

# Load model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    cache_folder='src/model_download_cache'
)
print(model)

# Read knowledge base into memory
passages = None
passages_details = None
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dax_functions_path = os.path.join(base_path, 'data', 'dax_functions.txt')
dax_functions_details_path = os.path.join(base_path, 'data', 'dax_functions_detailed.txt')
with open(dax_functions_path, 'r', encoding='utf-8') as file:
    passages = file.readlines()
with open(dax_functions_details_path, 'r', encoding='utf-8') as file2:
    passages_details = file2.readlines()


def get_top_k_results(queries: list[str], passages: list[str], top_k: int = 3) -> list[str]:
    """Get top k results using text embedding model.

    Args:
        queries (list[str]): Questions or queries to use to lookup.
        passages (list[str]): Possible results.
        top_k (int, optional): Number of results to return per query. Defaults to 3.

    Returns:
        list[str]: List of unique passages that best match the query, up to top_k matches per query.
    """
    input_texts = queries + passages
    embeddings = model.encode(input_texts, normalize_embeddings=True)
    query_embeddings = embeddings[:len(queries)]
    passage_embeddings = embeddings[len(queries):]
    search_results = semantic_search(query_embeddings, passage_embeddings, top_k=top_k)
    text_only_result_list = []
    for result in search_results:
        for result_match in result:
            if passages[result_match['corpus_id']] not in text_only_result_list:
                text_only_result_list.append(passages[result_match['corpus_id']])

    return text_only_result_list


def get_function_possibilities_from_question(question: str) -> str:
    """Get function possibilities from question using text embedding model.

    Args:
        question (str): Question to use to lookup.

    Returns:
        str: Function possibilities from question.
    """
    top_k_results = get_top_k_results([question], passages, top_k=10)
    detailed_results = []
    for result in top_k_results:
        for detailed_passage in passages_details:
            function_name = result.split(":")[0].strip()
            if detailed_passage.startswith(function_name):
                detailed_results.append(f"{result.strip()}. Additional information: {detailed_passage.strip()}")
                break

    return "\n".join(detailed_results)
