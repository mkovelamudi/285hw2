import requests
import json
from datetime import datetime
from pytz import reference
from flask import Flask, jsonify, request, render_template
import os


app = Flask(__name__, template_folder="./")

@app.route('/')
@app.route('/home')
def initial_page():
    return render_template('Finance.html')

@app.route('/submit', methods=['POST'])
def get_stock_details():
    try:
        error_msg = ""
        stockSymbol = request.form.get('stockSymbol')
       
        url = "https://real-time-finance-data.p.rapidapi.com/search"

        querystring = {"query":stockSymbol,"language":"en"}

        headers = {
	        "X-RapidAPI-Key": "8b4aba3b99msh05941ba8c07b031p1beb9ejsn37cbb66a0ea5",
	        "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        stock_data = json.loads(response.text)
        if len(stock_data['data']['stock']) > 0:
            current_time = datetime.now()
            timeZone = reference.LocalTimezone().tzname(current_time)
            time = f"{current_time.strftime('%a %b %d %Y %H:%M:%S')} {timeZone}"
            name = f"{stock_data['data']['stock'][0]['name']} ({stockSymbol})"
            value_change = stock_data['data']['stock'][0]['change']
            percent_change = stock_data['data']['stock'][0]['change_percent']
            change = ""
            if value_change > 0 or percent_change > 0:
                change += f"{stock_data['data']['stock'][0]['price']} +{value_change} (+{percent_change}%)"
            else:
                change += f"{stock_data['data']['stock'][0]['price']} {value_change} ({percent_change}%)"
            api_data = {
                "time": time,
                "name": name,
                "change": change
            }

            return render_template('output.html', data = api_data)
        else:
            return render_template('noSymbol.html')
    
    except requests.ConnectionError as e:
       send_error_response(e)
    except requests.Timeout as e:
        send_error_response(e)
    except requests.RequestException as e:
        send_error_response(e)
    except Exception as e:
        send_error_response(e)

def send_error_response(msg):
    error_data = {
            "error": str(msg)
        }
    return render_template('error.html', data=error_data)
        

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)