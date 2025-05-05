# Parser Implementation
### Course: Formal Languages & Finite Automata
### Author: Amza Vladislav FAF-233
----

## Theory
A parser is a fundamental component in language processing systems that transforms a sequence of tokens (provided by a lexer) into a structured representation according to the grammar rules of a language. In the context of formal languages, a parser validates whether input strings belong to the language defined by the grammar and builds a corresponding syntax tree.

The parser I've implemented follows a recursive descent approach—a top-down parsing technique where the parser's structure directly mirrors the grammar's production rules. Each non-terminal symbol in the grammar is represented by a method that recognizes that particular construct. This implementation focuses on parsing a domain-specific language for musical notation, allowing composers to express musical ideas in a structured, programmable way.

## Objectives:
* Implement a recursive descent parser for a musical notation language
* Create an abstract syntax tree (AST) representation for further processing
* Support various musical constructs including instrument calls, loops, and synchronization
* Implement robust error detection and reporting for syntax violations
* Enable a foundation for music composition through programming

## Implementation description

### Parser Structure and Design Philosophy

The parser is designed around the principle of recursive descent, where each grammatical construct is handled by a dedicated method. This approach creates a clear mapping between the language grammar and the parser implementation, making the code intuitive and maintainable.

The main components of the parser include:
- Token consumption mechanism (`eat` method)
- Top-level chunk parsing
- Statement parsing for various constructs
- Specialized parsers for different musical elements

```python
def parse_statement(self):
    if self.current_token[0] in {"TIME_SIGNATURE", "TEMPO", "VOLUME"}:
        return self.parse_setting_statement()
    elif self.current_token[0] == "PIANO":
        return self.parse_instrument_call("PIANO")
    # Additional statement types...
```

This method acts as a dispatcher, examining the current token and delegating to specialized parsing methods based on the token type. This approach allows for clear separation of concerns and makes extending the language with new constructs straightforward.

### Musical Constructs Representation

The parser creates a structured representation of musical elements as nested dictionaries that form an abstract syntax tree (AST). This representation captures the hierarchical nature of musical composition, where pieces contain chunks, chunks contain statements, and statements may contain other statements (like in loops or sync blocks).

For example, a musical chunk is represented as a dictionary with a type identifier and a list of contained statements:

```python
{"type": "CHUNK", "statements": [...]}
```

This clean, hierarchical representation facilitates subsequent processing, whether for interpretation, code generation, or analysis.

### Handling Musical Elements

The parser handles several types of musical constructs:

1. **Settings** - Fundamental parameters that affect the entire musical piece, such as time signature, tempo, and volume. These are parsed as simple key-value pairs that apply to the surrounding context.

2. **Instrument Calls** - Commands that trigger specific instruments (like piano or guitar) with parameters including channel, note, and duration. These represent the actual sounds to be produced.

3. **Loops** - Control structures that allow repetition of musical phrases with variations. The parser captures the loop variable, its range, and the body of statements to be repeated, enabling complex patterns from simple expressions.

4. **Pauses** - Explicit moments of silence with specified durations, essential for proper musical phrasing.

5. **Synchronization Blocks** - Constructs that ensure multiple statements are executed simultaneously, allowing for chord structures and polyphonic arrangements.

### Error Handling Strategy

The parser implements robust error detection by verifying each token against expected types. When encountering unexpected tokens, it raises exceptions with detailed information about what was expected versus what was found:

```python
raise SyntaxError(f"Expected {token_type}, got {self.current_token}")
```

This approach provides clear feedback to users about syntax errors, making the language more accessible to music composers who may not have extensive programming experience.

### Parsing Process Flow

The parsing process follows a logical flow:

1. The parser begins by recognizing top-level chunks in the source code.
2. Within each chunk, it processes a sequence of statements.
3. Each statement is parsed according to its specific grammar rules.
4. Complex constructs like loops and sync blocks recursively parse their inner statements.
5. The process continues until reaching the end of file or encountering an error.

This structured approach ensures completeness in parsing the entire source while maintaining the grammatical integrity of each construct.

### Output

    [{'type': 'CHUNK', 'statements': [{'type': 'TIME_SIGNATURE', 'value': 'TimeSignature=4/4'}, {'type': 'TEMPO', 'value': 'Tempo=120'}, {'type': 'VOLUME', 'value': 'Volume=80'}, {'type': 'PIANO', 'identifier1': 'R', 'identifier2': 'do', 'fraction': '2/4'}, {'type': 'PIANO', 'identifier1': 'L', 'identifier2': 'sol', 'fraction': '1/4'}, {'type': 'PIANO', 'identifier1': 'L', 'identifier2': 'fa', 'fraction': '1/4'}, {'type': 'SYNC', 'statements': [{'type': 'PIANO', 'identifier1': 'R', 'identifier2': 're', 'fraction': '1/4'}, {'type': 'PIANO', 'identifier1': 'R', 'identifier2': 'mi', 'fraction': '1/4'}]}, {'type': 'LOOP', 'identifier': 'note', 'start_value': 'do', 'condition_value': 'sol', 'increment_value': '1', 'body': [{'type': 'PIANO', 'identifier1': 'R', 'identifier2': 'note', 'fraction': '1/4'}]}]}]

## Conclusions

The implemented parser successfully transforms musical notation code into a structured representation that captures the composers' intent. The recursive descent approach proved particularly effective for handling the hierarchical nature of musical composition, where elements can be nested within others.

Key achievements of this implementation include:

1. **Expressiveness**: The parser enables a wide range of musical expressions through various constructs like instrument calls, loops, and synchronization blocks.

2. **Extensibility**: The design allows for easy addition of new musical constructs and instruments without significant refactoring.

3. **Error Detection**: The implementation provides clear error messages that help users identify and fix syntax issues in their compositions.

4. **Hierarchical Representation**: The resulting AST preserves the structural relationships between musical elements, facilitating further processing.

This parser forms the foundation of a domain-specific language for music composition, bridging the gap between programming and musical expression. It demonstrates how formal language theory can be applied to create intuitive interfaces for creative endeavors.

Future enhancements could include support for additional musical constructs (like conditional execution based on musical context), more sophisticated error recovery mechanisms, and integration with sound synthesis systems to bring the parsed compositions to life.

## References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd Edition). Addison Wesley.
2. Cooper, K., & Torczon, L. (2011). Engineering a Compiler (2nd Edition). Morgan Kaufmann.
3. Grune, D., & Jacobs, C. J. (2007). Parsing Techniques: A Practical Guide (2nd Edition). Springer.
4. Scott, M. L. (2015). Programming Language Pragmatics (4th Edition). Morgan Kaufmann.
5. Parr, T. (2010). Language Implementation Patterns: Create Your Own Domain-Specific and General Programming Languages. Pragmatic Bookshelf.
