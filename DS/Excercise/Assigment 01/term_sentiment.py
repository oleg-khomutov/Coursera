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
    term = term.strip()

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

    for term in twitText.strip().split(" "):
        normalizedTerm = NormalizeTerm(term)

        if len(normalizedTerm) > 0:
            termsOfTweet.append(normalizedTerm)

    return termsOfTweet


def CalculateSentimentScore(termsOfTwit, scores):
    scoreOfTwit = 0.00

    for term in termsOfTwit:
        if term in scores:
            scoreOfTwit += scores[term]

    return scoreOfTwit


def PrintTermSentimentScore(twitterSource, scores):
    terms = {}

    for twit in twitterSource:
        jsonTwit = json.loads(twit)

        if "text" in jsonTwit:
            twitText = jsonTwit["text"]

            termsOfTwit = CleanupTwit(twitText)
            scoreOfTwit = CalculateSentimentScore(termsOfTwit, scores)

            for term in termsOfTwit:
                if term in terms:
                    termScores = terms[term]

                    termScores[0] += scoreOfTwit
                    termScores[1] += 1.00

                    terms[term] = termScores
                else:
                    termScores = [0, 0]

                    termScores[0] = scoreOfTwit
                    termScores[1] = 1.00

                    terms[term] = termScores

    for term in terms:
        print("{0} {1:.3f}".format(term, terms[term][0]/terms[term][1]))


def main():
    sentimentSourcePath = sys.argv[1]
    twitterSourcePath = sys.argv[2]

    with GetSource(sentimentSourcePath) as sentimentSource:
        scores = GetSentimentsScores(sentimentSource)

    with GetSource(twitterSourcePath) as twitterSource:
        PrintTermSentimentScore(twitterSource, scores)


if __name__ == '__main__':
    main()