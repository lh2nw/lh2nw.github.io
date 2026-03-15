import string
from collections import Counter


def get_word_frequency(text):
    # 1. Ignore punctuation and capitalization
    # Create a translator to remove all punctuation
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text.translate(translator).lower()

    # Split the text into individual words
    words = clean_text.split()

    # 2. Store the results in a dictionary {word: count}
    # Counter is a specialized dictionary designed specifically for this task
    word_counts = Counter(words)

    # 3. Output the top 5 most frequent words as a list of tuples
    # most_common(5) returns a list of tuples sorted by frequency descending
    top_5 = word_counts.most_common(5)

    return dict(word_counts), top_5


# Example Usage:
sample_text = """
Physics is great. Physics is fun! Learning physics is 
a journey, and this journey is often a long one.
"""

full_dict, top_words = get_word_frequency(sample_text)

print("Full Dictionary:")
print(full_dict)
print("\nTop 5 Most Frequent:")
print(top_words)