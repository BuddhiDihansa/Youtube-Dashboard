# YouTube Creator Analytics Dashboard

An interactive Streamlit dashboard for exploring YouTube creator performance data. The app loads a large CSV dataset, applies sidebar filters, and visualizes views, likes, comments, engagement, geography, language, and time-based trends.

## Features

- Interactive sidebar filters for category, region, language, and date range
- KPI cards for total views, likes, comments, and average engagement
- Engagement charts by category and region
- Monthly views trend analysis
- Views vs engagement scatter plot
- Engagement distribution pie chart
- Top 15 high-performing videos table
- Summary metrics and AI-style insights for quick interpretation

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

- app.py - Streamlit dashboard UI and visualizations
- dashboard_shared.py - Data loading and filtering helpers
- global_youtube_creator_data_large.csv - Dataset used by the dashboard
- requirements.txt - Python dependencies

## Requirements

- Python 3.10 or newer
- A virtual environment is recommended

## Installation

1. Clone or download this project.
2. Open the project folder in your terminal.
3. Create and activate a virtual environment if you do not already have one:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

4. Install the dependencies:

```powershell
pip install -r requirements.txt
```

## Run the App

```powershell
streamlit run app.py
```

If you are using the bundled virtual environment, you can also run:

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

## How It Works

The dashboard reads the CSV dataset, calculates engagement from likes, comments, and shares divided by views, and adds time features such as month and hour for trend analysis. The sidebar filters update all charts and summary metrics instantly.

## Screenshots

Add one or two screenshots here after you take them from the running dashboard.

## LinkedIn Post Idea

I built my first Python dashboard using Streamlit, Pandas, and Plotly. It analyzes YouTube creator performance with interactive filters, KPIs, trend charts, and summary insights.

GitHub: your-repo-link

Live demo: your-demo-link

## License

No license has been added yet. Add one if you want to publish this publicly.
