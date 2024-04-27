from flask import Flask, request, jsonify
import yfinance as yf
import requests

weather_api_key = "a879e9b7995c46ec8ba221900242704"

app = Flask(__name__)


@app.route("/")
def api():
    airport = request.args.get('queryAirportTemp')
    stock_name = request.args.get("queryStockPrice")
    values = request.args.get('queryEval')

    if airport is not None:
        if len(airport) > 3:
            return jsonify({})

        info = requests.get(f"https://www.airport-data.com/api/ap_info.json?iata={airport}")

        data = info.json()
        longitude = data["longitude"]
        latitude = data["latitude"]

        temperature = requests.get(f"http://api.weatherapi.com/v1/current.json?q={latitude},{longitude}&key={weather_api_key}")
        temp_data = temperature.json()
        result = jsonify(temp_data['current']['temp_c'])
        result.headers.add('Content-Type', 'application/json')
        return result

    elif stock_name is not None:
        stock = yf.Ticker(stock_name)
        price = stock.info["currentPrice"]
        result = jsonify(price)
        result.headers.add('Content-Type', 'application/json')
        return result

    elif values is not None:
        result = eval(values)
        result = jsonify(result)
        result.headers.add('Content-Type', 'application/json')
        return result
    else:
        return jsonify({})
