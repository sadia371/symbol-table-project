import re

TOKEN_PATTERNS = [
    ('KEYWORD', r'\b(int|float|char|string|if|else|while|for|return)\b'),
    ('NUMBER', r'\b\d+(\.\d+)?\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('OPERATOR', r'[+\-*/=<>!]'),
    ('STRING', r'".*?"'),
    ('SEPARATOR', r'[;,(){}]'),
    ('WHITESPACE', r'\s+'),
]