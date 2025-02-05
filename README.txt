# Overview
Enterprise Name Similarity Detector
Identifies potentially duplicate business names considering numeric differences and industry keywords

# Initial Setup
pip install jellyfish

# How to use
python deduplicator.py advertisers.txt output.txt [--threshold 0.99]

# Description
default is 0.99 which I think works the best.
1.00 for 100% Similarity and 0.99 accepte few typo. which I found there are plenty of typos(Maybe I am wrong, if not considering typos, we could just use 1.00).
I list some common business suffixes to ignore, we can add more.
Also ignoring same business name with diffrent numbers. eg. Mazda 3 and Mazda shouldn't consider duplicate.
Using jellyfish.jaro_winkler_similarity to calculate similarity score.

# Things to Improvement
Time Complexity, currently it is O(n^2), to improve that, we could 
1. Process paires concurrently
2. Skip pairs with large length differences
Better similarity,
1. add more common_subffixes
2. Add region keywords to ignore eg. brightsolid online publishing (US) Inc,  brightsolid online publishing (UK) Inc