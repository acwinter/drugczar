import random
from random import randint

print "\n" * 6 # let's clear the screen



# -----------------------------------------------------------------------------
#       current project status notes & debug options
# -----------------------------------------------------------------------------
# July 20, 2014

global debug 
# debug = True
debug = False


# -----------------------------------------------------------------------------
#         set global variables & parameters
# -----------------------------------------------------------------------------

screen_width = 65

product_dict = { # we use this to translate user instructions
    "h":"heroin",
    "e":"ecstasy",
    "p":"pot",
    "u":"uppers",
    "d":"downers"
    }

product_options = "[h]eroin, [e]cstacy, [p]ot, [u]ppers, [d]owners, e[x]it"

city_dict = { # we use this to translate user instructions
    "b":"berkeley",
    "o":"oakland",
    "s":"san francisco",
    "a":"alameda",
    "m":"mountain view"
    }

city_options = "[b]erkeley, [o]akland, [s]an francisco, [a]lameda, [m]ountainview"
city_dict_2 = {}

# inventory initialized
max_inventory = 30
starting_units = 30

# wallet initialization
starting_money = 300



# -----------------------------------------------------------------------------
#         class definitions
# -----------------------------------------------------------------------------

class Product(object):
    def __init__(self, name, price_average, price_flux):
       self.name = name
       self.price_average = price_average
       self.price_flux = price_flux


class Location(object):
    def __init__(self, name, factor):
       self.name = name
       self.market_factor = factor

# this will hold the current prices for transactions
class CurrentPrices(object):
    def __init__(self, name):
        self.prices = {}

        if debug:
            print "# executing CurrentPrices()"

    def load_dictionary(self, product, price):
        self.prices[product] = price
        if debug:
            print "# load_dictionary: loaded %s at %s" % (product, price)
        # for key, value in self.prices.iteritems():
        #    print " - {%s : %s}" % (key, value)

    def read_price(self, product):
        
        price = self.prices.get(product)
        if debug:
            print "product is: ", product
            print "# read_price: the price for %s: %s" % (product, price)
        #print self.prices.get(product)
        
        #for key, value in self.prices.iteritems():
        #    print "# %s : %s" % (key, value)

        return(price)

class Inventory(object):
    def __init__(self, starting_amount, max_inventory):
        self.available = starting_amount
        self.max_inventory = max_inventory
        self.inventory_dict = {
            "heroin":0,
            "ecstasy":0,
            "pot":0,
            "uppers":0,
            "downers":0
            }

        if debug: # start us off with some inventory
            self.inventory_dict = {
                "heroin":4,
                "ecstasy":3,
                "pot":3,
                "uppers":15,
                "downers":20
                }

        # we're going to abstract this at some point

    def add(self, product, quantity):
        quantity = int(quantity)

        if debug:
            print "want to add %i of  %s to inventory" % (quantity, product)
            print "we currently have %i units available" % (self.available)

        if quantity > self.available:
            return("no_room")
        
        self.available = self.available - quantity

        self.inventory_dict[product] = self.inventory_dict[product] + quantity

        if debug:
            print "and now we have %i units left" % (self.available)
        
        if debug:
            for key, value in self.inventory_dict.iteritems():
                print key, " : ", value


    def subtract(self, product, quantity):
        quantity = int(quantity)

        if quantity > self.inventory_dict[product]:
            print "um... you only have %i of %s!" % (self.inventory_dict[product], product)
            request_user_command()
            if debug:
                print "inventory.subtract: user has %s and is selling %s" % (self.available, quantity)
            #return("no_room")
        
        self.available = self.available + quantity

        self.inventory_dict[product] = self.inventory_dict[product] - quantity


    def accounting(self, product):
        if debug:
            print "Inventory.accounting looking for:", product

        if product == "all":
            return(self.available)
        else:
            amount_held_in_inventory = self.inventory_dict[product]
            if debug:
                print "quantity found: ", amount_held_in_inventory
            return(amount_held_in_inventory)

class Wallet(object):
    def __init__(self,starting_amount):
        self.on_hand = starting_amount

    def add(self,amount):
        #on_hand = 0
        self.on_hand = self.on_hand + amount

    def subtract(self,amount):
        self.on_hand = self.on_hand - amount

    def accounting(self):
        return(self.on_hand)

        if debug:
            print "# wallet.accounting, on_hand: %s", self.on_hand



# -----------------------------------------------------------------------------
#         manage prices of items
# -----------------------------------------------------------------------------


# calculate a "random" price for a product in a moment
def current_base_price (product):
    pass
    # currently not in use


