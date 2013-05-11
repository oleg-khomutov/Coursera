import sys
import json


def GetSource(path):
    return open(path)


def GetSentimentsScores(sentimentSource):
    scores = {}

    for line in sentimentSource:
        term, score = line.split("\t")
        scores[term] = float(score)

    return scores


def NormalizeTerm(term):
    term = unicode.lower(term.strip())

    if term.isalpha():
        return term

    startIndex = 0
    endIndex = 0

    for char in term[:]:
        if char.isalpha():
            startIndex = term.index(char)
            break

    term = term[startIndex:]

    for char in term[:]:
        if not char.isalpha():
            endIndex = term.index(char)
            break

    term = term[:endIndex]

    return term


def CleanupTwit(twitText):
    termsOfTweet = []

    for term in twitText.split(" "):
        termsOfTweet.append(NormalizeTerm(term))

    return termsOfTweet


def CalculateSentimentScore(termsOfTwit, scores):
    scoreOfTwit = 0.00

    for term in termsOfTwit:
        if term in scores:
            scoreOfTwit += scores[term]

    return scoreOfTwit


def PrintTwitSentimentScore(twitterSource, scores):
    for twit in twitterSource:

        jsonTwit = json.loads(twit)
        scoreOfTwit = 0.00

        if "text" in jsonTwit:
            twitText = jsonTwit["text"]

            termsOfTwit = CleanupTwit(twitText)
            scoreOfTwit = CalculateSentimentScore(termsOfTwit, scores)

        print("%0.2f" % scoreOfTwit)


def main():
    sentimentSourcePath = sys.argv[1]
    twitterSourcePath = sys.argv[2]

    with GetSource(sentimentSourcePath) as sentimentSource:
        scores = GetSentimentsScores(sentimentSource)

    with GetSource(twitterSourcePath) as twitterSource:
        PrintTwitSentimentScore(twitterSource, scores)


if __name__ == '__main__':
    main()