import re

import phonenumbers
from kivy.properties import NumericProperty, StringProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from phonenumbers import number_type, carrier

from database import FireBase as FB

Window.size = (412, 732)


class Tab(MDBoxLayout, MDTabsBase):
    pass


class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= 10 or not substring.isdigit():
            return

        if len(self.text) == 0:
            if substring != "0":
                return
        elif len(self.text) == 1:
            if substring != "7" and substring != "6":
                return

        return super(NumberOnlyField, self).insert_text(substring, from_undo=from_undo)


class MainApp(MDApp):
    size_x, size_y = Window.size

    screens = ['entrance']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    # details
    attending_time = StringProperty("")
    user_name = StringProperty("")
    user_phone = StringProperty("")
    user_hair = StringProperty("")
    hair_price = StringProperty("")
    hair_time = StringProperty("")
    time_out = StringProperty("")
    price = StringProperty("")

    time = None
    hair_style = None

    def on_start(self):
        self.drop_it()
        self.drop_hair()

        self.notifi()

    def to_rgba(self, r, g, b, a):

        return r / 255, g / 255, b / 255, a

    def drop_it(self):

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in FB.saloon_get(FB())
        ]
        self.time = MDDropdownMenu(
            caller=self.root.ids.drop_item,
            items=menu_items,
            width_mult=2,
            position="center",
        )
        self.time.bind()

    def set_item(self, text_item):
        self.root.ids.drop_item.set_item(text_item)
        self.attending_time = text_item.split(" ")[0]
        self.calculate_time()
        print(self.attending_time)
        self.time.dismiss()

    def drop_hair(self):

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_hair(x),
            } for i, y in FB.get_hairstyle(FB()).items()
        ]
        self.hair_style = MDDropdownMenu(
            caller=self.root.ids.drop_hair,
            items=menu_items,
            width_mult=2,
            position="center",
        )
        self.hair_style.bind()

    def set_hair(self, text_item):
        self.root.ids.drop_hair.set_item(text_item)
        self.user_hair = text_item
        self.hair_details()
        self.calculate_time()
        self.hair_style.dismiss()

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def phone_number_check_admin(self, phone):
        new_number = ""
        if phone != "" and len(phone) == 10:
            for i in range(phone.__len__()):
                if i == 0:
                    pass
                else:
                    new_number = new_number + phone[i]
            number = "+255" + new_number
            if not carrier._is_mobile(number_type(phonenumbers.parse(number))):
                toast("Please check your phone number!", 1)
                return False
            else:
                self.public_number = number
                return True
        else:
            toast("enter phone number!")

    def book_saloon(self):

        if not isinstance(self.user_name, str) or not self.user_name:
            toast("Name must be a non-empty string")
            return

        if not isinstance(self.user_phone, str) or not re.match(r'^0[76]\d{8}$', self.user_phone):
            toast("Phone number must be a string of 10 digits starting with '07' or '06'")

            return

        if not isinstance(self.user_hair, str) or not self.user_hair:
            toast("Hair style must be a non-empty string")

            return
        if self.attending_time == "":
            toast("select attending time")

            return

        FB.book_saloon_data(FB(), self.user_name, self.user_phone, self.attending_time, self.time_out, self.hair_price,
                            self.user_hair)

    def calculate_time(self):
        if self.attending_time != "" and self.hair_time != "":
            self.attending_time = self.attending_time.split(" ")[0]
            self.hair_time = self.hair_time.split(" ")[0]
            self.time_out = str(int(self.attending_time) + int(self.hair_time))
            print(self.time_out)
            if int(self.time_out) < int("13"):
                self.time_out = f"{self.time_out} am"
            elif int(self.time_out) >= int("13"):
                self.time_out = f"{self.time_out} pm"

            if int(self.attending_time) < int("13"):
                self.attending_time = f"{self.attending_time} am"
            elif int(self.attending_time) >= int("13"):
                self.attending_time = f"{self.attending_time} pm"

    def hair_details(self):
        data = FB.get_hairstyle(FB())[self.user_hair]
        print(data)
        self.hair_price = data["price"]
        self.hair_time = data["time"]

    def add_sch(self, data):
        self.root.ids.order.data.append(
            {
                "viewclass": "SaloonInfo",
                "icon": "google-maps",
                "name": data["name"],
                "phone": data["phone"],
                "price": data["price"],
                "time_in": data["time_in"],
                "time_out": data["time_out"],
                "hair_style": data["hair_style"],
                "status": data["status"]
            }
        )

    def stream_handler(self, message):
        if True:
            print("hello")
            try:
                self.add_sch(FB.fetch_request(FB(), self.user_phone))
            except:
                pass

    def notifi(self):
        try:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            self.my_stream = db.reference('Saloon').child("Eva_beauty").child("Bookings").listen(
                self.stream_handler)

        except:
            print("you did good!")

    def build(self):
        pass


MainApp().run()
