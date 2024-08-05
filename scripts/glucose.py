"""
This module is on charge of getting data about blood glucose
"""

import pandas as pd


def get_sensor_glucose_data(df):
    """
    Get the data about blood glucose
    Args:
        df (pandas.DataFrame): The data frame containing the blood glucose data.
    """
    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    subdata = df[["Date", "Time", "Sensor Glucose (mg/dL)", "ISIG Value"]]
    # removing rows with missing values in the columns "Sensor Glucose (mg/dL)" and "ISIG Value"
    subdata = subdata.dropna(subset=["Sensor Glucose (mg/dL)", "ISIG Value"])

    return subdata
