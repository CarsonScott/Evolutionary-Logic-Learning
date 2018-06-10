# Rational Adaptive Learning Agent

RELA is an intelligent agent architecture that proposes lanuage as fundamentally tied to the motivational processes of low-level cognitive systems. Propositions defined by a linguistic structure feed into neural networks and change the goal characteristics (that is, variables determining whether certain outcomes are desirable), which alters the production of actions in order to move the current state toward some goal.

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


### Composite System
