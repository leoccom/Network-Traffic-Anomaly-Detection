import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest


# High "value" (network traffic) may indicate potential DDoS attack or network congestion.


def analyze_traffic(file_path, output_name, contamination=0.01):
    # Check if the output directory exists.
    os.makedirs("output", exist_ok=True)

    # 1. Load the data using the argument passed by the user.
    try:
        print(f"Loading data from {file_path}...")
        df = pd.read_csv(f"{file_path}")    # It reads CSV file and loads it into a table structure called a DataFrame.

        df["timestamp"] = pd.to_datetime(df["timestamp"])    ## Converts the text into actual Time Objects.

    except FileNotFoundError:    # File is not found.
        print("Error: File not found. Please check the path.")
        return
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    

    # 2. Train model
    ## contamination of 0.01 = 1% of the traffic is anomalous
    print(f"Training Isolation Forest (Contamination: {contamination})...")
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
    plt.title(f"Anomaly Detection Result - {file_path}")
    plt.legend()
    plt.grid(True, alpha=0.3) # Added grid for readability


    # 5. Save to the output path
    output_png_path = os.path.join("output", f"{output_name}_{contamination}.png")
    plt.savefig(output_png_path)
    print(f"Graph saved to {output_png_path}.")


    # 6. Save the anomaly list into a CSV format.
    output_csv_path = os.path.join("output", f"{output_name}_anomalies_{contamination}.csv")
    anomalies.to_csv(output_csv_path, index=False)
    print(f"Anomaly list saved to {output_csv_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect anomalies in a network traffic file.")

    # Add arguments
    parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file")
    parser.add_argument("--output", type=str, default=None, help="Name of the output graph image")
    parser.add_argument("--c", type=float, default=0.01, help="Contamination rate (Default is 0.01)")

    args = parser.parse_args()

    final_output_name = args.output
    if final_output_name is None:
        base_name = os.path.basename(args.input)    # "traffic.csv" from "data/traffic.csv"
        filename, extension = os.path.splitext(base_name)
        final_output_name = f"{filename}_graph"

    # Run the function
    analyze_traffic(args.input, final_output_name, args.c)