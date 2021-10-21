import re

def makeString(text):
    text = text.lower()
    regex = re.compile('[^a-zA-Z]')
    text = regex.sub('', text)
    return text.strip()

def is_palindrome(text, i = 0):
    text = makeString(text)
    if text[i] != text[(len(text) - 1) - i]:
        return False

    if i == (len(text)//2):
        return True

    return is_palindrome(text, i + 1)

print(is_palindrome("Taco cat"))
print(is_palindrome("Well hello there !"))
