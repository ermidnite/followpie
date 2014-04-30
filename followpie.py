from config import likePicture, unfollow_users, likeAndFollowUser, followUser 
from config import MAX_SECS, auth_token, client_id
from datetime import datetime
import random, time
import urllib,json,urllib2

# DO NOT TOUCH THESE THREE CONST VARIABLES
POPULAR = 1
LIKE = 2
LIKE_FOLLOW = 3
UNFOLLOW = 4

#Choose the tag you want to like based on, keep the word in double quotes, do not put a # sign in front of the tag
TAGS = ["tag", "tagallday", "tagallnight"]

#IF YOU WANT THE ACTION TO FOLLOW OR LIKE SOMEONE BASED ON THE CHOSEN TAG CHANGE IT TO EITHER
#   ACTION=POPULAR   - Popular follows people who have liked an image on the popular page (this means they are active users)
#   ACTION=LIKE
#   ACTION = UNFOLLOW

#added functionality of doing a round of unfollowing after it finishes 
ACTION=LIKE_FOLLOW

#CHANGE THE NUMBER OF LIKES OR FOLLOWS YOU WANT TO OCCUR, e.g. NO MORE THEN 100 is the current setting
MAX_COUNT = random.randint(12, 27)

######DO NOT TOUCH ANYTHING UNDER HERE UNLESS YOU KNOW WHAT YOU ARE DOING, DANGER DANGER, SERIOUS PROBLEMS IF YOU TOUCH ###########

print "FOLLOW PIE BEGINS - GRAB A SLICE AND SIT BACK"
print ""
print "The script will now proceed"
print ""
print ""

likedDict = {}

if(ACTION == LIKE or ACTION == LIKE_FOLLOW):
    def likeUsers(max_results,max_id,tag,c,fllw):
        urlFindLike="https://api.instagram.com/v1/tags/%s/media/recent?client_id=CLIENT_ID&access_token=%s" % (tag,auth_token);

        urlLike="https://api.instagram.com/v1/media/%s/likes"
        values = {'access_token' : auth_token,
                  'client_id' : client_id,
                  'max_id' : max_id}
        
        f = urllib.urlopen(urlFindLike)
        dataObj = json.loads(f.read())
        f.close()
        numResults = len(dataObj['data'])
        pictureId=0
        for likeObj in dataObj['data']:
                print ''                
                pictureId = likeObj['id']
                paginationId = dataObj["pagination"]['next_max_id']
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
                        followRatio = 3
                        if followRatio == random.randint(0,4):
                            fresult=followUser(userId)
                            fllw=fllw+fresult
                            print "Following user %s" % userId
                    c=c+result
                    seconds=random.randint(2, MAX_SECS)
                    randomBreakInterval=random.randint(0, 226)
                    if randomBreakInterval == 1:
                        sleepTime = random.randint(2644, 3982)
                        print "YOU JUST HIT 1/226 JACKPOT FUCK YEAH!"
                        print "sleeping for "+str(sleepTime / 60)+" minutes! Sneaky mofos"
                        print str(datetime.now())
                        time.sleep(sleepTime)
                    time.sleep(seconds)
                    print "Liked %s:  %s" % (tag,c)
                    if fllw != 0:
                        print "Followed %s:  %s" % (tag,fllw)
                    print str(datetime.now())  
                    if(c==max_results or c>27):
                        break
                except Exception, e:
                    print e
        if(c!=max_results):
            likeUsers(max_results,paginationId,tag,c,fllw)
        return c,fllw
        print ''
    i = random.randrange(len(TAGS))
    totalFollowCount = 0
    totalLikeCount = 0
    for tag in TAGS[i:]+TAGS[:i]:
        c=0
        f=0
        c,f=likeUsers(MAX_COUNT,0,tag,c,f)
        totalLikeCount += c
        totalFollowCount += f
        shortSleep = random.randint(70, 620)
        print "Liked %s: Followed %s: for tag %s" %(c,f,tag)
        print "Liked %s: Followed %s so far!" %(totalLikeCount,totalFollowCount)
        print "Taking a sneak nap "+str(shortSleep / 60)+" minutes."
        print str(datetime.now())
        time.sleep(shortSleep)

    for likes in likedDict:
        print "%s = %s" % (likes, likedDict[likes])
        print "Fuck yeah! Time to unfollow the haters"

elif(ACTION==POPULAR):
    urlPopular="https://api.instagram.com/v1/media/popular?client_id=CLIENT_ID";
    f = urllib.urlopen(urlPopular)
    dataObj=json.loads(f.read())
    f.close()
    i=0
    c=0
    l=0
    for obj in dataObj['data']:
        for comment in obj['likes']['data']:
            myid=comment['id']                   
            try:
                result=likeAndFollowUser(myid)
                if(result>0):
                    c=c+1
                l=l+result
                if(c%10==0):
                    print "Followed %s" % c
                seconds=random.randint(1, MAX_SECS)
                time.sleep(seconds)                       
            except Exception, e:
                print e
            if(c==MAX_COUNT):                        
                break
        if(c==MAX_COUNT):                        
            break         
        
    
            ""
        print ""
    print "Followed %s" % (c);
    print "Liked %s" % (l);

# elif(ACTION==UNFOLLOW):
#     num_unfollows = unfollow_users()
#     print "Number of users unfollowed is %s " % num_unfollows

num_unfollows = unfollow_users()
print "Number of users unfollowed is %s " % num_unfollows


print "FOLLOW PIE ENDS - HAPPY DIGESTING"
