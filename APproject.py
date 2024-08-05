import csv
import json
import datetime

# log in information
log_in_info = {"username": "", "password": ""}

# making a dict to save user info
users_info_dict = {"users": []}
with open('signup_information', 'w') as j_file:
    json.dump(users_info_dict, j_file)


def write_json(data, filename='signup_information'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# reading the csv file and storing each line as a dict in a list
flights_list = []
with open('flights.csv') as file:
    reader = csv.DictReader(file)
    y = 1
    for x in reader:
        flights_dict = {'id': y}
        flights_dict.update(x)
        flights_list.append(flights_dict)
        y += 1


# cleaning flights output
def clean_flight_info(flight_information):
    flight_information = flight_information.replace("'", "")
    flight_information = flight_information.replace(",", "")
    flight_information = flight_information.replace("dict_values([", "")
    flight_information = flight_information.replace("])", "")
    return flight_information


# user log in and sign in
class UserInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def signup(self):
        user_info = {}
        user_info["username"] = self.username
        user_info["password"] = self.password
        user_info["wallet"] = 0
        user_info["tickets"] = []

        with open('signup_information') as json_file:
            data = json.load(json_file)
            temp = data["users"]

            all_usernames = [x["username"] for x in temp]
            if self.username not in all_usernames:
                print("OK")
                temp.append(user_info)
                log_in_info["username"] = self.username
                log_in_info["password"] = self.password
            else:
                print("Bad Request")
        write_json(data)

    def login(self):
        with open('signup_information') as json_file:
            data = json.load(json_file)
            temp = data["users"]

            check = True

            for x in temp:
                if x["username"] == self.username and x["password"] == self.password:
                    print("OK")
                    log_in_info["username"] = self.username
                    log_in_info["password"] = self.password
                    check = False
                    print(temp)

            if check:
                print("Bad Request")
        write_json(data)

    def increase_wallet_amount(self, wallet_amount):
        with open('signup_information') as json_file:
            data = json.load(json_file)
            temp = data["users"]

            check = True

            for x in temp:
                if x["username"] == self.username and x["password"] == self.password:
                    x["wallet"] += wallet_amount
                    check = False
                    print("OK")

            if check:
                print("Bad Request")
        write_json(data)

    def decrease_wallet_amount(self, wallet_amount):
        with open('signup_information') as json_file:
            data = json.load(json_file)
            temp = data["users"]

            check = True

            for x in temp:
                if x["username"] == self.username and x["password"] == self.password:
                    x["wallet"] -= wallet_amount
                    check = False

            if check:
                print("Bad Request")
        write_json(data)

    def wallet_amount(self):
        with open('signup_information') as json_file:
            data = json.load(json_file)
            temp = data["users"]

            check = True

            for x in temp:
                if x["username"] == self.username and x["password"] == self.password:
                    check = False
                    write_json(data)
                    return float(x["wallet"])
            if check:
                print("Bad Request")
        write_json(data)

    def add_bought_ticket(self, booked_flight_info):
        with open('signup_information') as json_file:
            data = json.load(json_file)
            temp = data["users"]

            for x in temp:
                if x["username"] == self.username and x["password"] == self.password:
                    x["tickets"].append(booked_flight_info)
        write_json(data)

    def show_all_bought_tickets(self):
        with open('signup_information') as json_file:
            data = json.load(json_file)
            temp = data["users"]

            for x in temp:
                if x["username"] == self.username and x["password"] == self.password:
                    if len(x["tickets"]) == 0:
                        print("Empty")
                    else:
                        for y in x["tickets"]:
                            ticket_info = str(y.values())
                            print(clean_flight_info(ticket_info))
        write_json(data)

    def show_one_bought_ticket(self, ticket_id):
        with open('signup_information') as json_file:
            data = json.load(json_file)
            temp = data["users"]

            check = True

            for x in temp:
                if x["username"] == self.username and x["password"] == self.password:
                    for y in x["tickets"]:
                        if y["ticket_id"] == ticket_id:
                            check = False
                            ticket_info = str(y.values())
                            print(clean_flight_info(ticket_info))
                    if check:
                        print("Not Found")
        write_json(data)

    def cancel_one_ticket(self, ticket_id):
        with open('signup_information') as json_file:
            data = json.load(json_file)
            temp = data["users"]

            check = True

            for x in temp:
                if x["username"] == self.username and x["password"] == self.password:
                    for y in x["tickets"]:
                        if y["ticket_id"] == ticket_id:
                            check = False
                            if y["type"] == "nonrefundable":
                                print("Bad Request")
                            else:
                                x["wallet"] += (y["cost"] / 2)
                                flights_list[y["flight_id"] - 1]["seats"] += y["quantity"]
                                x["tickets"].remove(y)
                                print("OK")


                    if check:
                        print("Not Found")
        write_json(data)

    # add one to that flights seats again, make that flight available for others
    # after they canceled, the ticket wont be in their list


# classes for filtering through flights data
class Filter_City_to_City:
    def __init__(self, city_1, city_2):
        self.city_1 = city_1
        self.city_2 = city_2

    def filter(self):
        check = True
        for x in flights_list:
            if x["origin"] == self.city_1 and x["destination"] == self.city_2:
                flight_info = str(x.values())
                print(clean_flight_info(flight_info))
                check = False
        if check:
            print("Empty")


class Filter_Price_Range:
    def __init__(self, min_price, max_price):
        self.min_price = min_price
        self.max_price = max_price

    def filter(self):
        check = True
        for x in flights_list:
            if self.min_price <= float(x["cost"]) <= self.max_price:
                check = False
                flight_info = str(x.values())
                print(clean_flight_info(flight_info))
        if check:
            print("Empty")


class Filter_Airline:
    def __init__(self, airline):
        self.airline = airline

    def filter(self):
        for x in flights_list:
            if x["airline"] == self.airline:
                flight_info = str(x.values())
                print(clean_flight_info(flight_info))


class Filter_Departure_Date:
    def __init__(self, min_departure_time, max_departure_time):
        self.min_departure_time = min_departure_time
        self.max_departure_time = max_departure_time

    def filter(self):
        check = True
        for x in flights_list:
            flight_departure_time_compare = datetime.datetime(2022, 2, int(x["departure_date"]),
                                                              int(x["departure_time"][0:2]),
                                                              int(x["departure_time"][3:5]), 00)
            if self.min_departure_time <= flight_departure_time_compare <= self.max_departure_time:
                check = False
                flight_info = str(x.values())
                print(clean_flight_info(flight_info))
        if check:
            print("Empty")


def intro(flights):
    flights.filter()


# finding the cheapest flight
class Cheapest_Flight:
    def __init__(self, departure_date, city_1, city_2):
        self.departure_date = departure_date
        self.city_1 = city_1
        self.city_2 = city_2

    def find_the_flight(self):
        wanted_flights = []
        cheapest_flight_origin = []
        cheapest_flight_destination = []
        cheapest_flight_info = None
        cheapest_flight_price = float("inf")

        check = True

        for x in flights_list:
            if int(x["departure_date"]) == self.departure_date:
                wanted_flights.append(x)

        for y in wanted_flights:
            if y["origin"] == self.city_1 and y["destination"] == self.city_2:
                check = False
                if float(x["cost"]) < cheapest_flight_price:
                    cheapest_flight_price = float(x["cost"])
                    cheapest_flight_info = x

            elif y["origin"] == self.city_1 and y["destination"] != self.city_2:
                check = False
                print("here 1", y)
                cheapest_flight_origin.append(y)

            elif y["origin"] != self.city_1 and y["destination"] == self.city_2:
                check = False
                print("here 2", y)
                cheapest_flight_destination.append(y)

        for i in cheapest_flight_origin:
            for j in cheapest_flight_destination:
                if i["destination"] == j["origin"]:
                    total_cost = float(i["cost"]) + float(j["cost"])
                    if total_cost < cheapest_flight_price:
                        cheapest_flight_price = total_cost
                        cheapest_flight_info = [i, j]
        print(cheapest_flight_price)

        if check:
            print("Empty")
        print(wanted_flights)


# saving the current filter
current_filter = ""

# bought ticket id counter
bought_ticket_id = 1

# for the final overall_report
destinations_dict = {}
airlines_dict = {}

# input
while True:
    user_input = input().split()
    if user_input[0] == "GET":
        if log_in_info["username"] != "" and log_in_info["password"] != "":  # check for being in their acc
            if user_input[1] == "flights":
                # show all the flights
                if len(user_input) == 2:
                    if len(flights_list) == 0:
                        print("Empty")
                    else:
                        for x in flights_list:
                            if int(x["seats"]) >= 1:
                                flight_info = str(x.values())
                                print(clean_flight_info(flight_info))

                # show the flight with the id wanted
                else:
                    try:
                        if user_input[2] == "?":
                            flight_id = int(user_input[user_input.index("id") + 1]) - 1
                            if flight_id <= len(flights_list) - 1:
                                flight_info = str(flights_list[flight_id].values())
                                print(clean_flight_info(flight_info))
                            else:
                                print("Not Found")
                        else:
                            print("Bad Request")
                    except:
                        print("Bad Request")

            elif user_input[1] == "tickets":

                # show ONE specific bought ticket
                try:
                    if user_input[2] == "?":
                        ticket_id = int(user_input[user_input.index("id") + 1])
                        one_bought_ticket = UserInfo(log_in_info["username"], log_in_info["password"])
                        one_bought_ticket.show_one_bought_ticket(ticket_id)

                # show all bought tickets
                except:
                    if len(user_input) == 2:
                        all_bought_tickets = UserInfo(log_in_info["username"], log_in_info["password"])
                        all_bought_tickets.show_all_bought_tickets()
                    else:
                        print("Bad Request")

            # finding the cheapest flight
            elif user_input[1] == "cheapest_flight":
                try:
                    if user_input[2] == "?":
                        cheapest_departure_date = int(user_input[user_input.index("departure_date") + 1])
                        cheapest_city_1 = user_input[user_input.index("from") + 1]
                        cheapest_city_2 = user_input[user_input.index("from") + 3]

                        cheapest_flight = Cheapest_Flight(cheapest_departure_date, cheapest_city_1, cheapest_city_1)
                        cheapest_flight.find_the_flight()
                    else:
                        print("Bad Request")
                except:
                    print("Bad Request")

            # show overall report
            elif user_input[1] == "overall_report":
                # average_flight_cost
                all_flights_costs = [float(x["cost"]) for x in flights_list]

                average_flight_cost = str(sum(all_flights_costs) / len(all_flights_costs))
                average_flight_cost = average_flight_cost[0:7]
                print("average_flight_cost: ", average_flight_cost)

                min_flight_cost = min(all_flights_costs)
                print("min_flight_cost: ", min_flight_cost)

                max_flight_cost = max(all_flights_costs)
                print("max_flight_cost: ", max_flight_cost)

                most_popular_destination = ""
                most_popular_destination_no = 0
                for x in destinations_dict:
                    if most_popular_destination_no < destinations_dict[x]:
                        most_popular_destination_no = destinations_dict[x]
                        most_popular_destination = x
                print("most_popular_destination: ", most_popular_destination)

                airlines_dict_numbers = list(airlines_dict.values())
                for x in range(3 - len(airlines_dict_numbers)):
                    keep = [0] * (3 - len(airlines_dict_numbers))
                    airlines_dict_numbers.extend(keep)
                airlines_dict_numbers.sort()

                first_airline_number = airlines_dict_numbers[len(airlines_dict_numbers) - 1]
                second_airline_number = airlines_dict_numbers[len(airlines_dict_numbers) - 2]
                third_airline_number = airlines_dict_numbers[len(airlines_dict_numbers) - 3]

                for x in airlines_dict:
                    if first_airline_number == 0:
                        first_airline_print = ""
                    elif first_airline_number == airlines_dict[x]:
                        first_airline_print = x

                    if second_airline_number == 0:
                        second_airline_print = ""
                    elif second_airline_number == airlines_dict[x]:
                        second_airline_print = x

                    if third_airline_number == 0:
                        third_airline_print = ""
                    elif third_airline_number == airlines_dict[x]:
                        third_airline_print = x
                if first_airline_number == 0 and second_airline_number == 0 and third_airline_print == 0:
                    print("top_airlines: Empty")
                else:
                    print("top_airlines: ", first_airline_print, second_airline_print, third_airline_print)

            else: print("Bad Request")
        else:
            print("Permission Denied")

    elif user_input[0] == "POST":
        # signing up
        if user_input[1] == "signup":
            try:
                if user_input[2] == "?":
                    username_index = user_input.index("username") + 1
                    password_index = user_input.index("password") + 1

                    user = UserInfo(user_input[username_index], user_input[password_index])
                    user.signup()
                else:
                    print("Bad Request")
            except:
                print("Bad Request")

        # logging in
        elif user_input[1] == "login":
            try:
                if user_input[2] == "?":
                    username_index = user_input.index("username") + 1
                    password_index = user_input.index("password") + 1

                    user = UserInfo(user_input[username_index], user_input[password_index])
                    user.login()
                else:
                    print("Bad Request")
            except:
                print("Bad Request")

        elif log_in_info["username"] != "" and log_in_info["password"] != "":  # check for being in their acc
            # logging out of their acc
            if user_input[1] == "logout":
                log_in_info["username"] = ""
                log_in_info["password"] = ""
                print("OK")

            # change wallet amount
            elif user_input[1] == "wallet":
                try:
                    if user_input[2] == "?":
                        wallet_amount = float(user_input[user_input.index("amount") + 1])
                        if wallet_amount > 0:
                            user = UserInfo(log_in_info["username"], log_in_info["password"])
                            user.increase_wallet_amount(wallet_amount)
                        else:
                            print("Bad Request")
                    else:
                        print("Bad Request")
                except:
                    print("Bad Request")

            # filtering the flights
            elif user_input[1] == "filters":
                if user_input[2] == "?":

                    # filter from city to city
                    try:
                        if user_input[3] == "from":
                            city_1 = user_input[4]
                            city_2 = user_input[6]
                            city_to_city_filter = Filter_City_to_City(city_1, city_2)
                            intro(city_to_city_filter)

                            current_filter = "Filter_City_to_City"
                    except:
                        print("Bad Request")

                    # filtering price range
                    if user_input[3] == "min_price" or user_input[3] == "max_price":
                        if ("min_price" in user_input) and ("max_price" in user_input):
                            min_price = float(user_input[user_input.index("min_price") + 1])
                            max_price = float(user_input[user_input.index("max_price") + 1])
                            if (min_price >= 0) and (max_price >= 0) and (max_price >= min_price):
                                price_filter = Filter_Price_Range(min_price, max_price)
                                intro(price_filter)

                                current_filter = "Filter_Price_Range"
                            else:
                                print("Bad Request")

                        elif ("min_price" not in user_input) and ("max_price" in user_input):
                            min_price = 0
                            max_price = float(user_input[user_input.index("max_price") + 1])
                            if max_price >= 0:
                                price_filter = Filter_Price_Range(min_price, max_price)
                                intro(price_filter)

                                current_filter = "Filter_Price_Range"
                            else:
                                print("Bad Request")

                        elif ("min_price" in user_input) and ("max_price" not in user_input):
                            min_price = float(user_input[user_input.index("min_price") + 1])
                            max_price = float("inf")
                            if min_price >= 0:
                                price_filter = Filter_Price_Range(min_price, max_price)
                                intro(price_filter)

                                current_filter = "Filter_Price_Range"
                            else:
                                print("Bad Request")
                        else:
                            print("Bad Request")

                    # filtering airline
                    if user_input[3] == "airline":
                        airline_filter = Filter_Airline(user_input[4])
                        intro(airline_filter)

                        current_filter = "Filter_Airline"

                    # filtering departure date & time
                    if "departure_date" in user_input:
                        departure_date = int(user_input[user_input.index("departure_date") + 1])
                        if 1 <= departure_date <= 30:
                            if ("min_departure_time" in user_input) and ("max_departure_time" in user_input):
                                min_departure_time = user_input[user_input.index("min_departure_time") + 1]
                                max_departure_time = user_input[user_input.index("max_departure_time") + 1]

                                min_departure_time_compare = datetime.datetime(2022, 2, departure_date,
                                                                               int(min_departure_time[0:2]),
                                                                               int(min_departure_time[3:5]), 00)
                                max_departure_time_compare = datetime.datetime(2022, 2, departure_date,
                                                                               int(max_departure_time[0:2]),
                                                                               int(max_departure_time[3:5]), 00)
                                departure_date_filter = Filter_Departure_Date(min_departure_time_compare,
                                                                              max_departure_time_compare)
                                intro(departure_date_filter)

                                current_filter = "Filter_Departure_Date"

                            elif ("min_departure_time" not in user_input) and ("max_departure_time" in user_input):
                                max_departure_time = user_input[user_input.index("max_departure_time") + 1]

                                min_departure_time_compare = datetime.datetime(2022, 2, departure_date, 00, 00, 00)
                                max_departure_time_compare = datetime.datetime(2022, 2, departure_date,
                                                                               int(max_departure_time[0:2]),
                                                                               int(max_departure_time[3:5]), 00)
                                departure_date_filter = Filter_Departure_Date(min_departure_time_compare,
                                                                              max_departure_time_compare)
                                intro(departure_date_filter)

                                current_filter = "Filter_Departure_Date"

                            elif ("min_departure_time" in user_input) and ("max_departure_time" not in user_input):
                                min_departure_time = user_input[user_input.index("min_departure_time") + 1]

                                min_departure_time_compare = datetime.datetime(2022, 2, departure_date,
                                                                               int(min_departure_time[0:2]),
                                                                               int(min_departure_time[3:5]), 00)
                                max_departure_time_compare = datetime.datetime(2022, 2, departure_date, 23, 59, 59)

                                departure_date_filter = Filter_Departure_Date(min_departure_time_compare,
                                                                              max_departure_time_compare)
                                intro(departure_date_filter)

                                current_filter = "Filter_Departure_Date"

                            else:
                                min_departure_time_compare = datetime.datetime(2022, 2, departure_date, 00, 00, 00)
                                max_departure_time_compare = datetime.datetime(2022, 2, departure_date, 23, 59, 59)

                                departure_date_filter = Filter_Departure_Date(min_departure_time_compare,
                                                                              max_departure_time_compare)
                                intro(departure_date_filter)

                                current_filter = "Filter_Departure_Date"

                        else:
                            print("Bad Request")
                    elif ("departure_date" not in user_input) and (
                            "min_departure_time" in user_input or "max_departure_time" in user_input):
                        print("Bad Request")
                else:
                    print("Bad Request", "here")

            # buying flight tickets
            elif user_input[1] == "tickets":
                if user_input[2] == "?":
                    user_input.index("flight")
                    book_flight_id = int(user_input[user_input.index("flight") + 1])
                    book_quantity = int(user_input[user_input.index("quantity") + 1])
                    book_class = user_input[user_input.index("class") + 1]
                    book_type = user_input[user_input.index("type") + 1]
                    # refundable: half the money + cancel the ticket

                    if int(flights_list[book_flight_id - 1]["seats"]) >= book_quantity:
                        tickets_wallet_amount = UserInfo(log_in_info["username"], log_in_info["password"])
                        buying_ticket_wallet_amount = tickets_wallet_amount.wallet_amount()

                        if book_class == "economy":
                            total_tickets_cost = float(flights_list[book_flight_id - 1]["cost"]) * book_quantity
                            if total_tickets_cost <= buying_ticket_wallet_amount:
                                flights_list[book_flight_id - 1]["seats"] =\
                                    int(flights_list[book_flight_id - 1]["seats"]) - book_quantity
                                tickets_wallet_amount.decrease_wallet_amount(total_tickets_cost)

                                booked_flight = {"ticket_id": bought_ticket_id, "flight_id": book_flight_id,
                                                 "airline": flights_list[book_flight_id - 1]["airline"],
                                                 "quantity": book_quantity,
                                                 "origin": flights_list[book_flight_id - 1]["origin"],
                                                 "destination": flights_list[book_flight_id - 1]["destination"],
                                                 "departure_date": flights_list[book_flight_id - 1]["departure_date"],
                                                 "departure_time": flights_list[book_flight_id - 1]["departure_time"],
                                                 "arrival_date": flights_list[book_flight_id - 1]["arrival_date"],
                                                 "arrival_time": flights_list[book_flight_id - 1]["arrival_time"],
                                                 "class": book_class, "type": book_type, "cost": total_tickets_cost}
                                tickets_wallet_amount.add_bought_ticket(booked_flight)
                                print(bought_ticket_id)
                                bought_ticket_id += 1

                                # for the final overall_report
                                if flights_list[book_flight_id - 1]["destination"] not in destinations_dict.keys():
                                    destinations_dict[flights_list[book_flight_id - 1]["destination"]] = book_quantity
                                else:
                                    destinations_dict[flights_list[book_flight_id - 1]["destination"]] += book_quantity

                                if flights_list[book_flight_id - 1]["airline"] not in airlines_dict.keys():
                                    airlines_dict[flights_list[book_flight_id - 1]["airline"]] = book_quantity
                                else:
                                    airlines_dict[flights_list[book_flight_id - 1]["airline"]] += book_quantity

                            else: print("Bad Request")

                        elif book_class == "business":
                            total_tickets_cost = float(flights_list[book_flight_id - 1]["cost"]) * book_quantity * 2.5
                            if total_tickets_cost <= buying_ticket_wallet_amount:
                                flights_list[book_flight_id - 1]["seats"] = \
                                    int(flights_list[book_flight_id - 1]["seats"]) - book_quantity
                                tickets_wallet_amount.decrease_wallet_amount(total_tickets_cost)

                                booked_flight = {"ticket_id": bought_ticket_id, "flight_id": book_flight_id,
                                                 "airline": flights_list[book_flight_id - 1]["airline"],
                                                 "quantity": book_quantity,
                                                 "origin": flights_list[book_flight_id - 1]["origin"],
                                                 "destination": flights_list[book_flight_id - 1]["destination"],
                                                 "departure_date": flights_list[book_flight_id - 1]["departure_date"],
                                                 "departure_time": flights_list[book_flight_id - 1]["departure_time"],
                                                 "arrival_date": flights_list[book_flight_id - 1]["arrival_date"],
                                                 "arrival_time": flights_list[book_flight_id - 1]["arrival_time"],
                                                 "class": book_class, "type": book_type, "cost": total_tickets_cost}
                                tickets_wallet_amount.add_bought_ticket(booked_flight)
                                print(bought_ticket_id)
                                bought_ticket_id += 1

                                # for the final overall_report
                                if flights_list[book_flight_id - 1]["destination"] not in destinations_dict.keys():
                                    destinations_dict[flights_list[book_flight_id - 1]["destination"]] = book_quantity
                                else:
                                    destinations_dict[flights_list[book_flight_id - 1]["destination"]] += book_quantity

                                if flights_list[book_flight_id - 1]["airline"] not in airlines_dict.keys():
                                    airlines_dict[flights_list[book_flight_id - 1]["airline"]] = book_quantity
                                else:
                                    airlines_dict[flights_list[book_flight_id - 1]["airline"]] += book_quantity

                            else: print("Bad Request")
                        else: print("Bad Request")
                    else: print("Bad Request")
                else: print("Bad Request")
            else: print("Bad Request")
        else:
            print("Permission Denied")

    elif user_input[0] == "DELETE":
        if log_in_info["username"] != "" and log_in_info["password"] != "":  # check for being in their acc
            if user_input[1] == "filters":  # delete all the filters
                if len(user_input) == 2:
                    current_filter = ""
                    for x in flights_list:
                        if int(x["seats"]) >= 1:
                            flight_info = str(x.values())
                            print(clean_flight_info(flight_info))
                else:
                    print("Bad Request")

            # cancel bought ticket
            elif user_input[1] == "tickets":
                if user_input[2] == "?":
                    ticket_id = int(user_input[user_input.index("id") + 1])
                    cancel_ticket = UserInfo(log_in_info["username"], log_in_info["password"])
                    cancel_ticket.cancel_one_ticket(ticket_id)
                else:
                    print("Bad Request")
        else:
            print("Permission Denied")
    else:
        print("Bad Request")
