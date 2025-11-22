import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("network_traffic.csv")    # It reads CSV file and loads it into a table structure called a DataFrame.
df["timestamp"] = pd.to_datetime(df["timestamp"])    # Converts the text into actual Time Objects.

plt.figure(figsize=(12, 6))    # Sets up the empty space where the graph will be drawn.
plt.plot(df["timestamp"], df["value"])    # This actually draws the data.
plt.title("Raw Network Traffic")    # Adds a title to the plot.
plt.show()    # Renders the final image on your screen.