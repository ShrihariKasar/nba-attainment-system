import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_FOLDER = "static/results"

# ✅ Ensure the results folder exists
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def process_excel(filepath):
    """Processes an Excel file and generates graphs."""
    try:
        # ✅ Load the Excel file
        df = pd.read_excel(filepath)
        print(f"✅ Loaded Excel file: {filepath}")  
        print(f"✅ Columns in file: {df.columns.tolist()}")  

        # ✅ Check if the required column exists
        required_column = "Some Column"
        if required_column not in df.columns:
            print(f"❌ Required column '{required_column}' not found!")
            return {"error": f"Required column '{required_column}' not found in file."}

        # ✅ Drop NaN values to prevent errors in plots
        df = df.dropna(subset=[required_column])

        # ✅ Generate paths for output images
        histogram_path = os.path.join(RESULTS_FOLDER, "histogram.png")
        bar_chart_path = os.path.join(RESULTS_FOLDER, "bar_chart.png")

        # ✅ Generate Histogram
        plt.figure(figsize=(6, 4))
        df[required_column].hist()
        plt.savefig(histogram_path, bbox_inches='tight')
        plt.close()  # Clear plot

        # ✅ Generate Bar Chart
        plt.figure(figsize=(6, 4))
        df[required_column].value_counts().plot(kind="bar")
        plt.savefig(bar_chart_path, bbox_inches='tight')
        plt.close()

        print(f"✅ Saved histogram at: {histogram_path}")
        print(f"✅ Saved bar chart at: {bar_chart_path}")

        # ✅ Ensure paths are JSON-serializable (relative paths)
        return {
            "histogram": os.path.relpath(histogram_path, "static"),
            "bar_chart": os.path.relpath(bar_chart_path, "static")
        }

    except Exception as e:
        print(f"❌ Error while processing: {e}")
        return {"error": f"Processing failed: {str(e)}"}    