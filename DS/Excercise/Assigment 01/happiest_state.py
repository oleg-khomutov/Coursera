__author__ = 'Oleg_Khomutov'

import sys
import json
import operator

states = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawai'i", "ID": "Idaho",
    "IS": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"}


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


def GetTwitScore(twitText, scores):
    return CalculateSentimentScore(CleanupTwit(twitText), scores)


def GetState(locationString):
    for locationTerm in CleanupTwit(locationString):
        for stateShort, stateLong in states.iteritems():
            if (locationTerm == stateShort.lower()) or (locationTerm == stateLong.lower()):
                return stateShort

    return ""


def PrintHappiestState(twitterSource, scores):
    happiestState = {}

    for twit in twitterSource:

        jsonTwit = json.loads(twit)
        scoreOfTwit = 0.00
        locationState = ""

        if "text" in jsonTwit:
            scoreOfTwit = GetTwitScore(jsonTwit["text"], scores)

        if "user" in jsonTwit:
            user = jsonTwit["user"]

            if (user is not None) and ("location" in user):
                locationState = GetState(user["location"])

        if (len(locationState) == 0) and ("place" in jsonTwit):
            place = jsonTwit["place"]

            if (place is not None) and ("full_name" in place):
                locationState = GetState(place["full_name"])

        if len(locationState) > 0:
            if locationState in happiestState:
                happiestState[locationState] += scoreOfTwit
            else:
                happiestState[locationState] = scoreOfTwit

    happiestState = sorted(happiestState.iteritems(), key=operator.itemgetter(1), reverse=True)

    print(happiestState[0][0])


def main():
    sentimentSourcePath = sys.argv[1]
    twitterSourcePath = sys.argv[2]

    with GetSource(sentimentSourcePath) as sentimentSource:
        scores = GetSentimentsScores(sentimentSource)

    with GetSource(twitterSourcePath) as twitterSource:
        PrintHappiestState(twitterSource, scores)


if __name__ == '__main__':
    main()
