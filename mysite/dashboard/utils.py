from enum import IntEnum, Enum

from django.utils import timezone
from datetime import timedelta
import logging
from . import TravelRestrictionsAPI

from .models import *

logger = logging.getLogger(__name__)

travelRestrictionController = TravelRestrictionsAPI.TravelRestrictionController


def get_risk_label(risk_score):
    if risk_score >= 30:
        return "VERY HIGH"
    elif risk_score >= 20:
        return "HIGH"
    elif risk_score >= 10:
        return "MEDIUM"
    else:
        return "LOW"


def calculate_risk():
    log_date_range = timezone.now().date() - timedelta(days=14)
    logger.error("Calculating overall risk")
    logger.error("========================")
    risk  = calculate_overall_trip_risk(log_date_range)
    logger.error("Overall risk is currently " + str(risk) + "\n")
    risk += calculate_overall_food_risk(log_date_range)
    logger.error("Overall risk is currently " + str(risk) + "\n")
    risk += calculate_overall_friend_risk(log_date_range)
    logger.error("Overall risk is currently " + str(risk) + "\n")
    risk += calculate_overall_symptom_risk(log_date_range)
    logger.error("Overall risk is currently " + str(risk) + "\n")

    logger.error("========================")
    logger.error("Total overall risk is " + get_risk_label(risk))
    logger.error("========================")

    return get_risk_label(risk)


# Food
def calculate_overall_food_risk(log_date_range):
    logger.error("Calculating Food risk:")

    sum = 0
    all_food = Food.objects.filter(log_date__gte=log_date_range)

    for food in all_food:
        current_risk = food_risk(food)
        sum += current_risk
        logger.error("\t\"" + food.__str__() + "\" has a risk level of " + str(current_risk))

    return sum

def food_risk(food):
    #default risk for food is 0
    if food.risk_score >= 0:
        return food.risk_score

    risk = 0
    if not food.contactless:
        #increase total risk to 1
        risk += 1

    food.risk_score = risk
    food.save()

    return risk

# Trip
def calculate_overall_trip_risk(log_date_range):
    logger.error("Calculating Trip risk:")

    sum = 0
    all_trips = Trip.objects.filter(log_date__gte=log_date_range)

    for trip in all_trips:
        current_risk = trip_risk(trip)
        sum += current_risk
        logger.error("\t\"" + trip.__str__() + "\" has a risk level of " + str(current_risk))

    return sum

def trip_risk(trip):
    #default risk for any trip at all is 1?
    if trip.risk_score >= 0:
        return trip.risk_score

    risk = 1

    if trip.travel_mode == "AP":
        # This is very risky behavior
        # (Also likely illegal)
        if not trip.masked:
            risk = 20
        else:
            risk = 10

    elif trip.travel_mode == "TN" or trip.travel_mode == "BS":
        if not trip.masked:
            risk = 10
        else:
            risk = 5

    elif trip.travel_mode == "RS":
        if not trip.masked:
            risk = 5
        else:
            risk = 2

    # Destination Logic
    if travelRestrictionController.is_high_risk_site(trip.destination):
        risk += 15

    # Committing model change to DB
    trip.risk_score = risk
    trip.save()

    return risk

# Friend
def calculate_overall_friend_risk(log_date_range):
    logger.error("Calculating Friend risk:")

    sum = 0
    all_friends = Friend.objects.filter(log_date__gte=log_date_range)

    for friend in all_friends:
        current_risk = friend_risk(friend)
        sum += current_risk
        logger.error("\t\"" + friend.__str__() + "\" has a risk level of " + str(current_risk))

    return sum

def friend_risk(friend):
    if friend.risk_score >= 0:
        return friend.risk_score

    #Default friend risk is 0
    risk = 0

    if friend.indoor:
        risk += 1

    if not friend.masked:
        risk += 1

    if not friend.distanced:
        risk += 1

    if friend.duration <= 20:
        risk += 1
    else:
        risk += 2

    #Include a field to determine if all participants
    #are vaccinated that neutralizes this score?

    friend.risk_score = risk
    friend.save()

    return risk

# Symptom
def calculate_overall_symptom_risk(log_date_range):
    sum = 0
    all_symptoms = Symptom.objects.filter(log_date__gte=log_date_range)

    for symptom in all_symptoms:
        current_risk = symptom_risk(symptom)
        sum += current_risk
        logger.error("\t\"" + symptom.get_type_display() + "\" of Severity " + str(symptom.severity) + " has a risk level of " + str(current_risk))

    return sum

def symptom_risk(symptom):
    if symptom.risk_score >= 0:
        return symptom.risk_score

    risk = 0
    t = symptom.type
    # Fever, Cough, Fatigue, Muscle Aches, Difficulty Breathing
    if t == "FV" or t == "CH" or t == "SF" or t == "MA" or t == "DB":
        #These are very characteristic of COVID, and thus higher risk
        risk = 5

    # Loss of Taste/Smell
    elif t == "LT" or t == "LS":
        if symptom.severity > 3:
            # Severe loss of taste/smell is a major indicator of COVID
            # and should be very high risk.
            risk = 20
        else:
            # Still high risk, but could possibly be due to cold
            # or allergies at this severity
            risk = 5

    # Other
    elif t == "OT":
        # Unrelated to COVID, and thus low/now risk
        pass

    # All other symptom types
    else:
        #These are moderately characteristic of COVID, and thus medium risk
        risk += 3


    symptom.risk_score = risk
    symptom.save()

    return risk