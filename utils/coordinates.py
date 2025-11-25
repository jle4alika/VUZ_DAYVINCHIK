from geopy.geocoders import Nominatim
from haversine import haversine

geolocator = Nominatim(user_agent="vyz_daivinchik_bot")


async def resolve_city(name: str) -> None | dict:
    location = geolocator.geocode(name, language="ru")

    if not location:
        return None

    return {
        "city": location.raw.get("name"),
        "latitude": location.latitude,
        "longitude": location.longitude,
    }


def get_city_name(lat, lon):
    location = geolocator.reverse(f"{lat}, {lon}", language="ru", addressdetails=True)
    if location:
        print(location)
        address_details = location.raw.get("address", {})
        print(address_details)
        city = (
            address_details.get("city")
            or address_details.get("town")
            or address_details.get("village")
        )
        return city
    return None


def distance_km(p1, p2) -> float:
    return haversine((p1.latitude, p1.longitude), (p2.latitude, p2.longitude))
