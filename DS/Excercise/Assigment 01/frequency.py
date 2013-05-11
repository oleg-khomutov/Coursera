__author__ = 'Oleg_Khomutov'

import sys
import json


def GetSource(path):
    return open(path)


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

    for term in twitText.strip().split(" "):
        normalizedTerm = NormalizeTerm(term)

        if len(normalizedTerm) > 0:
            termsOfTweet.append(normalizedTerm)

    return termsOfTweet


def PrintTermFrequencyScore(twitterSource):
    terms = {}
    occurrencesOfAllTermsInAllTweets = 0

    for twit in twitterSource:
        jsonTwit = json.loads(twit)

        if "text" in jsonTwit:
            twitText = jsonTwit["text"]

            termsOfTwit = CleanupTwit(twitText)

            for term in termsOfTwit:
                if term in terms:
                    terms[term] += 1
                else:
                    terms[term] = 1

                occurrencesOfAllTermsInAllTweets += 1

    for term in sorted(terms):
        print("{0} {1:.4f}".format(term, terms[term]/occurrencesOfAllTermsInAllTweets))


def main():
    twitterSourcePath = sys.argv[1]

    with GetSource(twitterSourcePath) as twitterSource:
        PrintTermFrequencyScore(twitterSource)


if __name__ == '__main__':
    main()