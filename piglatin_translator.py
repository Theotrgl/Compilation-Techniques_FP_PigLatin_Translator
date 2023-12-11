import nltk
nltk.download('words')

from nltk.corpus import words as nltk_words

#Defines the types of tokens that are accepted in the translator
class TokenType:
    WORD = 'WORD'
    NUMBER = 'NUMBER'
    PUNCTUATION = 'PUNCTUATION'
    EOF = 'EOF'

#Initializes each identifier as a member of the Token class
#Meaning each identifier is assigned a token type
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

#Lexer class to define logic of tokenizing process
class Lexer:
    #initializes important variables for current text such as current char position and defining set of valid english words from the nltk corpus
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        self.english_words = set(word.lower() for word in nltk_words.words())

    #Function to increment char position by 1 and read the next identifier
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    #Define bundle of identifier as word
    def word(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        if len(result) > 0:  # Ensure a valid word is captured before returning
            return result
        else:
            return ''

    #Define bundle of identifier as number
    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result if result else None

    #Main lexer function which integrates other functions into one that reads the input text and iterates each char.
    #Detecting words, numbers, punctuations, EOF, and skipping whitespaces .
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                word = self.word()
                if word.lower() in self.english_words:
                    return Token(TokenType.WORD, word)

            if self.current_char.isdigit():
                num = self.number()
                if num:
                    return Token(TokenType.NUMBER, num)

            if self.current_char in '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~':
                token_value = self.current_char
                self.advance()
                return Token(TokenType.PUNCTUATION, token_value)

            self.error()

        return Token(TokenType.EOF, None)

    #Utilize isalpha function to constrain char as alphabet
    def isalpha(self, char):
        return char.isalpha()
    
    #Error handling
    def error(self):
        raise Exception('Invalid syntax')

#Parser class to define logic of converting english to pig latin 
class Parser:
    #Initializing important variables such as creating lexer class for inputted text and utilizing get_next_token() function to get current token
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')
    
    #Function that handles which action to be taken for each token types 
    def factor(self):
        token = self.current_token
        
        #Checks the token type of the current token
        if token.type == TokenType.WORD:
            #Translate word tokens using translate_word_to_pig_latin() function
            translated_word = self.translate_word_to_pig_latin(token.value)
            self.current_token = self.lexer.get_next_token()
            return translated_word
        elif token.type == TokenType.NUMBER:
            # For numbers, just return the number itself
            num = token.value
            self.current_token = self.lexer.get_next_token()
            return num
        elif token.type == TokenType.PUNCTUATION:
            self.current_token = self.lexer.get_next_token()
            return token.value

    #Defining what constitutes as a term
    def term(self):
        result = self.factor()

        while self.current_token.type == TokenType.PUNCTUATION:
            result += self.factor()

        return result

    #Define what constitues an expression
    def expr(self):
        result = self.term()

        while self.current_token.type == TokenType.WORD or self.current_token.type == TokenType.NUMBER:
            result += ' ' + self.term()

        return result

    #Function to translate words into pig latin using formula
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

#Main loop
def main():
    while True:
        try:
            #Ask user input
            text = input('Enter English text: ')
        except EOFError:
            print("No input detected")
            break
        
        #Set conditional to exit on the input "exit"
        if not text:
            continue
        elif text.lower() == "exit":
            break
        
        #Implement Previously mentioned classes
        lexer = Lexer(text)
        parser = Parser(lexer)
        translated_text = parser.expr()
        print('Pig Latin Translation:', translated_text)

if __name__ == '__main__':
    main()
