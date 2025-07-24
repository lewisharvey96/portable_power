import streamlit as st

st.title("Optimisation")
st.markdown(
    """
    Given our hybrid model and the available generator and battery sizing, can we optimise to:
    - minimize generator size
    - minimize battery size
    - minimize co2
    - balance cost and co2
    
    To do this, we will use the model and available price information to build "cost" functions for each case which can be
    minimised - in this case using the `scipy` library.
    """
)
st.info(
    """
    Assumptions:
    - Variables are continuous
    - Generator power can range from 5-35kW
    - Batter power can range from 5-40kW
    - Battery capacity can range from 5-50kWh
    """
)

with st.expander("Minimize Generator Size"):
    st.info(
        r"""
        Cost Function:
        $$
        \text{generator power} \,+ penalty(no. faults)
        $$
        """
    )
    st.success(
        """
        Results:
        
        **Optimal generator power**: 8.50 kW **Optimal battery capacity**: 40.00 kWh **Optimal battery power**: 34.00 kW\n
        
        Given we only have certain sizing available the closest match is:
        
        **Generator power**: 10 kW **Battery capacity**: 40 kWh **Battery power**: 30 kW
        
        Compared to our generator only counterfactual:
        
        **Additional cost** = £841 (~£170 per week) **CO2 savings** = 3214 kg
        """
    )

with st.expander("Minimize System Cost"):
    st.info(
        r"""
        Cost Function:
        $$
        \text{rental costs} \,+ \text{fuel costs} \, + penalty(no. faults)
        $$
        """
    )
    st.success(
        """
        Results:

        **Optimal generator power**: 31.0 kW **Optimal battery capacity**: 5.0 kWh **Optimal battery power**: 9.20 kW

        Given we only have certain sizing available the closest match is:

        **Generator power**: 30 kW **Battery capacity**: 5 kWh **Battery power**: 10 kW

        Compared to our generator only counterfactual:

        **Cost saving** = £60 **CO2 savings** = 1218 kg
        
        *This scenario barely uses the battery and effectively runs the generator for all demand.*
        """
    )

with st.expander("Minimize System Carbon"):
    st.info(
        r"""
        Cost Function:
        $$
        \text{fuel carbon} \, + penalty(no. faults)
        $$
        """
    )
    st.success(
        """
        Results:

        **Optimal generator power**: 8.60 kW **Optimal battery capacity**: 39.70 kWh **Optimal battery power**: 35.00 kW

        Given we only have certain sizing available the closest match is:

        **Generator power**: 10 kW **Battery capacity**: 35 kWh **Battery power**: 30 kW

        Compared to our generator only counterfactual:

        **Additional cost** = £680 (~£140 per week) **CO2 savings** = 3217 kg
    
        """
    )

with st.expander("Balance System Carbon and Price"):
    st.info(
        r"""
        Cost Function:
        $$
        \frac{\text{rental + fuel costs}}{\text{generator only costs}} + \frac{\text{fuel carbons}}{\text{generator only carbon}} + penalty(no. faults)
        $$
        """
    )
    st.success(
        """
        Results:

        **Optimal generator power**: 8.60 kW **Optimal battery capacity**: 39.70 kWh **Optimal battery power**: 35.00 kW

        Given we only have certain sizing available the closest match is:

        **Generator power**: 10 kW **Battery capacity**: 35 kWh **Battery power**: 30 kW

        Compared to our generator only counterfactual:

        **Additional cost** = £680 (~£140 per week) **CO2 savings** = 3217 kg

        *This matches our carbon optimisation scenario*
        """
    )

st.header("Conclusions")
st.markdown(
    """
    Given the model and available components, a large battery rated around 35 kW to cover peak demand and a smaller
    generator around 10 kW seems like the a good option to minimize additional costs and maximise CO2 savings.
    
    The generator only scenario is cheaper, however, the additional cost reduces the CO2 footprint by ~40% for a small additional
    cost of around 15%.
    """
)

st.header("Further Work")
st.markdown(
    """
    The presented analysis aimed to show conceptually who you can approach this sort of problem, however, given the time
    I would recommend additional analysis, namely:
    - developing a more granular system control strategy for the model(i.e. including state of charge limits, noise limits etc)
    - more comprehensive optimisation including business constraints i.e available equipment combinations
    - sensitivity analysis to understand the optimisation space
    """
)
