import string
import collections
import sys

# Create 32x32 confusion matrix for insertion, deletion, substitution and transposition
rows, cols = (32, 32)
insertion_matrix = [[0 for i in range(cols)] for j in range(rows)]
deletion_matrix = [[0 for i in range(cols)] for j in range(rows)]
substitution_matrix = [[0 for i in range(cols)] for j in range(rows)]
transposition_matrix = [[0 for i in range(cols)] for j in range(rows)]

# This part take input from user
first_input = sys.argv[1]  # First input is corpus
second_input = sys.argv[2]  # Second input is spell-errors, this txt file create confusion matrix
third_input = sys.argv[3]  # Third input is to be corrected file
fourth_input = sys.argv[4]  # Fourth input is determine smooth or non-smooth

# This function take one word and determine all words with one edit distance to it and if these
# words in the file, add list to these words and return it.
def edit_distance_word(d, word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    edit_list = set(deletes + transposes + replaces + inserts)
    return_list=[]
    for w in edit_list:
        if w in d:
            return_list.append(w)
    return return_list

def find_max(filename, i, list):
    if len(list) == 0:  # If the length of the list is 0, return empty string
        return " "
    if len(list) == 1:  # If the length of the list is 1, return this element
        return list[0]
    new_int_list = []  # Create new list for write the usage rate of the words
    if len(list) > 1:  # If the length of the list is more than 1, determine usage rate one by one
        for w in list:
            ratio = return_ratio_of_word_in_dict(d, w)  # Determine the usage rate of the word in corpus
            returning_list = determine_operation(i, w)  # Determine the needed operation from i to w
            if returning_list is None:  # If do not need any operation, add 0 to list
                new_int_list.append(0)
            else:
                if returning_list[0] == "substitution":  # If substitution need look substitution confusion matrix
                    # in needed row and col which we can reach using determine operation
                    row, col = find_ascii(returning_list[1], returning_list[2])
                    num1 = substitution_matrix[row][col]
                    num2 = return_num_of_letter_in_dict(filename, returning_list[1])
                    if num2 == 0 and fourth_input == "nonsmooth":  # If we do not use smoothing, calculate like this
                        num2 = 1000000
                    elif num2 == 0 and fourth_input == "smooth":  # If we use smoothing, calculate like this
                        num1 = num1+1
                        num2 = num2+26
                    new_int_list.append((num1/num2)*ratio)  # After the calculation, add to the list
                # This parts make same duty with just above part, only difference is operation is insertion
                elif returning_list[0] == "insertion":
                    row, col = find_ascii(returning_list[1], returning_list[2])
                    num1 = insertion_matrix[row][col]
                    num2 = return_num_of_letter_in_dict(filename, returning_list[1])
                    if num2 == 0 and fourth_input == "nonsmooth":
                        num2 = 1000000
                    elif num2 == 0 and fourth_input == "smooth":
                        num1 = num1 + 1
                        num2 = num2 + 26
                    new_int_list.append((num1/num2)*ratio)
                # This parts make same duty with just above part, only difference is operation is transposition
                elif returning_list[0] == "transposition":
                    row, col = find_ascii(returning_list[1], returning_list[2])
                    num1 = transposition_matrix[row][col]
                    num2 = return_num_of_duos_in_dict(filename, returning_list[1]+returning_list[2])
                    if num2 == 0 and fourth_input == "nonsmooth":
                        num2 = 1000000
                    elif num2 == 0 and fourth_input == "smooth":
                        num1 = num1 + 1
                        num2 = num2 + 26
                    new_int_list.append((num1/num2)*ratio)
                # This parts make same duty with just above part, only difference is operation is deletion
                elif returning_list[0] == "deletion":
                    row, col = find_ascii(returning_list[1], returning_list[2])
                    num1 = deletion_matrix[row][col]
                    num2 = return_num_of_duos_in_dict(filename, returning_list[1]+returning_list[2])
                    if num2 == 0 and fourth_input == "nonsmooth":
                        num2 = 1000000
                    elif num2 == 0 and fourth_input == "smooth":
                        num1 = num1 + 1
                        num2 = num2 + 26
                    new_int_list.append((num1/num2)*ratio)
        max_value = max(new_int_list)
        max_index = new_int_list.index(max_value)
        return list[max_index]

# This function determine and return ascii value of letters and symbols. I will use these numbers
# when creating confusion matrix.
def find_ascii(letter1, letter2):
    if letter1 == "?":
        row = ord(letter1) - 37
    elif letter1 == "#":
        row = ord(letter1) - 4
    elif letter1 == "'":
        row = ord(letter1) - 12
    elif letter1 == "-":
        row = ord(letter1) - 17
    elif letter1 == ".":
        row = ord(letter1) - 17
    elif letter1 == "_":
        row = ord(letter1) - 65
    else:
        row = ord(letter1) - 97
    if letter2 == "?":
        col = ord(letter2) - 37
    elif letter2 == "#":
        col = ord(letter2) - 4
    elif letter2 == "'":
        col = ord(letter2) - 12
    elif letter2 == "-":
        col = ord(letter2) - 17
    elif letter2 == ".":
        col = ord(letter2) - 17
    elif letter2 == "_":
        col = ord(letter2) - 65
    else:
        col = ord(letter2) - 97
    return row, col

# This function according to operation and ascii values, make changes in confusion matrix.
def update_matrix(operation, letter1, letter2):
    row, col = find_ascii(letter1, letter2)
    if operation == "insertion":
        insertion_matrix[row][col] = insertion_matrix[row][col] + 1
    if operation == "deletion":
        deletion_matrix[row][col] = deletion_matrix[row][col] + 1
    if operation == "substitution":
        substitution_matrix[row][col] = substitution_matrix[row][col] + 1
    if operation == "transposition":
        transposition_matrix[row][col] = transposition_matrix[row][col] + 1

# This function return frequency of the given word in all words in corpus
def return_ratio_of_word_in_dict(dict, key):
    if word in dict.keys():
        return (d[key]+1)/(len(d)+26)
    else:
        return None

# This function return the number of duo letters in the corpus
def return_num_of_duos_in_dict(filename, duo):
    file = open(filename, 'r').read()
    str = ''.join(duo)
    count = file.count(str)
    return count

# This function return of the number of letters in the corpus
def return_num_of_letter_in_dict(filename, letter):
    with open(filename, 'r') as f:
        original_text = f.read()
    alphabet = string.ascii_lowercase
    filename = original_text.lower()
    alphabet_set = set(alphabet)
    counts = collections.Counter(c for c in filename if c in alphabet_set)
    return counts[letter]

# This function takes 2 string as a input. Create edit distance matrix for this 2 string.
# According to this matrix, create a path and find operation to reach from s to t.
def determine_operation(s, t):
    s = "#" + s
    t = "#" + t
    rows = len(s) + 1
    cols = len(t) + 1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    for i in range(1, rows):
        dist[i][0] = i
    for i in range(1, cols):
        dist[0][i] = i
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row - 1][col] + 1,  # deletion
                                 dist[row][col - 1] + 1,  # insertion
                                 dist[row - 1][col - 1] + cost)  # substitution
            if row > 1 and col > 1 and s[row - 1] == t[col - 2] and s[row - 2] == t[col - 1]:
                dist[row][col] = min(dist[row][col], dist[row - 2][col - 2] + cost)  # transposition
    while row != 0 and col != 0:
        prev_cost = dist[row][col]
        neighbors = []
        cross2 = 99
        if row > 1 and col > 1:
            if s[row - 1] == t[col - 2] and s[row - 2] == t[col - 1]:
                cross2 = dist[row - 2][col - 2]
        neighbors.append(cross2)
        if row != 0 and col != 0:
            neighbors.append(dist[row - 1][col - 1])
        if row != 0:
            neighbors.append(dist[row - 1][col])
        if col != 0:
            neighbors.append(dist[row][col - 1])
        min_cost = min(neighbors)
        if min_cost == prev_cost:
            row, col = row - 1, col - 1
        elif row != 0 and col != 0 and min_cost == dist[row - 1][col - 1]:
            row, col = row - 1, col - 1
            return ["substitution", s[row], t[col]]
        elif row != 0 and min_cost == dist[row - 1][col]:
            row, col = row - 1, col
            return ["deletion", t[col - 1], s[row]]
        elif col != 0 and min_cost == dist[row][col - 1]:
            row, col = row, col - 1
            return ["insertion", s[row - 1], t[col]]
        elif row != 0 and col != 0 and min_cost == dist[row - 2][col - 2]:
            row, col = row - 2, col - 2
            return ["transposition", s[row], t[col]]

