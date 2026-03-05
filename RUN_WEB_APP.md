# Web Scraper - Quick Start Guide

## Start the Server

Open terminal and run:
```bash
cd /Users/macbook/Desktop/Curiosity/Website\ Scraper
python app.py
```

You'll see:
```
Starting Web Scraper at http://localhost:5001
Open your browser and visit http://localhost:5001
```

## Use the App

1. **Open browser**: Go to `http://localhost:5001`
2. **Paste URL**: Enter any website URL (e.g., `https://www.retailtechnologyshow.com/exhibitors`)
3. **Set max pages**: How many pages to scrape (default: 20)
4. **Click "Scrape"**: Wait for results (shows spinner)
5. **View results**: Table appears with company names & URLs
6. **Download CSV**: Click "📥 Download CSV" to save the results

## How It Works

- **JSON-LD first**: Looks for structured data (fastest, most reliable)
- **HTML fallback**: If no JSON-LD found, scans HTML for common patterns
- **Auto-stops**: Stops scraping when a page returns no results
- **Shows method**: Tells you which extraction method was used

## Example URLs to Test

✓ **Works great with JSON-LD:**
- `https://www.retailtechnologyshow.com/exhibitors`

Try any other website with:
- Company/exhibitor directories
- Product listings
- Directory pages with links

## Troubleshooting

**"Address already in use" or port conflict?**
- Edit `app.py` line 95, change `port=5001` to a different number (e.g., 5002)

**No results found?**
- Website may not have structure we can parse
- Check the "method" shown (JSON-LD or HTML fallback)
- Try another website

**Download not working?**
- Make sure you've scraped at least once
- Try the scrape again before downloading

---

**To stop the server**: Press `Ctrl+C` in the terminal

Enjoy! 🚀
