# Browser Mode - JavaScript Support

## What is Browser Mode?

Some websites (like Bar Convention London) load their exhibitor listings using JavaScript after the page loads. Regular scraping can't see this dynamic content.

**Browser Mode** runs a real headless browser that:
1. Loads the full page
2. Waits for JavaScript to execute
3. Extracts the rendered content
4. Then applies our normal extraction methods

## When to Use Browser Mode

✓ **Use Browser Mode for:**
- Sites with "no results found" or only navigation links
- Modern React/Vue/Angular sites
- Dynamic product listings
- Any site where data appears after page load

✗ **Don't use for:**
- Sites with static HTML or JSON-LD (slower for no reason)
- Simple HTML directory sites
- When you see actual company names/links already

## Speed Comparison

| Mode | Speed | Works With |
|------|-------|-----------|
| **Fast (default)** | 2-3 sec/page | Static HTML, JSON-LD |
| **Browser** | 15-30 sec/page | JavaScript-rendered content |

## How to Use in Web App

1. Open http://localhost:5001
2. **Check the box:** "🌐 Use Browser (slower but works with JavaScript sites)"
3. Paste your URL
4. Click **Scrape**

That's it! The app will use a headless Chrome browser instead of just fetching HTML.

## Example: Bar Convention London

**Without Browser:**
- Gets navigation links only ❌

**With Browser:**
- Waits for JavaScript to render exhibitors
- Extracts real company data ✓

## How It Works Under the Hood

```
1. Playwright launches headless Chromium
2. Navigates to page (with 30s timeout)
3. Waits for network to settle ("networkidle")
4. Gets fully rendered HTML
5. Applies JSON-LD or HTML extraction
6. Returns results
```

## Troubleshooting

**"Browser mode is very slow"**
- Yes, it's normal (15-30s per page)
- Use for JS-heavy sites only
- Use "Fast mode" for normal sites

**"Still no results with browser mode"**
- Website might not have structured exhibitor data
- Data could be in an inaccessible database
- Try viewing the site manually to see what's shown

**"Browser won't start"**
- Make sure Playwright and Chromium are installed:
  ```bash
  pip install playwright
  playwright install chromium
  ```

---

**Pro tip:** Try the site in Fast mode first. If you get only navigation links, switch to Browser mode.