output = open("output.txt", 'w')  # Create output file and write it correct words.
file = open(first_input, 'r')  # Open the corpus.txt or given first input
d = dict()  # Create dictionary
# This part change corpus to the desired format and create dictionary from their content
for line in file:
    line = line.strip()
    line = line.lower()
    line = line.translate(line.maketrans("", "", string.punctuation))
    words = line.split(" ")
    for word in words:
        if word in d:
            d[word] = d[word] + 1
        else:
            d[word] = 1

# This part create confusion matrix from spell-errors or given second input
with open(second_input) as f:
    for line in f:
        line = line.replace(":", "")
        line = line.replace(",", "")
        line = line.replace("\n", "")
        temp_list = line.split(" ")  # Add list to inputs line by line
        for w in temp_list:
            new_list = (temp_list[0], w)  # Create new list with first element of the input
            if "*" in new_list[1]:  # if line has *, this mistake makes n times which writes after the *
                data = new_list[1].split("*")  # Split the line after the *
                edited_word = data[0]  # determine the word
                again = int(data[1])  # determine the repetition
                for i in range(0, again):  # update matrix repetition times using
                    # "determine_operation" and "update_matrix" functions
                    if determine_operation(new_list[0].lower(), edited_word.lower()) is not None:
                        return_list = determine_operation(new_list[0].lower(), edited_word.lower())
                        update_matrix(return_list[0], return_list[1], return_list[2])
            else:  # if line does not contain * , update matrix using "determine_operation"
                # and "update_matrix" functions
                if determine_operation(new_list[0].lower(), new_list[1].lower()) is not None:
                    return_list = determine_operation(new_list[0].lower(), new_list[1].lower())
                    update_matrix(return_list[0], return_list[1], return_list[2])

# This part reads test-words-misspelled or given third input and create output and write to the file
with open(third_input, 'r') as f:
    misspelled_words = f.readlines()  # Read all lines
edit_list = []  # Create empty list
for i in misspelled_words:  # Look all misspelled words
    i = i.replace("\n", "")
    edit_list = edit_distance_word(d, i)  # Create list with edit distance is 1 and exist in the corpus
    output.write(find_max(first_input, i, edit_list) + '\n')  # Find usage rate of this list's contents
    # and return the maximum
    edit_list = []  # Make empty to edit list
output.close()
