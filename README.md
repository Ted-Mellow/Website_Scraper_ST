# 🔍 Website Scraper

Extract company names and URLs from any website into a CSV file. Perfect for building lists of exhibitors, vendors, sponsors, or partners.

## What It Does

**Paste URL → Scrape companies → Download CSV**

Works with:
- ✅ JSON-LD structured data (fastest: 1-2 sec/page)
- ✅ Traditional HTML sites (2-3 sec/page)
- ✅ JavaScript-rendered sites (slower but works: 15-30 sec/page)

## Quick Start

### Install (one-time)
```bash
pip install -r requirements.txt
```

### Run (every time)
```bash
python app.py
```

Open: **http://localhost:5001** in your browser

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

## How to Use

1. **Paste a URL** (e.g., `https://www.example.com/exhibitors`)
2. **Set max pages** (default 20)
3. **Check "Use Browser"** only if the site has lots of JavaScript (slower)
4. **Click "Scrape"** and wait 5-30 seconds
5. **See results** in a table
6. **Filter** by name or URL if needed
7. **Download CSV** with a timestamp

## Features

- 🚀 Works with any website (no hardcoding)
- 📄 Smart extraction (JSON-LD first, HTML fallback)
- 📑 Auto-pagination (detects page format automatically)
- 🔍 Filter by name or URL
- 📊 Download as CSV with website context
- 🌐 Beautiful, responsive web interface
- ✨ Shows which extraction method was used

## How It Works

### Two Extraction Modes

**Fast Mode (Default)**
- Analyzes the static HTML
- Looks for JSON-LD structured data
- Falls back to HTML pattern matching
- No JavaScript execution
- ~2-3 seconds per page

**Browser Mode** (🌐 Use Browser)
- Runs a headless Chromium browser
- Renders JavaScript before extraction
- Works with React/Vue/Angular sites
- Slower but more compatible
- ~15-30 seconds per page

### Smart Pagination

Automatically:
- Detects pagination format (`?page=`, `?p=`, `?page_num=`)
- Follows pagination links
- Stops when no new results found

### Data Extraction

1. Tries to find **JSON-LD structured data** first
   - Fast and reliable
   - Works if website embeds company data as JSON

2. Falls back to **HTML pattern matching**
   - Searches for common company link patterns
   - Filters out navigation and footer links
   - Extracts company names and URLs

## Files

```
.
├── app.py                 # Flask web server (runs on localhost:5001)
├── scraper.py             # Core scraping logic
├── templates/index.html   # Web interface
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── QUICKSTART.md         # Quick start guide
```

## Requirements

- **Python 3.8+**
- **500MB disk space** (for Playwright browser)
- **Internet connection**

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Port 5001 in use" | Change port in `app.py` line 135 |
| "No companies found" | Try enabling "Use Browser" or check site structure |
| "Slow performance" | Reduce max pages or try smaller sites |
| Python import error | Run `pip install -r requirements.txt` again |

## Technical Stack

- **Backend**: Python 3 + Flask
- **HTML Parsing**: BeautifulSoup4 + lxml
- **Browser Automation**: Playwright (Chromium)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **No database** needed (in-memory storage)

## Tips for Best Results

- **JSON-LD sites** (like Retail Tech Show): Fastest, no browser needed
- **Static HTML sites**: Default mode works great
- **JavaScript sites** (React/Vue): Enable "Use Browser" toggle
- **Large sites**: Be patient—100+ pages takes time
- **Stuck?** Try fewer max pages to test first

---

**Questions?** Check [QUICKSTART.md](QUICKSTART.md) for more help.

Happy scraping! 🚀
