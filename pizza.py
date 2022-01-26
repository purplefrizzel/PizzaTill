#!/usr/bin/python

# Pizza Till
# Lewis Shaw

import os
import sys
import time
import re

isProgramRuning = True
welcomeMessageDisplay = False
lastShownMenu = 0

order = { "pizzas": [] }
customer = { "customerName": None, "customerPhoneNumber": None, "customerAddress": { "postcode": None, "houseNumber": None } }

class TooManyPizzasError(BaseException):
    pass


class OrderIsNotValidError(BaseException):
    pass


def is_order_valid() -> bool:
    pizzas = order["pizzas"]

    if len(pizzas) > 0 and customer["customerName"] != None:
        return True

    return False


def cancel_order():
    global order
    global customer

    order = { "pizzas": [] }
    customer = { "customerName": None, "customerPhoneNumber": None, "customerAddress": { "postcode": None, "houseNumber": None } }


def print_title(title: str):
    new_line()
    print(title)
    print("." * 32)


def new_line():
    print()


def enter_customer_name():
    try:
        customerName = str(input("Enter customer's first name: "))
        customerName = customerName.strip(" ")

        if customerName.isalpha() == False:
            raise ValueError
        
        if len(customerName) == 0:
            raise ValueError

        customer["customerName"] = customerName
    except ValueError:
        handle_error("Please enter an correct value.")
        enter_customer_name()


def enter_customer_phone_number():
    try:
        customerPhoneNumber = str(input("Enter customer's phone number: "))

        customerPhoneNumber = customerPhoneNumber.strip(" ")

        if len(customerPhoneNumber) != 11:
            raise ValueError

        customer["customerPhoneNumber"] = customerPhoneNumber

    except ValueError:
        handle_error("Please enter an correct UK phone number.")
        enter_customer_phone_number()


def enter_customer_address():
    try:
        customerAddress = str(input("Enter customer's house number and postcode (seperate by a comma): "))

        customerAddressDetails = customerAddress.split(",")
        houseNumber = str(customerAddress[0]).strip(" ")
        postcode = str(customerAddressDetails[1]).strip(" ")

        if houseNumber.isnumeric() == False:
            raise ValueError

        if re.search("/^[a-z]{1,2}\d[a-z\d]?\s*\d[a-z]{2}$/i", postcode) == False:
            raise ValueError

        customer["customerAddress"] = { "houseNumber": houseNumber, "postcode": postcode }
    except ValueError:
        handle_error("Please enter an correct house number and UK postcode.")
        enter_customer_address()
    except IndexError:
        handle_error("Please seperate the address details by comma like this 32,PC11 4RT.")
        enter_customer_address()


def customer_details():
    new_line()
    print("Customer Name:", customer["customerName"])
    print("Customer Phone Number:", customer["customerPhoneNumber"])
    print("Customer Address:", customer["customerAddress"])


def customer_details_menu():
    global customer

    print_title("Enter Customer Details")

    new_line()

    enter_customer_name()
    enter_customer_phone_number()
    enter_customer_address()

    customer_details()
    new_line()

    answer = str(input("Is this data correct? "))
    answer = answer.lower()

    if answer == "yes":
        clear_screen()
        showMenus(1)
    else:
        clear_screen()
        showMenus(2)


def complete_order_menu():
    print_title("Complete Order")
    new_line()
    new_line()

    smallPizza = 0
    mediumPizza = 0
    largePizza = 0
    extraToppingsCharge = 0


    for pizza in order["pizzas"]:
        if pizza["size"] == "small":
            smallPizza += 1
        elif pizza["size"] == "medium":
            mediumPizza += 1
        elif pizza["size"] == "large":
            largePizza += 1

        if pizza["addedTopping"] == 1:
            extraToppingsCharge += 0.75
        elif pizza["addedTopping"] == 2:
            extraToppingsCharge += 1.35
        elif pizza["addedTopping"] == 3:
            extraToppingsCharge += 2.00
        else:
            extraToppingsCharge += 2.50

    smallPizzaCost = round(smallPizza * 3.25, 2)
    mediumPizzaCost = round(mediumPizza * 5.50, 2)
    largePizzaCost = round(largePizza * 7.15, 2)
    extraToppingsCharge = round(extraToppingsCharge, 2)
    subtotal = round(smallPizzaCost + mediumPizzaCost + largePizzaCost + extraToppingsCharge, 2)

    print("_" * 38)
    print("{:>15} {:>10} {:>10}".format("Qty", "Pizza", "Amount"))

    if smallPizza != 0:
        print("{:>15} {:>10} £{:>10}".format(smallPizza, "Small Pizza", smallPizzaCost))
    if mediumPizza != 0:
        print("{:>15} {:>10} £{:>10}".format(mediumPizza, "Medium Pizza", mediumPizzaCost))
    if largePizza != 0:
        print("{:>15} {:>10} £{:>10}".format(largePizza, "Large Pizza", largePizzaCost))

    print("_" * 38)

    if extraToppingsCharge != 0:
        print("{:>15} £{:>20}".format("Extra Toppings Charge", extraToppingsCharge))

    if subtotal >= round(20.0, 2):
        #subtotal = subtotal / 0.1
        print("{:>15} £{:>20}".format("Discount", "10%"))

    print("{:>15} £{:>20}".format("Delivery Charge", "2.50"))

    print("{:>15} £{:>20}".format("Subtotal", round(subtotal, 2)))

    print("_" * 38)

    total = round(subtotal + 2.5, 2)

    print("{:>15} £{:>20}".format("Total", total))

    print("_" * 38)

    new_line()
    new_line()

    corret = input("Is this corret? ").lower()

    if corret == "yes":
        cancel_order()
        clear_screen()
        showMenus(0)
    else:
        clear_screen()
        showMenus(1)


