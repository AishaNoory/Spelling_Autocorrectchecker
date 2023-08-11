#import libraries
import re
import collections
from collections import Counter
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from autocorrect import Speller 
#load and preprocess data
import chardet
def load_text_data(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    encoding = result['encoding']
    with open(file_path, 'r', encoding=encoding) as file:
        text = file.read()
    return text
text_data= load_text_data(r'C:\Users\aisha\Desktop\corpus\corpus.txt')
words= re.findall(r'\w+', text_data.lower())
word_counts=Counter(words)
#build a unigram model
def build_language_model(word_counts):
    total_words = sum(word_counts.values())
    probabilities = {word: count / total_words for word, count in word_counts.items()}
    return probabilities

language_model = build_language_model(word_counts)
def build_smoothed_language_model(word_counts, smoothing_factor=1):
    total_words = sum(word_counts.values())
    vocab_size = len(word_counts)
    probabilities = {word: (count + smoothing_factor) / (total_words + smoothing_factor * vocab_size) for word, count in word_counts.items()}
    return probabilities
#candidate generation and selection
def generate_candidates(word):
    # Generate candidate words by inserting, deleting, substituting, or transposing letters
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    inserts = [a + c + b for a, b in splits for c in letters]
    deletes = [a + b[1:] for a, b in splits if b]
    substitutes = [a + c + b[1:] for a, b in splits if b for c in letters]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    candidates = set(inserts + deletes + substitutes + transposes)
    return candidates

def autocorrect(word, language_model, n=5):
    if word in language_model:
        return [word]
    candidates = generate_candidates(word)
    suggestions = sorted(candidates, key=lambda w: language_model.get(w, 0), reverse=True)[:n]
    return suggestions
#input word and test_word definitions
# Test the system
test_words = ["droppe", "speling", "ocurr", "writting"]
for test_word in test_words:
    suggestions = autocorrect(test_word, language_model)
    print("Input:", test_word)
    print("Suggestions:", suggestions)

#GUI for the user


class AutocorrectGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Autocorrect System")

        self.create_widgets()

    def create_widgets(self):
        self.input_label = ttk.Label(self.root, text="Enter text:")
        self.input_label.pack()

        self.input_text = scrolledtext.ScrolledText(self.root, height=10, width=40)
        self.input_text.pack()

        self.suggestions_label = ttk.Label(self.root, text="Suggestions:")
        self.suggestions_label.pack()

        self.suggestions_text = tk.Text(self.root, height=5, width=40)
        self.suggestions_text.pack()

        self.correct_button = ttk.Button(self.root, text="Autocorrect", command=self.autocorrect)
        self.correct_button.pack()

    def autocorrect(self):
        input_text = self.input_text.get("1.0", "end-1c")
        autocorrected_text = self.autocorrect_text(input_text)
        self.suggestions_text.delete(1.0, "end")
        self.suggestions_text.insert("end", autocorrected_text)

    def autocorrect_text(self, text):
        # Implement your autocorrect logic here
        # For example, you can use the Speller class from the autocorrect library
        spell = Speller()
        autocorrected_text = " ".join(spell(word) for word in text.split())
        return autocorrected_text

if __name__ == "__main__":
    root = tk.Tk()
    app = AutocorrectGUI(root)
    root.mainloop()



