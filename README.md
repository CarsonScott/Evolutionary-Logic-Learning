RELA is an intelligent agent architecture that emulates the emphasizes the characteristics of [high-order cognitition](http://condor.depaul.edu/cwren/courses/other/outmn444/ch7think.htm) in humans.

### Symbolic Representation

The symbols '^' and '<' are logical connectives that correspond to conjunction and implication respectively. Each pair of opened/closed parentheses represents boundary points of a sub-expression, which may contain or be contained by other sub-expressions, giving rise to a containment hierarchy. 

    expression = "((a ^ b) < (c ^ d));" 
    memory = {'a':1,'b':1,'c':1,'d':1}
    
    function = generate(expression)
    output = function(memory)

function is equivalent to the previous example's function, and the same applies for the expression. This shows how we are able to construct and seemlessly move between symbolic and functional representations, a central theme that is important to the learning and adaptation processes of the system.

### Functional Representation

We can also build hierarchical structures with functions and translate them into expressions. All propositional functions are created using a constructor, which takes a label along with a data set and uses its elements to fill certain “slots” which are necessary to initialize a function of the specific type given by the label. For example, an implication function has two main elements, a premise and conclusion, which are extracted by the constructor and assigned to the new function. 

    premise = create('conjunction', ['a', 'b'])
    conclusion = create('conjunction', ['c', 'd'])
    template = create('implication', [left, right])

    function = convert(template)
    expression = express(function)

The expression given above is equivalent to the following: *if a and b are true, then c and d are true.* When the functional form of an implication gets called, it tests both the premise as well as the conclusion against a set of observations, allowing us not just to see whether a given implication is applicable, but also whether the following conclusion is reliable, i.e. tends to hold true over many observations. In this case our premise is true and our conclusion reliable, and therefore yields a truth value of 1.
