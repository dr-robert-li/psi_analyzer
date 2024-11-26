# PageSpeed Insights Bulk Testing Tool

A Python tool for running Google PageSpeed Insights tests on multiple URLs and generating detailed performance reports.

## 📋 Features

- Bulk testing of multiple URLs
- Support for both TXT and CSV input files
- Detailed performance metrics extraction
- Raw JSON data export
- Formatted performance summary
- Console output with real-time results

## 🚀 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/pagespeed-insights-tool.git
    cd pagespeed-insights-tool
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create .env file and add your API key:
    ```bash
    PSI_API_KEY=your_api_key_here
    ```

## 📖 Usage

1. Prepare your input file:
    - TXT format:
        ```text
        https://www.example.com
        https://www.google.com
        ```
    - CSV format:
        ```csv
        URL
        https://www.example.com
        https://www.google.com
        ```

2. Run the script:
    ```bash
    python psi_analyzer.py
    ```

## 📊 Output Files

### PSI_raw_metrics.csv
Contains complete API responses for each URL:
```csv
URL,Raw JSON
https://www.example.com,{complete JSON response}
```

### PSI_performance_summary.csv
Contains tabulated performance metrics:
```csv
URL,timestamp,performance_score,first_contentful_paint,speed_index
https://www.example.com,2024-01-20T12:34:56.789Z,95.2,1.2s,2.1s
```

## 📈 Performance Metrics

Metric	Description
Performance Score	Overall score (0-100)
First Contentful Paint	Time until first content appears
Speed Index	How quickly content is visually displayed
Largest Contentful Paint	Largest content element load time
Time to Interactive	When page becomes fully interactive
Total Blocking Time	Sum of blocking time periods
Cumulative Layout Shift	Visual stability measure

## 📝 License
MIT License

### 🤝 Contributing

1. Fork the repository
2. Create your feature branch
```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes
```bash
git commit -m 'Add some AmazingFeature'
```

4. Push to the branch
```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request