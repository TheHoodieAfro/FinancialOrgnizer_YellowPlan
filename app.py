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
        flash('The distributions must sum up 100%')
    return redirect(url_for('dashboard'))

@app.route('/end', methods=['POST'])
def view_end_month():
    end_month()
    return redirect(url_for('dashboard'))

@app.route('/distribution/percentage/edit', methods=['POST'])
def view_edit_percentage():
    edit_percentage(request.form['dist_name'], int(request.form['dist_new_percentage']))
    return redirect(url_for('dashboard'))

@app.route('/money/add/previous', methods=['POST'])
def view_add_previous_money():
    add_previous_money(request.form['loc_name'], request.form['dist_name'], int(request.form['money']))
    return redirect(url_for('dashboard'))

@app.route('/spend', methods=['POST'])
def spend():
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