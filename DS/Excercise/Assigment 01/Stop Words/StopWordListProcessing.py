import sys

__author__ = 'Oleg_Khomutov'

tFilePath = "AFINN-111.txt"
swFilePath = "StopWords.txt"
swtaFilePath = "StopWordsToAdd.txt"

terms = []
stopWords = []
stopWordsToAdd = []


with open(tFilePath, "r") as tFile:
    for term in tFile:
        terms.append(term)

try:
    with open(swFilePath, "r") as swFile:
        for stopWord in swFile:
            stopWords.append(stopWord.lower().strip())
except IOError:
    stopWords = []

with open(swtaFilePath, "r") as swtaFile:
    for stopWordToAdd in swtaFile:
        for sw in stopWordToAdd.lower().split():
            stopWordsToAdd.append(sw.strip())

for stopWordToAdd in stopWordsToAdd:
    if (stopWordToAdd not in terms) and (stopWordToAdd not in stopWords):
        stopWords.append(stopWordToAdd)

with open(swFilePath, "w") as swFile:
    for stopWord in sorted(stopWords):
        swFile.write(stopWord + "\n")