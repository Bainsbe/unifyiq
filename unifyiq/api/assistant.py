from retrieval.query_open_ai import search_and_generate_prompt, generate_answer_from_llm
from utils.constants import NO_ANSWER


def skill_q_and_a(query):
    query_with_contexts = search_and_generate_prompt(query)
    print("----------------")
    print(query_with_contexts)
    result = NO_ANSWER
    if query_with_contexts == NO_ANSWER:
        return result
    result = generate_answer_from_llm(query_with_contexts)
    print("----------------")
    print(result)
    return result
