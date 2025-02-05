import argparse
import re
import itertools
import jellyfish

# List of common business suffixes to ignore
COMMON_SUFFIXES = {"inc", "llc", "ltd", "corp", "company", "co", "com", "llp", "plc"}

def normalize(name):
    """
    Simplifies a company name by:
    - Converting it to lowercase
    - Removing special characters
    - Trim common suffixes (e.g., 'Inc', 'LLC')
    """
    name = re.sub(r"[^a-z0-9]", "", name.lower())  # Keep only numbers and characters
    for suffix in COMMON_SUFFIXES:
        name = re.sub(rf"{suffix}$", "", name)  # Trim common suffixes
    return name

def has_fundamental_conflict(name1, name2):
    """Determines if two names have fundamental differences"""
    # Numeric must match
    num_set1 = set(re.findall(r'\d+', name1))
    num_set2 = set(re.findall(r'\d+', name2))
    return num_set1 != num_set2

def identify_similar_entities(name_list, similarity_threshold=0.99):
    """
    Finds similar names using Jaro-Winkler similarity, 
    skipping conflicting ones.
    """
    processed_names = [(name, normalize(name)) for name in name_list]
    matched_pairs = []
    
    # Compare all unique combinations
    for (orig_name1, clean_name1), (orig_name2, clean_name2) in itertools.combinations(processed_names, 2):
        if orig_name1 == orig_name2: continue  # Skip identical names
        if has_fundamental_conflict(orig_name1.lower(), orig_name2.lower()): continue
        
        similarity_score = jellyfish.jaro_winkler_similarity(clean_name1, clean_name2)
        if similarity_score >= similarity_threshold:
            matched_pairs.append( (orig_name1, orig_name2, similarity_score) )
    
    # Sort by similarity
    return sorted(matched_pairs, key=lambda x: x[2], reverse=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--threshold", type=float, default=0.99)
    args = parser.parse_args()
    
    # Read input names, stripping empty lines
    with open(args.input, "r", encoding="utf-8") as f:
        names = [line.strip() for line in f if line.strip()]
    
    # Get potential duplicates
    results = identify_similar_entities(names, args.threshold)
    
    # Write output file
    with open(args.output, "w", encoding="utf-8") as f:
        for a, b, score in results:
            f.write(f"Similarity {score:.2f}:\n{a}\n{b}\n\n")

if __name__ == "__main__":
    main()