import csv
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os
import argparse

# Load environment variables
load_dotenv()

class PageSpeedInsights:
    def __init__(self, strategy='desktop'):
        self.api_key = os.getenv('PSI_API_KEY')
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        self.strategy = strategy
        
    def load_urls(self, input_file):
        file_ext = Path(input_file).suffix.lower()
        urls = []
        
        if file_ext == '.txt':
            with open(input_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        elif file_ext == '.csv':
            with open(input_file, 'r') as f:
                reader = csv.reader(f)
                urls = [row[0].strip() for row in reader if row and row[0].strip()]
                
        return urls

    def run_psi_test(self, url):
        api_url = f"{self.base_url}?url={url}&strategy={self.strategy}"
        if self.api_key:
            api_url += f"&key={self.api_key}"

        try:
            result = subprocess.run(['curl', api_url], capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error testing {url}: {str(e)}")
            return None

    def extract_metrics(self, psi_result):
        if not psi_result:
            return None

        metrics = {
            'url': psi_result.get('id', ''),
            'timestamp': psi_result.get('analysisUTCTimestamp', ''),
            'strategy': self.strategy,
            'performance_score': psi_result.get('lighthouseResult', {}).get('categories', {}).get('performance', {}).get('score', 0) * 100,
            'first_contentful_paint': psi_result.get('lighthouseResult', {}).get('audits', {}).get('first-contentful-paint', {}).get('displayValue', ''),
            'speed_index': psi_result.get('lighthouseResult', {}).get('audits', {}).get('speed-index', {}).get('displayValue', ''),
            'largest_contentful_paint': psi_result.get('lighthouseResult', {}).get('audits', {}).get('largest-contentful-paint', {}).get('displayValue', ''),
            'time_to_interactive': psi_result.get('lighthouseResult', {}).get('audits', {}).get('interactive', {}).get('displayValue', ''),
            'total_blocking_time': psi_result.get('lighthouseResult', {}).get('audits', {}).get('total-blocking-time', {}).get('displayValue', ''),
            'cumulative_layout_shift': psi_result.get('lighthouseResult', {}).get('audits', {}).get('cumulative-layout-shift', {}).get('displayValue', '')
        }
        return metrics

    def save_raw_result(self, url, result, filename='psi_raw_metrics.csv'):
        if not Path(filename).exists():
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['URL', 'Strategy', 'Raw JSON'])

        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([url, self.strategy, json.dumps(result)])

    def save_summary_result(self, metrics, filename='psi_performance_summary.csv'):
        if not Path(filename).exists():
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(metrics.keys())

        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(metrics.values())

    def print_summary(self, metrics):
        print("\n" + "="*50)
        print(f"PageSpeed Insights Results for {metrics['url']}")
        print(f"Strategy: {self.strategy.upper()}")
        print("="*50)
        print(f"Performance Score: {metrics['performance_score']:.1f}/100")
        print(f"First Contentful Paint: {metrics['first_contentful_paint']}")
        print(f"Speed Index: {metrics['speed_index']}")
        print(f"Largest Contentful Paint: {metrics['largest_contentful_paint']}")
        print(f"Time to Interactive: {metrics['time_to_interactive']}")
        print(f"Total Blocking Time: {metrics['total_blocking_time']}")
        print(f"Cumulative Layout Shift: {metrics['cumulative_layout_shift']}")
        print("="*50 + "\n")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run PageSpeed Insights analysis on multiple URLs')
    parser.add_argument('input_file', 
                      help='Input file containing URLs (txt or csv)')
    parser.add_argument('--raw-output', 
                      default='psi_raw_metrics.csv',
                      help='Output file for raw metrics (default: psi_raw_metrics.csv)')
    parser.add_argument('--summary-output', 
                      default='psi_performance_summary.csv',
                      help='Output file for performance summary (default: psi_performance_summary.csv)')
    parser.add_argument('--strategy',
                      choices=['desktop', 'mobile'],
                      default='desktop',
                      help='Analysis strategy: desktop or mobile (default: desktop)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    psi = PageSpeedInsights(strategy=args.strategy)
    print(f"\nRunning PageSpeed Insights analysis using {args.strategy.upper()} strategy")
    
    urls = psi.load_urls(args.input_file)
    total_urls = len(urls)
    successful_tests = 0
    failed_tests = 0
    
    for index, url in enumerate(urls, 1):
        print(f"\nTesting {url} ({index}/{total_urls})...")
        try:
            result = psi.run_psi_test(url)
            if result:
                if 'error' in result:
                    print(f"❌ API Error for {url}: {result['error']['message']}")
                    failed_tests += 1
                else:
                    # Save raw result immediately
                    psi.save_raw_result(url, result, args.raw_output)
                    
                    metrics = psi.extract_metrics(result)
                    if metrics:
                        # Save metrics immediately
                        psi.save_summary_result(metrics, args.summary_output)
                        psi.print_summary(metrics)
                        successful_tests += 1
                    else:
                        print(f"❌ Failed to extract metrics for {url}")
                        failed_tests += 1
            else:
                print(f"❌ No result returned for {url}")
                failed_tests += 1
                
        except Exception as e:
            print(f"❌ Error processing {url}: {str(e)}")
            failed_tests += 1
            
        time.sleep(1)  # Rate limiting
    
    # Print final summary
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE")
    print(f"Total URLs tested: {total_urls}")
    print(f"Successful: {successful_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Results saved to {args.raw_output} and {args.summary_output}")
    print("="*50)

if __name__ == "__main__":
    main()