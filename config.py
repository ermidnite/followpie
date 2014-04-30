import time, random
import urllib,json,urllib2

#MAX seconds is the number of seconds to randomly wait between doing your next follow or like (this helps to avoid acting like a crazy spam bot)
MAX_SECS = 12

#Hit the URL below, the returned GET request will give you an auth token from Instagram.
#
#THE AUTH TOKEN IS THE KEY THAT YOU GET WHEN YOU SIGN IN WITH THE FOLLOWING CLIENT URL.
#DOES NOT NEED TO CHANGE UNLESS AUTH TOKEN EXPIRES
#
#
#   https://api.instagram.com/oauth/authorize/?client_id=CLIENT_ID&redirect_uri=http://yoururl.com&response_type=token&display=touch&scope=likes+relationships
#
auth_token = "AUTH_TOKEN"
client_id = 'CLIENT_ID'

user_agent = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
headers = { 'User-Agent' : user_agent,
            "Content-type": "application/x-www-form-urlencoded"
            }

def likePicture(pictureId):
    liked = 0
    try:
        urlLike = "https://api.instagram.com/v1/media/%s/likes"
        values = {'access_token' : auth_token,
                  'client_id' : client_id}
        newLike = urlLike % (pictureId)
        print newLike
        data = urllib.urlencode(values)
        req = urllib2.Request(newLike,data,headers)
        response = urllib2.urlopen(req)
        result = response.read()
        dataObj = json.loads(result)
        liked = 1
    except Exception, e:
        print e
    return liked

FOLLOWS = 1
DOES_NOT_FOLLOW = 0
PENDING = 2


#unfollow users who don't follow you.
def unfollow_users(next_url=None, num_unfollows=0):
    if next_url == None:
        urlUserMedia = "https://api.instagram.com/v1/users/self/follows?access_token=%s" % (auth_token)
    else:
        urlUserMedia = next_url

    values = {
              'client_id' : client_id}
    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(urlUserMedia,None,headers)
        response = urllib2.urlopen(req)
        result = response.read()
        dataObj = json.loads(result)
        next_url = None
        if dataObj.get('pagination') is not None:
            next_url = dataObj.get('pagination')["next_url"]

        for user in dataObj['data']:
            for k, v in user.iteritems():
                if k == "id":
                    userId = v
            relationship = get_relationship(userId)
            if relationship == DOES_NOT_FOLLOW:
                result = unfollow_user(userId)
                num_unfollows = num_unfollows+result
            seconds=random.randint(1, MAX_SECS)
            time.sleep(seconds)
        print num_unfollows
        if num_unfollows % 10 == 0:
            print "Unfollowed %s users " % num_unfollows

        if next_url is not None:
            unfollow_users(next_url, num_unfollows)

    except Exception, e:
        print e
    return num_unfollows


def get_relationship(userId):
    unfollowed=0

    followUrl = "https://api.instagram.com/v1/users/%s/relationship?access_token=%s&client_id=%s" % (userId, auth_token, client_id)

    values = {'access_token' : auth_token,
              'client_id' : client_id}
    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(followUrl,None,headers)
        response = urllib2.urlopen(req)
        result = response.read()
        dataObj = json.loads(result)
        status = dataObj["data"]
        incoming = status["incoming_status"]
        print '%s - %s ' % (userId, incoming)
        if incoming != "followed_by":
            return DOES_NOT_FOLLOW
        else:
            return FOLLOWS
    except Exception, e:
        print e
    return unfollowed


def unfollow_user(userId):
    unfollowed=0
    followUrl = "https://api.instagram.com/v1/users/%s/relationship?action=allow"

    values = {'access_token' : auth_token,
              'action' : 'unfollow',
              'client_id' : client_id}
    try:
        newFollow = followUrl % (userId)
        data = urllib.urlencode(values)
        req = urllib2.Request(newFollow,data,headers)
        response = urllib2.urlopen(req)
        result = response.read()
        dataObj = json.loads(result)
        unfollowed = 1
    except Exception, e:
        print e
    return unfollowed


def followUser(userId):
    followed=0
    followUrl = "https://api.instagram.com/v1/users/%s/relationship?action=allow"

    values = {'access_token' : auth_token,
              'action' : 'follow',
              'client_id' : client_id}    
    try:
        newFollow = followUrl % (userId)
        print newFollow
        data = urllib.urlencode(values)
        req = urllib2.Request(newFollow,data,headers)
        response = urllib2.urlopen(req)
        result = response.read()                      
        print result
        dataObj = json.loads(result);
        followed = 1
                                       
    except Exception, e:
        print e
        
    return followed


def likeAndFollowUser(userId):
    numLikesFollows=0
    urlUserMedia = "https://api.instagram.com/v1/users/%s/media/recent/?access_token=%s" % (userId,auth_token)
    values = {
              'client_id' : client_id}    
    try:
        print urlUserMedia
        data = urllib.urlencode(values)
        req = urllib2.Request(urlUserMedia,None,headers)
        response = urllib2.urlopen(req)
        result = response.read()                      
        dataObj = json.loads(result);
        picsToLike = random.randint(1, 3)
        print "Liking %s pics for user %s" % (picsToLike, userId)
        countPicViews=0
        for picture in dataObj['data']:
            print "Liking picture %s " % picture['id']
            likePicture(picture['id'])
            countPicViews = countPicViews+1
            numLikesFollows = numLikesFollows+1
            if(countPicViews == picsToLike):
                break
        followed=1
    except Exception, e:
        print e
        
    followUser(userId)
    return numLikesFollows
