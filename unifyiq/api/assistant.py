from retrieval.query_open_ai import search_and_generate_prompt, generate_answer_from_llm
from utils.constants import NO_ANSWER

from utils.log_util import get_logger

logger = get_logger(__name__)


def skill_q_and_a(query):
    query_with_contexts = search_and_generate_prompt(query)
    logger.info("----------------")
    logger.info("Question: " + query)
    logger.info(query_with_contexts)
    result = NO_ANSWER
    if query_with_contexts == NO_ANSWER:
        return result

    try:
        result = generate_answer_from_llm(query_with_contexts)
    except BaseException as e:
        logger.error("Error calling LLM: {}".format(e))

    if NO_ANSWER in result:
        result = NO_ANSWER
    else:
        result = result.replace("SOURCE", "\n\nSOURCE")
        result = result.replace("Source", "\n\nSource")
    logger.info("----------------")
    logger.info("Result : " + result)
    logger.info("----------------")
    return result
