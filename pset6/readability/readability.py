import cs50 as cs

text = cs.get_string("Text: ")


def count_letters(text):

    sum_letters = 0

    for i in range(len(text)):
        if text[i].isalpha():
            sum_letters += 1
    return sum_letters

# returns words


def count_words(text):

    sum_words = 1

    for i in range(len(text)):
        if text[i] == ' ':
            sum_words += 1

    return sum_words

# returns sentc


def count_sentences(text):

    sum_sentc = 0

    for i in range(len(text)):
        if(text[i] == "." or text[i] == "?" or text[i] == "!"):
            sum_sentc += 1

    return sum_sentc


letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)

# print(letters, words, sentences)

L = letters / words * 100
S = sentences / words * 100

# calc index
index = 0.0588 * L - 0.296 * S - 15.8

# calc based on index
if (index > 1 and index < 16):
    print(f"Grade {round(index)}")
elif (index < 1):
    print("Before Grade 1")
elif (index > 16):
    print("Grade 16+")

