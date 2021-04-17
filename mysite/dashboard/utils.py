from enum import IntEnum, Enum

# high = more than 5 flags in the past 2 weeks
# medium = between 2-5 flags in the past 2 weeks
# low = between 0-1 flags in the past 2 weeks
from django.utils import timezone
from datetime import timedelta
import logging

from .models import *

logger = logging.getLogger(__name__)

def get_risk_label(num_flags):

    if num_flags >= 30:
        return "VERY HIGH"
    elif num_flags >= 20:
        return "HIGH"
    elif num_flags >= 10:
        return "MEDIUM"
    else:
        return "LOW"

#get risk by counting the number of flagged events of each type
def get_risk(flags_list):
    count = 0
    for flags in flags_list:
        count += len(flags)

    return get_risk_label(count)




def calculate_risk():
    log_date_range = timezone.now().date() - timedelta(days=14)
    logger.error("Calculating overall risk")
    logger.error("========================")
    sum  = calculate_overall_trip_risk(log_date_range)
    logger.error("Overall risk is currently " + str(sum) + "\n")
    sum += calculate_overall_food_risk(log_date_range)
    logger.error("Overall risk is currently " + str(sum) + "\n")
    sum += calculate_overall_friend_risk(log_date_range)
    logger.error("Overall risk is currently " + str(sum) + "\n")
    sum += calculate_overall_symptom_risk(log_date_range)
    logger.error("Overall risk is currently " + str(sum) + "\n")

    logger.error("========================")
    logger.error("Total overall risk is " + get_risk_label(sum))
    logger.error("========================")

    return get_risk_label(sum)

#tests
# food=[1,2,3]
# symptom = [1,2]
# print(get_risk([food, symptom]))



# Food
def calculate_overall_food_risk(log_date_range):
    logger.error("Calculating overall Food risk:")

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
    logger.error("Calculating overall Trip risk:")

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

    if not trip.masked:
        #increase total risk to 3
        risk += 2

    trip.risk_score = risk
    trip.save()

    return risk

# Friend
def calculate_overall_friend_risk(log_date_range):
    logger.error("Calculating overall Friend risk:")

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
        logger.error("\t\"" + symptom.__str__() + "\" has a risk level of " + str(current_risk))

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