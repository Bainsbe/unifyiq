# Connector types
SLACK = "SLACK"
GOOGLE_DOCS = "GOOGLE_DOCS"

# Storage types
LOCAL = "LOCAL"
# S3 = "S3"
# GCS = "GCS"

CONNECTOR_TYPES = {SLACK, GOOGLE_DOCS}
SUPPORTED_STORAGE_TYPES = {LOCAL}
CONVERSATION_CONNECTORS = {SLACK}

# Search fields
TEXT = "text"
ID = "id"
SOURCE = "source"
EMBEDDINGS = "embeddings"
NORMALIZED_TEXT = "normalized_text"
DISTANCE = "DISTANCE"

NO_ANSWER = "Sorry, I don't have an answer"

MAX_ATTEMPTS_FOR_SLACK_API_CALL = 20
SKIP_INDEX_FILE_SUFFIX = ".skip"
