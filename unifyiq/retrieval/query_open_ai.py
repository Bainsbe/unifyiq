import os

import openai

from retrieval import semantic_search
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

    results = {}
    distance = {}
    for result in top_k_results:
        url = result[SOURCE]
        if url not in results:
            results[url] = []
            distance[url] = result[DISTANCE]
        if result[DISTANCE] < distance[url]:
            distance[url] = result[DISTANCE]
        results[url].append([result[ID], result[TEXT]])
    contexts = []
    sorted_urls = sorted(distance.items(), key=lambda x: x[1])
    for url, score in sorted_urls:
        texts = results[url]
        texts.sort(key=lambda x: x[0])
        context = ""
        for txt in texts:
            context += txt[1]
        context += "SOURCE: " + url + "\n"
        contexts.append(context)
    print("---------------")
    print(contexts)

    if len(contexts) == 0:
        return NO_ANSWER

    # build our prompt with the retrieved contexts included
    prompt_start = (
            "Answer the question based on the Context given below. Each context has a SOURCE."
            "Return the csv list of SOURCE urls from the context at the end of the answer. Answer in 3 paragraphs"
            f"And return '{NO_ANSWER}' only if you can't find any answer in the context.\n\n" +
            "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
    context = "\n\n---\n\n".join(contexts)
    if len(context) > limit:
        for i in range(len(contexts) - 1, 0, -1):
            context = "\n\n---\n\n".join(contexts[:i - 1])
            if len(context) <= limit:
                break
    prompt = prompt_start + context + prompt_end
    return prompt