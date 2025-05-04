import re

TOKEN_TYPES = [
    ("CHUNK", r'chunk\d+'),
    ("TIME_SIGNATURE", r'TimeSignature=[0-9]+/[0-9]+'),
    ("TEMPO", r'Tempo=[0-9]+'),
    ("VOLUME", r'Volume=[0-9]+'),
    ("PIANO", r'Piano'),
    ("GUITAR", r'Guitar'),
    ("PAUSE", r'Pause'),
    ("LOOP", r'for'),
    ("SYNC", r'sync'),
    ("FRACTION", r'[0-9]+/[0-9]+'),  
    ("NUMBER", r'[0-9]+'),  
    ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'), 
    ("LBRACE", r'\{'),
    ("RBRACE", r'\}'),
    ("LPAREN", r'\('),
    ("RPAREN", r'\)'),
    ("COMMA", r','),
    ("EQUALS", r'='),
    ("LESS", r'<'),
    ("PLUS_EQUALS", r'\+='),
    ("SEMICOLON", r';'),
    ("WHITESPACE", r'[ \t\n]+'),  
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = self.tokenize()

    def tokenize(self):
        tokens = []
        for match in re.finditer(TOKEN_REGEX, self.text):
            token_type = match.lastgroup
            value = match.group()

            if token_type == "WHITESPACE":  # Ignore spaces and newlines
                continue

            tokens.append((token_type, value))
        
        tokens.append(("EOF", None))  # Add end of file token
        return tokens

    def next_token(self):
        return self.tokens.pop(0) if self.tokens else ("EOF", None)


# Example usage:
if __name__ == "__main__":
    code = """
    chunk1 {
        TimeSignature=4/4
        Tempo=120
        Volume=80
        Piano(R, do, 2/4)
        Piano(L, sol, 1/4)
        Piano(L, fa, 1/4)
        sync {
            Piano(R, re, 1/4)
            Piano(R, mi, 1/4)
        }
        for(note = do; note < sol; note+=1){
            Piano(R, note, 1/4)
        }
    }
    """
    lexer = Lexer(code)
    for token in lexer.tokens:
        print(token)
