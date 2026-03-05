# Filtering Guide - New Feature

## What's New

Your scraper now has **live filtering** to help you refine results after scraping.

## How to Use

### 1. Scrape a Website
- Paste URL → Click Scrape → Wait for results

### 2. Filter Results (NEW!)
After scraping, you'll see a filter panel:

```
┌─────────────────────────────────────────┐
│ Filter by Company Name                  │
│ [Type to filter...]    [Filter Type: ▼] │
│ - Company Name (default)                │
│ - URL                                   │
│                          [ Reset ]      │
└─────────────────────────────────────────┘
```

### 3. Choose Filter Type
**Company Name Filter:**
- Filters by company/exhibitor name
- Example: Type "cloud" → Shows all companies with "cloud" in name
- Case-insensitive

**URL Filter:**
- Filters by URL/link
- Example: Type "bacardi" → Shows all companies with "bacardi" in URL
- Case-insensitive

### 4. See Results
Filter shows: **X/Y** companies matched
- X = Filtered results
- Y = Total companies

Example: Filter "winery" on Bar Convention → Shows "1/96"

### 5. Reset
Click **Reset** button to clear filter and see all results again

---

## Examples

### Example 1: Find All Cloud Companies
**Website:** Retail Technology Show
**Total results:** 24

Steps:
1. Type "cloud" in filter field
2. See: "1/24" (1 company matches)
3. Result: "3D Cloud"

### Example 2: Find Spirits/Wine Vendors
**Website:** Bar Convention London
**Total results:** 96

Steps:
1. Change filter type to "URL"
2. Type "wine" in filter field
3. See: "1/96" (1 winery matches)
4. Result: "LEA Winery S.R.L."

### Example 3: Find by URL Domain
**Website:** Retail Technology Show
**Total results:** 24

Steps:
1. Use "URL" filter type
2. Type ".io" in filter field
3. See: "2/24" (2 companies with .io domain)

---

## CSV Download with Website Context

**New Filenames:**
```
retailtechnologyshow_exhibitors_20260305_121500.csv
barconventlondon_exhibitors_20260305_121500.csv
```

**Old Filenames:**
```
exhibitors_20260305_121500.csv  (no context)
```

Benefits:
- Know which website the data came from
- Organize multiple exports easily
- Clear file naming

---

## Important Notes

✓ **Filtering works on ALL results**
- If you scraped 100 pages, filter searches all 100 pages
- Not just the visible page

✓ **Filter is case-insensitive**
- "Cloud" = "cloud" = "CLOUD" (all match)

✓ **Partial matches work**
- Filter "tech" finds "Technology", "technical", etc.

✓ **Real-time feedback**
- See count update as you type
- Reset button always available

---

## Tips & Tricks

**Narrow Down Large Results:**
```
Scrape 1000 companies
Filter by "uk" → See only UK companies
Filter by "com" → See only .com domains
```

**Find Specific Companies:**
```
Type exact company name → Should find it
Example: "Bacardi" → Finds "Bacardi-Martini Limited"
```

**Combine with CSV Download:**
```
1. Scrape website
2. Filter results
3. Download CSV → CSV contains ONLY visible (filtered) results
```

**No Filter Applied?**
```
Reset button → See all results again
```

---

## Troubleshooting

**Filter not working?**
- Make sure filter field is focused (text cursor visible)
- Check that you typed the search term
- Try reset to clear

**Filter shows 0 results?**
- Your search term doesn't match any companies
- Try a shorter keyword
- Check spelling
- Try URL filter instead

**Filter very slow?**
- Filtering is instant (shouldn't be slow)
- If slow, check browser console for errors
- Refresh page and try again

---

## Future Enhancements

Possible filter additions:
- Filter by URL domain (.com, .co.uk, etc.)
- Multiple filters combined (AND/OR logic)
- Filter by text length
- Regex pattern matching
- Date range filters (when available)

---

**Happy filtering!** Use this to quickly narrow down results from large scrapes.
