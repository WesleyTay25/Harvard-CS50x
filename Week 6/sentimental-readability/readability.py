text = input("Text: ")

n = len(text)
letters = 0
words = 1
sentences = 0

for i in text:
    if i.isalpha() == True:
        letters += 1
    if i == " ":
        words += 1
    if i in ['.', '!', '?']:
        sentences += 1

L = (float(letters) / float(words)) * 100
S = (float(sentences) / float(words)) * 100
subindex = 0.0588 * L - 0.296 * S - 15.8
index = int(round(subindex))

if index > 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {index}")
