class Symbol:
    def __init__(self, index, token, lexeme, line_no, scope):
        self.index = index
        self.token = token
        self.lexeme = lexeme
        self.line_no = line_no
        self.scope = scope


class SymbolTable:

    def __init__(self):
        self.entries = []
        self.counter = 1

    def insert(self, token, lexeme, line_no, scope):

        symbol = Symbol(
            self.counter,
            token,
            lexeme,
            line_no,
            scope
        )

        self.entries.append(symbol)
        self.counter += 1

    def get_table(self):

        return [
            {
                "Index": s.index,
                "Token": s.token,
                "Lexeme": s.lexeme,
                "Line": s.line_no,
                "Scope": s.scope
            }
            for s in self.entries
        ]