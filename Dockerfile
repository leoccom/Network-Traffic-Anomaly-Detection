# 1. Use an official lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy requirements first (better for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the entire project structure (src, data, models, etc.)
COPY . .

# 5. critical step: Add the current directory to Python's path
# This allows 'src.model' imports to work correctly
ENV PYTHONPATH="${PYTHONPATH}:/app"

# 6. Run the main analysis script
CMD ["python", "src/analysis.py"]