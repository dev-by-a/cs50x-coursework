text = input("Text: ")

letters = sum(c.isalpha() for c in text)
words = len(text.split())
sentences = sum(c in ".!?" for c in text)

L = letters / words * 100
S = sentences / words * 100
grade = round(0.0588 * L - 0.296 * S - 15.8)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
