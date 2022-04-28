from flask import Flask

# Aplication classes
class Distribution:
    '''Class depicting the plan money distributions'''

    def __init__(self, percentage, name, total_month, total=0):
        if (percentage < 0 and percentage > 100):
            self.percentage = percentage
        else:
            raise Exception('The percentage for a distribution cannot be 0 or below, or over 100')

        self.name = name

        self.total_month = total_month

        self.total=total

class Location:
    '''Class depicting the location of the money'''

    def __init__(self, name):
        self.name = name

        self.money={}

# Aplication variables
distributions=[]

locations=[]

plan_status = False

# Application logic
## Basic functions
def create_distribution(percentage, name, total_month, total):
    distributions.append(Distribution(percentage, name, total_month, total))

def create_location(name, total):
    locations.append(Location(name))

def check_total_percentage():
    percentage = 0

    for dist in distributions:
        percentage += dist.percentage
    
    return True if percentage==100 else False

def edit_percentage(distribution, new_percentage):
    cond = False

    for dist in distributions:
        if dist.name == distribution:
            dist.percentage = new_percentage
            cond = True
    return cond

def add_previous_money(location, distribution, money):
    for loc in locations:
        if loc.name == location:
            loc.money[distribution] = money
    
    for dist in distributions:
        if dist.name == distribution:
            dist.total = money

## Advanced functions
def start_plan():
    if check_total_percentage() == False:
        return False
    
    for loc in locations:
        for dist in distributions:
            loc.money[dist.name] = 0

def static_income(location, money):
    for dist in distributions:
        por = dist.percentage * money
        dist.total_month = por

        for loc in locations:
            if loc.name == location:
                loc.money[dist.name] = por

# Application API
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hellold'