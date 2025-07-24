import pandas as pd
import streamlit as st
import plotly.express as px

from constants import DATA_DIR

st.title("Generator Sizing")

st.header("Load Profile")
st.markdown(
    """
    The client gave us a minutely load profile from a single meter over ~ 5 weeks. This data was cleaned and is presented
    below. We can see the demand varies and has a peak demand of around 34kW.
    """
)
st.info(
    """
    Assumptions:
    - The minutely meter readings were averaged to give us an estimate of the load profile
    - Gaps in the data were forward filled
    """
)

filled_load_df = pd.read_csv(DATA_DIR / "filled_load_df.csv", index_col=0)

st.plotly_chart(px.line(filled_load_df))

st.header("Sizing a Generator")
st.markdown(
    """
    The site has no access to grid power and therefore to meet the peak demand of 34kW a generator must be sized to meet
    this.
    """
)
st.info(
    """
    Assumptions:
    - Generator has load factor of 1 (how much of nameplate capacity can be drawn as real power)
    - Generators can be rented only in 10kW blocks
    """
)
st.markdown(
    """
    #### Question 1.1
    What is the size of generator you would recommend?
    """
)
st.success(
    """
    #### Answer
    A 40kW generator. This slight oversizing also builds in some redundancy if the load profile was to drift.
    """
)
st.markdown(
    """
    #### Question 1.2
    Calculate the total cost of powering the site with the diesel generator over the period covered in the load profile data.
    """
)
st.info(
    """
    Assumptions:
    - Generator has load factor of 1 (how much of nameplate capacity can be drawn as real power)
    - Cost of fuel is £1.43/litre
    - Rental cost of generator is £20/10kW block per week
    - Generator's fuel efficiency depends on the load  (see efficiency curve below)
    """
)
gen_curve = pd.read_csv(DATA_DIR / "gen_fuel_eff_curves.csv", index_col=0)
st.plotly_chart(px.line(gen_curve))
st.success(
    """
    #### Answer
    In order to calculate the total cost of power the site we need to calculate the **rental cost** and the **fuel cost**.
    
    **Fuel cost** can be calculated as follows:
    - Use the load series and generator efficiency curve to calculate the fuel efficiency series i.e. kWh/litre
    - Calculate the energy required in each timestep using the load series (kW -> kWh)
    - Divide the energy required by the fuel efficiency to get the amount of fuel used
    - Use the cost of fuel (£/litre) to calculate the total
    
    **Rental cost** can be calculated as follows:
    - no. generator 10kW blocks * no. weeks * rental price/10kW per week
    
    The total cost is calculated as follows as the **rental cost** + **fuel cost** = **£4601**
    """
)
st.markdown(
    """
    #### Question 1.3
    Calculate the Co2 emissions.
    """
)
st.info(
    """
    Assumptions:
    - CO2 per litre of fuel = 2.86kg/litre
    """
)
st.success(
    """
    #### Answer
    If we take the previously calculated fuel usage we can compute the CO2 emissions as:
    - fuel used * CO2 per litre of fuel = **8426 kg of CO2**
    """
)
