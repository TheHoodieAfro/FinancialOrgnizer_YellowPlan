from asyncio.windows_events import NULL
from contextlib import nullcontext
from flask import Flask, render_template, request, redirect, url_for, flash

# Aplication variables
distributions=[]

locations=[]

# Aplication classes
class Distribution:
    """Class depicting the plan money distributions
    """    

    def __init__(self, percentage, name):        
        if (percentage < 0 or percentage > 100):
            raise Exception('The percentage for a distribution cannot be 0 or below, or over 100')
        else:
            self.percentage = percentage

        self.name = name
        
        self.percentage = percentage

        self.total_month = 0

        self.total = 0

class Location:
    """Class depicting the location of the money
    """    

    def __init__(self, name):
        self.name = name

        self.total = 0

        self.money={}

class expense:
    """Class depicting the expenses
    """    
    
    def __init__(self, money, description, location, distribution):
        self.money = money
        
        self.description = description

        self.location = location

        self.distribution = distribution

# Application logic
## Basic functions
def create_distribution(percentage, name):
    """Creates and saves a distribution

    Args:
        name (String): Name of the distribution
        name (int): percetage of the distribution
    """ 
    
    distributions.append(Distribution(percentage, name))

def create_location(name):
    """Creates and saves a location

    Args:
        name (String): Name of the location
    """    
    
    locations.append(Location(name))

def check_total_percentage():
    """Checks if the sum of percetages in the distributions is 100

    Returns:
        Boolean: Returns True if the percetage is 100, False if not
    """    
    
    percentage = 0

    for dist in distributions:
        percentage += dist.percentage
    
    return True if percentage==100 else False

def edit_percentage(distribution, new_percentage):
    """Edits the percentage of the specified distribution

    Args:
        distribution (string): Name of the distributions to change the percetage
        new_percentage (int): New percentage

    Returns:
        Boolean: Return True if the distribution exists and its percetage was changed, False if the distribution does not exist
    """    
    
    temp = [x for x in distributions if x.name == distribution]
    
    if len(temp) == 0:
        return False
        
    temp[0].percentage = new_percentage
        
    return True

## Advanced functions
def start_plan():
    """Starts the plan, meaning, the money array is filed with distributions

    Returns:
        Boolean: Returns True if the plan was started succesfully, Flase if the total percentage was not 100
    """    
    
    if check_total_percentage() == False:
        return False
    
    for loc in locations:
        for dist in distributions:
            loc.money[dist.name] = 0
    return True

def add_previous_money(location, distribution, money):
    """Adds money stored before the start of the plan

    Args:
        location (String): Name of the locations the money is
        distribution (String): Name of the distribution the money is about
        money (float): Amount of money to add
    """    
    
    for loc in locations:
        if loc.name == location:
            loc.money[distribution] = money
    
    for dist in distributions:
        if dist.name == distribution:
            dist.total = money

def static_income(location, money):
    """Adds money as a static income, meaning its added to the locations specified with the distributions by percentage

    Args:
        location (String): Name of the locations
        money (float): Amount of money
    """    
    
    for loc in locations:
        if loc.name == location:
            loca = loc
    
    for dist in distributions:
        por = (dist.percentage)/100 * money
        dist.total_month += por

        loca.money[dist.name] += por

def variable_income(distribution, location, money):
    """Add money as a variable income, meaning its added to whatever distribution and locations without dividing it

    Args:
        distribution (String): Name of the distribution
        location (String): Name of the locations
        money (float): Amount of money
    """        
    
    for loc in locations:
        if loc.name == location:
            loc.money[distribution] += money
    
    for dist in distributions:
        if dist.name == distribution:
            dist.total_month += money

