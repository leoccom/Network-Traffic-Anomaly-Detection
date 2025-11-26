import argparse
import os
from posixpath import basename
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest


# df = pd.read_csv("data/network_traffic.csv")    # It reads CSV file and loads it into a table structure called a DataFrame.
# df["timestamp"] = pd.to_datetime(df["timestamp"])    # Converts the text into actual Time Objects.


# df["moving_avg"] = df["value"].rolling(window=50).mean()    # Calculate and store 50-point moving average.


# plt.figure(figsize=(12, 6))    # Sets up the empty space where the graph will be drawn.
# plt.plot(df["timestamp"], df["value"])    # This actually draws the data.
# plt.plot(df["timestamp"], df["moving_avg"])    # Draws the moving average.
# plt.title("Raw Network Traffic")    # Adds a title to the plot.
# # plt.show()    # Renders the final image on your screen.


# data_for_model = df["value"]


# # contamination of 0.01 = 1% of the traffic is anomalous
# model = IsolationForest(contamination=0.01, random_state=42)
# model.fit(df[["value"]])

# df["anomaly"] = model.predict(df[["value"]])    # -1: Anomaly, 1: Normal

# anomalies = df[df["anomaly"] == -1]

# plt.scatter(anomalies["timestamp"], anomalies["value"], color="red")
# plt.show()


# High value (network traffic) may indicate potential DDoS attack or network congestion.


def analyze_traffic(file_name, output_image, contamination=0.01):
    # 1. Load the data using the argument passed by the user.
    try:
        print(f"Loading data from data/{file_name}.csv...")
        df = pd.read_csv(f"data/{file_name}.csv")    # It reads CSV file and loads it into a table structure called a DataFrame.

        df["timestamp"] = pd.to_datetime(df["timestamp"])    ## Converts the text into actual Time Objects.

    except FileNotFoundError:    # File is not found.
        print("Error: File not found. Please check the path.")
        return
    

    # 2. Train model
    ## contamination of 0.01 = 1% of the traffic is anomalous
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(df[["value"]])
    
    df["anomaly"] = model.predict(df[["value"]])    # -1: Anomaly, 1: Normal
    
    # 3. Extract anomalies
    anomalies = df[df["anomaly"] == -1]
    print(f"{len(anomalies)} anomalies found.")


    # 4. Save the graph
    plt.figure(figsize=(15, 6))
    plt.plot(df["timestamp"], df["value"], color="blue", label="Normal Traffic", alpha=0.6)
    plt.scatter(anomalies["timestamp"], anomalies["value"], color="red", label="Anomaly")
    plt.plot([], [], ' ', label=f'Contamination: {contamination}')
    plt.title(f"Anomaly Detection Result - {file_name}.csv")
    plt.legend()


    # 5. Save to the output path
    plt.savefig(f"output/{output_image}_{contamination}.png")
    print(f"Graph saved to output/{output_image}_{contamination}.png.")


    # 6. Save the anomaly list into a CSV format.
    anomalies.to_csv(f"output/{file_name}_anomaly_{contamination}", index=False)
    print(f"Anomaly list saved to output/{file_name}_anomaly_{contamination}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect anomalies in a network traffic file.")

    # Add arguments
    parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file")
    parser.add_argument("--output", type=str, default=None, help="Name of the output graph image")
    parser.add_argument("--c", type=float, default=0.01, help="Contamination rate (Default is 0.01)")

    args = parser.parse_args()

    base_name = os.path.basename(args.input)    # "traffic.csv" from "data/traffic.csv"
    filename, extension = os.path.splitext(base_name)

    final_output_name = args.output
    if final_output_name is None:
        final_output_name = f"{filename}_graph.png"

    # Run the function
    analyze_traffic(filename, final_output_name, args.c)