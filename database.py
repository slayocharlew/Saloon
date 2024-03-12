from datetime import datetime

from kivymd.toast import toast


class FireBase:

    def saloon_get(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("Info").child(self.year()).child(
                    self.month_date())
                data = ref.get()

                return self.tweak_time(data["available_time"])

    def get_hairstyle(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("HairStyle")

                hairstyle = ref.get()

                return hairstyle

    def fetch_request(self, phone):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("Bookings").child(phone)

                bookings = ref.get()

                return bookings

    def book_saloon_data(self, name, phone, time_in, time_out, price, hair_style):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('Saloon').child("Eva_beauty").child("Bookings").child(phone)
                ref.set(
                    {
                        "name": name,
                        "phone": phone,
                        "time_in": time_in,
                        "time_out": time_out,
                        "hair_style": hair_style,
                        "price": price,
                        "status": "pending"
                    }
                )
                toast("Booking Sent")

    def tweak_time(self, time):
        new_time = []
        for i in time:
            if i < 13:
                new_time.append(f"{i} am")
            else:
                new_time.append(f"{i} pm")
        return new_time

    def year(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return y

    def month_date(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return f"{m}_{d}"


# x = FireBase.fetch_request(FireBase(), "0788204327")
# print(x)
