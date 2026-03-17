import string

# ==========================================
# CORPUS WORD FREQUENCY ANALYZER
# ==========================================

# Setting up our empty storage containers
word_freq = {}          # Empty dictionary to store 'word: frequency' pairs
total_sentences = 0     # Counter for total sentences
total_words = 0         # Counter for total words
total_characters = 0    # Counter for the length of all words combined

input_file = "corpus.txt"
output_file = "results.txt"

# Using try-except to catch pathing errors and prevent the terminal from crashing. (happened before XD)
try:
    with open(input_file, "r", encoding="utf-8") as file:
        # Phase 1: Reading the corpus
        content = file.read()
        
        # Counting sentences since they end with '.','?','!'
        # Estimate sentences by counting end marks before we delete punctuation.
        total_sentences = content.count('.') + content.count('?') + content.count('!')
        
        # Phase 2: Normalizing the case
        content = content.lower()
        
        # Swapping hyphens and em dashes for a space to prevent merging words together. 
        # Preventing cases like faster-than-light -> fasterthanlight -> faster than light
        content = content.replace("-", " ").replace("—", " ")
        
        # Removing punctuation
        # Applying the rulebook to strip commas, quotes, etc.
        content = content.translate(str.maketrans("", "", string.punctuation))
        
        # Phase 3: Tokenization
        # Chopping the string into a list of individual words at the white spaces.
        words = content.split()
        
        # Phase 4: Counting (Word frequency, Sentence count, Average word length)
        for word in words:
            total_words += 1                
            total_characters += len(word)    
            
            # Dictionary frequency logic
            if word in word_freq:
                word_freq[word] += 1        
            else:
                word_freq[word] = 1          

except FileNotFoundError:
    print(f"\nERROR: Could not find '{input_file}'.")
    print("Make sure your VS Code terminal is opened directly to your project folder!")
    exit()

# Finding average word length
avg_word_length = 0
# Safe math check to prevent a ZeroDivisionError crash if the file is empty
if total_words > 0:
    avg_word_length = total_characters / total_words

# ==========================================
# PHASE 5: SORTING BY FREQUENCY
# ==========================================

# --- ADVANCED ALTERNATIVE (Lecture 9: Lambda) ---
# As discussed, Python can sort this in one line using a lambda function:
# frequency_list = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

# --- FOUNDATIONAL METHOD (Implemented Below) ---
# I chose to implement the manual list-packing method below to demonstrate 
# a step-by-step understanding of tuple unpacking and data manipulation:

frequency_list = [] # Create a brand new, ordered list

# Loop through the chaotic, unordered dictionary
for word, freq in word_freq.items():
    # Pack them into the new list, flipping the order to (Number, Word) 
    # because Python's sort() prioritizes the first element.
    # 'light': 5 becomes (5, 'light')
    frequency_list.append((freq, word))

# Numbers are now sitting in the very front (position 0),
# Python's basic sort tool will automatically organize them mathematically. 
# reverse=True flips it so the highest numbers stay at the top.
frequency_list.sort(reverse=True)

# ==========================================
# PHASE 6: OUTPUT & SAVING
# ==========================================

# Displaying top 20 words and saving the result to a new file
with open(output_file, "w", encoding="utf-8") as out:
    
    # Write the core statistics to the top of the file
    out.write("--- CORPUS ANALYSIS RESULTS ---\n")
    out.write(f"Total Sentences: {total_sentences}\n")
    out.write(f"Total Words: {total_words}\n")
    out.write(f"Average Word Length: {round(avg_word_length, 2)} characters\n\n")
    
    out.write("--- TOP 20 WORDS BY FREQUENCY ---\n")
    print("\n--- TOP 20 WORDS BY FREQUENCY ---")
    
    # SLICING & OUTPUTTING
    # Since the data is flipped to (Number, Word) earlier,
    # we must unpack it as 'freq, word' here so they match!
    for freq, word in frequency_list[0:20]:
        line = f"{word}: {freq}"
        
        print(line)             
        out.write(line + "\n")  

print(f"\nAnalysis complete! Full results successfully saved to '{output_file}'.")