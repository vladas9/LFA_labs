from lexer import Lexer
from parser import Parser
from interpreter import MusicInterpreter

# Main function to parse and interpret code
if __name__ == "__main__":
    # Path to the test file
    file_path = '/home/dima/Documents/LFA/lab6/test.test'
    
    # Step 1: Read the content of the file
    with open(file_path, 'r') as file:
        code = file.read()

    # Step 2: Tokenize the code using the lexer
    lexer = Lexer(code)
    
    # Step 3: Parse the tokens using the parser
    parser = Parser(lexer)
    parsed_data = parser.parse()
    
    # Step 4: Interpret the parsed data and generate audio
    interpreter = MusicInterpreter(parsed_data)
    interpreter.generate_music()
    
    # Optional: Export or play the audio
    # For example: Save the generated audio to a file
    interpreter.final_audio.export("output_music.mp3", format="mp3")
    print("Music generated and saved to output_music.mp3")
