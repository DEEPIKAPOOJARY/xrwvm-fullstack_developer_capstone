from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from .models import CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse(
            {"userName": username, "status": "Authenticated"}
        )
    return JsonResponse({"userName": username})


def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug(f"{username} is new user")

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse(
            {"userName": username, "status": "Authenticated"}
        )

    return JsonResponse({"userName": username, "error": "Already Registered"})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
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


def get_dealer_details(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchDealer/{dealer_id}"
    dealer_obj = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": [dealer_obj]})


def add_review(request):
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    data = json.loads(request.body)
    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception:
        return JsonResponse(
            {"status": 401, "message": "Error in posting review"}
        )


def get_cars(request):
    if CarModel.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.all()
    data = [
        {
            "CarModel": model.name,
            "CarMake": model.car_make.name,
            "Type": model.type,
            "Year": model.year,
            "DealerID": mo
