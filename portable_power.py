import pandas as pd
from plotly.subplots import make_subplots
from scipy.interpolate import interpolate
import plotly.graph_objects as go
from constants import (
    PERIOD_WEEKS,
    PRICE_PER_LITRE,
    CO2_LITRE,
    TOTAL_GEN_COST,
    TOTAL_GEN_CO2,
)


def simulate_battery_generator(
    load_ser: pd.Series,
    battery_capacity_kwh: float,
    battery_power_kw: float,
    generator_power_kw: float,
    normalised_gen_curve: pd.DataFrame,
    battery_efficiency: float = 0.92,
    initial_soc: float = 0.5,
) -> pd.DataFrame:
    time_step_hours = pd.to_datetime(load_ser.index).diff().mean() / pd.Timedelta("1hr")
    soc_kwh = initial_soc * battery_capacity_kwh
    max_charge_kwh = max_discharge_kwh = (
        battery_power_kw * time_step_hours
    ) * battery_efficiency

    # efficiency curve scales to gen power
    fuel_func = interpolate.interp1d(
        generator_power_kw * normalised_gen_curve.index,
        normalised_gen_curve["kWh_litre"],
    )

    soc_history = []
    fault_history = []
    battery_power_history = []
    gen_power_history = []
    fuel_efficiency_history = []
    fuel_usage_history = []

    for load_kw in load_ser:
        net_power_kw = generator_power_kw - load_kw  # peak shaving

        # generator can meet demand at 100% load
        if net_power_kw == 0:
            generator_power_kw_actual = generator_power_kw
            fuel_eff = fuel_func(generator_power_kw_actual)  # kWh/litre
            generator_usage_kwh = generator_power_kw_actual * time_step_hours
            fuel_usage = (generator_usage_kwh) / fuel_eff
            fault = 0
            battery_power_kw_actual = 0

        # run generator as high as possible and charge battery if possible
        elif net_power_kw > 0:
            # charge amount limited by power, net power and batter cap left
            charge_energy_kwh = min(
                max_charge_kwh,
                (net_power_kw * time_step_hours) * battery_efficiency,
                (battery_capacity_kwh - soc_kwh),
            )

            # Generator runs at full load and battery takes extra
            if (
                charge_energy_kwh
                == (net_power_kw * time_step_hours) * battery_efficiency
            ):
                generator_power_kw_actual = generator_power_kw
                fuel_eff = fuel_func(generator_power_kw_actual)  # kWh/litre
                generator_usage_kwh = generator_power_kw_actual * time_step_hours
                fuel_usage = (generator_usage_kwh) / fuel_eff

            # Generator runs as high as possible and battery charges as much as it can
            else:
                gen_load_kwh = (generator_power_kw * time_step_hours) - (
                    (net_power_kw * time_step_hours) - charge_energy_kwh
                )
                generator_power_kw_actual = gen_load_kwh / time_step_hours
                fuel_eff = fuel_func(generator_power_kw_actual)  # kWh/litre
                fuel_usage = (gen_load_kwh) / fuel_eff

            # Battery charges
            soc_kwh += charge_energy_kwh
            battery_power_kw_actual = (
                -charge_energy_kwh / time_step_hours
            )  # negative = charging

            fault = 0

        elif net_power_kw < 0:
            # Generator runs at 100%
            generator_power_kw_actual = generator_power_kw
            fuel_eff = fuel_func(generator_power_kw_actual)  # kWh/litre
            generator_usage_kwh = generator_power_kw_actual * time_step_hours
            fuel_usage = (generator_usage_kwh) / fuel_eff

            # discharge amount limited by power, net power and soc
            discharge_energy_kwh = min(
                max_discharge_kwh,
                (abs(net_power_kw) * time_step_hours) / battery_efficiency,
                soc_kwh,
            )

            if (
                discharge_energy_kwh == max_discharge_kwh
            ):  # battery cant supply load - clips at max discharge rate
                battery_power_kw_actual = max_discharge_kwh / time_step_hours
                fault = 1
            # battery empty
            elif discharge_energy_kwh == 0:
                battery_power_kw_actual = 0
                fault = 1
            # battery discharges required energy
            else:
                battery_power_kw_actual = (
                    discharge_energy_kwh / time_step_hours
                )  # positive = discharging
                fault = 0

            soc_kwh -= discharge_energy_kwh

        else:
            # no load
            battery_power_kw_actual = 0
            fault = 0
            fuel_eff = 0
            fuel_usage = 0
            generator_power_kw_actual = 0

        soc_history.append(soc_kwh)
        battery_power_history.append(battery_power_kw_actual)
        fault_history.append(fault)
        gen_power_history.append(generator_power_kw_actual)
        fuel_efficiency_history.append(float(fuel_eff))
        fuel_usage_history.append(float(fuel_usage))

    return pd.DataFrame(
        {
            "Load_kW": load_ser,
            "SOC_kWh": soc_history,
            "Battery_Power_kW": battery_power_history,
            "fault_history": fault_history,
            "fuel_eff": fuel_efficiency_history,
            "fuel_usage_history": fuel_usage_history,
            "generator_power_kW_actual": gen_power_history,
        },
        index=load_ser.index,
    )


