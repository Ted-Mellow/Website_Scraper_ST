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
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')

# Single-slot cache for latest scrape results (prevents memory leak)
session_data = {
    'last_results': None,
    'last_method': None,
    'last_url': None,
    'last_domain': None
}

def extract_domain_name(url: str) -> str:
    """Extract readable domain name from URL"""
    parsed = urlparse(url)
    netloc = parsed.netloc.replace('www.', '')

    # Remove port
    if ':' in netloc:
        netloc = netloc.split(':')[0]

    # Split by dots and get most meaningful part
    parts = netloc.split('.')

    if len(parts) >= 3 and parts[-2] in ['co', 'com', 'org', 'net', 'gov']:
        # Domain like "retailtechnologyshow.co.uk" → use first part
        return parts[0]
    elif len(parts) >= 2:
        # Standard domain like "example.com" → use first part
        return parts[0]
    else:
        # Single word like "localhost"
        return parts[0]

    return netloc


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

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'

        # Validate URL structure
        parsed = urlparse(url)
        if not parsed.netloc or not parsed.netloc.count('.') >= 1:
            return jsonify({'error': 'Invalid URL format'}), 400

        if parsed.scheme not in ['http', 'https']:
            return jsonify({'error': 'Only HTTP(S) URLs supported'}), 400

        max_pages = int(data.get('max_pages', 20))
        if not (1 <= max_pages <= 100):
            max_pages = 20

        use_browser = data.get('use_browser', False)

        logger.info(f"Scrape request: {url} (max {max_pages} pages, browser={use_browser})")

        # Run scraper
        scraper = FlexibleScraper(url)
        results, method = scraper.run(start_page=1, max_pages=max_pages, use_browser=use_browser)

        if not results:
            logger.info(f"No results for {url}")
            return jsonify({
                'error': 'No companies found on this website',
                'count': 0,
                'method': 'none'
            }), 200

        # Extract domain name (single-slot cache, overwrites previous)
        domain = extract_domain_name(url)

        # Store results for download (single-slot cache, prevents memory leak)
        session_data['last_results'] = results
        session_data['last_method'] = method
        session_data['last_url'] = url
        session_data['last_domain'] = domain

        logger.info(f"Scrape complete: {len(results)} results found using {method}")

        return jsonify({
            'results': results,
            'count': len(results),
            'method': method,
            'url': url,
            'domain': domain
        }), 200

    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        return jsonify({'error': 'Invalid input format'}), 400
    except Exception as e:
        logger.error(f"Scrape error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/filter', methods=['POST'])
def filter_results():
    """Filter results by company name or URL"""
    if not session_data['last_results']:
        return jsonify({'error': 'No results to filter. Please scrape first.'}), 400

    data = request.json
    filter_type = data.get('type', 'name')  # 'name' or 'url'
    filter_value = data.get('value', '').strip()

    if not filter_value:
        # Return all results if no filter value
        results = session_data['last_results']
        return jsonify({
            'results': results,
            'count': len(results),
            'original_count': len(results),
            'filtered_out': 0
        }), 200

    filter_value = filter_value.lower()
    results = session_data['last_results']

    try:
        if filter_type == 'name':
            filtered = [r for r in results if filter_value in r.get('name', '').lower()]
        elif filter_type == 'url':
            filtered = [r for r in results if filter_value in r.get('url', '').lower()]
        else:
            return jsonify({'error': 'Invalid filter type'}), 400

        logger.debug(f"Filter: {filter_type} by '{filter_value}' → {len(filtered)}/{len(results)} results")

        return jsonify({
            'results': filtered,
            'count': len(filtered),
            'original_count': len(results),
            'filtered_out': len(results) - len(filtered)
        }), 200
    except Exception as e:
        logger.error(f"Filter error: {e}", exc_info=True)
        return jsonify({'error': 'Filter operation failed'}), 500


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
