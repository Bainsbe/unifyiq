import nltk

nltk.download('punkt')


def split_document_to_sentences(document):
    sentences = nltk.sent_tokenize(document)
    return sentences


def normalize(text):
    text = text.replace("\n", " ")
    text = text.replace("`", "")
    text = text.strip()
    text = text.lower()
    # pattern = r"<[^>]+>"
    # text = re.sub(pattern, "", text)
    # text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def add_space_if_not_empty(prev_context):
    if prev_context:
        return prev_context + " "
    return prev_context
