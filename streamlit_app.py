import streamlit as st
import pandas as pd
import altair as alt
import time

# Custom CSS to style KPI boxes, center text, and adjust sidebar
st.markdown("""
    <style>
        .css-1d391kg {
            display: flex;
            flex-direction: row-reverse;
        }
        .kpi-box {
            border: 1px solid #ddd;
            padding: 20px;
            margin: 10px 0;
            border-radius: 5px;
            background-color: white; /* White background for KPI boxes */
            text-align: center;
            min-height: 100px; /* Ensure all KPI boxes have the same height */
        }
        .kpi-box h2 {
            margin: 0;
            font-size: 24px;
        }
        .kpi-box p {
            margin: 0;
            color: #555;
        }
        .kpi-box .percentage {
            color: #28a745; /* Green color for positive change */
            font-size: 0.7em; /* Smaller font size for percentage */
        }
        .section-header {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        }
        .kpi-box.green-value h2 span.value {
            color: #28a745; /* Green color for the value only */
        }
    </style>
""", unsafe_allow_html=True)

# Set title and description
st.title("Mental Health Solution ROI Calculator")
st.write("Estimate the financial impact of our mental health solution by identifying and addressing high-risk employees in your organization.")

# Sidebar for input fields
with st.sidebar:
    num_employees = st.number_input('Number of Employees', min_value=1, value=1000)
    industry = st.selectbox('Industry', ['Tech', 'Healthcare', 'Finance', 'Manufacturing', 'Retail'])

# Industry-specific data (sample values)
industry_data = {
    'Tech': {'triage_pct': 20, 'high_risk_pct': 3.0, 'average_salary': 30000, 'solution_effectiveness': 0.30},
    'Healthcare': {'triage_pct': 30, 'high_risk_pct': 5.0, 'average_salary': 25000, 'solution_effectiveness': 0.25},
    'Finance': {'triage_pct': 15, 'high_risk_pct': 1.0, 'average_salary': 35000, 'solution_effectiveness': 0.28},
    'Manufacturing': {'triage_pct': 25, 'high_risk_pct': 6.0, 'average_salary': 20000, 'solution_effectiveness': 0.20},
    'Retail': {'triage_pct': 45, 'high_risk_pct': 7.0, 'average_salary': 19000, 'solution_effectiveness': 0.35}
}

days_off_per_high_risk = 19.6  # Days off per high-risk employee per year

if st.button('Predict'):
    with st.spinner('Calculating results...'):
        time.sleep(2)  # Simulate a delay for calculation

    industry_values = industry_data.get(industry, {})
    triage_pct = industry_values.get('triage_pct', 50)
    high_risk_pct = industry_values.get('high_risk_pct', 15.0) / 100
    average_salary = industry_values.get('average_salary', 70000)
    solution_effectiveness = industry_values.get('solution_effectiveness', 0.30)

    triaged_employees = num_employees * (triage_pct / 100)
    predicted_high_risk_employees = int(round(triaged_employees * high_risk_pct, 0))
    total_days_off = predicted_high_risk_employees * days_off_per_high_risk

    daily_salary = average_salary / 250  # Assuming 250 working days in a year
    total_cost_current = total_days_off * daily_salary

    reduction_in_high_risk = predicted_high_risk_employees * solution_effectiveness
    reduced_high_risk_employees = int(round(predicted_high_risk_employees - reduction_in_high_risk, 0))
    reduced_days_off = reduced_high_risk_employees * days_off_per_high_risk
    total_cost_with_solution = reduced_days_off * daily_salary
    savings = total_cost_current - total_cost_with_solution

    # Data for vertical bar chart
    data = pd.DataFrame({
        'Metric': ['Predicted Cost', 'Predicted Cost with solution', 'Estimated Savings'],
        'Amount': [total_cost_current, total_cost_with_solution, savings]
    })

    # Vertical bar chart with value labels above the bars and title
    bars = alt.Chart(data).mark_bar().encode(
        x=alt.X('Metric:N', title='', sort=['Predicted Cost', 'Predicted Cost with solution', 'Estimated Savings'], axis=alt.Axis(labelAngle=0, labelFontSize=12)),
        y=alt.Y('Amount:Q', title='Cost (€)', axis=alt.Axis(labelFontSize=12)),
        color=alt.Color('Metric:N', scale=alt.Scale(domain=['Predicted Cost', 'Predicted Cost with solution', 'Estimated Savings'], range=['#ff7f0e','#1f77b4', '#2ca02c']), legend=None)
    ).properties(
        height=400,  # Increased height for better label visibility
        width=700,
        title='Predicted Costs',
        padding={"bottom": 50}  # Increased bottom padding
    )

    # Adding text labels above the bars
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-10  # Position the text above the bars
    ).encode(
        text=alt.Text('Amount:Q', format=',.2f€')
    )

    # Combine the bar and text layers
    chart = alt.layer(bars, text).configure_axis(
        labelPadding=20  # Increased padding to avoid cutting off labels
    )

    st.altair_chart(chart, use_container_width=True)

    # Display detailed results in two KPI-style boxes
    col_current, col_solution = st.columns(2)

    with col_current:
        st.markdown("<div class='section-header'>Without solution</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-box'><h2>{predicted_high_risk_employees}</h2><p>High Risk Employees</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-box'><h2>{total_days_off:.2f}</h2><p>Total Days Off</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-box'><h2>€{total_cost_current:.2f}</h2><p>Total Cost of Days Off</p></div>", unsafe_allow_html=True)

    with col_solution:
        st.markdown("<div class='section-header'>With solution</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-box'><h2>{reduced_high_risk_employees} <span class='percentage'>↓{percentage_reduction_high_risk:.2f}%</span></h2><p>High Risk Employees</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-box'><h2>{reduced_days_off:.2f} <span class='percentage'>↓{percentage_reduction_days_off:.2f}%</span></h2><p>Total Days Off</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-box'><h2>€{total_cost_with_solution:.2f} <span class='percentage'>↓{percentage_reduction_cost:.2f}%</span></h2><p>Total Cost of Days Off</p></div>", unsafe_allow_html=True)

    # KPI-style box for estimated savings with green value only
    st.markdown(f"<div class='kpi-box'><h2>Estimated Yearly Savings</h2><h2><span class='value' style='color:#28a745'>€{savings:.2f}</span></h2></div>", unsafe_allow_html=True)









