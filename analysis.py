import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest


df = pd.read_csv("network_traffic.csv")    # It reads CSV file and loads it into a table structure called a DataFrame.
df["timestamp"] = pd.to_datetime(df["timestamp"])    # Converts the text into actual Time Objects.


df["moving_avg"] = df["value"].rolling(window=50).mean()    # Calculate and store 50-point moving average.


plt.figure(figsize=(12, 6))    # Sets up the empty space where the graph will be drawn.
plt.plot(df["timestamp"], df["value"])    # This actually draws the data.
plt.plot(df["timestamp"], df["moving_avg"])    # Draws the moving average.
plt.title("Raw Network Traffic")    # Adds a title to the plot.
# plt.show()    # Renders the final image on your screen.


data_for_model = df["value"]


# contamination of 0.01 = 1% of the traffic is anomalous
model = IsolationForest(contamination=0.01, random_state=42)
model.fit(df[["value"]])

df["anomaly"] = model.predict(df[["value"]])    # -1: Anomaly, 1: Normal

anomalies = df[df["anomaly"] == -1]

plt.scatter(anomalies["timestamp"], anomalies["value"], color="red")
plt.show()