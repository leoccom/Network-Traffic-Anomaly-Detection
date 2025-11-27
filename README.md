# Network Traffic Anomaly Detection

A robust command-line interface (CLI) tool designed to detect cybersecurity threats and anomalies in network traffic logs. This project uses Unsupervised Machine Learning to identify potential DDoS attacks and data exfiltration attempts in real-time server data.

**Link to project:** [https://github.com/leoccom/Network-Traffic-Anomaly-Detection](https://github.com/leoccom/Network-Traffic-Anomaly-Detection)

![Network Anomaly Detection Result](output/network_traffic_graph.png_0.001.png)

## How It's Made:

**Tech used:** Python, Pandas, Scikit-Learn, Matplotlib, Argparse

The core of this project is the **Isolation Forest** algorithm, an unsupervised machine learning model ideal for high-dimensional anomaly detection.

1.  **Data Ingestion:** The script accepts any CSV-formatted network log file (with columns `timestamp` and `value`) via the command line.
2.  **Preprocessing:** It parses timestamps and cleans the data for analysis.
3.  **Anomaly Detection:** The Isolation Forest model isolates outliers by randomly partitioning the data. Anomalies (such as massive traffic spikes) require fewer partitions to be isolated than normal data points.
4.  **Visualization:** The tool automatically generates a visualization plotting the "Normal" traffic in blue and the "Detected Threats" in red, giving network admins an instant visual assessment of server health.
5. **Documentation:** The script also saves a CSV file including anomalies. (`timestamp` and `value` for anomaly points)

## Optimizations

To make this script production-ready, I refactored it into a modular **CLI tool**.

* **Dynamic Argument Parsing:** Users can now specify input files, output filenames, and sensitivity levels (`--c`) directly from the terminal without touching the code.
* **Smart Defaults:** The script uses `os.path` to automatically generate meaningful output filenames based on the input file (e.g., `traffic.csv` -> `traffic_graph_0.01.png`).
* **Performance:** Removed unnecessary rolling-average calculations to speed up processing on large datasets, focusing purely on the raw metric analysis.

## Lessons Learned:

Building this project taught me the importance of **trade-offs in Machine Learning**. 

* **Sensitivity vs. Noise:** I learned that tuning the *contamination* hyperparameter is critical. Set it too low, and you miss attacks; set it too high, and you flood the user with false alarms.
* **User Experience:** Making the script as a CLI tool highlighted the need for good error handling (e.g., what if the file doesn't exist?) and clear user feedback (logging progress to the console).
* **Time-Series Analysis:** I gained a deeper understanding of how network patterns (like heartbeats vs. spikes) manifest in raw data.

## Usage Examples:

To run the analysis on a standard log file:
```bash
python3 src/analysis.py --input data/network_traffic.csv
```
(Be sure to locate your log file under data directory.)