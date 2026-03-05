# Web Scraper - Complete Features

## ✓ What You Can Do

### 1. Scrape Static Websites (Fast)
- JSON-LD structured data
- Traditional HTML listings
- Multi-page sites with pagination
- **Speed:** 2-3 seconds per page

**Example:** Retail Technology Show
```
Input: https://www.retailtechnologyshow.com/exhibitors
Result: 399 companies via JSON-LD
```

### 2. Scrape JavaScript-Rendered Sites (Browser Mode)
- React/Vue/Angular applications
- Dynamically loaded listings
- Modern web applications
- **Speed:** 15-30 seconds per page

**Example:** Bar Convention London
```
Input: https://www.barconventlondon.com/en-gb/exhibitor-directory.html
Result: 96 exhibitors from JavaScript-rendered page
```

### 3. Automatic Data Quality
- **All-or-nothing:** Only saves entries with name AND URL
- Deduplication by URL
- Filters out navigation/footer links
- Clean CSV output

### 4. Smart Extraction Methods
- **JSON-LD first** (fastest, most reliable)
- **HTML pattern matching** (fallback when no JSON-LD)
  - `.company a`, `.exhibitor a`, `.vendor a`
  - `article > a`, `h2 > a`, `h3 > a`
  - Skips navigation keywords (home, contact, privacy, etc.)

### 5. Auto-Pagination
- Automatically stops when page has no results
- No need to guess pagination limits
- Configurable max pages (1-100)

## Web Interface

**Open:** http://localhost:5001

### Input Fields
- **Website URL** - Any exhibitor/company directory
- **Max Pages** - How many pages to try (default 20)
- **🌐 Use Browser** - Toggle for JavaScript sites

### Output
- **Results Table** - All companies with clickable links
- **Download CSV** - Export as exhibitors_TIMESTAMP.csv
- **Status Message** - Shows which method was used

## Comparison

| Feature | Fast Mode | Browser Mode |
|---------|-----------|--------------|
| Speed | ⚡ 2-3s/page | 🐌 15-30s/page |
| JSON-LD | ✓ Yes | ✓ Yes |
| HTML Parsing | ✓ Yes | ✓ Yes |
| JavaScript | ✗ No | ✓ Yes |
| Best For | Static sites | Modern apps |
| Recommended | Default | Only if needed |

## Tested Websites

✓ **Works Great (Fast Mode)**
- Retail Technology Show (JSON-LD)
- Any site with static HTML/JSON-LD

✓ **Works Great (Browser Mode)**
- Bar Convention London (React-based)
- Any JavaScript-rendered directory

## Quick Tips

1. **Try fast mode first** - It's much faster
2. **If you get navigation links** - Use browser mode
3. **Check the status message** - It tells you which method worked
4. **Download after scraping** - The button appears after success
5. **Use reasonable page counts** - 20 is usually enough (browser mode is slow)

## Command Line Usage

For advanced users, you can also scrape from Python:

```python
from scraper import FlexibleScraper

# Fast mode (default)
scraper = FlexibleScraper('https://example.com/exhibitors')
results, method = scraper.run(start_page=1, max_pages=20)
print(f"Found {len(results)} companies using {method}")

# Browser mode
scraper = FlexibleScraper('https://example.com/exhibitors')
results, method = scraper.run(start_page=1, max_pages=20, use_browser=True)
```

## Files

- `app.py` - Flask web server
- `scraper.py` - Core scraping logic
- `templates/index.html` - Web UI
- `requirements.txt` - Dependencies (includes playwright)
- `BROWSER_MODE.md` - Detailed browser mode info
- `RUN_WEB_APP.md` - Startup instructions

---

**Ready to scrape?**
1. Start the server: `python app.py`
2. Open http://localhost:5001
3. Paste a URL and click Scrape!
