
from flask import Flask,render_template,request
import tweepy
import csv
import itertools

#authorization keys
consumer_key = "XXX" 
consumer_secret = "XXX"
access_key = "XXX"
access_secret = "XXX"

callback_uri='oob'


app=Flask(__name__)

def get_auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #authenticate and authorizes the resource access request and returns authorization grant
    api = tweepy.API(auth)

    return api

    # Open/Create a file to append data
csvFile = open('minipro.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

#function that searches for media url in tweets data and stores it in the array and returns it
def get_images_using_keyword(hashtag):
    api=get_auth()
    images=[]
    img_url=[]
    for tweets in tweepy.Cursor(api.search_tweets,q=hashtag,count=10).items(100):
        #print(tweets.entities)
        if 'media' in tweets.entities:
            k=tweets.entities['media'][0]['media_url']
            images.append(k)
            link="https://twitter.com/twitter/statuses/"+str(tweets.id)
            img_url.append(link)
            print ("NAME:",tweets.author.screen_name.encode('utf-8'),"LINK:",link)
            print (tweets.created_at,tweets.text,"/n/n")
            csvWriter.writerow([tweets.author.screen_name.encode('utf-8'),tweets.created_at, tweets.text.encode('utf-8')])
    
    return images,img_url                                  
        

@app.route("/",methods=["POST","GET"])
@app.route("/login",methods=["POST","GET"])

def login():
    if(request.method=="POST"):
        form_data=request.form["nm"]
        image_url,link_img=get_images_using_keyword(form_data)
    
        return render_template('home.html',sent=image_url,sent1=link_img,n=len(image_url))
    else:
        return render_template("/login.html")

@app.route('/about')
def about():
    return render_template('/about.html')

if __name__== '__main__':
    app.run(debug=True) 

csvFile.close()