def move_money_location(location_origin, location_end, distribution, money):
    """Moves the money from a locations distribution to another locations distribution

    Args:
        location_origin (String): Name of the origin location
        location_end (String): Name of the ending location
        distribution (String): Name of the distribution
        money (float): Amount of money

    Returns:
        Boolean: False if the amount of money asked is not present in the locations distribution
    """    
    
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
    """Moves the money from a distribution in a locations to another

    Args:
        distribution_origin (String): Name of the origin distribution
        distribution_end (String): Name of the end distribution
        location (String): Name of the location
        money (float): Amount of money
        month (String): If the money should be taken from the month or total (True, False)

    Returns:
        Boolean: True if worked
    """    
    
    origin = distributions[0]
    end = distributions[0]
    
    for dist in distributions:
        if dist.name == distribution_origin:
            origin = dist
        elif dist.name == distribution_end:
            end = dist
        
    print(origin.name)
    print(end.name)

    if month == 'True':
        if origin.total_month >= money:
            origin.total_month += -money
            end.total_month += money
        else:
            return False
    else:
        if origin.total >= money:
            origin.total += -money
            end.total += money
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
            if loc.money[distribution] >= money:
                loc.money[distribution] += -money
                break
            else:
                return False

    for dist in distributions:
        if dist.name == distribution:
            if month == "True":
                dist.total_month += -money
            else:
                dist.total += -money
    
    return True

def end_month():
    """Merges the total amount of money with the money of the month for each distribution
    """    
    for dist in distributions:
        dist.total += dist.total_month
        dist.total_month = 0

# Application API
app = Flask(__name__)
app.secret_key = 'c948fa4931abd65ec6174e2b'

@app.route('/')
def dashboard():
    return render_template('/dashboard.html', list_distributions=distributions, list_locations=locations)

@app.route('/distribution/create', methods=['POST'])
def view_create_distribution():
    create_distribution(int(request.form['dist_percentage']), request.form['dist_name'])
    return redirect(url_for('dashboard'))

@app.route('/location/create', methods=['POST'])
def view_create_location():
    create_location(request.form['loc_name'])
    return redirect(url_for('dashboard'))

@app.route('/start', methods=['POST'])
def view_start_plan():
    state = start_plan()
    if state == False:
        flash('The distributions must be 100%')
    return redirect(url_for('dashboard'))

@app.route('/end', methods=['POST'])
def view_end_month():
    end_month()
    return redirect(url_for('dashboard'))

@app.route('/distribution/percentage/edit', methods=['POST'])
def view_edit_percentage():
    edit_percentage(request.form['dist_name'], float(request.form['dist_new_percentage']))
    return redirect(url_for('dashboard'))

@app.route('/money/add/previous', methods=['POST'])
def view_add_previous_money():
    add_previous_money(request.form['loc_name'], request.form['dist_name'], float(request.form['money']))
    return redirect(url_for('dashboard'))

@app.route('/money/add/static', methods=['POST'])
def view_static_income():
    static_income(request.form['loc_name'], float(request.form['money']))
    return redirect(url_for('dashboard'))

@app.route('/money/add/variable', methods=['POST'])
def view_variable_income():
    variable_income(request.form['dist_name'], request.form['loc_name'], float(request.form['money']))
    return redirect(url_for('dashboard'))

@app.route('/money/move/location', methods=['POST'])
def view_move_money_location():
    state = move_money_location(request.form['loc_name'], request.form['loc_name2'], request.form['dist_name'], float(request.form['money']))
    if state == False:
        flash('The locations distribution does not have that amount of money')
    return redirect(url_for('dashboard'))

@app.route('/money/move/distribution', methods=['POST'])
def view_move_money_distribution():
    state = move_money_distribution(request.form['dist_name'], request.form['dist_name2'], request.form['loc_name'], float(request.form['money']), request.form['month'])
    if state == False:
        flash('The distribution in the location does not have that amount of money')
    return redirect(url_for('dashboard'))

@app.route('/money/spend', methods=['POST'])
def view_spend_money():
    state = spend_money(float(request.form['money']), request.form['loc_name'], request.form['dist_name'], request.form['month'])
    if state == False:
        flash('Not enough money in there lil shite')
    return redirect(url_for('dashboard'))

@app.route('/tests', methods=['POST'])
def tests():
    create_distribution(20, 'savings')
    create_distribution(30, 'costs')
    create_distribution(30, 'investments')
    create_distribution(20, 'ahorro')
    
    create_location('bancolombia')
    create_location('rappi')
    create_location('cash')
    create_location('emergency cash')
    return redirect(url_for('dashboard'))