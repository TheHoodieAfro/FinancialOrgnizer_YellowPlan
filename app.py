from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hellold'

class Distribution:
    '''Class depicting the plan money distributions'''

    def __init__(self, percentage, total_month, total=0):
        if (percentage <= 0 and percentage > 100):
            self.percentage = percentage
        else:
            raise Exception('The percentage for a distribution cannot be 0 or below, or over 100')

        self.total=total

        self.total_month = total_month