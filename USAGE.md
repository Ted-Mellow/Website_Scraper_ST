# How to Use the Scraper

## The Simple Way

### Step 1: Install dependencies (one-time only)
```bash
pip install -r requirements.txt
```

### Step 2: Run the scraper
```bash
python scraper.py
```

That's it!

The scraper will:
- Download all 17 pages from the Retail Technology Show website
- Extract company names and URLs
- Save results to `exhibitors.csv`

### Step 3: Check your results
Open `exhibitors.csv` in Excel or any text editor to see the data.

---

## What You Get

A CSV file with 2 columns:
- **name** - Company name
- **url** - Company website or profile link

Example:
```
name,url
RGIS Inventory Specialists,https://www.rgis.co.uk
Ricoh UK,https://www.ricoh.co.uk/
Roke,https://www.retailtechnologyshow.com/exhibitors/roke
```

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'requests'"**
- Run: `pip install -r requirements.txt`

**"No data in CSV"**
- The website may have changed its structure
- Contact me to update the scraper

**Want to scrape a different website?**
- Contact me—the scraper is designed to be adaptable

---

## Advanced (Optional)

Edit `scraper.py` line 130-131 to change what you scrape:

```python
# Scrape only pages 1-5
success = scraper.run(start_page=1, end_page=5)

# Scrape just page 13
success = scraper.run(start_page=13, end_page=13)
```

That's all you need to know!
