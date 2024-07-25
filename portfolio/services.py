import finnhub
import requests
import yfinance as yf

from datetime import datetime
from decimal import Decimal, DivisionUndefined
from django.utils.http import urlencode

from .models import Stock, Transaction


# API KEYS
NEWS_API_KEY = "bcda9f940e6649a1b330e72c0297b235"
FINNHUB_API_KEY = "cq1o6hhr01qjh3d5s4tgcq1o6hhr01qjh3d5s4u0"

def format_large_number(number):
    if number is None:
        return "N/A"
    elif number >= 1_000_000_000_000:
        return f"{number / 1_000_000_000_000:.2f} Trillion"
    elif number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f} Billion"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.2f} Million"
    else:
        return f"{number:,}"
    

def format_unix_timestamp(timestamp):
    date_object = datetime.fromtimestamp(timestamp)
    formatted_date1 = date_object.strftime("%B %d")
    formatted_date2 = date_object.strftime("%B %d, %Y")
    return [formatted_date1, formatted_date2]


def get_latest_news():
    try:
        symbols = Stock.objects.values_list("symbol", flat=True)
        if not symbols:
            print("No symbols found in the database.")
            return []
        
        query = ' OR '.join([f'"{symbol}"' for symbol in symbols])

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": NEWS_API_KEY
        }

        encoded_params = urlencode(params)
        full_url = f"{url}?{encoded_params}"
        response = requests.get(full_url)

        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])
            for article in articles:
                if "publishedAt" in article:
                    timestamp = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                    article["formatted_time"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            return articles
        else:
            print(f"Failed to fetch news. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
            

def get_company_info(symbol):
    finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
    try:
        company_profile = finnhub_client.company_profile2(symbol=symbol)
        stock = yf.Ticker(symbol)
        info = stock.info

        company_officers = info.get("companyOfficers", [])
        formatted_officers = []
        for officer in company_officers:
            officer["totalPayFormatted"] = format_large_number(officer.get("totalPay"))
            formatted_officers.append(officer)

        return {
            # Company Information
            "name": info.get("longName", "N/A"),
            "is_active": finnhub_client.market_status(exchange="US").get("isOpen", False),
            "bio": info.get("longBusinessSummary", "N/A"),
            "logo": company_profile.get("logo"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "employee_count": info.get("fullTimeEmployees", "N/A"),
            "fy_end": format_unix_timestamp(info.get("nextFiscalYearEnd"))[0],
            "website": company_profile.get("weburl", "N/A"),
            "company_officers": formatted_officers,

            # OHLCV + Core Data
            "current_price": format(info.get("currentPrice", 0), ".2f"),
            "previous_close": format(info.get("previousClose", 0), ".2f"),
            "price_delta": round(info.get("currentPrice", 0) - info.get("previousClose", 0), 2),
            "delta_percentage": format(((info.get("currentPrice", 0) - info.get("previousClose", 0)) / info.get("previousClose", 1)) * 100, ".2f"),
            "open": format(info.get("open", 0), ".2f"),
            "high": format(info.get("dayHigh", 0), ".2f"),
            "low": format(info.get("dayLow", 0), ".2f"),
            "volume": format_large_number(info.get("volume", 0)),
            "avg_volume": format_large_number(info.get("averageVolume", 0)),
            "shares_outstanding": format_large_number(info.get("sharesOutstanding", 0)),
            "market_cap": format_large_number(info.get("marketCap", 0)),
            "pe_ratio": format(info.get("trailingPE", 0), ".2f"),
            "eps": format(info.get("trailingEps", 0), ".2f"),
            "beta": format(info.get("beta", 0), ".2f"),
            "target_mean_price": info.get("targetMeanPrice", "N/A"),
            "fifty_two_week_high": format(info.get("fiftyTwoWeekHigh", 0), ".2f"),
            "fifty_two_week_low": format(info.get("fiftyTwoWeekLow", 0), ".2f"),

            # Financial Metrics
            "total_cash": format_large_number(info.get("totalCash", 0)),
            "total_revenue": format_large_number(info.get("totalRevenue", 0)),
            "total_debt": format_large_number(info.get("totalDebt", 0)),
            "ebitda": format_large_number(info.get("ebitda", 0)),
            "free_cf": format_large_number(info.get("freeCashflow", 0)),
            "operating_cf": format_large_number(info.get("operatingCashflow", 0)),
            "earnings_growth": format(info.get("earningsGrowth", 0) * 100, ".2f"),
            "revenue_growth": format(info.get("revenueGrowth", 0) * 100, ".2f"),
            "debt_to_equity": info.get("debtToEquity", "N/A"),
            "quick_ratio": info.get("quickRatio", "N/A"),
            "current_ratio": info.get("currentRatio", "N/A"),
            "revenue_per_share": info.get("revenuePerShare", "N/A"),
            "return_on_assets": format(info.get("returnOnAssets", 0) * 100, ".2f"),
            "return_on_equity": format(info.get("returnOnEquity", 0) * 100, ".2f"),
            "operating_margins": format(info.get("operatingMargins", 0) * 100, ".2f"),
            "gross_margins": format(info.get("grossMargins", 0) * 100, ".2f"),

            # Share Information
            "float_shares": format_large_number(info.get("floatShares", 0)),
            "shares_short": format_large_number(info.get("sharesShort", 0)),
            "short_ratio": info.get("shortRatio", "N/A"),
            "held_percent_insiders": format(info.get("heldPercentInsiders", 0) * 100, ".2f"),
            "held_percent_institutions": format(info.get("heldPercentInstitutions", 0) * 100, ".2f"),

            # Corporate Governance
            "audit_date": format_unix_timestamp(info.get("governanceEpochDate"))[1] if info.get("governanceEpochDate") is not None else None,
            "audit_risk": info.get("auditRisk", "N/A"),
            "board_risk": info.get("boardRisk", "N/A"),
            "compensation_risk": info.get("compensationRisk", "N/A"),
            "shareholder_rights_risk": info.get("shareHolderRightsRisk", "N/A"),
            "overall_risk": info.get("overallRisk", "N/A"),

            # Other Useful Data
            "dividend_rate": format(info.get("dividendRate", 0) if info.get("dividendRate") is not None else 0, ".2f"),
            "dividend_yield": format(info.get("dividendYield", 0) * 100, ".2f"),
            "ex_dividend_date": format_unix_timestamp(info.get("exDividendDate"))[1] if info.get("exDividendDate") is not None else None
        }
    except Exception as e:
        print(f"Error fetching company information for {symbol}: {e}")
        return None


def get_intraday_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d", interval="1m")
        hist.index = hist.index.strftime("%I:%M %p")
        intraday_data = hist[["Open", "High", "Low", "Close", "Volume"]].to_dict(orient="index")
        return intraday_data
    except Exception as e:
        print(f"Error fetching intraday data for {symbol}: {e}")
        return None


def get_historical_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="max")
        hist.index = hist.index.strftime("%Y-%m-%d")
        historical_data = hist[["Open", "High", "Low", "Close", "Volume"]].to_dict(orient="index")
        return historical_data
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return None


def get_company_news(symbol):
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": symbol,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])
            for article in articles:
                if "publishedAt" in article:
                    timestamp = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                    article["formatted_time"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            return articles
        else:
            print(f"Failed to fetch news for {symbol}. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching company news for {symbol}: {e}")
        return []
    

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    current_price = stock.history(period="1d")["Close"].iloc[0]
    previous_price = stock.history(period="5d")["Close"].iloc[-2]
    return current_price, previous_price


from decimal import Decimal, DivisionUndefined

def get_portfolio_summary(user_portfolio):
    transactions = Transaction.objects.filter(portfolio=user_portfolio)
    holdings_summary = {}
    portfolio_value = Decimal("0.00")
    day_change = Decimal("0.00")
    percent_change = Decimal("0.00")
    unrealised_gain_loss = Decimal("0.00")

    for transaction in transactions:
        stock = transaction.stock
        if stock.symbol not in holdings_summary:
            holdings_summary[stock.symbol] = {
                "name": stock.name,
                "symbol": stock.symbol,
                "total_quantity": Decimal("0.00"),
                "average_cost": Decimal("0.00"),
                "current_price": Decimal("0.00"),
                "cost_basis": Decimal("0.00"),
                "market_value": Decimal("0.00"),
                "day_change": Decimal("0.00"),
                "percent_change": Decimal("0.00"),
                "unrealised_gain_loss": Decimal("0.00")
            }

        quantity = Decimal(transaction.quantity)
        purchase_price = Decimal(transaction.purchase_price)

        holdings_summary[stock.symbol]["total_quantity"] += quantity
        holdings_summary[stock.symbol]["cost_basis"] += purchase_price * quantity

    for symbol, holding in holdings_summary.items():
        try:
            current_price, previous_close = get_stock_data(symbol)
        except DivisionUndefined:
            current_price = previous_close = Decimal("0.00")

        if holding["total_quantity"] != Decimal("0.00"):
            holding["average_cost"] = holding["cost_basis"] / holding["total_quantity"]
        else:
            holding["average_cost"] = Decimal("0.00")

        holding["current_price"] = Decimal(current_price)
        holding["market_value"] = holding["total_quantity"] * Decimal(current_price)
        holding["day_change"] = holding["total_quantity"] * (Decimal(current_price) - Decimal(previous_close))
        if holding["average_cost"] != Decimal("0.00"):
            holding["percent_change"] = ((holding["current_price"] - holding["average_cost"]) / holding["average_cost"]) * Decimal("100.00")
        else:
            holding["percent_change"] = Decimal("0.00")
        holding["unrealised_gain_loss"] = holding["market_value"] - holding["cost_basis"]

        holding["total_quantity"] = format(holding["total_quantity"], ".2f")
        holding["average_cost"] = format(holding["average_cost"], ".2f")
        holding["current_price"] = format(holding["current_price"], ".2f")
        holding["cost_basis"] = format(holding["cost_basis"], ".2f")
        holding["market_value"] = format(holding["market_value"], ".2f")
        holding["day_change"] = round(holding["day_change"], 2)
        holding["percent_change"] = round(holding["percent_change"], 2)
        holding["unrealised_gain_loss"] = round(holding["unrealised_gain_loss"], 2)

        portfolio_value += Decimal(holding["market_value"])
        day_change += Decimal(holding["day_change"])
        unrealised_gain_loss += Decimal(holding["unrealised_gain_loss"])

    if portfolio_value != Decimal("0.00"):
        percent_change = round(100 - ((portfolio_value - unrealised_gain_loss) / portfolio_value) * Decimal("100.00"), 2)

    portfolio_value = format(portfolio_value, ".2f")
    day_change = round(day_change, 2)
    unrealised_gain_loss = round(unrealised_gain_loss, 2)

    return {
        "portfolio_value": portfolio_value,
        "day_change": day_change,
        "percent_change": percent_change,
        "unrealised_gain_loss": unrealised_gain_loss,
        "holdings_summary": holdings_summary
    }


def get_portfolio_performance_data(symbols):
    portfolio_data = []
    try:
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1mo")
            if not hist.empty:
                hist.reset_index(inplace=True)
                hist["Date"] = hist["Date"].dt.strftime("%Y-%m-%d")
                hist = hist[["Date", "Close"]]
                hist["Symbol"] = symbol
                portfolio_data.append(hist.to_dict(orient="records"))
        return portfolio_data
    except Exception as e:
        print(f"Error fetching portfolio performance data: {e}")
        return None