class SecurityConfig:
    # Input validation
    MAX_MESSAGE_LENGTH=2500
    MIN_MESSAGE_LENGTH=1
    BLOCKED_KEYWORDS = {
        'sql', 'exec', 'system', 'os.', 'subprocess',
        'rm -rf', 'format', 'delete', 'drop table'
    }

    # Content moderation
    SENSITIVE_TOPICS ={
        'explicit_content': ['porn', 'xxx', 'nsfw'],
        'hate_speech': ['hate', 'racist', 'discrimination'],
        'violence': ['kill', 'murder', 'attack'],
        'personal_info': ['ssn', 'credit card', 'passport']
    }

    # Output Validation
    MAX_RESPONSE_LENGTH=4096
    RESTRICTED_PATTERNS = [
        r'(?i)(password|secret|key):\s*\w+', # Sensitive data pattern
        r'(?i)(<script>|javascript:)', # XSS patterns
        r'(?i)(SELECT|INSERT|UPDATE|DELETE)\s+FROM' # SQL Patterns
    ]

    # Max Length
    MAX_LENGTH=500