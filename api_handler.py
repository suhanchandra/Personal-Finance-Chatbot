# api_handler.py
# This file handles external API calls, like fetching stock data.

import requests

def get_stock_data(symbol):
    """
    Fetches real-time stock data from the Alpha Vantage API.

    Args:
        symbol (str): The stock symbol to query (e.g., "IBM").

    Returns:
        str: A formatted string with the stock data or an error message.
    """
    if not symbol or not symbol.strip():
        return "❌ Please enter a valid stock symbol."
        
    # NOTE: This is a demo API key with limitations.
    # For production, use your own key from https://www.alphavantage.co/support/#api-key
    API_KEY = "N5NLCPNQT6HD4IXK"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol.upper()}&apikey={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        quote = data.get('Global Quote')

        if not quote or not quote.get('05. price'):
            note = data.get("Note", "The API may have limitations. Try another symbol like 'IBM' or 'MSFT'.")
            return f"❌ No data available for `{symbol.upper()}`. {note}"
        
        # Safely convert data to float, defaulting to 0.0 if conversion fails
        try:
            price = float(quote.get('05. price', 0))
            change = float(quote.get('09. change', 0))
            high = float(quote.get('03. high', 0))
            low = float(quote.get('04. low', 0))
            volume = int(quote.get('06. volume', 0))
            change_percent = quote.get('10. change percent', '0%')
        except (ValueError, TypeError):
            return f"❌ Could not parse financial data for `{symbol.upper()}`."

        return f"""
📊 **Stock Analysis: {symbol.upper()}**

- 💰 **Current Price**: ₹{price:,.2f}
- 📈 **Change**: ₹{change:,.2f} ({change_percent})
- 📊 **Volume**: {volume:,}
- 🎯 **Day's High**: ₹{high:,.2f}
- 🎯 **Day's Low**: ₹{low:,.2f}

💡 *Real-time data from Alpha Vantage API.*
"""
    except requests.exceptions.Timeout:
        return "❌ The request timed out. Please try again later."
    except requests.exceptions.RequestException as e:
        return f"❌ API Error: Could not connect to the service. Details: {e}"
    except Exception as e:
        return f"❌ An unexpected error occurred: {str(e)}"
