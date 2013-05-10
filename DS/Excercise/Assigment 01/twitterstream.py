import sys
import urllib2 as urllib
import oauth2 as oauth


class Configuration:

    _debug = 0

    HTTP_URL = "https://stream.twitter.com/1/statuses/sample.json"
    HTTP_Method = "GET"
    HTTP_Handler = urllib.HTTPHandler(debuglevel=_debug)
    HTTPS_Handler = urllib.HTTPSHandler(debuglevel=_debug)

    SignatureMethod_HMAC_SHA1 = oauth.SignatureMethod_HMAC_SHA1()


def GetTwitterStream():
    oauth_token = oauth.Token(key=Configuration.AccessTokenKey,
                              secret=Configuration.AccessTokenSecret)

    oauth_consumer = oauth.Consumer(key=Configuration.ConsumerKey,
                                    secret=Configuration.ConsumerSecret)

    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=Configuration.HTTP_Method,
                                                http_url=Configuration.HTTP_URL,
                                                parameters=[])

    req.sign_request(Configuration.SignatureMethod_HMAC_SHA1,
                     oauth_consumer,
                     oauth_token)

    if Configuration.HTTP_Method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        Configuration.HTTP_URL = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(Configuration.HTTP_Handler)
    opener.add_handler(Configuration.HTTPS_Handler)

    return opener.open(Configuration.HTTP_URL, encoded_post_data)


def GetDestination(path):
    return open(path, "w")


def FetchSamples():
    i = 0

    with GetDestination(sys.argv[1]) as destination:
        for line in GetTwitterStream():
            destination.write(line.strip() + "\n")
            i += 1

            if i % 10000 == 0:
                print(str(i) + " elements")

            if i == 250000:
                return


if __name__ == '__main__':
    FetchSamples();