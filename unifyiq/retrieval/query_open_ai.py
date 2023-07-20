import os

import openai

from retrieval import semantic_search
from utils import log_util
from utils.configs import get_open_ai_api_key
from utils.constants import ID, SOURCE, TEXT, DISTANCE, NO_ANSWER

os.environ["TOKENIZERS_PARALLELISM"] = "false"
# get API key from top-right dropdown on OpenAI website
openai.api_key = get_open_ai_api_key()

limit = 7000


def generate_answer_from_llm(prompt):
    # query text-davinci-003
    res = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return res['choices'][0]['text'].strip()


def search_and_generate_prompt(query):
    top_k_results = semantic_search.semantic_search(query)
    logger = log_util.get_logger(__name__)
    logger.debug("Query: " + query)
    logger.debug(top_k_results)
    results = {}
    distance = {}
    for result in top_k_results:
        url = result[SOURCE]
        if url not in results:
            results[url] = []
            distance[url] = result[DISTANCE]
        if result[DISTANCE] > distance[url]:
            distance[url] = result[DISTANCE]
        results[url].append([result[ID], result[TEXT]])
    contexts = []
    sorted_urls = sorted(distance.items(), key=lambda x: x[1], reverse=True)
    for url, score in sorted_urls:
        texts = results[url]
        texts.sort(key=lambda x: x[0])
        context = ""
        for txt in texts:
            context += txt[1]
        context += "\nSOURCE: " + url + "\n"
        contexts.append(context)
    print("---------------")
    print(contexts)

    if len(contexts) == 0:
        return NO_ANSWER

    # build our prompt with the retrieved contexts included
    prompt_start = (
            f"Answer the question \"\"\"{query}\"\"\" only from the Context given below. Each context has a SOURCE."
            " Return the SOURCES that were used to answer at the end of the answer."
            f" And return '{NO_ANSWER}' if you can't find answer to the question from the given Context.\n\n" +
            "Context:\n"
    )
    prompt_end = (
        f"\nAnswer:"
    )
    context = "\n\n---\n\n".join(contexts)
    if len(context) > limit:
        for i in range(len(contexts) - 1, 0, -1):
            context = "\n\n---\n\n".join(contexts[:i - 1])
            if len(context) <= limit:
                break
    prompt = prompt_start + context + prompt_end
    return prompt
