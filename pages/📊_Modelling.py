import pandas as pd
import streamlit as st

from constants import DATA_DIR

from portable_power import simulate_battery_generator, simulation_plot, calc_savings_str

st.title("Modelling")
st.markdown(
    """
    We believe that adding a battery in tandem with the generator could create a hybrid solution which can save carbon and cost.
    The battery is able to charge from the generator and discharge to power the load.
    
    In order to design the solution we therefore need a model of this hybrid system. Below is a description of how a simple
    model may work:
    - If the generator or battery cannot the total load both are used - the generator run and battery tops up
    - If the generator can meet the load then it runs and charges battery with any extra power
    
    This model depends on the load, generator efficiency, generator size, battery capacity (kWh) and size (kW) and is often
    called "peak shaving" where the average load is delivered by the generator and the battery delivers peak loads.
    """
)
st.info(
    """
    Assumptions:
    - The Generator is able to adjust its generation to match the load
    - Battery round trip efficiency is 85%, so assume discharge and charging efficiency of 92%
    - Battery rental price: 100£/week per 10kW block, 33£/week for 5kWh block (any combination allowed)
    - The battery is able to automatically adjust its power to both power the site and absorb the excess power from the generator
    - Battery starts with 50% state of charge
    - Battery state of charge can run from 0-100%
    - Charging and discharging maximum power are equal to the battery power
    """
)

gen_curve = pd.read_csv(DATA_DIR / "gen_fuel_eff_curves.csv", index_col=0)
filled_load_df = pd.read_csv(DATA_DIR / "filled_load_df.csv", index_col=0)

col1, col2, col3 = st.columns(3)
with col1:
    generator_power_kw = st.number_input(
        "Generator Power (kW)", min_value=5, max_value=40, value=10, step=10
    )
with col2:
    battery_power_kw = st.number_input(
        "Battery Power (kW)", min_value=5, max_value=40, value=30, step=10
    )
with col3:
    battery_capacity_kwh = st.number_input(
        "Battery Capacity (kWh)", min_value=5, max_value=40, value=40, step=5
    )

results_df = simulate_battery_generator(
    load_ser=filled_load_df["Power"],
    battery_capacity_kwh=battery_capacity_kwh,
    battery_power_kw=battery_power_kw,
    generator_power_kw=generator_power_kw,
    normalised_gen_curve=gen_curve,
)

st.plotly_chart(simulation_plot(results_df))

st.info(
    calc_savings_str(
        generator_power_kw, battery_capacity_kwh, battery_power_kw, results_df
    )
)
