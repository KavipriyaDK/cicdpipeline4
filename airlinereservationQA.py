from airlinereservation import AirlineReservation


passed = 0
failed = 0


def run_test(number, description, test_function):

    global passed, failed

    try:
        test_function()
        print(f"TEST {number:02d} PASS - {description}")
        passed += 1

    except Exception as e:
        print(f"TEST {number:02d} FAIL - {description}")
        print(f"       Reason: {e}")
        failed += 1


# 1. Flight search
def test_01():

    system = AirlineReservation()

    result = system.search_flights("Chennai", "Delhi")

    assert "AI101" in result


# 2. Invalid route
def test_02():

    system = AirlineReservation()

    result = system.search_flights("Chennai", "Mumbai")

    assert result == []


# 3. Economy seat availability
def test_03():

    system = AirlineReservation()

    seats = system.check_seat_availability(
        "AI101",
        "Economy"
    )

    assert seats == 10


# 4. Business seat availability
def test_04():

    system = AirlineReservation()

    seats = system.check_seat_availability(
        "AI101",
        "Business"
    )

    assert seats == 5


# 5. Invalid flight
def test_05():

    system = AirlineReservation()

    try:
        system.check_seat_availability(
            "INVALID",
            "Economy"
        )
        assert False

    except ValueError:
        assert True


# 6. Invalid seat class
def test_06():

    system = AirlineReservation()

    try:
        system.check_seat_availability(
            "AI101",
            "Premium"
        )
        assert False

    except ValueError:
        assert True


# 7. Economy fare
def test_07():

    system = AirlineReservation()

    fare = system.calculate_fare(
        "Economy",
        30
    )

    assert fare == 5000


# 8. Business fare
def test_08():

    system = AirlineReservation()

    fare = system.calculate_fare(
        "Business",
        30
    )

    assert fare == 12000


# 9. Senior citizen discount
def test_09():

    system = AirlineReservation()

    fare = system.calculate_fare(
        "Economy",
        60
    )

    assert fare == 4250


# 10. Student discount
def test_10():

    system = AirlineReservation()

    fare = system.calculate_fare(
        "Economy",
        25,
        is_student=True
    )

    assert fare == 4500


# 11. Peak season pricing
def test_11():

    system = AirlineReservation()

    fare = system.calculate_fare(
        "Economy",
        30,
        peak_season=True
    )

    assert fare == 6250


# 12. Senior citizen during peak season
def test_12():

    system = AirlineReservation()

    fare = system.calculate_fare(
        "Economy",
        65,
        peak_season=True
    )

    assert fare == 5312.5


# 13. Student during peak season
def test_13():

    system = AirlineReservation()

    fare = system.calculate_fare(
        "Economy",
        20,
        is_student=True,
        peak_season=True
    )

    assert fare == 5625


# 14. Invalid age
def test_14():

    system = AirlineReservation()

    try:
        system.calculate_fare(
            "Economy",
            0
        )
        assert False

    except ValueError:
        assert True


# 15. Successful booking
def test_15():

    system = AirlineReservation()

    booking_id = system.book_flight(
        "AI101",
        "Passenger1",
        30,
        "Economy"
    )

    assert booking_id >= 1001


# 16. Booking decreases seat count
def test_16():

    system = AirlineReservation()

    before = system.check_seat_availability(
        "AI101",
        "Economy"
    )

    system.book_flight(
        "AI101",
        "Passenger2",
        30,
        "Economy"
    )

    after = system.check_seat_availability(
        "AI101",
        "Economy"
    )

    assert after == before - 1


# 17. Invalid passenger name
def test_17():

    system = AirlineReservation()

    try:
        system.book_flight(
            "AI101",
            "",
            30,
            "Economy"
        )

        assert False

    except ValueError:
        assert True


# 18. Cancellation charge
def test_18():

    system = AirlineReservation()

    booking_id = system.book_flight(
        "AI101",
        "Passenger3",
        30,
        "Economy"
    )

    result = system.cancel_booking(booking_id)

    assert result["cancellation_charge"] == 1000


# 19. Refund calculation
def test_19():

    system = AirlineReservation()

    booking_id = system.book_flight(
        "AI101",
        "Passenger4",
        30,
        "Economy"
    )

    result = system.cancel_booking(booking_id)

    assert result["refund"] == 4000


# 20. Cancellation restores seat
def test_20():

    system = AirlineReservation()

    before = system.check_seat_availability(
        "AI101",
        "Economy"
    )

    booking_id = system.book_flight(
        "AI101",
        "Passenger5",
        30,
        "Economy"
    )

    system.cancel_booking(booking_id)

    after = system.check_seat_availability(
        "AI101",
        "Economy"
    )

    assert after == before


# Run tests

tests = [
    (1, "Flight search", test_01),
    (2, "Invalid route", test_02),
    (3, "Economy seat availability", test_03),
    (4, "Business seat availability", test_04),
    (5, "Invalid flight", test_05),
    (6, "Invalid seat class", test_06),
    (7, "Economy fare", test_07),
    (8, "Business fare", test_08),
    (9, "Senior citizen discount", test_09),
    (10, "Student discount", test_10),
    (11, "Peak season pricing", test_11),
    (12, "Senior peak-season fare", test_12),
    (13, "Student peak-season fare", test_13),
    (14, "Invalid age", test_14),
    (15, "Successful booking", test_15),
    (16, "Booking decreases seats", test_16),
    (17, "Invalid passenger name", test_17),
    (18, "Cancellation charge", test_18),
    (19, "Refund calculation", test_19),
    (20, "Cancellation restores seat", test_20)
]


print("\nAIRLINE RESERVATION QA")
print("======================\n")

for number, description, test_function in tests:
    run_test(number, description, test_function)


print("\n======================")
print(f"TOTAL TESTS : {len(tests)}")
print(f"PASSED      : {passed}")
print(f"FAILED      : {failed}")

if failed == 0:
    print("\nALL 20 TESTS PASSED")
else:
    print("\nSOME TESTS FAILED")