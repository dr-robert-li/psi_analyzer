# PageSpeed Insights Bulk Testing Tool

A Python tool for running Google PageSpeed Insights tests on multiple URLs and generating detailed performance reports.

## 📋 Features

- Bulk testing of multiple URLs
- Support for both TXT and CSV input files
- Detailed performance metrics extraction
- Raw JSON data export
- Formatted performance summary
- Console output with real-time results
- Customizable output filenames
- Environment variable support for API key
- Desktop/Mobile strategy selection
- Real-time data persistence
- Comprehensive error handling
- Detailed success/failure statistics

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
    - With default settings (desktop strategy):
        ```bash
        python psi_analyzer.py input_urls.txt
        ```
    
    - With mobile strategy:
        ```bash
        python psi_analyzer.py input_urls.txt --strategy mobile
        ```
    
    - With custom output filenames:
        ```bash
        python psi_analyzer.py input_urls.txt --raw-output custom_raw.csv --summary-output custom_summary.csv
        ```
    
    - Get help on usage:
        ```bash
        python psi_analyzer.py --help
        ```

## 📊 Output Files

### Real-time Data Persistence
Results are saved immediately after each test:
- Preserves progress if script stops unexpectedly
- Reduces memory usage
- Ideal for long-running tests

### File Structure

1. Raw Metrics CSV:
    ```csv
    URL,Strategy,Raw JSON
    https://www.example.com,desktop,{complete JSON response}
    ```

2. Performance Summary CSV:
    ```csv
    URL,timestamp,strategy,performance_score,first_contentful_paint,speed_index
    https://www.example.com,2024-01-20T12:34:56.789Z,desktop,95.2,1.2s,2.1s
    ```

## 📈 Performance Metrics

| Metric | Description |
|--------|-------------|
| Performance Score | Overall score (0-100) |
| First Contentful Paint | Time until first content appears |
| Speed Index | How quickly content is visually displayed |
| Largest Contentful Paint | Largest content element load time |
| Time to Interactive | When page becomes fully interactive |
| Total Blocking Time | Sum of blocking time periods |
| Cumulative Layout Shift | Visual stability measure |

## 🛠️ Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| input_file | Input file path (required) | None |
| --raw-output | Raw metrics output filename | psi_raw_metrics.csv |
| --summary-output | Summary output filename | psi_performance_summary.csv |
| --strategy | Analysis strategy (desktop/mobile) | desktop |

## 📊 Console Output

The script provides detailed console feedback:
- Progress tracking (X/Y URLs completed)
- Real-time test results
- Error messages for failed tests
- Final summary with success/failure statistics
- Visual indicators (✅/❌) for quick status recognition

## 📝 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch:
    ```bash
    git checkout -b feature/AmazingFeature
    ```

3. Commit your changes:
    ```bash
    git commit -m 'Add some AmazingFeature'
    ```

4. Push to the branch:
    ```bash
    git push origin feature/AmazingFeature
    ```

5. Open a Pull Request