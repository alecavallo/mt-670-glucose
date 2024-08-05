"""
This module contains a function to load a CSV file into a pandas DataFrame.
"""

import pandas as pd

DATA_TYPES = {
    "Index": float,
    "Date": str,
    "Time": str,
    "BG Source": str,
    "BG Reading (mg/dL)": float,
    "Linked BG Meter ID": str,
    "Basal Rate (U/h)": float,
    "Temp Basal Amount": float,
    "Temp Basal Type": str,
    "Bolus Type": str,
    "Bolus Volume Selected (U)": float,
    "Bolus Volume Delivered (U)": float,
    "Prime Type": str,
    "Prime Volume Delivered (U)": float,
    "Alarm": str,
    "Suspend": str,
    "Rewind": str,
    "BWZ Estimate (U)": float,
    "BWZ Target High BG (mg/dL)": int,
    "BWZ Target Low BG (mg/dL)": int,
    "BWZ Carb Ratio (g/U)": float,
    "BWZ Insulin Sensitivity (mg/dL/U)": int,
    "BWZ Carb Input (grams)": int,
    "BWZ BG Input (mg/dL)": int,
    "BWZ Correction Estimate (U)": float,
    "BWZ Food Estimate (U)": float,
    "BWZ Active Insulin (U)": float,
    "BWZ Status": str,
    "Sensor Calibration BG (mg/dL)": int,
    "Sensor Glucose (mg/dL)": int,
    "ISIG Value": float,
    "Event Marker": str,
    "Bolus Number": int,
    "Bolus Cancellation Reason": str,
    "BWZ Unabsorbed Insulin Total (U)": float,
    "Final Bolus Estimate": float,
    "Scroll Step Size": str,
    "Insulin Action Curve Time": str,
    "Sensor Calibration Rejected Reason": str,
    "Preset Bolus": str,
    "Bolus Source": str,
    "BLE Network Device": str,
    "Device Update Event": str,
    "Network Device Associated Reason": str,
    "Network Device Disassociated Reason": str,
    "Network Device Disconnected Reason": str,
    "Sensor Exception": str,
    "Preset Temp Basal Name": str,
}


def load_csv(file_path, delimiter=",", skiprows=6):
    """
    Load a CSV file into a pandas DataFrame.
    Args:
        file_path (str): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file.
        skiprows (int): The number of rows to skip at the beginning of the file.
    Returns:
        pandas.DataFrame: The loaded CSV data as a DataFrame.
    """

    df = pd.read_csv(
        file_path,
        delimiter=delimiter,
        skiprows=skiprows,
        parse_dates=["New Device Time"],
        na_values=["-------"],
        on_bad_lines="skip",
        low_memory=False,
    )
    header_row = "Index	Date	Time	New Device Time	BG Source	BG Reading (mg/dL)	Linked BG Meter ID	Basal Rate (U/h)	Temp Basal Amount	Temp Basal Type	Temp Basal Duration (h:mm:ss)	Bolus Type	Bolus Volume Selected (U)	Bolus Volume Delivered (U)	Bolus Duration (h:mm:ss)	Prime Type	Prime Volume Delivered (U)	Alarm	Suspend	Rewind	BWZ Estimate (U)	BWZ Target High BG (mg/dL)	BWZ Target Low BG (mg/dL)	BWZ Carb Ratio (g/U)	BWZ Insulin Sensitivity (mg/dL/U)	BWZ Carb Input (grams)	BWZ BG Input (mg/dL)	BWZ Correction Estimate (U)	BWZ Food Estimate (U)	BWZ Active Insulin (U)	BWZ Status	Sensor Calibration BG (mg/dL)	Sensor Glucose (mg/dL)	ISIG Value	Event Marker	Bolus Number	Bolus Cancellation Reason	BWZ Unabsorbed Insulin Total (U)	Final Bolus Estimate	Scroll Step Size	Insulin Action Curve Time	Sensor Calibration Rejected Reason	Preset Bolus	Bolus Source	BLE Network Device	Device Update Event	Network Device Associated Reason	Network Device Disassociated Reason	Network Device Disconnected Reason	Sensor Exception	Preset Temp Basal Name"
    df = df[df.apply(lambda row: "\t".join(row.astype(str)) != header_row, axis=1)]

    # remove all rows that comtains "MiniMed" in the columns "Date" or "Time"
    df = df[~df["Date"].str.contains("MiniMed")]
    df = df[~df["Time"].str.contains("MiniMed")]

    df = df.fillna(
        {
            "Index": 0,
            "BWZ Target High BG (mg/dL)": 0,
            "BWZ Target Low BG (mg/dL)": 0,
            "BWZ Insulin Sensitivity (mg/dL/U)": 0,
            "BWZ Carb Input (grams)": 0,
            "BWZ BG Input (mg/dL)": 0,
            "BWZ Correction Estimate (U)": 0,
            "BWZ Food Estimate (U)": 0,
            "BWZ Active Insulin (U)": 0,
            "Sensor Calibration BG (mg/dL)": 0,
            "Sensor Glucose (mg/dL)": 0,
            "Bolus Number": 0,
        }
    )
    df["BWZ Carb Input (grams)"] = (
        df["BWZ Carb Input (grams)"].astype(float).astype(int)
    )
    df = df.astype(DATA_TYPES)
    return df
