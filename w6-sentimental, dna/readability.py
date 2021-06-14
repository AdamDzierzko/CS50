import cs50

grade = 0
letters = words = sentences = L = S = index = 0.0
text = cs50.get_string("Text: ")


def count_letters(t):
    a = 0
    for i in range(len(t)):
        if (t[i].isalpha()):
            a += 1
    return a


def count_words(t):
    a = 1
    for i in range(len(t)):
        if (t[i] == ' '):
            a += 1
    return a


def count_sentences(t):
    a = 0
    for i in range(len(t)):
        if (t[i] == '.' or t[i] == '!' or t[i] == '?'):
            a += 1
    return a


letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)

L = (letters / words) * 100
S = (sentences / words) * 100
index = 0.0588 * L - 0.296 * S - 15.8

if (index < 1):
    print("Before Grade 1")
elif (index > 16):
    print("Grade 16+")
else:
    grade = int(round(index))
    print("Grade " + str(grade))

