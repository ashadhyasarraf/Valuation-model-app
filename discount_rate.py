# discount_rate.py

def calculate_cost_of_equity(rf_rate, beta, market_return):
    return rf_rate + beta * (market_return - rf_rate)

def calculate_wacc(equity, debt, cost_of_equity, cost_of_debt, tax_rate):
    total_capital = equity + debt
    equity_weight = equity / total_capital
    debt_weight = debt / total_capital
    after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate)
    return (equity_weight * cost_of_equity) + (debt_weight * after_tax_cost_of_debt)