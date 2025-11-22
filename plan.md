# 📅 7-Day Action Plan: CAIDA REU Application
**Goal:** Build a "Network Traffic Anomaly Detection" project to secure an interview.
**Dataset:** Numenta Anomaly Benchmark (AWS Cloudwatch)
**Target Role:** Data Science Assistant (Time-Series Analysis)

---

## ✅ Day 1: Setup & Data Exploration
**Focus:** Environment setup and visualizing the raw data.

- [ ] **Step 1: Install Tools**
  - Install VS Code and Python (Anaconda recommended).
  - Run in terminal: `pip install pandas numpy matplotlib scikit-learn jupyter`
  - Create a project folder: `Network-Traffic-Anomaly-Detection/`

- [ ] **Step 2: Get the Data**
  - Go to Kaggle: [Numenta Anomaly Benchmark](https://www.kaggle.com/datasets/boltzmannbrain/nab)
  - Download and extract the zip file.
  - Locate file: `realAWSCloudwatch/ec2_network_in_5min.csv`
  - Move this CSV into your project folder.

- [ ] **Step 3: Initial Plot (Jupyter Notebook)**
  - Create `analysis.ipynb`.
  - Run the following to verify data:
    ```python
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv('ec2_network_in_5min.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    plt.figure(figsize=(12,6))
    plt.plot(df['timestamp'], df['value'])
    plt.title("Raw Network Traffic")
    plt.show()
    ```

---

## ✅ Day 2: Feature Engineering
**Focus:** Smoothing the data so the Machine Learning model can understand it.

- [ ] **Step 1: Understanding Noise**
  - The raw data is jagged. We need a baseline.

- [ ] **Step 2: Create a Moving Average**
  - Add this code to your notebook:
    ```python
    # Create a rolling window of 50 intervals
    df['moving_avg'] = df['value'].rolling(window=50).mean()
    
    # Visualize the difference
    plt.figure(figsize=(12,6))
    plt.plot(df['timestamp'], df['value'], label='Raw')
    plt.plot(df['timestamp'], df['moving_avg'], label='Moving Avg', color='orange')
    plt.legend()
    plt.show()
    ```

- [ ] **Step 3: Prepare for Model**
  - Read up on **Isolation Forest** for 20 mins.
  - Concept: "It identifies anomalies by randomly cutting the data; outliers are easier to isolate."

---

## ✅ Day 3: The Machine Learning Model
**Focus:** Implementing Isolation Forest to detect threats.

- [ ] **Step 1: Train the Model**
  ```python
  from sklearn.ensemble import IsolationForest
  
  # Prepare data (Model only wants the values, not timestamps)
  data = df[['value']]
  
  # Contamination = % of data we think is an attack (e.g., 1%)
  model = IsolationForest(contamination