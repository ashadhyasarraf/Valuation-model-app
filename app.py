import streamlit as st
import pandas as pd
# 📥 Import custom valuation modules
from dcf_model import calculate_dcf
from discount_rate import calculate_wacc, calculate_cost_of_equity
from valuation_summary import generate_pdf_summary

st.title("\U0001F4C8 Valuation Model App")

st.header("Upload Excel File with Financials")
uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

import streamlit as st

# Add this where you want the download button to appear
with open("valuation_template.xlsx", "rb") as template_file:
    st.download_button(
        label="📥 Download Excel Template",
        data=template_file,
        file_name="valuation_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Initialize placeholders for final outputs
dcf_value = 0
pe_equity = 0
ev_ebitda = 0

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")
    st.subheader("Preview of Uploaded Data:")
    st.write(df)

    # 📌 Extract Variables
    def get_value(metric_name):
        return df.loc[df['Metric'] == metric_name, 'Value'].values[0]

    revenue = get_value('Revenue')
    ebitda = get_value('EBITDA')
    net_income = get_value('Net Income')
    total_debt = get_value('Total Debt')
    cash = get_value('Cash')
    share_price = get_value('Share Price')
    shares_outstanding = get_value('Shares Outstanding')

    st.markdown("### \U0001F4CC Extracted Financial Data")
    st.write(f"EBITDA: ₹{ebitda}")
    st.write(f"Net Income: ₹{net_income}")
    st.write(f"Total Debt: ₹{total_debt}")
    st.write(f"Cash: ₹{cash}")
    st.write(f"Share Price: ₹{share_price}")
    st.write(f"Shares Outstanding: {shares_outstanding}")

    st.markdown("## \U0001FA8E Discount Rate - WACC Calculation")

    with st.expander("Enter Assumptions for WACC"):
        st.markdown("### \U0001F4C8 Cost of Equity (via CAPM)")

        rf_rate = st.number_input("Risk-Free Rate (%)", min_value=0.0, value=6.0, step=0.1) / 100
        beta = st.number_input("Beta", min_value=0.0, value=1.2, step=0.1)
        market_return = st.number_input("Market Return (%)", min_value=0.0, value=12.0, step=0.1) / 100

        cost_of_equity = calculate_cost_of_equity(rf_rate, beta, market_return)

        st.markdown(f"✅ **Cost of Equity (Re)** = `{cost_of_equity:.2%}`")

        st.markdown("---")
        st.markdown("### \U0001F3E6 Cost of Debt & WACC")

        cost_of_debt = st.number_input("Cost of Debt (%)", min_value=0.0, value=8.0, step=0.1) / 100
        tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, value=25.0, step=0.1) / 100

        equity = share_price * shares_outstanding
        debt = total_debt

        wacc = calculate_wacc(equity, debt, cost_of_equity, cost_of_debt, tax_rate)

        st.success(f"\U0001F3AF **Weighted Average Cost of Capital (WACC): {wacc:.2%}**")

    # \U0001F522 Multiples Valuation
    st.header("\U0001F50D Multiples Valuation")

    market_cap = share_price * shares_outstanding
    enterprise_value = market_cap + total_debt - cash

    ev_ebitda = enterprise_value / ebitda if ebitda != 0 else None
    pe_ratio = market_cap / net_income if net_income != 0 else None

    st.write(f"✅ Market Cap: ₹{market_cap:,.0f}")
    st.write(f"✅ Enterprise Value (EV): ₹{enterprise_value:,.0f}")
    st.write(f"📊 EV/EBITDA: {ev_ebitda:.2f}" if ev_ebitda else "EV/EBITDA: N/A")
    st.write(f"📊 P/E Ratio: {pe_ratio:.2f}" if pe_ratio else "P/E Ratio: N/A")

    st.markdown("## \U0001F4B0 DCF Valuation")

    # Ask for FCF projections
    fcf_years = st.slider("Number of forecast years", 3, 10, 5)
    fcf_list = []
    for i in range(fcf_years):
        fcf = st.number_input(f"Enter Free Cash Flow for Year {i+1} (₹):", min_value=0)
        fcf_list.append(fcf)

    terminal_growth = st.number_input("Terminal Growth Rate (%)", value=2.0) / 100
    discount_rate = st.number_input("Discount Rate (WACC %) again if needed", value=10.0) / 100

    if st.button("Calculate DCF Value"):
        dcf_value, pv_list, terminal_val = calculate_dcf(
            fcf_list, discount_rate, terminal_growth, final_year=fcf_years
        )

        st.success(f"✅ DCF Valuation = ₹{dcf_value:,.2f}")
        st.markdown(f"📌 Present Value of Terminal Value = ₹{terminal_val:,.2f}")
        st.bar_chart(pv_list + [terminal_val])

        st.markdown("---")

    st.subheader("📈 Valuation Multiples")

    pe_ratio = st.number_input("P/E Ratio", min_value=0.0, value=15.0, step=0.5)
    pe_equity = net_income * pe_ratio

    st.success(f"P/E-based Equity Valuation: ₹ {pe_equity:,.2f}")

    st.header("📊 Valuation Summary")

    valuation_data = {
        "Method": ["DCF Valuation", "P/E Multiple", "EV/EBITDA Multiple"],
        "Value (₹)": [dcf_value, pe_equity, ev_ebitda]
    }

    valuation_df = pd.DataFrame(valuation_data)
    valuation_df["Value (₹)"] = valuation_df["Value (₹)"].apply(lambda x: f"₹ {x:,.2f}")

    st.table(valuation_df)

    st.bar_chart(data=pd.DataFrame({
        "Valuation": [dcf_value, pe_equity, ev_ebitda]
    }, index=["DCF", "P/E", "EV/EBITDA"]))

    st.markdown("## 📊 Valuation Summary")

    if st.button("Generate Summary"):
        summary_data = {
            "EBITDA": ebitda,
            "Net Income": net_income,
            "Total Debt": total_debt,
            "Cash": cash,
            "Equity Value (P/E)": pe_equity,
            "Enterprise Value (EV/EBITDA)": ev_ebitda,
            "Discount Rate (WACC)": discount_rate * 100,
            "DCF Valuation": dcf_value
        }

        for k, v in summary_data.items():
            st.write(f"**{k}:** ₹{v:,.2f}")

        pdf_download_link = generate_pdf_summary(summary_data)
        st.markdown(pdf_download_link, unsafe_allow_html=True)


    




    


