from pydantic import BaseModel, Field, field_validator
from typing import Optional
from config.security_config import SecurityConfig

class ChatMessage(BaseModel):
    message: str = Field(...,
                         min_length=SecurityConfig.MIN_MESSAGE_LENGTH,
                         max_length=SecurityConfig.MAX_MESSAGE_LENGTH)
    context: Optional[str] = Field(None, max_length=SecurityConfig.MAX_LENGTH)

    @field_validator('message')
    def validate_message_content(cls, v):
        # Check for block keywords
        lower_message = v.lower()
        for keyword in SecurityConfig.BLOCKED_KEYWORDS:
            if keyword in lower_message:
                raise ValueError(f"Message contains prohibited content.")
        # Check for sensitive topics
        for category, terms in SecurityConfig.SENSITIVE_TOPICS.items():
            if any(term in lower_message for term in terms):
                raise ValueError(f"Message contains inappropriate content.")
        return v