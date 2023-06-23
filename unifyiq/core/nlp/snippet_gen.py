import json
import pickle

from utils.constants import CONVERSATION_CONNECTORS, ID, SOURCE, TEXT, NORMALIZED_TEXT, EMBEDDINGS
from core.nlp.sentence_transformer_embeddings import SentenceTransformerEmbeddings
from utils.file_utils import get_fetcher_output_path_from_config, get_jsonl_files, get_core_output_path_from_config
from utils.text_utils import add_space_if_not_empty, normalize

THREE_HOURS_IN_SECONDS = 3 * 60 * 60


def add_to_snippets(anchor_id, anchor_url, text, normalized_text, snippets, conversations, anchor_index,
                    prev_anchor_index, prev_snippet_overlap_word_count):
    # Go back to find the previous snippet to provide context
    context_wc = 0
    prev_context = ""
    normalized_prev_context = ""
    for j in range(anchor_index - 1, prev_anchor_index - 1, -1):
        context_wc += conversations[j][5]
        if context_wc > prev_snippet_overlap_word_count:
            for k in range(j + 1, anchor_index):
                prev_context = add_space_if_not_empty(prev_context) + conversations[k][3]
                normalized_prev_context = add_space_if_not_empty(normalized_prev_context) + conversations[k][4]
            break
    prev_context = prev_context.strip()
    normalized_prev_context = normalized_prev_context.strip()
    snippets[ID].append(anchor_id)
    snippets[SOURCE].append(anchor_url)
    snippets[TEXT].append(add_space_if_not_empty(prev_context) + text)
    snippets[NORMALIZED_TEXT].append(add_space_if_not_empty(normalized_prev_context) + normalized_text)


def build_snippets(conversations, max_snippet_word_count, prev_snippet_overlap_word_count, snippets):
    conversations.sort(key=lambda x: x[0])
    anchor_start_time = conversations[0][0]
    anchor_id = conversations[0][1]
    anchor_url = conversations[0][2]
    snippet = conversations[0][3]
    normalized_snippet = conversations[0][4]
    norm_snippet_wc = conversations[0][5]
    anchor_index = 0
    prev_anchor_index = 0
    for i in range(1, len(conversations)):
        projected_wc = norm_snippet_wc + conversations[i][5]
        if conversations[i][0] - anchor_start_time > THREE_HOURS_IN_SECONDS or projected_wc > max_snippet_word_count:

            add_to_snippets(anchor_id, anchor_url, snippet, normalized_snippet, snippets, conversations, anchor_index,
                            prev_anchor_index, prev_snippet_overlap_word_count)
            # Start new snippet
            prev_anchor_index = anchor_index
            anchor_index = i
            anchor_start_time = conversations[i][0]
            anchor_id = conversations[i][1]
            anchor_url = conversations[i][2]
            snippet = conversations[i][3]
            normalized_snippet = conversations[i][4]
            norm_snippet_wc = conversations[i][5]
        else:
            snippet += " " + conversations[i][3]
            normalized_snippet += " " + conversations[i][4]
            norm_snippet_wc += conversations[i][5]
    # add last snippet
    if len(snippet) > 0:
        add_to_snippets(anchor_id, anchor_url, snippet, normalized_snippet, snippets, conversations, anchor_index,
                        prev_anchor_index, prev_snippet_overlap_word_count)
    return snippets


def process_documents(input_files, embeddings_generator, output_path):
    pass


def process_short_conversations(input_files, embeddings_generator, output_path):
    grouped_text = {}
    for file in input_files:
        with open(file, 'r') as f:
            for line in f:
                json_data = json.loads(line)
                if json_data['group'] not in grouped_text:
                    grouped_text[json_data['group']] = []
                group_conversations = grouped_text[json_data['group']]
                norm_curr_conv = normalize(json_data['text'])
                norm_curr_conv_wc = len(norm_curr_conv.split())
                group_conversations.append((json_data['created_at'], json_data['id'], json_data['url'],
                                            json_data['text'], norm_curr_conv, norm_curr_conv_wc))
        f.close()
    snippets = {ID: [], SOURCE: [], TEXT: [], NORMALIZED_TEXT: [], EMBEDDINGS: []}
    with open(f'{output_path}/embeddings.pkl', "wb") as fOut:
        for group, conversations in grouped_text.items():
            build_snippets(conversations, embeddings_generator.get_word_count(),
                           embeddings_generator.get_prev_snippet_overlap_word_count(), snippets)
        embeddings = embeddings_generator.get_embeddings(snippets[NORMALIZED_TEXT])
        snippets[EMBEDDINGS] = embeddings
        pickle.dump(snippets, fOut, protocol=pickle.HIGHEST_PROTOCOL)
    print("SNIPPET SIZE:" + str(len(snippets[ID])))
    fOut.close()


def update_embeddings(config, version):
    """
    Update embeddings in vector store
    :param config: Config object
    :param version: Date in format YYYY-MM-DDTHH:00:00
    :return:
    """
    fetcher_output_path = get_fetcher_output_path_from_config(config, version)
    input_files = get_jsonl_files(fetcher_output_path)
    embeddings_gen = SentenceTransformerEmbeddings()
    output_path = get_core_output_path_from_config(config, version)
    if config.connector_type in CONVERSATION_CONNECTORS:
        # Short conversations. Cluster to form snippets
        process_short_conversations(input_files, embeddings_gen, output_path)
        pass
    else:
        # Long conversations. Chunk to form snippets
        process_documents(input_files, embeddings_gen, output_path)
        pass
