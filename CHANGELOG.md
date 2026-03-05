# Changelog - Version 2.0

## New Features Added

### 1. Website Context in CSV Filenames
**What:** CSV files now include the website name for clarity

**Before:**
```
exhibitors_20260305_121500.csv
```

**After:**
```
retailtechnologyshow_exhibitors_20260305_121500.csv
barconventlondon_exhibitors_20260305_121500.csv
```

**Benefit:** Know which website your data came from at a glance

---

### 2. Live Filtering
**What:** Filter results by company name or URL in real-time

**Features:**
- Type to filter (instant results)
- Two filter types: Name & URL
- Shows match count (X/Y)
- Reset button to clear filter
- Works on all results (not just visible page)

**Use Cases:**
- Find specific companies by name
- Filter by URL domain or pattern
- Narrow down large result sets
- Organize data before export

**Example:**
```
Scrape Bar Convention: 96 companies
Filter "winery" by name → Shows 1/96
Download CSV with only filtered results
```

---

## Code Changes

### Flask App (app.py)
- Added `/filter` endpoint for filtering results
- Added domain extraction from URLs
- Updated `/download` to use website context
- Added imports for URL parsing

### HTML UI (templates/index.html)
- Added filter input field
- Added filter type selector (Name/URL)
- Added reset button
- Updated result count display
- Styled filter panel

### JavaScript
- Added `filterInput` event listeners
- Added `applyFilter()` function
- Added `displayFilteredResults()` function
- Added `resetFilter()` function
- Stored all results in `allResults[]` for filtering

---

## Testing Results

### Websites Tested
✓ Retail Technology Show (24 companies, JSON-LD, Fast Mode)
✓ Bar Convention London (96 companies, JS-rendered, Browser Mode)

### Features Tested
✓ Scraping still works (all methods)
✓ Domain extraction works
✓ Filter by name works
✓ Filter by URL works
✓ CSV download works with new filename
✓ Reset filter works
✓ Backward compatibility maintained

### Known Limitations
✗ Black Hat Asia (WAF-protected, requires authentication)

---

## Breaking Changes
**None!** All existing features work exactly as before.

---

## Performance Impact
**Negligible** - No impact on scraping speed, filters are instant (<0.1s)

---

## Files Changed
1. `app.py` - Added filter endpoint, domain extraction
2. `templates/index.html` - Added filter UI
3. New docs:
   - `TEST_RESULTS.md` - Comprehensive test results
   - `FILTERING_GUIDE.md` - User guide for filtering
   - `CHANGELOG.md` - This file

---

## How to Use New Features

### Filtering
1. Scrape a website
2. In results, use filter field at top
3. Type to filter by company name
4. Or select "URL" and type to filter by URL
5. Click Reset to see all results again

### Website Context in Filenames
1. Scrape a website
2. Click "Download CSV"
3. Filename now includes website (e.g., `retailtechnologyshow_exhibitors_...`)

---

## Future Roadmap

Potential enhancements:
- [ ] Advanced filtering (regex, multiple filters)
- [ ] Export to other formats (JSON, Excel)
- [ ] Filter by URL domain (.com, .co.uk)
- [ ] Search highlighting in results
- [ ] Pagination for large result sets
- [ ] Company name suggestions while typing
- [ ] Filter presets (favorites)

---

## Backward Compatibility

✓ Old scrapes still work
✓ Old API calls still work
✓ Existing websites still scrape
✓ No database migrations needed
✓ No breaking API changes

---

**Version:** 2.0
**Release Date:** March 5, 2026
**Status:** Stable & Tested
