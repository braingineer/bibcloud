---
layout: main
index: $~/posts/
title: "Too many features"
date: 2016-02-12
categories: gist logs
---

> This document details my plan to go from 6.7 million features to much less. 
It also details the flattening of the chains for classification-signal training and 
the heuristics for their subsequent pruning.


### Contents 
* TOC
{:toc}

### Current feature Sets
1. Our current feature set is:
    1. head word
    2. template
        - bracketed string with head word replaced with ""
    3. surface form
    4. surface form with empties
    5. children relationships
        - headword -> headword
2. What can I reduce?
    1. headword
        - i should keep this one. it reflects standard word embeddings. right?
    2. template
        - i used this as my argument it encodes the grammar. but does it?
    3. surface form
        - i was using this to capture the out of place word order
    4. surface form with empties
        - i was using this to capture arguments-to-come
    5. children relationships
        - this encodes graph structure. 
3. What are some alternatives?
    1. Using POS tags somehow
    2. Some sort of featurizing so that 

### Different datapoints
1. good paths
    - these were outputs from the CSG that had correct word order & unified to the predicates
2. bad paths
    - these were outputs from the CSG that didn't have the correct word order
    - the issue is that some of their subtrees DO have correct word order
    - there is usually a lot more of these than of the good paths. like 20-1 type disparity.


### Reduction methods
1. Sub sample the number of bad paths
    - we might also have to regenerate paths, this time only letting the timer kicked it out when there is at least one generated good parse
2. Reduce all features to just head words
    - this is an experiment I should run anyway
3. Reduce surface form to ngram context
    - though, isn't it already?
4. **Did this feb 11**: reduced the feature set to the first 3 features. 


### Other investigations
1. I should actually be counting the number of features by source. Why I didn't think of this, I dont know. 
    - Did this. I got these [logs](#output-from-feature-conversion)
    - Basically, this means that the 4th and 5th features are completely bogus. 
        + These are the word order and word order with empty-argument markers
    - Or rather, we'll never know because there's just simply too much .
    - so now I'm running it without these. 





### Appendix 

##### Output from feature conversion. 

```
Number of Features: 6714818 features [55:39, 1507.92 features/s]
Out of 9693530 path nodes
28847/28847 [55:39<00:00, 11.60it/s]
For feature type f1, we saw 7576 features 
For feature type f2, we saw 903 features
For feature type f3, we saw 24552 features
For feature type f4, we saw 3323584 features
For feature type f5, we saw 3358203 features
```
