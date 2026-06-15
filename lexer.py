import re
from tokken_patterns import TOKEN_PATTERNS


class LexicalAnalyzer:

    def __init__(self):
        self.tokens = []
        self.errors = []
        self.scope = 0

        # compile regex ONCE (optimization)
        self.compiled_patterns = [
            (t, re.compile(p)) for t, p in TOKEN_PATTERNS
        ]

    def reset(self):
        """Reset for new input run"""
        self.tokens = []
        self.errors = []
        self.scope = 0

    def tokenize(self, code):

        self.reset()

        lines = code.split('\n')

        for line_no, line in enumerate(lines, start=1):

            position = 0

            while position < len(line):

                match_found = False

                for token_type, regex in self.compiled_patterns:

                    match = regex.match(line, position)

                    if match:
                        lexeme = match.group(0)

                        # skip whitespace
                        if token_type == "WHITESPACE":
                            position = match.end()
                            match_found = True
                            break

                        # BRACES (scope handling)
                        if lexeme == "{":
                            self.scope += 1

                        elif lexeme == "}":
                            self.scope = max(0, self.scope - 1)

                        # store token
                        self.tokens.append({
                            "token": token_type,
                            "lexeme": lexeme,
                            "line": line_no,
                            "scope": self.scope
                        })

                        position = match.end()
                        match_found = True
                        break

                if not match_found:
                    self.errors.append(
                        f"Invalid token at line {line_no}: '{line[position]}'"
                    )
                    position += 1

        return self.tokens, self.errors