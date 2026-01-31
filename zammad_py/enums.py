from enum import Enum


class KnowledgeBaseAnswerPublicity(Enum):
    INTERNALLY = "internal"
    PUBLICLY = "publish"
    ARCHIVE = "archive"
    UNARCHIVE = "unarchive"
