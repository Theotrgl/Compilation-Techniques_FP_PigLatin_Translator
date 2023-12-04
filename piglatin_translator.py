import nltk
nltk.download('words')

from nltk.corpus import words as nltk_words

class TokenType:
    WORD = 'WORD'
    PUNCTUATION = 'PUNCTUATION'
    EOF = 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        self.english_words = set(word.lower() for word in nltk_words.words())

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def word(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()  # Move to the next character
        if len(result) > 0:  # Ensure a valid word is captured before returning
            return result
        else:
            return ''

    def get_next_token(self):
        while self.current_char is not None:
            # print("Current character:", self.current_char)  # Debug statement
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                word = self.word()
                # print("Detected word:", word)  # Debug statement
                if word.lower() in self.english_words:
                    return Token(TokenType.WORD, word)

            if self.current_char in '.,?!':
                token_value = self.current_char
                self.advance()
                return Token(TokenType.PUNCTUATION, token_value)

            self.error()

        return Token(TokenType.EOF, None)

    def isalpha(self, char):
        return char.isalpha()

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def factor(self):
        token = self.current_token
        # print("Current token:", token.type, token.value)  # Debug statement
        if token.type == TokenType.WORD:
            translated_word = self.translate_word_to_pig_latin(token.value)
            # print("Translated word:", translated_word)  # Debug statement
            self.current_token = self.lexer.get_next_token()
            return translated_word
        elif token.type == TokenType.PUNCTUATION:
            self.current_token = self.lexer.get_next_token()
            return token.value


    def term(self):
        result = self.factor()

        while self.current_token.type == TokenType.PUNCTUATION:
            result += self.factor()

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type == TokenType.WORD:
            result += ' ' + self.term()

        return result

    def translate_word_to_pig_latin(self, word):
        vowels = ['a', 'e', 'i', 'o', 'u']
        if len(word) > 0 and word[0].lower() in vowels:
            return word + 'way'
        elif len(word) > 0:
            i = 0
            while i < len(word) and word[i].lower() not in vowels:
                i += 1
            return word[i:] + word[:i] + 'ay'
        else:
            return word  # Return the word as-is if it's empty


# text_to_translate = "Hello, this is a test sentence."
# lexer = Lexer(text_to_translate)
# parser = Parser(lexer)
# translated_text = parser.expr()
# print(translated_text)  # Output: "elloHay, isthay isway away esttay entencesay."




def main():
    while True:
        try:
            text = input('Enter English text: ')
        except EOFError:
            break

        if not text:
            continue
        elif text.lower() == "exit":
            break
            

        lexer = Lexer(text)
        parser = Parser(lexer)
        translated_text = parser.expr()
        print('Pig Latin Translation:', translated_text)

if __name__ == '__main__':
    main()
