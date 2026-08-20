class AirlineReservation:

    BASE_FARES = {
        "Economy": 5000,
        "Business": 12000
    }

    PEAK_SEASON_MULTIPLIER = 1.25
    SENIOR_DISCOUNT = 0.15
    STUDENT_DISCOUNT = 0.10
    CANCELLATION_CHARGE = 0.20

    def __init__(self):
        self.flights = {
            "AI101": {
                "source": "Chennai",
                "destination": "Delhi",
                "economy_seats": 10,
                "business_seats": 5
            },
            "AI202": {
                "source": "Mumbai",
                "destination": "Delhi",
                "economy_seats": 8,
                "business_seats": 4
            },
            "AI303": {
                "source": "Bangalore",
                "destination": "Mumbai",
                "economy_seats": 6,
                "business_seats": 3
            }
        }

        self.bookings = {}
        self.next_booking_id = 1001

    # Flight search
    def search_flights(self, source, destination):

        results = []

        for flight_no, flight in self.flights.items():

            if (
                flight["source"].lower() == source.lower()
                and flight["destination"].lower() == destination.lower()
            ):
                results.append(flight_no)

        return results

    # Seat availability
    def check_seat_availability(self, flight_no, seat_class):

        if flight_no not in self.flights:
            raise ValueError("Invalid flight number")

        if seat_class not in ["Economy", "Business"]:
            raise ValueError("Invalid seat class")

        key = "economy_seats" if seat_class == "Economy" else "business_seats"

        return self.flights[flight_no][key]

    # Fare calculation
    def calculate_fare(
        self,
        seat_class,
        passenger_age,
        is_student=False,
        peak_season=False
    ):

        if seat_class not in self.BASE_FARES:
            raise ValueError("Invalid seat class")

        if passenger_age <= 0:
            raise ValueError("Invalid passenger age")

        fare = self.BASE_FARES[seat_class]

        # Peak season pricing
        if peak_season:
            fare *= self.PEAK_SEASON_MULTIPLIER

        # Senior citizen discount
        if passenger_age >= 60:
            fare *= (1 - self.SENIOR_DISCOUNT)

        # Student discount
        elif is_student:
            fare *= (1 - self.STUDENT_DISCOUNT)

        return round(fare, 2)

    # Booking
    def book_flight(
        self,
        flight_no,
        passenger_name,
        passenger_age,
        seat_class,
        is_student=False,
        peak_season=False
    ):

        if flight_no not in self.flights:
            raise ValueError("Invalid flight number")

        if not passenger_name:
            raise ValueError("Passenger name cannot be empty")

        available = self.check_seat_availability(
            flight_no,
            seat_class
        )

        if available <= 0:
            raise ValueError("No seats available")

        fare = self.calculate_fare(
            seat_class,
            passenger_age,
            is_student,
            peak_season
        )

        key = (
            "economy_seats"
            if seat_class == "Economy"
            else "business_seats"
        )

        self.flights[flight_no][key] -= 1

        booking_id = self.next_booking_id
        self.next_booking_id += 1

        self.bookings[booking_id] = {
            "flight_no": flight_no,
            "passenger_name": passenger_name,
            "passenger_age": passenger_age,
            "seat_class": seat_class,
            "fare": fare,
            "status": "CONFIRMED"
        }

        return booking_id

    # Cancellation
    def cancel_booking(self, booking_id):

        if booking_id not in self.bookings:
            raise ValueError("Invalid booking ID")

        booking = self.bookings[booking_id]

        if booking["status"] == "CANCELLED":
            raise ValueError("Booking already cancelled")

        cancellation_charge = (
            booking["fare"] * self.CANCELLATION_CHARGE
        )

        refund = booking["fare"] - cancellation_charge

        flight_no = booking["flight_no"]

        key = (
            "economy_seats"
            if booking["seat_class"] == "Economy"
            else "business_seats"
        )

        self.flights[flight_no][key] += 1

        booking["status"] = "CANCELLED"

        return {
            "original_fare": booking["fare"],
            "cancellation_charge": round(cancellation_charge, 2),
            "refund": round(refund, 2)
        }


if __name__ == "__main__":

    system = AirlineReservation()

    print("AIRLINE RESERVATION SYSTEM")
    print("--------------------------")

    flights = system.search_flights("Chennai", "Delhi")

    print("Available flights:", flights)

    booking_id = system.book_flight(
        "AI101",
        "Rahul",
        25,
        "Economy",
        is_student=True,
        peak_season=False
    )

    print("Booking ID:", booking_id)

    print(
        "Remaining Economy seats:",
        system.check_seat_availability("AI101", "Economy")
    )

    cancellation = system.cancel_booking(booking_id)

    print("Cancellation details:", cancellation)