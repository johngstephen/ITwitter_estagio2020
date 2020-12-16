from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from .forms import searchForm
import requests
import re
from .models import Users, FavoriteTweet
from django.http import HttpResponse, HttpResponseRedirect


@login_required
def home(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            searchText = form.cleaned_data.get('keyword')
            requestHeader = {
                "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAABisGwEAAAAAGRecj8qfrGUP3N9dfd%2FJO%2FMPvU4%3DVXnmAnQZQSrxusYW2fvycKlnkCwsYp0zZWXOdOHhSbCNiyHPuS",
                "Accept": "json"}
            requestParams = {"q": searchText, "result-type": "recent", "tweet_mode": "extended"}
            resultList = []

            r = requests.get("https://api.twitter.com/1.1/search/tweets.json?", headers=requestHeader,
                             params=requestParams)
            r = r.json()
            for tweet in r['statuses']:
                tweetText = tweet['full_text']
                if tweetText.startswith('RT'):
                    print("Retweet found")
                else:
                    imageList = []
                    if 'media' in tweet['entities']:
                        for mediaItem in tweet['entities']['media']:
                            imageList.append(mediaItem['media_url_https'])

                    item = {"tweet_username": tweet['user']['screen_name'],
                            "username_image": tweet['user']['profile_image_url_https'],
                            "tweet_text": findurlintweet(tweet['full_text']),
                            "tweet_images": imageList,
                            "tweet_id": tweet['id']}
                    resultList.append(item)
        return render(request, 'results.html', {'username': request.user.get_full_name(), 'resultList': resultList})
    else:
        form = searchForm()
    return render(request, 'home.html', {'username': request.user.get_full_name(), 'form': form})


def findurlintweet(tweetTxt):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, tweetTxt)
    for img in url:
        for link in img:
            tweetTxt = tweetTxt.replace(link, '')
    return tweetTxt


@login_required
def tweetSaver(request):
    tweetCounter = 0
    if request.method == 'POST':
        request_user = request.user.email
        user_object = Users.objects.get(username=request_user)
        for tweet in request.POST.getlist('tweet'):
            fav_tweet = FavoriteTweet(user=user_object, tweet_id=tweet)
            fav_tweet.save()
            tweetCounter += 1
    return render(request, 'tweet_save_done.html', {'tweets_saved_count': tweetCounter, 'username': request.user.get_full_name()})


@login_required
def history(request):
    request_user = request.user.email
    user_object = Users.objects.get(username=request_user)
    fav_tweets_list = FavoriteTweet.objects.filter(user=user_object)
    tweets_id_list = []
    for t in fav_tweets_list:
        tweets_id_list.append(str(t.tweet_id))

    if len(tweets_id_list) == 0:
        return render(request, 'no_favorites.html', {'username': request.user.get_full_name()})
    resultList = []
    fav_tweets_request_ids = ",".join(tweets_id_list)

    requestHeader = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAABisGwEAAAAAGRecj8qfrGUP3N9dfd%2FJO%2FMPvU4%3DVXnmAnQZQSrxusYW2fvycKlnkCwsYp0zZWXOdOHhSbCNiyHPuS",
        "Accept": "json"}
    requestParams = {"id": fav_tweets_request_ids, "tweet_mode": "extended"}

    r = requests.get("https://api.twitter.com/1.1/statuses/lookup.json?", headers=requestHeader,
                    params=requestParams)
    r = r.json()

    for tweet in r:
        imageList = []
        if 'media' in tweet['entities']:
            for mediaItem in tweet['entities']['media']:
                imageList.append(mediaItem['media_url_https'])

        item = {"tweet_username": tweet['user']['screen_name'],
                "username_image": tweet['user']['profile_image_url_https'],
                "tweet_text": findurlintweet(tweet['full_text']),
                "tweet_images": imageList,
                "tweet_id": tweet['id']}
        resultList.append(item)

    return render(request, 'history.html', {'username': request.user.get_full_name(), 'resultList': resultList})


@login_required
def tweetDelete(request):
    tweetCounter = 0
    if request.method == 'POST':
        request_user = request.user.email
        user_object = Users.objects.get(username=request_user)
        for tweet in request.POST.getlist('tweet'):
            FavoriteTweet.objects.filter(user=user_object, tweet_id=tweet).delete()
            tweetCounter += 1
    return render(request, 'tweets_delete_done.html', {'tweets_saved_count': tweetCounter, 'username': request.user.get_full_name()})