class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.current_token = self.lexer.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")

    def parse_chunk(self):
        # Start a new chunk node in the tree
        self.eat("CHUNK")
        self.eat("LBRACE")
        chunk_data = self.parse_statements()  # Get the statements inside this chunk
        self.eat("RBRACE")
        return {"type": "CHUNK", "statements": chunk_data}

    def parse_statements(self):
        statements = []
        while self.current_token and self.current_token[0] not in {"RBRACE"}:
            statement = self.parse_statement()
            statements.append(statement)
        return statements

    def parse_statement(self):
        if self.current_token[0] in {"TIME_SIGNATURE", "TEMPO", "VOLUME"}:
            return self.parse_setting_statement()
        elif self.current_token[0] == "PIANO":
            return self.parse_instrument_call("PIANO")
        elif self.current_token[0] == "LOOP":
            return self.parse_loop()
        elif self.current_token[0] == "PAUSE":  # ✅ Add this case
                return self.parse_pause()
        elif self.current_token[0] == "GUITAR":  # ✅ Handle Guitar
            return self.parse_instrument_call("GUITAR")
        elif self.current_token[0] == "SYNC":
            return self.parse_sync_block()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token}")

    def parse_setting_statement(self):
        statement_type = self.current_token[0]
        value = self.current_token[1]
        self.eat(statement_type)  # Consume the setting token
        return {"type": statement_type, "value": value}


    def parse_pause(self):
        self.eat("PAUSE")
        self.eat("LPAREN")
        duration = self.current_token[1]  
        self.eat("FRACTION")
        self.eat("RPAREN")
        return {"type": "PAUSE", "duration": duration}

    def parse_instrument_call(self, instrument_type):
        self.eat(instrument_type)
        self.eat("LPAREN")
        identifier1 = self.current_token[1]  # Left/Right Channel (L/R)
        self.eat("IDENTIFIER")
        self.eat("COMMA")
        identifier2 = self.current_token[1]  # Note (do, mi, sol, etc.)
        self.eat("IDENTIFIER")
        self.eat("COMMA")
        fraction = self.current_token[1]  # Duration (1/8, 1/4, etc.)
        self.eat("FRACTION")
        self.eat("RPAREN")
        
        return {
            "type": instrument_type,
            "identifier1": identifier1,
            "identifier2": identifier2,
            "fraction": fraction
        }

    def parse_loop(self):
        self.eat("LOOP")
        self.eat("LPAREN")
        
        # Extract the loop variable (e.g., 'note') and its initialization (e.g., 'do')
        loop_data = {
            "identifier": self.current_token[1],  # 'note'
        }
        self.eat("IDENTIFIER")  # 'note'
        self.eat("EQUALS")
        
        # Capture the value assigned to 'note', e.g., 'do'
        loop_data["start_value"] = self.current_token[1]  # 'do'
        self.eat("IDENTIFIER")  # 'do'
        
        self.eat("SEMICOLON")
        
        # Extract the loop condition (e.g., 'note < sol')
        self.eat("IDENTIFIER")  # 'note'
        self.eat("LESS")
        
        # Capture the value being compared to 'note', e.g., 'sol'
        loop_data["condition_value"] = self.current_token[1]  # 'sol'
        self.eat("IDENTIFIER")  # 'sol'
        
        self.eat("SEMICOLON")
        
        # Extract the increment (e.g., 'note += 1')
        self.eat("IDENTIFIER")  # 'note'
        self.eat("PLUS_EQUALS")
        
        # Ensure the increment value is either an identifier or a number
        if self.current_token[0] in {"IDENTIFIER", "NUMBER"}:
            loop_data["increment_value"] = self.current_token[1]
            self.eat(self.current_token[0])  # Consume the increment value
        else:
            raise SyntaxError(f"Expected IDENTIFIER or NUMBER for increment, got {self.current_token}")
        
        self.eat("RPAREN")
        self.eat("LBRACE")
        
        # Parse the statements inside the loop body
        loop_data["body"] = self.parse_statements()
        self.eat("RBRACE")
        
        return {"type": "LOOP", **loop_data}

    def parse_sync_block(self):
        self.eat("SYNC")
        self.eat("LBRACE")
        sync_data = self.parse_statements()  # Sync block statements
        self.eat("RBRACE")
        return {"type": "SYNC", "statements": sync_data}

    def parse(self):
        print("Starting parsing...")
        parsed_chunks = [] 

        while self.current_token and self.current_token[0] != "EOF":  # Loop over chunks
            print(f"Parsing chunk starting with: {self.current_token}")  # Debugging
            chunk = self.parse_chunk()  
            parsed_chunks.append(chunk) 
            print("Chunk successfully parsed!\n") 
        
        if self.current_token and self.current_token[0] == "EOF":
            print("Reached EOF. Parsing complete!") 
            print(f"Parsed structure:\n{parsed_chunks}") 
            return parsed_chunks  

        raise SyntaxError(f"Unexpected token {self.current_token}")  # ❌ Error if anything extra
