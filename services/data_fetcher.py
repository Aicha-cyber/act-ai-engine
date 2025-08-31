import yfinance as yf  # import the yfinance library to get stock data from Yahoo finance


def get_stock_data(ticker):  # Function that takes a stock ticker
    # Get basic stock data from Yahoo finance
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            """return a dictionary with specific fields selected
            taken from Yahoo finance info
            try current price, else regular market price else N/A"""
            
            'current_price': info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'company_name': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A')
        }
    except Exception as e:  # catch errors
        print(f"Error fetching data for {ticker}: {e}") # return to console for debugging
        return {  # return a dictionary with N/A placeholders so code won't break
            'current_price': 'N/A',
            'pe_ratio': 'N/A',
            'market_cap': 'N/A',
            'company_name': ticker,
            'sector': 'N/A',
            'industry': 'N/A'
        }


# Test function by running the script directly
if __name__ == "__main__":
    print("Testing data fetcher...")
    print(get_stock_data("AAPL"))