# now calculate the _actual price_ for an object at a location
def calculate_market_value(product, location):
    this_location_name = location
    this_location_market_factor = location.market_factor

    this_product_name = product
    this_product_price_average = product.price_average
    this_product_price_flux = product.price_flux

    if debug:
        print "calculate_market_value ", product
    
    flux_modifier = randint(1,this_product_price_flux)
    more_or_less = randint(0,1)

    # debug: are we fluctuating price up or down?
    if more_or_less == 1:
        actual_price = this_product_price_average + flux_modifier
    else:
        actual_price = this_product_price_average - flux_modifier

    # we want to make amounts with $.25, $.50, $.75 or $.00
    # we pick a random number out of 100, round it up 
    # and, if it's not '1.0' add it to price 
    quarters = round(random.random() * 4 ) / 4
    if quarters != 1.0:
        actual_price = actual_price + quarters

    return(actual_price)


# set prices for all products in a location at a given visit
def get_product_prices(location):
    if debug:
        print "# execturing get_product_prices(%s" % location.name, ")"
    # iterate over the list of products

    for i in range(len(product_list)):
       actual_price = calculate_market_value(product_list[i],location)
       if debug:
        print "#get_product_prices price for %s in %s is $%.2f" % (product_list[i].name, location.name, actual_price),
       market_values.load_dictionary(product_list[i].name, actual_price)



# -----------------------------------------------------------------------------
#         display routines
# -----------------------------------------------------------------------------

# show the player the prices for all products at that location
def display_product_prices_inventory(location):


    if debug:
        print "location: %s", location
        print "# executing display_product_prices(%s" % location.name, ")"
        this = raw_input("ready to move on>")

    # prepare to display nicely (later to put in own def)
    global screen_width
    price_width = 10
    price_width2 = 9
    inventory_width = 15
    item_width = screen_width - (price_width + inventory_width)
    header_format = "%-*s%*s%*s"
    format = "%-*s%*s%*s"
    print "=" * screen_width
    title_width = (screen_width - len(location.name))/2
    print " " * title_width, location.name, " " * title_width
    print "=" * screen_width
    print format % (item_width, 'Product', price_width, 'Price', inventory_width,'You Own')
    print "-" * screen_width

    # get prices for all products and display nicely
    for i in range(len(product_list)):

        if debug:
            print "display_product_prices_inventory ", product_list[i].name
        product = product_list[i].name
        price = market_values.read_price(product_list[i].name)
        price = make_nice_money(price)

        inventory = player_inventory.accounting(product_list[i].name)
        if inventory == 0:
            inventory = "none"

        print format % (item_width, product, price_width, price,inventory_width,inventory)
    
    # finish printing nicely
    print "=" * screen_width


def display_cash_and_inventory():
    if debug:
        print "# executing display_cash_and_inventory"

    # prepare to display nicely (later to put in own def)
    global screen_width
    cash = player_wallet.accounting()
    cash = make_nice_money(cash)
    cash_text = "Cash: " + cash

    inventory = player_inventory.accounting("all")
    inventory = str(inventory)
    inventory_text = "Inventory Avail: " + inventory + " units"

    middle_width = screen_width - (len(inventory_text) + len(cash_text) + 2) # the +2 is for whitespace

    print cash_text, " " * middle_width, inventory_text
    # finish printing nicely


def display_options(options, screen):
    global screen_width
    options = options 
    format_width = (screen_width - len(options))/2
    print "=" * screen_width
    print format_width * " " + options + format_width * " "
    
    if screen != "city_screen":
        set_options = "[c]ity screen  [*]help  e[x]it"
    else:
        set_options = "[*]help  e[x]it"
    format_width = (screen_width - len(set_options))/2
    print format_width * " " + set_options + format_width * " "

    print "=" * screen_width


def display_city_screen(city):
    global this_city 
    this_city = oakland
    if city != "same": # otherwise, preserve last city 
        this_city = city

    print "\n" * 3

    display_product_prices_inventory(this_city)
    display_cash_and_inventory()

    if debug:
        print "disaply_city_screen ", product_list[2].name

    request_user_command()


def display_intro_screen():
    # need a routine to format block of text for screen size?
    intro = """
      _____                    _____               
     |  __ \                  / ____|              
     | |  | |_ __ _   _  __ _| |     ______ _ _ __ 
     | |  | | '__| | | |/ _` | |    |_  / _` | '__|
     | |__| | |  | |_| | (_| | |____ / / (_| | |   
     |_____/|_|   \__,_|\__, |\_____/___\__,_|_|   
                         __/ |                     
                        |___/  
    """
    print intro
    return(raw_input("'i' for the intro or any other key to start playing Drug Czar >"))


def display_help_screen():
    # need a routine to format block of text for screen size?
    print """
    Here are the commands you can use, not all are available on
    every screen:
     type (*) to reach this (the help) menu
     type (x) to exit the program -- nothing will be saved
     type (b) to buy a product
     type (s) to sell a product
     type (c) to return to the city screen
     type (t) to reach the city screen where you can move
              from one city to the next

    various drugs use different names and different command 
    letters. 
    """
    raw_input("press any key to return to the game >")


