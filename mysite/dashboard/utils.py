from enum import IntEnum, Enum


# high = more than 5 flags in the past 2 weeks
# medium = between 2-5 flags in the past 2 weeks
# low = between 0-1 flags in the past 2 weeks
def get_risk_label(num_flags):

    if num_flags>=5:
        return "HIGH"
    elif num_flags>=2:
        return "MEDIUM"
    else:
        return "LOW"

#get risk by counting the number of flagged events of each type
def get_risk(flags_list):
    count=0
    for flags in flags_list:
        count+=len(flags)

    return get_risk_label(count)


# class SYMPTOMTYPES(Enum):
#     COUGH = 'COUGH'
#     FEVER = 'FEVER'
#     OTHER = 'OTHER'
#
#     @classmethod
#     def choices(cls):
#         return [(tag, tag.value) for tag in cls]


SEVERITY= [tuple([x,x]) for x in range(1,6)]


#tests
# food=[1,2,3]
# symptom = [1,2]
# print(get_risk([food, symptom]))