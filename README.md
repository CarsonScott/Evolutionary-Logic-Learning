# Evolutionary Logic Learning

[General Overview](https://signifiedorigins.wordpress.com/2018/06/03/1024/)

Evolutionary Logic Learning (ELL) is an unsupervised ML algorithm that uses a trial-and-error-based approach to learning recursive propositional functions. Each propostion is given by an expression, or a sentence in a formal language that, when interpreted, is said to be equivalent to a propositional function, which is either derived from or produces the expression depending on which representation comes first. In other words, any valid propositional function can be translated to a linguistic form and back, providing both concrete as well as abstract models of the proposition from which to derive judgements.
    
    expression = '((a ^ b) / (c ^ d));'
        
  
The symbols '^' and '/' are logical connectives that correspond to conjunction and implication respectively. Each pair of opened/closed parentheses represents boundary points of a sub-expression, which may contain or be contained by other sub-expressions, giving rise to  a containment hierarchy.

The propositional function can therefore be generated and executed over a given memory space:

    memory = {'a':1,'b':1,'c':1,'d':1}
    function = generate(expression)
    output = function(memory)
 
 yielding a truth value that proves whether an expression is accurate at the current time-step:  
    
__OUTPUT:__ `True`
