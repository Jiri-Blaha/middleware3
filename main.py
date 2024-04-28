from flask import Flask, request, jsonify
import yfinance as yf
import requests

WEATHER_TOKEN = "a879e9b7995c46ec8ba221900242704"

app = Flask(__name__)


@app.route("/")
def api():
    airport_name = request.args.get('queryAirportTemp', None)
    stock_name = request.args.get("queryStockPrice", None)
    query = request.args.get('queryEval', None)

    if airport_name is not None:
        if len(airport_name) > 3:
            result = jsonify({})
            result.headers.add('Content-Type', 'application/json')
            return result

        info = requests.get(f"https://www.airport-data.com/api/ap_info.json?iata={airport_name}")

        try:
            data = info.json()
            longitude = data["longitude"]
            latitude = data["latitude"]

            temperature = requests.get(f"http://api.weatherapi.com/v1/current.json?q={latitude},{longitude}&key={WEATHER_TOKEN}")
            result = jsonify(temperature.json()['current']['temp_c'])
        except:
            result = jsonify({})
        result.headers.add('Content-Type', 'application/json')
        return result

    elif stock_name is not None:
        try:
            stock = yf.Ticker(stock_name)
            price = stock.info["currentPrice"]
        except:
            price = {}
        result = jsonify(price)
        result.headers.add('Content-Type', 'application/json')
        return result

    elif query is not None:
        try:
            result = jsonify(eval(query))
        except:
            result = jsonify({})
        result.headers.add('Content-Type', 'application/json')
        return result
    else:
        return jsonify({})
