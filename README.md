# CS50W CAPSTONE PROJECT: STOCK TRACKER

## Overview
Stock Tracker is a comprehensive web application designed to help users track and analyse their stock portfolios. The application leverages Django for the backend and JavaScript for the frontend to provide a robust and user-friendly experience. It incorporates real-time stock data, historical analysis, portfolio management, and news aggregation to keep users informed about their investments.

I set out to create an interactive web application to allow beginnners to try their hands at playing the stock market (risk-free!) by tracking the performance of the stocks which they are interested in. The main components are:

* Home Page (This displays all news articles related to stocks which the user has searched for. This has already been prefilled with some of the most popular stocks such as AAPL, NVDA, GOOG, META, etc.)
* Login/Logout/Register
* Search for stocks via their symbols
* A stock details page which displays all information relevant to the company and stock
* A portfolio page tracking the performance of stocks that were "purchased" via the stock details page

## Distinctiveness and Complexity
Stock Tracker is distinct from other projects in the CS50W course in several key ways:

- **Complexity and Scope**: Unlike the simpler e-commerce or social networking applications, Stock Tracker integrates multiple APIs (Finnhub, Yahoo Finance, News API) to fetch real-time and historical stock and news data, which is then processed and presented in a user-friendly manner. This involves handling large datasets, performing calculations for portfolio metrics, and rendering complex visualisations. Suffice to say that Stock Tracker is more than sufficiently distinct from all the other projects in this course, and is also not based on the old CS50W Pizza project. More than 1 Django model was used, and JavaScript was used extensively on the front-end.
- **Functionality**: The application includes advanced features such as dynamic portfolio performance updates, stock detail views with extensive data (market data, financial metrics, etc.), historical data charts, and a news aggregation system. These functionalities go beyond the typical CRUD operations found in standard projects.
- **Mobile Responsiveness**: The application is fully mobile-responsive, ensuring that users have a seamless experience across different devices. This involves using responsive design principles and testing on various screen sizes.
- **User Experience**: Emphasis is placed on providing a clean, intuitive user interface with smooth interactions. Features like dynamic data updates using JavaScript, interactive charts, and hover effects enhance the user experience.

## Project Structure

### `portfolio` app
- `templates/portfolio`: Contains the HTML templates for the application.
- `static/portfolio`: Includes static files written in CSS and JavaScript.
- `models.py`: Defines the data models for Stock, Portfolio, and Transaction.
- `services.py`: Contains utility functions for interacting with external APIs and processing stock data.
- `urls.py`: Maps URL patterns to their corresponding views.
- `views.py`: Contains the views for handling user requests and rendering the appropriate templates.

### `templates/portfolio`
- `layout.html`: The base template that includes common elements like the navbar and sidebar.
- `login.html`: The login page template.
- `register.html`: The register page template.
- `latest_news.html`: Displays all relevant news articles to the user.
- `stock_details.html`: Shows detailed information about a specific stock.
- `portfolio_view.html`: Displays the user's portfolio with detailed performance metrics.

### `static/portfolio`
- `styles.css`: Custom CSS styles for the application. Used to add styling that couldn't be done via Bootstrap.
- `icon_hover.js`: JavaScript for hover effects on icons in the navbar.
- `portfolio_chart.js`: JavaScript for rendering an interactive portfolio performance chart.
- `price_chart.js`: JavaScript for rendering an interactive intraday and historical stock price performance chart.
- `stock_details.js`: JavaScript for managing the display and interaction of stock details sections in the DOM.

## `services.py` Functions
- `API Keys`: Stores API keys for News API and Finnhub API.
- `format_large_number`: Formats large numbers into a readable string with appropriate suffixes (Million, Billion, Trillion).
- `format_unix_timestamp`: Converts Unix timestamps into formatted date strings.
- `get_latest_news`: Fetches the latest news articles related to stock symbols stored in the database using the News API.
- `get_company_info`: Retrieves detailed company information, including financial metrics, officer details, and market data using Finnhub and Yahoo Finance APIs.
- `get_intraday_data`: Fetches intraday stock data for the current day with minute-level intervals using Yahoo Finance API.
- `get_historical_data`: Retrieves historical stock data over the maximum available period using Yahoo Finance API.
- `get_company_news`: Fetches the latest news articles for a specific company using the News API.
- `get_stock_data`: Retrieves the current and previous closing prices for a given stock symbol using Yahoo Finance API.
- `get_portfolio_summary`: Computes a summary of the user's portfolio, including total value, day change, unrealised gain/loss, and detailed holdings information.
- `get_portfolio_performance_data`: Fetches historical performance data for multiple stock symbols over the past month using Yahoo Finance API.

## `views.py` Functions
- `latest_news`: Fetches the news data from the `get_latest_news` utility function and paginates the news articles for display.
- `login_view`: Handles user login authentication. Displays error messages from unauthenticated users trying to access locked functionalities.
- `logout_view`: Logs out the currently authenticated user.
- `register`: Registers new users with username, email, and password. Handles password confirmation and checks for existing usernames.
- `stock_search`: Redirects to stock_details_view with the queried stock symbol.
- `stock_details_view`: Retrieves detailed information about a specific stock symbol. Renders the stock details page with various data categories.
- `buy_stock`: Handles purchasing stocks by authenticated users. Creates a new transaction record in the database.
- `portfolio_view`: Displays the user’s portfolio summary. Retrieves holdings summary, portfolio performance data, and renders the portfolio view page.

## How to Run the Application
1. Install the required packages:
```
pip install -r requirements.txt
```

2. Apply migrations:
```
python3 manage.py makemigrations portfolio
python3 manage.py migrate
```

3. Run server:
```
python3 manage.py runserver
```

4. Access the application in your web browser at http://127.0.0.1:8000/.