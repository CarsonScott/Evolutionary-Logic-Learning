# Function Language


### Overview

The function language is a compact scripting language that runs within python. The language revolves around four main phrase-structures that are used to express a strong fundamental logic. The four structures are listed below along with the corresponding script-code and a description of the logical process they represent.

__1. Function calls__

"f(x)"
		
	f(x)

__2. Variable Declarations__

"y=f(x)"

	y = f(x)

__2. If Statements__

"z: y=f(x)"

	if z:
		y = f(x)

__3. Else Statements__
		
"z: y=f(x) / y=g(x)"
	
		if z:
			y = f(x)
		else:
			y = g(x)


__4. If-Else Statements__

"z: y=f(x) /: h: y=g(x)"

		if x:
			y = f(x)
		elif h:
			y = g(x)
