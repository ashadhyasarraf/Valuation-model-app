def calculate_dcf(fcf_projections, discount_rate, terminal_growth_rate, final_year):
    # Calculate present value of each year's FCF
    present_values = [
        fcf / ((1 + discount_rate) ** year)
        for year, fcf in enumerate(fcf_projections, start=1)
    ]
    # Terminal Value using Gordon Growth Model
    terminal_value = (
        fcf_projections[-1] * (1 + terminal_growth_rate)
        / (discount_rate - terminal_growth_rate)
    )
    terminal_value_discounted = terminal_value / ((1 + discount_rate) ** final_year)

    dcf_value = sum(present_values) + terminal_value_discounted
    return dcf_value, present_values, terminal_value_discounted
