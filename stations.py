import time

import googlemaps


class GoogleStations:
    name_stop = []
    cord_stop = []

    API_KEY = 'AIzaSyBTG2Z2tCQyE4MiqIw6Cafil_TaVZaVON4'
    map_client = googlemaps.Client(API_KEY)

    def miles_to_meters(self, miles):
        try:
            return miles * 1_609.344
        except:
            return 0

    def SaloonPoint(self, address):
        print(address)

        # address = address  # 'Gamex, Makutano Road, Jitegemee, Mabibo, Ubungo Municipal, Dar es Salaam, Coastal Zone, 21493, Tanzania'
        geocode = self.map_client.geocode(address=address)
        (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

        # Saloon
        search_string = 'Saloon'
        distance = self.miles_to_meters(2)
        business_list = []

        response = self.map_client.places_nearby(
            location=(lat, lng),
            keyword=search_string,
            radius=distance
        )

        business_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token')

        while next_page_token:
            time.sleep(2)
            response = self.map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance,
                page_token=next_page_token
            )
            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

        for i in range(6):
            self.name_stop.append(business_list[i]["name"])
            cord = f'{business_list[i]["geometry"]["location"]["lat"]},{business_list[i]["geometry"]["location"]["lng"]}'.strip()
            self.cord_stop.append(cord)
            print(business_list[i]["name"])
            print(cord)


"""GoogleStations.GetBusStop(GoogleStations(),'Gamex, Makutano Road, Jitegemee, Mabibo, Ubungo Municipal, Dar es Salaam, Coastal Zone, 21493, Tanzania')"""
