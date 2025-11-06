from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    # Function code unchanged
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_user(request):
    # Function code unchanged
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    # Function code unchanged
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


def get_dealerships(request, state="All"):
    # Function code unchanged
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    # Function code unchanged
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint) or []
        for review_detail in reviews:
            try:
                response = analyze_review_sentiments(review_detail['review'])
                review_detail['sentiment'] = (
                    response.get('sentiment', 'neutral') if response else 'neutral'
                )
            except Exception as e:
                print("Sentiment analyzer error:", e)
                review_detail['sentiment'] = 'neutral'
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    # Function code unchanged
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealer_obj = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": [dealer_obj]})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    # Function code unchanged
    if request.user.is_anonymous is False:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})


def get_cars(request):
    # Function code unchanged
    if CarModel.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.all()
    data = []
    for model in car_models:
        data.append(
            {
                "CarModel": model.name,
                "CarMake": model.car_make.name,
                "Type": model.type,
                "Year": model.year,
                "DealerID": model.dealer_id,
            }
        )

    return JsonResponse({"CarModels": data})
