# Evolutionary Logic Learning

Evolutionary Logic Learning is an intelligent agent architecture that assumes lanuage as fundamentally being tied to the motivational processes of lower-level cognition. Propositions defined by a linguistic structure feed into neural networks and change the goal characteristics (that is, variables determining whether certain outcomes are desirable), which alters the production of actions in order to move the current state toward some goal.

### Reinforcement System 

Inside the mind exists cognitive mappings that are not tied to any sensory or motor apparatus but are rather sparse distributions over internal spaces that are given by automated processes.

This is highly relevant to things like emotion and drive, but also deals with for example, measuring glucose levels in the blood. Automated regulatory mechanisms are built upon these functions, e.g. starting or stopping insulin production.
The mapping of various internal spaces can be used to direct attention. similar emotional states will produce similar thought processes, meaning concepts that typically occur during/around the same time of the internal response will naturally grow associated with that response. for example, a decrease in hunger is associated with the perceptual experience of eating.
If a particular response is understood as a goal, then the solution is likely to be related to the concepts with which that response is associated. A concept represents patterns of perceptual and/or behavioral information.
Concepts that are associated with goals become understood as goals, which map to other concepts that then also become goals and so on. therefore high-level concepts are endowed with motivational attitudes that stem from internal mechanisms.
At each level, goals increase the sensitivity of their solutions, making them easier to detect. each solution then makes all of the patterns with which it’s associated more sensitive as well. if one level’s solution is not effective, the next level’s solution becomes active.
Solutions are effective when the bias placed on the concepts allows those concepts to be realized, i.e. become active given a perceptual input. if some goal state shares too few associations with the real state, it will not become active. the motivational attitude toward that state remains the same, and thus the goal has not been met.
Because higher-level concepts relate disconnected patterns, the next level’s solution is more likely to be realized since it represents a particular context in which the low-level goal may be realized. the motivational attitude extends to the associated patterns of the high-level goal, and the context becomes a new goal.
The low-level goals now include various sub-goals of the context, directing motivational attitudes toward their solutions. This effectively overrides goals that are unfeasible with more general problems. General problems are typically easier to solve because they have more potential solutions and therefore more paths leading to success, making it more favorable as well as efficient.

### Proposition System

The symbols '^' and '<' are logical connectives that correspond to conjunction and implication respectively. Each pair of opened/closed parentheses in the exppresion represent boundary points of a sub-expression, which may contain or be contained by other sub-expressions, giving rise to a containment hierarchy. 

    expression = "((a ^ b) < (c ^ d));" 
    memory = {'a':1,'b':1,'c':1,'d':1}
    
    function = generate(expression)
    output = function(memory)
    
The expression means *if a and b are true, then c and d are true*, where it takes a premise *if a and b are true* and a conclusion *then c and b are true*. If the premise is true and the conclusion false, then the output is false. if the premise is true and the conclusion is true, the output is true. otherwise, the output is null.

We can also build hierarchical structures with functions and translate them into expressions. All propositional functions are created using a constructor, which takes a label along with a data set and uses its elements to fill certain “slots” which are necessary to initialize a function of the specific type given by the label. For example, an implication function has two main elements, a premise and conclusion, which are extracted by the constructor and assigned to the new function. 

    premise = create('conjunction', ['a', 'b'])
    conclusion = create('conjunction', ['c', 'd'])
    template = create('implication', [left, right])

    function = convert(template)
    expression = express(function)

The function is equivalent to the previous example's function, and the same applies for the expression. This shows how we are able to construct and easily move between symbolic and functional representations, a central theme that is important to the learning and adaptation processes of the system.


### Construction System

the systems learns to create by making observations of matrices that represent the identity of a given input. a matrix representing the possibility of a given input declares which elements must be present in order for a function to be valid. relationships between variables are defined by functions. identity and possibility matrices relate to one another in shape, that is, they have the same number of rows/vertices. shape equivalence allows for new matrices to be calculated by relating variables in difference ways. value equivalence, index equivalence, and type equivalence are the three core identity functions that produce an identity matrix for a given value.


matrix:
    
    shape equivalence

variable:

    type equivalence 
    value equivalence
    index equivalence


each form of equivalence results in a set of functions which, being declared valid, become available as an option to relate groups of variables. in other words, the possibilities that arise from an observation are related to an inherent validity given by the preprogrammed rules of inference. over time, the possibility matrices are learned such that observations of particular inputs give rise to the automatic retrieval of a certain pattern stored in memory. this is a learned inference rule whose validity is not inherent, in that it may be proven wrong given enough failed attempts, i.e. applications of inference in which the assumption led to error.

sets of relations over a given input are joined to form a generalization of the original pattern. by representing patterns in terms of relations, we reduce the calculations performed when testing its existence. only the variables in the original which exist as an input to a relation need to be stored in the new pattern, thereby reducing the input to a characteristic model. construction of a new pattern is driven by statistical calculations over groups of examples. decisions are based on probability spaces with assigned boundaries that determine subgrouping, allowing examples to be analyzed in terms of their model, 

identity matrices produced for high level patterns are given by rules, just like the previous level except for the fact that they are not necessarily true, and therefore fail under certain circumstances not unaccounted for by the current model. patterns are learned in a two step process: first, frequent groups of variables observed by the system over time are generated and stored in memory as a cluster. the subset of elements in a cluster then become subject to tests by the construction process, in which different computations are made both observational and behavioral, in which the former constitutes measurements on the subspace, and the latter involves potential relations between elements of the subspace. measurement naturally gives rise to consideration of potential actions,  due to the stream of knowledge produced by the inference rules, which yield specific relations in response to certain observed measurements on members of a group being compared.  


Equivalence Functions
    to_all (equal_to, to_all(get_type, X))  # Type equivalence
    to_all (equal_to, to_all(get_value, X)) # Value equivalence
    to_all (equal_to, to_all(get_index, X)) # Index equivalence



array (4 x 1), all equal to 0

    X = 4:0
    X = {0,0,0,0}

array with shape of X, all equal to 1

    Y = X:1
    Y = {1,1,1,1}

array with identity of X

    Z = :X
    Z = {0,0,0,0}

array with identity of X, shape of 2

    H = 2:X
    H = {0,0}

array with joint identity of X and Y

    G = X+Y
    G = {0,0,0,0,1,1,1,1}

matrix (X by Y)
    
    M = X:Y
      = {{1,1,1,1}, 
         {1,1,1,1}, 
         {1,1,1,1}, 
         {1,1,1,1}}


operations

    :X (identity of X)
    X: (shape of X)
    X+Y (union of X and Y)
    X:Y (matrix of X by Y)
    X~Y (congruence of X and Y)
    X=Y (equivalence of X and Y)
    X-Y (difference between X and Y)
    X/Y (overlap between X and Y)
    

relations

    X ~ Y (shape)
    X = Y (value)
    X / Y (intersection)
    X + Y (union)
    X - Y (compliment)
    

functions

    X = {1,0,0,1}
    Y = X:Not(X)
    Y = {0,1,1,0}
