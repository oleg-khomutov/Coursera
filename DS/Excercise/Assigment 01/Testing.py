__author__ = 'Oleg_Khomutov'

examples = [u"done",
            u"dOne! fuck shit",
            u"Done!1 suck my dick",
            u"1Done!1 1212121212#Justin",
            u"'Do4ne!1 #Twitter! dead",
            u"'#Do4ne!1"]


def NormalizeHashTag(term):
    return term[term.index("#"):]


def GetTwitHashTags(twitText):
    for term in twitText.split(" "):
        print("testing term " + term)
        if term.find("#") >= 0:
            print("term " + term + " has hashTag! Normalizing...")
            return NormalizeHashTag(term)

    return ""


test = "test\n"

print(test.strip())
print("111")