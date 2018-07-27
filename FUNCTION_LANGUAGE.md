# Function Language


### Overview

The function language is a compact scripting language that runs within python. The language revolves around four main phrase-structures that are used to express a strong fundamental logic. The four structures are listed below along with the corresponding script-code and a description of the logical process they represent.

__1. Function calls__

		"f(x)"	

- passes x (variable) to f (function).


__2. If Statements__

		"x:y"
- executes x (statement) given y (condition).


__3. Else Statements__
		
		"x:y/z"
- executes x (statement) given y (condition),
  otherwise executes z (statement).

__4. If-Else Statements__

		"x:y /: a:b"
- executes x (statement) given y (condition), 
  otherwise executes a (statement) given b (condition).

### Example

Each statement in the language is defined by a dictionary structure with additional functionality for parsing and executing script-code. Statements built using a class called Function.