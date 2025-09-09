def main():
    text = input("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    L = float((float(letters) / float(words)) * 100)
    S = float((float(sentences) / float(words)) * 100)
    sub_index = 0.0588 * L - 0.296 * S - 15.8
    index = round(sub_index)
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def count_letters(text):
    letters = 0
    for i in range(0, len(text)):
        c = text[i]
        if c.isalpha():
            letters += 1
    return letters


def count_words(text):
    words = 0
    for i in range(0, len(text)):
        if text[i].isspace():
            words += 1
    return words + 1


def count_sentences(text):
    sentences = 0
    for i in range(0, len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            sentences += 1
    return sentences


main()
