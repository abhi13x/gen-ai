from config.security_config import SecurityConfig
import re

class ResponseFilter:
    @staticmethod
    def filter_output(response: str) -> str:
        # Check response length
        if len(response) > SecurityConfig.MAX_RESPONSE_LENGTH:
            response = response[:SecurityConfig.MAX_RESPONSE_LENGTH] + "..."

        # Check for restricted patterns
        for pattern in SecurityConfig.RESTRICTED_PATTERNS:
            if re.search(pattern):
                response = re.sub(pattern, "[FILTERED]", response)
        return response