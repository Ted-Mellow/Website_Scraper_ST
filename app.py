"""
Flask Web App for Flexible Website Scraper
Allows users to paste URLs and extract company names + links
"""

from flask import Flask, render_template, request, jsonify, send_file
from scraper import FlexibleScraper
import io
import csv
from datetime import datetime
from urllib.parse import urlparse
import re

app = Flask(__name__, template_folder='templates')

# Store results in memory (keyed by session)
session_data = {}


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    """Scrape a website and return results as JSON"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        max_pages = int(data.get('max_pages', 20))
        use_browser = data.get('use_browser', False)

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        if not url.startswith('http'):
            url = f'https://{url}'

        # Run scraper
        scraper = FlexibleScraper(url)
        results, method = scraper.run(start_page=1, max_pages=max_pages, use_browser=use_browser)

        if not results:
            return jsonify({
                'error': 'No companies found on this website',
                'count': 0,
                'method': 'none'
            }), 200

        # Extract website name from URL for filename context
        domain = urlparse(url).netloc.replace('www.', '').split('.')[0]

        # Store results for download
        session_data['last_results'] = results
        session_data['last_method'] = method
        session_data['last_url'] = url
        session_data['last_domain'] = domain

        return jsonify({
            'results': results,
            'count': len(results),
            'method': method,
            'url': url,
            'domain': domain
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/filter', methods=['POST'])
def filter_results():
    """Filter results by company name or URL"""
    if 'last_results' not in session_data:
        return jsonify({'error': 'No results to filter'}), 400

    data = request.json
    filter_type = data.get('type', 'name')  # 'name' or 'url'
    filter_value = data.get('value', '').strip().lower()

    if not filter_value:
        return jsonify({'error': 'Filter value required'}), 400

    results = session_data['last_results']
    filtered = []

    if filter_type == 'name':
        filtered = [r for r in results if filter_value in r['name'].lower()]
    elif filter_type == 'url':
        filtered = [r for r in results if filter_value in r['url'].lower()]
    else:
        return jsonify({'error': 'Invalid filter type'}), 400

    return jsonify({
        'results': filtered,
        'count': len(filtered),
        'original_count': len(results),
        'filtered_out': len(results) - len(filtered)
    }), 200


@app.route('/download', methods=['GET'])
def download():
    """Download the last scraped results as CSV"""
    if 'last_results' not in session_data:
        return 'No data to download', 404

    results = session_data['last_results']
    domain = session_data.get('last_domain', 'exhibitors')

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['name', 'url'])
    writer.writeheader()
    writer.writerows(results)

    # Return as file with website context
    output.seek(0)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{domain}_exhibitors_{timestamp}.csv'

    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )


if __name__ == '__main__':
    print("Starting Web Scraper at http://localhost:5001")
    print("Open your browser and visit http://localhost:5001")
    app.run(debug=True, port=5001)