def display_exit_screen():
    pass
    print "ok, we've exited! sorry to see you go..."
    exit(1)


def display_info_screen():
    pass
    print """
    The goal in DrugCzar is to gather as much money as possible
    by buying and selling drugs of various types. You start 
    with a certain amount of money and with the ability to 
    carry a certain amount of units of drugs with you from city
    to city. Your goal is to buy low and sell high! Now, get 
    going bucko!
    """


def make_nice_money (amount):
    # takes an integer like "4.2" and formats it as "$4.20"
    amount = amount
    amount = str(amount)

    if "." in amount:
        location = amount.find(".")
        length = len(amount)
        before_decimal = amount[0:location]
        after_decimal = amount[location:length]
        if len(after_decimal) != 3: # 3 b/c of decimal mark
            after_decimal = after_decimal + "0"
        amount = "$" + before_decimal + after_decimal
        return amount
    else:
        amount = "$" + amount + ".00"
        return amount



# -----------------------------------------------------------------------------
#         initialize the wallet
# -----------------------------------------------------------------------------

def initialize_inventory():
    inventory = dict()
    for i in range(len(product_list)):
        inventory[product_list[i].name] = 0
        if debug:
            print "assigning", product_list[i].name   
    return(inventory)



# -----------------------------------------------------------------------------
#         player command interpretation & response logic
# -----------------------------------------------------------------------------

def start_game():
    command = display_intro_screen()
    play_options={'i':'info','':'null'}
    command = clean_up_response(command,play_options)
    if (command == "info"):
        display_info_screen()
        display_help_screen()


def clean_up_response(response, options):
    # pass it a user response and dictionary of valid
    # response options and it should translate respones
    # to proper lowercase, trimmed, long version
    
    response_orig = response
    response = str(response)
    response = response.lower()
    response = response.strip()

    if (response == "x") or (response == "exit"):
        display_exit_screen()

    if (response == "city screen") or (response == "city") or (response == "c"):
        display_city_screen('same')

    if (response == "help") or (response == "*"):
        display_help_screen()

    if debug:
        print "clean_up_response: looking for ", response

    for short, long in options.items():
        if short == response or long == response:
            if debug:
                print "clean_up_response: found ", short, ":", long
            return(long)
        elif short == "" or long == "null": # dictionary will have '':"null" for "anything else"
            return()
    
    # not found in the dictionary loop? warn user return invalid
    print "sorry, '%s' isn't a valid choice." % response_orig
    return("invalid")



def request_user_command():
    display_options("[b]uy, [s]ell, [t]ravel", "city_screen")
    command = raw_input("what would you like to do? > ")
    
    play_options={'b':'buy','s':'sell','t':'travel'}

    command = clean_up_response(command,play_options)

    if debug:
        print "request_user_command: recieved '", command, "'"
        print command

    if command ==  'sell':
        sell_what()
    elif command == 'buy':
        buy_what()
    elif command == 'travel':
        travel()
    elif command == 'invalid': # response from "cleanup response"
        request_user_command()
    else:
        print "sorry, but '%s' doesn't mean anything to me." % command
        request_user_command()



def sell_what():
    product = raw_input("sell what? > ")

    product = clean_up_response(product, product_dict)

    if product == "invalid":
        sell_what()
    #product = product.lower()
    #if product not in product_list_short:
    #    print "there aint no such thing as ", product, "!"
    #    sell_what()

    #product = convert_product_to_long(product)
    if debug:
        print "sell_what() looking for amount of: ", product
    
    amount_in_inventory = player_inventory.accounting(product)

    if amount_in_inventory > 0:
        how_much(product, 'sell', amount_in_inventory)
    else:
        "I'm afraid you don't have any ", product, "!"
        request_user_command()




def buy_what():
    display_options(product_options, "buy_screen")
    product_to_buy = raw_input("what would you like to buy?> ")

    # for short, long in product_dict.items():
    # print "%s : %s" % (short, long)

    product_to_buy = clean_up_response(product_to_buy, product_dict)

    if product_to_buy == "invalid":
        buy_what()
    else:
        how_much(product_to_buy, 'buy', quantity = 0)




