# Quick Start Guide

## One-Time Setup (5 minutes)

### 1. Install Python
Make sure you have Python 3.8+ installed.
```bash
python3 --version  # Should show 3.8 or higher
```

### 2. Install Dependencies
```bash
cd Website\ Scraper
pip install -r requirements.txt
```

This installs:
- **Flask** - web server
- **Playwright** - browser automation (for JavaScript sites)
- **BeautifulSoup4** - HTML parsing
- **requests** - HTTP client

## Running the Scraper (Every Time)

```bash
python app.py
```

Then open: **http://localhost:5001** in your browser

## Using the Scraper

1. **Paste a website URL** (e.g., `https://www.example.com/exhibitors`)
2. **Set max pages** (default 20 is fine for most sites)
3. **Check "Use Browser"** if the site has lots of JavaScript (slower but works with interactive sites)
4. **Click Scrape** and wait 5-30 seconds
5. **See results in a table** with company names and URLs
6. **Filter** by name or URL if needed
7. **Download CSV** with a timestamp

## Tips

- **JSON-LD sites** (like Retail Tech Show): Fastest, no need for browser mode
- **JavaScript sites** (React/Vue): Enable "Use Browser" (slower but works)
- **Large scrapers**: Be patient—downloading 100+ pages takes time

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5001 in use | Change port in `app.py` line 135 |
| "No companies found" | Try enabling "Use Browser" or check the site structure |
| Slow performance | Try fewer max pages or smaller sites |
| TypeError about Playwright | Run `pip install -r requirements.txt` again |

## Stopping the Scraper

Press **Ctrl+C** in the terminal.

---

That's it! Enjoy scraping 🚀
