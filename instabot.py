import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from testwrd import generate_word_cloud
from termcolor import colored

APP_ACCESS_TOKEN='4649009910.2af61a0.93e42eb4dcda4c2894d7fde2065844f2'
#Token Owner : AVinstaBot.main10
#Sandbox Users : AVinstaBot.test0, AVinstaBot.test1, AVinstaBot.test2...... AVinstaBot.test10

BASE_URL = 'https://api.instagram.com/v1/'
list=[]

#with the help of this function i can get info of my own followers,follows and how much posts i get added.


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
         print'Status code other than 200 received!'

# with the help of this funtion i can get the id of a user by user name
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()
#here i can declare the function by here i can get the info of a user by username
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'
# here i can use a funtion by this you can get your recent post.
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
# here i can use a funtion by this you can get the recent post of a user.
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    print user_media

    if user_media['meta']['code'] == 200:
        rang=len(user_media['data'])
        i=0
        for i in range(rang):
            print user_media['data'][0]['images']['standard_resolution']['url']
           # image_name = user_media['data'][0]['id'] + '.jpeg'
           # image_url = user_media['data'][0]['images']['standard_resolution']['url']
           #urllib.urlretrieve(image_url, image_name)
           #print 'Your image has been downloaded!'
         #else:
          #  print 'Post does not exist!'
           # return None
    else:
        print 'Status code other than 200 received!'
#By this function you can get the ID of the recent post of a user by username
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()
#here i can make the function by this you can like the recent post of a user
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        text= colored('Your like was unsuccessful. Try again!',"red")
#here i can make a function by this you can make a comment on the recent post of the user
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()
    print make_comment
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


#by this funtion you can get the list of comments on the recent post of the user
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    get_a_comment = requests.get(request_url).json()
    print get_a_comment
    if get_a_comment['meta']['code'] == 200:
        x=1
        for temp in get_a_comment['data']:
            print "%d. %s : %s"%(x,temp['from']['username'],temp['text'])
            x=x+1
    else:
        text = colored('Your comment was unsuccessful. Try again!', "red")


def tag_name(insta_username):
    #get_user_post(insta_username)
    media_id=get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    tag_trends= requests.get(request_url).json()
    print tag_trends

    if tag_trends['meta']['code']==200:
        file = open("sahil.txt", "w")
        for item in tag_trends['data']['caption']['text']:

                file.write(item)

        file.close()



                    #if len(tag_trends['data']):
         #   tag=tag_trends['data']['tags']
          #  print tag
    else:
        print 'Status code other than 200 received!'
        exit()


def start_bot():
    while True:
        print '\n'
        text=colored('************** Welcome to instaBot***************',"red")
        print text
        text=colored('Here are your menu options:',"red")
        print text
        text=colored("1.Get your own details\n","red")
        print text
        text=colored ("2.Get details of a user by username\n","red")
        print text
        text=colored ("3.Get your own recent post\n","red")
        print text
        text=colored ("4.Get the recent post of a user by username\n","red")
        print text
        text= colored("5.Get a  liked  on the recent post of a user\n","red")
        print text
        text=colored ("6.Get a list of comments on the recent post of a user\n","red")
        print text
        text=colored ("7.Make a comment on the recent post of a user\n","red")
        print text
        text=colored ("8.Trends And Subtrends","red")
        print text
        text=colored ("0.Exit","red")
        print text

        choice= int(raw_input("Enter you choice: "))
        if choice == 1:
            self_info()
        elif choice == 2:
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == 3:
            get_own_post()
        elif choice == 4:
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice==5:
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice==6:
           insta_username = raw_input("Enter the username of the user: ")
           get_comment_list(insta_username)
        elif choice==7:
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice==8:
            insta_username = raw_input("Enter the username of the user: ")
            tag_name(insta_username)
            generate_word_cloud()
        elif choice ==0:
            exit()
        else:
            print "wrong choice"

start_bot()
# the last and the main objective word cloud should be done on the testwrd.py