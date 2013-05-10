__author__ = 'Oleg_Khomutov'

import sys
import json
import operator


def GetSource(path):
    return open(path)


def NormalizeTerm(term):
    term = term.lower()
    term = term[term.index("#") + 1:]

    if term.isalnum():
        return term

    endIndex = len(term)

    for char in term[:]:
        if not char.isalnum():
            endIndex = term.index(char)
            break

    return term[:endIndex]


def GetTwitHashTags(twitText):
    twitHashTags = []

    for term in twitText.split(" "):
        if (term.find("#") >= 0) and (len(term) > 1):
            normalizedTerm = NormalizeTerm(term)
            if len(normalizedTerm) > 0:
                twitHashTags.append(normalizedTerm)

    return twitHashTags


def UpdateHashTags(hashTags, twitHashTags):
    for hashTag in twitHashTags:
        if hashTag in hashTags:
            hashTags[hashTag] += 1.0
        else:
            hashTags[hashTag] = 1.0

    return


def CalculateHashTags(twitterSource):
    hashTags = {}

    for twit in twitterSource:
        jsonTwit = json.loads(twit)

        if "text" in jsonTwit:
            UpdateHashTags(hashTags, GetTwitHashTags(jsonTwit["text"]))

    return hashTags


def SortHashTags(hashTags):
    return sorted(hashTags.iteritems(), key=operator.itemgetter(1), reverse=True)


def PrintHashTags(hashTags):
    for hashTagKey in hashTags[0:10]:
        print(hashTagKey[0] + " " + str(hashTagKey[1]))


def GetHashTags(twitterSourcePath):
    with GetSource(twitterSourcePath) as twitterSource:
        return CalculateHashTags(twitterSource)


def main():
    twitterSourcePath = sys.argv[1]

    PrintHashTags(SortHashTags(GetHashTags(twitterSourcePath)))


if __name__ == '__main__':
    main()