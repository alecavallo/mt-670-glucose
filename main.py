from scripts.glucose import get_sensor_glucose_data
from scripts.load_csv import load_csv


if __name__ == "__main__":
    FILE_PATH = "./data/raw/24-08-04.csv"
    data_frame = load_csv(FILE_PATH)

    glucose = get_sensor_glucose_data(data_frame)
    print(glucose)
