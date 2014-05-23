from config import unfollow_users, likeUsers
from config import TAGS, ACTION, LIKE, LIKE_FOLLOW, UNFOLLOW, MAX_PICS, MAX_CYCLES, likedDict
from datetime import datetime
from pprint import pprint
import random, time
import urllib,json,urllib2

print "What has become of the world?? Building spam bots is a depressing feat"
print ""
print "The script will now proceed"
print ""
print ""

x = 0
totalCycleCount = 0
totalFollowCount = 0
totalLikeCount = 0

while x < MAX_CYCLES:
    totalCycleCount += 1
    if(ACTION == LIKE or ACTION == LIKE_FOLLOW):
        i = random.randrange(len(TAGS))
        #starts tag on random entry in array to be more random
        for tag in TAGS[i:]+TAGS[:i]:
            c=0
            f=0
            MAX_COUNT = random.randint(12, MAX_PICS)
            c,f=likeUsers(MAX_COUNT,0,tag,c,f)
            totalLikeCount += c
            totalFollowCount += f
            shortSleep = random.randint(70, 620)
            print ''
            print ''
            print "Taking a sneak nap "+str(shortSleep / 60)+" minutes."
            print "Liked %s: Followed %s: for tag %s" %(c,f,tag)
            print "Liked %s: Followed %s so far!" %(totalLikeCount,totalFollowCount)
            print str(datetime.now())
            print ''
            print ''
            time.sleep(shortSleep)

        for likes in likedDict:
            print "%s = %s" % (likes, likedDict[likes])

        print "Finished cycle "+str(totalCycleCount)+". Rinse and repeat mofooo"
        print str(MAX_CYCLES - x)+" iterations left!"
        print ""

        print "Ding ding jackpot! Time to unfollow the haters"
        num_unfollows = unfollow_users()
        print "Number of users unfollowed is %s " % num_unfollows
        print ""

    elif(ACTION==UNFOLLOW):
        num_unfollows = unfollow_users()
        print "Number of users unfollowed is %s " % num_unfollows

    #comment this to run infinite loop
    x += 1

print "Tears of joy ensue... spam over."



