# Evolutionary Logic Learning

[General Overview](https://signifiedorigins.wordpress.com/2018/06/03/1024/)

Evolutionary Logic Learning (ELL) is an unsupervised ML algorithm that uses a trial-and-error-based approach to learning recursive propositional functions. Each propostion is given by an expression, or a sentence in a formal language that, when interpreted, is said to be equivalent to a propositional function, which is either derived from or produces the expression depending on which representation comes first. In other words, any valid propositional function can be translated to a linguistic form and back, providing both concrete as well as abstract models of the proposition from which to derive judgements.

## Symbolic Representation

The symbols '^' and '<' are logical connectives that correspond to conjunction and implication respectively. Each pair of opened/closed parentheses represents boundary points of a sub-expression, which may contain or be contained by other sub-expressions, giving rise to  a containment hierarchy. The propositional function is generated by recursively translating each sub-expression at the lowest level to functional form, then again at the next level, and again until the root node containing the whole expression is reached and translated, resulting in a callable function that follows the same logic as the initial expression. We can now measure the effect of computing each function over a given input space. 


    expression = "((a ^ b) < (c ^ d));" 
    memory = {'a':1,'b':1,'c':1,'d':1}
    
    function = generate(expression)
    output = function(memory)
    
The expression given above is equivalent to the following: *if a and b are true, then c and d are true.* When the functional form of an implication gets called, it tests both the premise as well as the conclusion against a set of observations, allowing us not just to see whether a given implication is applicable, but also whether the following conclusion is reliable, i.e. tends to hold true over many observations. In this case our premise is true and our conclusion reliable, and therefore yields a truth value of 1.

## Functional Representation

We can also build hierarchical structures with functions and translate them into expressions. All propositional functions are created using a constructor, which takes a label along with a data set and uses its elements to fill certain “slots” which are necessary to initialize a function of the specific type given by the label. For example, an implication function has two main elements, a premise and conclusion, which are extracted by the constructor and assigned to the new function. 

    A = create('association', ['a', 'b'])
    B = create('association', ['c', 'd'])
    C = create('implication', [A, B])

    function = convert(C)
    expression = express(function)

The function is equivalent to the previous example's function, and the same applies for the expression. This shows how we are able to construct and seemlessly move between symbolic and functional representations, a central theme that is important to the learning and adaptation processes of the system.
