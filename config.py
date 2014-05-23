import time, random
import urllib,json,urllib2
from pprint import pprint
from datetime import datetime
#global vars, leave these be
POPULAR = 1
LIKE = 2
LIKE_FOLLOW = 3
UNFOLLOW = 4
likedDict = {}

#User options =====================================================================================

#choose tags, as many as you want. I recommend >30. Tags are recycled after complete round
TAGS = ["TAG1", "TAG2", "etc"]

#Choose which action you would like to do
#ACTION = LIKE
#ACTION = UNFOLLOW
ACTION=LIKE_FOLLOW


#maximum number of seconds to wait inbetween next like or follow. avoid spam behavior
MAX_SECS = 12

#maximum number of pictures to like. Minimum is set at 12 to avoid spam behavior
MAX_PICS = 27

#number of times to cycle through the tags.
MAX_CYCLES = 100

#input your instagram auth info
auth_token = "auth_token"
client_id = "client_id"

#End Options ======================================================================================

FOLLOWS = 1
DOES_NOT_FOLLOW = 0
PENDING = 2

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
    error = -1
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
        return unfollowed
    except Exception, e:
        print e
        return error 

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
                if result == -1:
                    print "Number of follows limited! Come back to this later ;)"
                    return num_unfollows
                num_unfollows = num_unfollows+result
                seconds=random.randint(1, 6)
                time.sleep(seconds)
        print num_unfollows
        if num_unfollows % 10 == 0:
            print "Unfollowed %s users " % num_unfollows

        if next_url is not None:
            unfollow_users(next_url, num_unfollows)

    except Exception, e:
        print e
    return num_unfollows

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

def likeUsers(max_results,max_id,tag,c,fllw):
    print "Switching to new tag: "+tag
    urlFindLike="https://api.instagram.com/v1/tags/%s/media/recent?client_id=%s&access_token=%s" % (tag,client_id,auth_token);

    urlLike="https://api.instagram.com/v1/media/%s/likes"
    values = {'access_token' : auth_token,
              'client_id' : client_id,
              'max_id' : max_id}
    
    f = urllib.urlopen(urlFindLike)
    dataObj = json.loads(f.read())
    f.close()

    #testing
    # z = dir(dataObj)
    # pprint (z)

    #this if keeps bot running when you are rate limited. 'code' returns 400 on error
    if dataObj['meta']['code'] == 200:
        numResults = len(dataObj['data'])
        pictureId=0
        for likeObj in dataObj['data']:
                print ''                
                pictureId = likeObj['id']
                paginationId = dataObj["pagination"]['next_max_tag_id']
                user = likeObj['user']
                userId = user['id']
                try:
                    numLikes = likedDict[pictureId]
                    numLikes = numLikes+1
                    likedDict[pictureId] = numLikes
                except:
                    numLikes = 1
                    likedDict[pictureId] = numLikes
                    
                try:
                    result = likePicture(pictureId)
                    if(ACTION==LIKE_FOLLOW):

                        #randomized 1/6 chance of following user to prevent following too many
                        #   and getting rate limited on followers
                        followRatio = 3
                        if followRatio == random.randint(0,5):
                            fresult=followUser(userId)
                            fllw=fllw+fresult
                            print "Following user %s" % userId
                    c=c+result
                    print "Liked %s:  %s" % (tag,c)
                    if fllw != 0:
                        print "Followed %s:  %s" % (tag,fllw)

                    #random long sleep to stay within API limit and act more human
                    randomBreakInterval=random.randint(0, 226)
                    if randomBreakInterval == 1:
                        sleepTime = random.randint(2644, 3982)
                        print "YOU JUST HIT 1/226 JACKPOT FUCK YEAH!"
                        print "sleeping for "+str(sleepTime / 60)+" minutes! Sneaky mofos"
                        print str(datetime.now())
                        time.sleep(sleepTime)

                    print str(datetime.now())  
                    seconds=random.randint(2, MAX_SECS)
                    time.sleep(seconds)
                    if(c==max_results):
                        break
                except Exception, e:
                    print e
        if(c!=max_results):
            likeUsers(max_results,paginationId,tag,c,fllw)
        print ''

    else:
        pprint (dataObj['meta'])
        print 'Instagram tryin to play you, switch tags!'
        time.sleep(random.randint(2, MAX_SECS))
    return c,fllw
    print ''

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
