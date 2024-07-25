from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe

from .models import User, Stock, Portfolio, Transaction
from .services import *

import json


def latest_news(request):
    news = get_latest_news()
    paginator = Paginator(news, 30)
    page = request.GET.get("page")

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    
    return render(request, "portfolio/latest_news.html", {
        "news": news
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "portfolio/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        next_url = request.GET.get("next", "")

        if next_url == "/portfolio":
            return render(request, "portfolio/login.html", {
                "message": "Please log in to view your portfolio."
            })
        elif next_url == "/buy_stock":
            return render(request, "portfolio/login.html", {
                "message": "Please log in to purchase stocks."
            })
        return render(request, "portfolio/login.html")
    

def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "portfolio/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "portfolio/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "portfolio/register.html")


def stock_search(request):
    query = request.GET.get("q", "").upper()
    if query:
        return redirect("stock_details", symbol=query)
    return render(request, "portfolio/stock_details.html", {
        "message": "Stock not found or data not available."
    })


def stock_details_view(request, symbol):
    company_info = get_company_info(symbol)
    intraday_data = get_intraday_data(symbol)
    historical_data = get_historical_data(symbol)

    if company_info and intraday_data and historical_data:
        stock, created = Stock.objects.get_or_create(
            symbol=symbol,
            defaults={
                "name": company_info["name"]
            })
        
        if not created:
            stock.name = company_info["name"]

        company_news = get_company_news(symbol)
        paginator = Paginator(company_news, 20)
        page = request.GET.get("page")

        try:
            company_news = paginator.page(page)
        except PageNotAnInteger:
            company_news = paginator.page(1)
        except EmptyPage:
            company_news = paginator.page(paginator.num_pages)

        return render(request, "portfolio/stock_details.html", {
            "stock": stock,

            # Company Information
            "company_name": company_info["name"],
            "is_active": company_info["is_active"],
            "company_bio": company_info["bio"],
            "company_logo": company_info["logo"],
            "sector": company_info["sector"],
            "industry": company_info["industry"],
            "employee_count": company_info["employee_count"],
            "fy_end": company_info["fy_end"],
            "website": company_info["website"],
            "company_officers": company_info["company_officers"],

            # OHLCV + Core Data
            "current_price": company_info["current_price"],
            "previous_close": company_info["previous_close"],
            "price_delta": company_info["price_delta"],
            "delta_percentage": company_info["delta_percentage"],
            "latest_open": company_info["open"],
            "latest_high": company_info["high"],
            "latest_low": company_info["low"],
            "latest_volume": company_info["volume"],
            "avg_volume": company_info["avg_volume"],
            "shares_outstanding": company_info["shares_outstanding"],
            "market_cap": company_info["market_cap"],
            "pe_ratio": company_info["pe_ratio"],
            "eps": company_info["eps"],
            "beta": company_info["beta"],
            "target_mean_price": company_info["target_mean_price"],
            "fifty_two_week_high": company_info["fifty_two_week_high"],
            "fifty_two_week_low": company_info["fifty_two_week_low"],

            # Financial Metrics
            "total_cash": company_info["total_cash"],
            "total_revenue": company_info["total_revenue"],
            "total_debt": company_info["total_debt"],
            "ebitda": company_info["ebitda"],
            "free_cf": company_info["free_cf"],
            "operating_cf": company_info["operating_cf"],
            "earnings_growth": company_info["earnings_growth"],
            "revenue_growth": company_info["revenue_growth"],
            "debt_to_equity": company_info["debt_to_equity"],
            "quick_ratio": company_info["quick_ratio"],
            "current_ratio": company_info["current_ratio"],
            "revenue_per_share": company_info["revenue_per_share"],
            "return_on_assets": company_info["return_on_assets"],
            "return_on_equity": company_info["return_on_equity"],
            "operating_margins": company_info["operating_margins"],
            "gross_margins": company_info["gross_margins"],

            # Share Information
            "float_shares": company_info["float_shares"],
            "shares_short": company_info["shares_short"],
            "short_ratio": company_info["short_ratio"],
            "held_percent_insiders": company_info["held_percent_insiders"],
            "held_percent_institutions": company_info["held_percent_institutions"],

            # Corporate Governance
            "audit_date": company_info["audit_date"],
            "audit_risk": company_info["audit_risk"],
            "board_risk": company_info["board_risk"],
            "compensation_risk": company_info["compensation_risk"],
            "shareholder_rights_risk": company_info["shareholder_rights_risk"],
            "overall_risk": company_info["overall_risk"],

            # Other Useful Data
            "dividend_rate": company_info["dividend_rate"],
            "dividend_yield": company_info["dividend_yield"],
            "ex_dividend_date": company_info["ex_dividend_date"],

            # Table Data
            "intraday_data": mark_safe(json.dumps(intraday_data)),
            "historical_data": mark_safe(json.dumps(historical_data)),

            # Company News
            "company_news": company_news
        })
    else:
        return render(request, "portfolio/stock_details.html", {
            "message": "Stock not found or data not available."
        })


@login_required
def buy_stock(request):
    if request.method == "POST":
        stock_id = request.POST.get("stock_id")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        date = request.POST.get("date")

        stock = Stock.objects.get(id=stock_id)
        user_portfolio, created = Portfolio.objects.get_or_create(user=request.user)

        transaction = Transaction.objects.create(
            portfolio=user_portfolio,
            stock=stock,
            quantity=quantity,
            purchase_price=price,
            purchase_date=date
        )
        return redirect("stock_details", symbol=stock.symbol)


@login_required
def portfolio_view(request):
    try:
        user_portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        user_portfolio = Portfolio.objects.create(user=request.user)
    
    summary = get_portfolio_summary(user_portfolio)
    symbols = [holding["symbol"] for holding in summary["holdings_summary"].values()]
    portfolio_performance_data = get_portfolio_performance_data(symbols)

    return render(request, "portfolio/portfolio_view.html", {
        "portfolio_value": summary["portfolio_value"],
        "day_change": summary["day_change"],
        "percent_change": summary["percent_change"],
        "unrealised_gain_loss": summary["unrealised_gain_loss"],
        "holdings": summary["holdings_summary"].values(),
        "portfolio_performance_data": mark_safe(json.dumps(portfolio_performance_data))
    })