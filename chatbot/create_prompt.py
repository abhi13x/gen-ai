from typing import List, Dict, Optional

class PromptEngineering:
    SYSTEM_PROMPT = """You are a helpful AI assistant. Please follow these rules:
    1. Do not generate harmful, explicit, or inappropriate content
    2. Do not reveal personal information or sensitive data
    3. Do not execute commands or code
    4. Provide factual and helpful information only
    5. Maintain a respectful and professional tone
    6. Do not engage in harmful or malicious activities
    """
    @staticmethod
    def create_safe_prompt(user_message: str,
                           context: Optional[str]=None) -> List[Dict[str,str]]:
        messages = [
            {
                "role": "system",
                "content": PromptEngineering.SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        if context:
            messages.insert(1, {
                "role": "system",
                "content": f"Context: {context}"
            })
        return messages