def simulation_plot(results_df: pd.DataFrame) -> go.Figure:
    selected_columns = [
        "Load_kW",
        "SOC_kWh",
        "Battery_Power_kW",
        "fault_history",
        # "fuel_eff",
        "generator_power_kW_actual",
    ]

    fig = make_subplots(
        rows=len(selected_columns),
        cols=1,
        shared_xaxes=True,
        subplot_titles=selected_columns,
        vertical_spacing=0.05,
    )

    for i, col in enumerate(selected_columns, start=1):
        fig.add_trace(
            go.Scatter(x=results_df.index, y=results_df[col], name=col, mode="lines"),
            row=i,
            col=1,
        )

    fig.update_layout(height=100 * len(selected_columns), showlegend=False)
    return fig


def system_rental_price(
    generator_power_kw: float, battery_capacity_kwh: float, battery_power_kw: float
) -> float:
    rental_gen_cost = generator_power_kw * PERIOD_WEEKS * (20 / 10)  # £20/10kW per week
    battery_cap_rental_cost = (
        battery_capacity_kwh * PERIOD_WEEKS * (33 / 5)
    )  # £33/5kWh per week
    battery_power_rental_cost = (
        battery_power_kw * PERIOD_WEEKS * (100 / 10)
    )  # £100/10kW per week
    return sum([rental_gen_cost, battery_cap_rental_cost, battery_power_rental_cost])


def fuel_cost_and_co2_faults(results_df: pd.DataFrame) -> dict:
    return {
        "fuel_cost_£": results_df["fuel_usage_history"].sum() * PRICE_PER_LITRE,
        "co2_kg": results_df["fuel_usage_history"].sum() * CO2_LITRE,
        "no_faults": results_df["fault_history"].sum(),
    }


def calc_savings_str(
    generator_power_kw: float,
    battery_capacity_kwh: float,
    battery_power_kw: float,
    results_df: pd.DataFrame,
) -> str:
    rental_price = system_rental_price(
        generator_power_kw, battery_capacity_kwh, battery_power_kw
    )
    fuel_cost_and_co2_faults_dict = fuel_cost_and_co2_faults(results_df)
    total_price = fuel_cost_and_co2_faults_dict["fuel_cost_£"] + rental_price

    return (
        f"Compared to our generator only counterfactual:\n"
        f"\nThe total cost = £{total_price:.0f} which represents an additional cost of £{abs(TOTAL_GEN_COST - total_price):.0f}\n"
        f"\nThe total co2 = {fuel_cost_and_co2_faults_dict['co2_kg']:.0f} which represents a saving of {TOTAL_GEN_CO2 - fuel_cost_and_co2_faults_dict['co2_kg']:.0f}kg\n"
        f"\nTotal no. of faults (i.e. load cannot be met) = {fuel_cost_and_co2_faults_dict['no_faults']:.0f}"
    )
