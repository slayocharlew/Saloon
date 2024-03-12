import requests
from locations import Location as LC


class Distance:

    def mi_km(self, mi):
        km = mi * 1.60934 / 1

        print(km, mi)

        return km



    def get_distance(self, origins, destination):
        API_KEY = 'AIzaSyBTG2Z2tCQyE4MiqIw6Cafil_TaVZaVON4'

        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destination}&units=imperial&key={API_KEY}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()

        distance = data["rows"][0]["elements"][0]['distance']["text"]
        time = data["rows"][0]["elements"][0]['duration']["text"]

        new_d = float(distance.strip().split(" ")[0])
        distance = int(self.mi_km(new_d))

        return [distance, time]
