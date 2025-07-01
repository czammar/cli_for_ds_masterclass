from pydantic import BaseModel
from typing import Optional


class ChatbotResponseModel(BaseModel):
    """
    Request model for dictamination processing.

    Attributes:
        text (str):
            The input text to be processed.
        thread_id (Optional[str]):
            A unique identifier for the conversation thread. If None, a
            new thread may be created automatically.
    """
    text: str
    checkpointer_id: Optional[str] = None