def add_pizza_menu():
    print_title("Select a Pizza Size")
    print("1. Small - £3.25")
    print("2. Medium - £5.50")
    print("3. Large - £7.15")
    print("4. Done?")

    new_line()

    option = int(input("Please select an option: "))
    
    try:
        if len(order["pizzas"]) > 5 and option != 4:
            raise TooManyPizzasError
        elif option == 1:
            order["pizzas"].append({ "size": "small", "addedTopping": None })
        elif option == 2:
            order["pizzas"].append({ "size": "medium", "addedTopping": None })
        elif option == 3:
            order["pizzas"].append({ "size": "large", "addedTopping": None })
        elif option == 4:
            clear_screen()
            showMenus(1)
        else:
            handle_error(str(option) + " is not a correct option.")
    except ValueError:
        handle_error("Please enter an correct option.")
    except TooManyPizzasError:
        handle_error("You can only order a max of 6 pizzas at one time.")


def pizza_toppings_menu():
    print_title("Add Toppings to Order")
    new_line()

    pizzas = order["pizzas"]
    pizzaIndex = 0

    for pizza in pizzas:
        print(pizzaIndex, pizza)
        pizzaIndex += 1

    print("7: Done?")

    try:
        new_line()
        pizza = int(input("Select a pizza to add toppings to: "))

        if pizza == 7:
            clear_screen()
            showMenus(1)

        if pizza > len(pizzas):
            raise ValueError

        new_line()
        toppings = int(input("How many toppings would you like: "))

        pizzas[pizza]["addedTopping"] = toppings
        clear_screen()
    except ValueError:
        handle_error("Please enter an correct pizza.")


def order_pizza_menu():
    print_title("Order Pizza")
    print("1. Customer details")
    print("2. Add pizza to order")
    print("3. Add extra toppings to order")
    print("4. Complete order")
    print("5. Cancel")

    new_line()

    try:
        option = int(input("Select an option > "))

        if option == 1:
            if customer["customerName"] == None:
                clear_screen()
                showMenus(2)
            else:
                customer_details()
        elif option == 2:
            clear_screen()
            showMenus(3)
        elif option == 3:
            clear_screen()
            showMenus(4)
        elif option == 4:
            if is_order_valid() == False:
                raise OrderIsNotValidError
            
            clear_screen()
            showMenus(5)
        elif option == 5:
            cancel_order()

            clear_screen()
            showMenus(0)
        else:
            handle_error(str(option) + " is not a correct option.")
    except ValueError:
        handle_error("Please enter an correct option.")
    except OrderIsNotValidError:
        handle_error("The order is not valid, please check the order.")


def welcome_message(username: str):
    print("     Pizza till")
    print("     Welcome,", username)
    print("." * 32)
    new_line()


def main_menu():
    global isShowingMainMenu

    print_title("Main Menu")
    print("1. Create an order")
    print("2. Exit")

    new_line()

    try:
        option = int(input("Select an option > "))

        if option == 1:
            clear_screen()
            showMenus(1)
        elif option == 2:
            exit(0)
        else:
            handle_error(str(option) + " is not a correct option.")
    except ValueError:
        handle_error("Please enter an correct option.")


def handle_error(error):
    clear_screen()

    if error == None or error == "":
        print("There was an unknown error.")
    else:
        print(error)

    new_line()


def program():
    global isShowingMainMenu
    global welcomeMessageDisplay

    if welcomeMessageDisplay == False:
        welcome_message("Lewis")
        welcomeMessageDisplay = True
        isShowingMainMenu = True

    showMenus(lastShownMenu)


def showMenus(index: int):
    global lastShownMenu

    if index == 0:
        lastShownMenu = 0
        main_menu()
    elif index == 1:
        lastShownMenu = 1
        order_pizza_menu()
    elif index == 2:
        lastShownMenu = 2
        customer_details_menu()
    elif index == 3:
        lastShownMenu = 3
        add_pizza_menu()
    elif index == 4:
        lastShownMenu = 4
        pizza_toppings_menu()
    elif index == 5:
        lastShownMenu = 5
        complete_order_menu()


def exit(code: int):
    global isProgramRuning
    isProgramRuning = False

    print("Exiting...")
    time.sleep(1)
    sys.exit(code)


def clear_screen():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


while isProgramRuning:
    program()