def how_much(product, action, quantity):
    if debug:      
        print "product: ", product
        exit(1)

    quantity = raw_input("how much %s do you want to %s? e(x)it > " % (product, action))

    if quantity == "x":
        exit(1)

    try:
        val = int(quantity)
    except ValueError:
        print "sorry, ", quantity, " ain't a number..."
        how_much(product, action, 0)

    if debug:
        print "how_much product ", product

    price = market_values.read_price(product)
    
    if debug:
        print "how_much price", price

    price = float(price)
    quantity = float(quantity)

    if debug:
        print product
        print price

    if debug:
        print "we found the price of %s to be $%.02f" % (product, price)

    if debug:
        print "price: ", price

    if debug:
        print "the price I found is %s" % price
        print "the quantity is ", quantity

    total_cost = quantity * price
    remaining_wallet = player_wallet.accounting() - total_cost

    if remaining_wallet < 0 and action == "buy":
        print "ha! you can't afford that!"
        how_much(product, action, 0)

    if action == "sell":
        dialog = "if you sell %i units of %s you'll get $%.2f!" % (quantity, product, total_cost)
    elif action == "buy":
        dialog = "buying %i units of %s will cost you $%.2f" % (quantity, product, total_cost)
    else:
        print "um.. we have a problem with your buy/sell choice"
        exit(1)

#    display_options(dialog) # let's leave this out for now

    if action == "buy":
        on_hand = player_wallet.accounting()
        #print "you have %s" % make_nice_money(on_hand)
        if on_hand > total_cost:
            #command = raw_input("proceed? (y, n) > ") # got rid of this question and if/else
            #if command == "y":
                result = player_inventory.add(product,quantity)
                if result == "no_room":
                    raw_input("sorry, not enough room! (any key to continue)>")
                    display_city_screen('same')
                player_wallet.subtract(total_cost)
                raw_input("congrats, you now own %i of %s! any key to coninue>" % (quantity, product))
                display_city_screen('same')
            #else:
            #    exit(1)
        else:
            raw_input("dude, you don't have enough money! any key to continue>")
            display_city_screen('same')
    elif action == "sell":
        #command = raw_input("proceed? (y, n) > ") # got rid of this question and if/else
        #if command == "y":
        player_inventory.subtract(product,quantity)
        player_wallet.add(total_cost)
        print 
        raw_input("congrats, you're now %s richer! any key to continue>" % (make_nice_money(total_cost)))
        #display_cash_and_inventory()
        display_city_screen('same')
        #else:
        #    exit(1)
    else:
        "um, we have a problem here"
        exit(1)


def travel():
    #display_options("[h]eroin, [e]cstacy, [p]ot, [u]ppers, [d]owners, e[x]it")
    display_options(city_options, "travel_screen")
    go_to_city = raw_input("where would you like to go?> ")
    go_to_city = clean_up_response(go_to_city, city_dict)

    go_to_city = city_dict_2[go_to_city]
    get_product_prices(go_to_city)
    display_city_screen(go_to_city)

def is_product(product):
    # is user identifying a real product?
    print "is_product()"
    a = product_list

    if a.count(5) == 1:
        b=a.index(5)
        print "found it"
        exit(1)



# -----------------------------------------------------------------------------
#         let's create our products and set their price scope
# -----------------------------------------------------------------------------


product_list_short = ['h','e','p','u','d']
product_list_long = ['heroin', 'ecstasy', 'pot', 'uppers', 'downers']


# here we init our CurrentPrices() object
market_values = CurrentPrices('current')
player_wallet = Wallet(starting_money)
# player_wallet.add(300)
player_inventory = Inventory(starting_units, max_inventory)

# eventually this should just cycle through some initializeation variables
heroin = Product('heroin', 50, 10)
ecstasy = Product('ecstasy', 35, 10)
pot = Product('pot', 20, 5)
uppers = Product('uppers', 10, 2)
downers = Product('downers', 8, 3)

product_list = [heroin, ecstasy, pot, uppers, downers]



# -----------------------------------------------------------------------------
#         create cities and populate their pricing effect
# -----------------------------------------------------------------------------


oakland = Location('oakland', 2)
city_dict_2['oakland'] = oakland

berkeley = Location('berkeley', 7)
city_dict_2['berkeley'] = berkeley

san_francisco = Location('san francisco', 4)
city_dict_2['san francisco'] = san_francisco

alameda = Location('alameda', 3)
city_dict_2['alameda'] = alameda

mountain_view = Location('mountain view', 9)
city_dict_2['mountain view'] = mountain_view



# -----------------------------------------------------------------------------
#         initialize the player wallet
# -----------------------------------------------------------------------------

my_inventory = initialize_inventory()
if debug:
    print "# heroin in inventory = %i" % my_inventory[heroin]
    print "# cash on hand = ", player_wallet.accounting


# -----------------------------------------------------------------------------
#        start the game
# -----------------------------------------------------------------------------

start_game()


# -----------------------------------------------------------------------------
#         setup our first city and take us there!
# -----------------------------------------------------------------------------

get_product_prices(oakland)
print

if debug:
    print "# checking price for heroin. found: %s" % market_values.read_price('Heroin')

go_to_city = city_dict_2['oakland']
display_city_screen(go_to_city)
