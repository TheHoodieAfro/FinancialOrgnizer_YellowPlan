from flask import Flask

# Aplication variables
distributions=[]

locations=[]

# Aplication classes
class Distribution:
    '''Class depicting the plan money distributions'''

    def __init__(self, percentage, name):        
        if (percentage < 0 and percentage > 100):
            self.percentage = percentage
        else:
            raise Exception('The percentage for a distribution cannot be 0 or below, or over 100')

        self.name = name

        self.total_month = 0

        self.total = 0

class Location:
    '''Class depicting the location of the money'''

    def __init__(self, name):
        self.name = name

        self.total = 0

        self.money={}

class expense:
    
    def __init__(self, money, description, location, distribution):
        self.money = money
        
        self.description = description

        self.location = location

        self.distribution = distribution

# Application logic
## Basic functions
def create_distribution(percentage, name):
    distributions.append(Distribution(percentage, name))

def create_location(name, total):
    locations.append(Location(name))

def check_total_percentage():
    percentage = 0

    for dist in distributions:
        percentage += dist.percentage
    
    return True if percentage==100 else False

def edit_percentage(distribution, new_percentage):
    temp = [x for x in distributions if x.name == distribution]
    
    if temp.len() == 0:
        return False
        
    else:
        temp[0].percentage = new_percentage
        
        return True

## Advanced functions
def start_plan():
    if check_total_percentage() == False:
        return False
    
    for loc in locations:
        for dist in distributions:
            loc.money[dist.name] = 0

def add_previous_money(location, distribution, money):
    for loc in locations:
        if loc.name == location:
            loc.money[distribution] = money
    
    for dist in distributions:
        if dist.name == distribution:
            dist.total = money

def static_income(location, money):
    for dist in distributions:
        por = dist.percentage * money
        dist.total_month += por

        for loc in locations:
            if loc.name == location:
                loc.money[dist.name] += por

def variable_income(distribution, location, money):
    for loc in locations:
        if loc.name == location:
            loc.money[distribution] += money
    
    for dist in distributions:
        if dist.name == distribution:
            dist.total_month += money

def move_money_location(location_origin, location_end, distribution, money):
    i = 0
    origin = 0
    end = 0

    for loc in locations:
        if loc.name == location_origin:
            origin = i
        elif loc.name == location_end:
            end = i

        i += 1

    if locations[origin].money[distribution] >= money:
        locations[origin].money[distribution] += -money
        locations[end].money[distribution] += money
    else:
        return False

    return True

def move_money_distribution(distribution_origin, distribution_end, location, money, month):
    i = 0
    origin = 0
    end = 0

    for dist in locations:
        if dist.name == distribution_origin:
            origin = i
        elif dist.name == distribution_end:
            end = i

        i += 1

    if month == True:
        if distributions[origin].total_month >= money:
            distributions[origin].total_month += -money
            distributions[end].total_month += money
        else:
            return False
    else:
        if distributions[origin].total >= money:
            distributions[origin].total += -money
            distributions[end].total += money
        else:
            return False
    
    for loc in locations:
        if loc.name == location:
            loc.money[distribution_origin] += -money
            loc.money[distribution_end] += money

            break

    return True

def spend_money(money, location, distribution, month):
    """Spends money from the especified location and distribution

    Args:
        money (float): Amount of money to spend
        location (string): Location where the money was taken from
        distribution (string): Distribution where the money was used from
        month (boolean): Flag defining if the money should be taken from the full total or month total

    Returns:
        boolean: True if the money was spent, false if not
    """    
    for loc in locations:
        if loc.name == location:
            if loc[distribution] >= money:
                loc[distribution] += -money
                break
            else:
                return False

    for dist in distributions:
        if dist.name == distribution:
            if month == True:
                dist.total_month += -money
            else:
                dist.total += -money
    
    return True

def end_month():
    """Merges the total amount of money with the money of the month for each distribution
    """    
    for dist in distributions:
        dist.total += dist.total_money
        dist.total_money = 0

# Application API
app = Flask(__name__)

@app.route('/')
def hello():   
    return 'hello word'