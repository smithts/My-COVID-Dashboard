import logging

logger = logging.getLogger(__name__)

high_risk_sites = ["New York City", "NYC", "Los Angeles",
                       "LA", "Chicago", "Houston", "Phoenix",
                       "Philadelphia", "San Antonio", "San Diego",
                       "Dallas", "San  Jose", "Austin", "Jacksonville",
                       "Fort Worth", "San Francisco", "Columbus",
                       "Charlotte", "Indianapolis", "Seattle", "Denver",
                       "Washington", "Washington, DC", "DC", "El Paso",
                       "Las Vegas", "Portland"]

class TravelRestrictionController:

    def is_high_risk_site(destination):
        return destination in high_risk_sites
