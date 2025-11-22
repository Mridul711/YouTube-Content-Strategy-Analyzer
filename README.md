# 📹 YouTube Content Strategy Auditor (API & Interactive Dashboard)

## 📌 Project Overview
This project is an analytical tool designed to audit YouTube channels and identify viral content strategies. Instead of relying on manual checks, I built an automated pipeline that connects to the **YouTube Data API v3** to extract granular video metrics (Views, Likes, Duration, Engagement).

The output is an **Interactive Dark-Mode Dashboard** (built with Plotly) that helps creators answer:
* "Does video length correlate with higher views?"
* "What is the average engagement rate?"
* "Which video format (Short vs Long) performs best?"

## 🛠️ Tech Stack
* **Data Source:** YouTube Data API v3 (Google Cloud Platform).
* **ETL Pipeline:** Python (`google-api-python-client`, `pandas`).
* **Data Processing:** `isodate` (for parsing ISO 8601 durations).
* **Visualization:** `Plotly` (Interactive Charts, Dark Mode, Heatmaps).

## 📊 Key Features
1.  **Automated Extraction:** Fetches the last 50-100 videos from any channel ID.
2.  **Data Cleaning:** Converts raw API data (e.g., `PT10M5S`) into analyzable metrics (Minutes).
3.  **Interactive Dashboard:** Generates a standalone HTML file with:
    * **Growth Trends:** Time-series analysis of views.
    * **Strategy Scatter Plot:** Video Duration vs. Views (Color-coded by Engagement).
    * **Correlation Matrix:** Heatmap to find hidden relationships between Likes/Comments/Views.

## 📷 Dashboard Preview
*(Download the `youtube_dashboard_dark_v2.html` file to interact with the charts!)*

**Key Insights found for sample channel:**
* **Correlation:** Strong positive correlation (0.88) between Video Length and Views, suggesting the audience prefers in-depth tutorials over quick tips.
* **Engagement:** Average engagement rate is **3.2%**, with "Medium Length" videos (10-20 mins) driving the highest community interaction.

## ⚙️ How to Run
1.  **Clone the repo:**
    ```bash
    git clone https://github.com/Mridul711/YouTube-Content-Strategy-Analyzer.git
    ```
2.  **Install dependencies:**
    ```bash
    pip install pandas google-api-python-client plotly isodate
    ```
3.  **Get a YouTube API Key:**
    * Go to Google Cloud Console -> Enable "YouTube Data API v3".
    * Generate an API Key and paste it into `youtube_extractor.py`.
4.  **Run the Pipeline:**
    ```bash
    python youtube_extractor.py  # Extracts data to csv
    python dashboard_pro_dark_v2.py   # Generates the dashboard
    ```
