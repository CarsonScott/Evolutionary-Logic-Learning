# Evolutionary Logic Learning

[General Overview](https://signifiedorigins.wordpress.com/2018/06/03/1024/)

Evolutionary Logic Learning (ELL) is an unsupervised ML algorithm that uses a trial-and-error-based approach to learning recursive propositional functions. Each propostion is given by an expression, or a sentence in a formal language that, when interpreted, is said to be equivalent to a propositional function, which is either derived from or produces the expression depending on which representation comes first. In other words, any valid propositional function can be translated to a linguistic form and back, providing access to both concrete as well as abstract representations for any given proposition.

__EXAMPLE:__ *Expressing propositional functions with a formal language*

firsy we write an expression to translate the following proposition in natural language to a valid expression:
*"if A and B are true, then C and D are also true."*

A translation is given by the expression below:

    
    expression = "((A ^ B) < (C ^ D));"
        
  
expressions are strings of symbols that represent certain objects in memory, namely logical templates and relations along with non-logical elements or variables that are observed from a given input space. in the expression above, we signify 4 variables, A,B,C and D, which we then combine using relations ^ and <, wherein a substructure exists for each relation between two every pairs of objects, resulting in 3 structures areanged in a hierarchy. Those at the lowest level are given by atomic formulas, and contain no sub-structures. 



The relation symbols ^ and < correspond to conjunction and implication respectively. every structure contains an open and close boundary points of a sub-expression, which may contain or be contained by other sub-expressions, giving rise to  a containment hierarchy. The proposition is be generated from the expression and executed given a memory space:

    memory = {'A':1,'B':1,'C':1,'D':1}
    function = generate(expression)
    output = function(memory)
 
 yielding a truth value that proves whether an expression is accurate at the current time-step:  
    
__OUTPUT:__ `True`
