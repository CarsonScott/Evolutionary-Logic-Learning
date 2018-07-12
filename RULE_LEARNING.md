# Inference Rules and Sequences

Inference rules are at the core of what it means to understand a language, as they give rise to additional knowledge that is not contained by any one element of a language but rather is derived through the interaction between those elements when they are composed in a sequence.

Inference-rule learning (IRL) is a two-step process by which a topology is constructed from observations of variables that are recorded over a finite period of time and then transformed into descriptive inferential functions. These functions reflect certain patterns discovered throughout the observation process, which are expressed in a first-order logical language called the metalogic.

The metalogical language is a construction language, used internally by systems to optimize the handling of complex data types. All   languages contain statements, which combine variable and function symbols in a specific sequence to generate models. Models represent low-level patterns, abstracted and transformed into more complex structures that carry more meaning than any one constituent. Preserving the grammar of lower-level structures in this way causes the inference rules to transfer upward and shape the grammar created at higher levels, because each new structure must necessarily satisfy the grammar at its own level before mapping to higher levels and causing influence elsewhere.


__Inference-Rule Example:__

    "if a and b and c, then infer d."
    
    (INFER, (a, b, c), d)
    
Inference rules allow complex functions to be described relatively simply, i.e. through sets of rules. The sequential nature of inference allows planning and prediction to yield models of future events. A RuleLearner is an agent that generates rules of inference based on sequential patterns related through time. Extending these rules to action allows behavior to be guided according to which action is best given in a current situation, 'best' meaning that which is likely to yield the most reward, with respect to predicted results of actions. 

# Game Rules and Actions

Agents who tend to make more accurate judgements about the world and themselves survive longer in competitive environments. Those that make use of knowledge more efficiently than others will likely outperform the competition, as a general rule of thumb. Evolving in a competitive environment yields a different kind of inference rule, specialized in predicting rewards/losses for itself and for others, as well as detecting when the goals of itself and others are mutually beneficial or mutually exclusive.   
