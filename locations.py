from geopy.geocoders import Nominatim


class Location:
    data_adress = {}

    def get_address(self, cordinates):
        locator = Nominatim(user_agent="myGeocoder")
        coordinates = cordinates[0], cordinates[1]
        location = locator.reverse(coordinates)
        address_data = location.raw
        print(address_data)

        return address_data

    def save_data(self, cordinates):
        Location.data_adress = self.get_address(cordinates)

    def get_spec_add(self, name):
        return Location.data_adress["address"][name]


