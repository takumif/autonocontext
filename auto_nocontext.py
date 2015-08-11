import praw
import sys
import requests
import requests.auth
from earliest_usage_cache import EarliestUsageCache

# Constants
API_ACCESS_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
REDIRECT_URI = "http://127.0.0.1:65010/authorize_callback"
AUTONOCONTEXT = "autonocontext"
CLIENT_ID = "my_client_id"
CLIENT_SECRET = "my_client_secret"
ACCOUNT_USERNAME = "AutoNocontext"
ACCOUNT_PASSWORD = "my_password"
USER_AGENT_INFO = "Auto Nocontext by /u/AutoNocontext"

def nextLimit(limit):
    if limit == 1000:
        return 940
    else:
        return limit + 1

def printInline(text):
    print text,
    sys.stdout.flush()

def makeSubmission(comment, r):
    r.submit(subreddit=AUTONOCONTEXT, title=getSubmissionTitle(comment), text=getSubmissionText(comment))

def getSubmissionTitle(comment):
    if len(comment.body) < 300:
        return comment.body

    return comment.body[:295] + " ..."

def getSubmissionText(comment):
    return "[Original comment]({permalink}) by {author}".format(permalink=comment.permalink, author=comment.author.name)

# function from http://www.baransja.com/Reddit-API-OAuth2/
def getAccessToken():
    response = requests.post(API_ACCESS_TOKEN_URL,
        auth=requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={"grant_type": "password", "username": ACCOUNT_USERNAME, "password": ACCOUNT_PASSWORD},
        headers={"User-Agent": USER_AGENT_INFO})
    response = dict(response.json())
    return response["access_token"]

def isLegitimateNocontextMention(comment, cache):
    return (("nocontext" in comment.body or "Nocontext" in comment.body)
            and not cache.contains(comment.parent_id)
            and "bot" not in comment.author.name
            and comment.author.name != "autonocontext"
            and "nocontext" not in comment.subreddit.url)

def isComment(thing):
    return type(thing) is praw.objects.Comment

def hasAppearedInSub(comment, r, limit=10):
    recentPosts = r.get_new(AUTONOCONTEXT, limit=limit)
    for recentPost in recentPosts:
        minLength = min(len(comment.body), len(recentPost.title) - len(" ..."))
        if comment.body[:minLength] == recentPost.title[:minLength]:
            return True
    return False

def getReddit():
    r = praw.Reddit(user_agent=USER_AGENT_INFO,
                    oauth_client_id=CLIENT_ID,
                    oauth_client_secret=CLIENT_SECRET,
                    oauth_redirect_uri=REDIRECT_URI)
    r.set_access_credentials(set(["identity", "submit"]), getAccessToken())

    return r

def run():
    r = getReddit()
    limit = 940
    count = 0
    cache = EarliestUsageCache()

    print "Running Auto Nocontext"

    while True:
        try:
            comments = r.get_comments('all', limit=limit)
            for comment in comments:
                count += 1
                if isLegitimateNocontextMention(comment, cache):
                    parent = r.get_info(thing_id=comment.parent_id)
                    if isComment(parent) and not hasAppearedInSub(comment, r):
                        cache.add(comment.parent_id, parent.body)
                        makeSubmission(parent, r)

            limit = nextLimit(limit)
        except:
            print "ERROR"
            r = getReddit()

if __name__ == "__main__":
    run()