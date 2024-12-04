from flask import Flask, render_template_string
import vnstock3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_yesterday_price(symbol):
    try:
        stock = vnstock3.Vnstock().stock(symbol=symbol, source='VCI')
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        data = stock.quote.history(start=yesterday_str, end=yesterday_str)
        return data['close'].iloc[-1]
    except Exception as e:
        return None
    
def get_current_price(symbol):
    try:
        stock = vnstock3.Vnstock().stock(symbol=symbol, source='VCI')
        now = datetime.now()
        now_str = now.strftime('%Y-%m-%d')
        data = stock.quote.history(start=now_str, end=now_str)
        return data['close'].iloc[-1]
    except Exception as e:
        return None

template = '''
<table>
    <tr>
        <td>{{ price }}</td>
    </tr>
</table>
'''

@app.route('/api/current_price/<symbol>', methods=['GET'])
def get_current_price_route(symbol):
    price = get_current_price(symbol)
    if price is not None:
        return render_template_string(template, price=price)
    else:
        return 'Failed to get current price', 404
    
@app.route('/api/yesterday_price/<symbol>', methods=['GET'])
def get_yesterday_price_route(symbol):
    price = get_yesterday_price(symbol)
    if price is not None:
        return render_template_string(template, price=price)
    else:
        return 'Failed to get yesterday price', 404

if __name__ == "__main__":
    app.run(debug=True)
