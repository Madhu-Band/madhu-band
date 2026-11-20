# Madhu site tools

The site is plain static HTML. The pages are generated from the files in `content/`
so a change in one place updates every page.

## Update the site
1. Edit `content/site.json` (bio, members, videos, email, social links) or `content/shows.json`.
2. Run `python3 tools/build.py` from the repo root.
3. Commit the changed files. GitHub Pages republishes in about a minute.

## Add a show
Add an entry to `content/shows.json`. Dates must be `YYYY-MM-DD`; `time`, `city`, `notes`
and `tickets` (must start with https://) are optional:

    {
      "shows": [
        {"date": "2026-12-12", "time": "8:00 PM", "venue": "Nameless Saloon",
         "city": "Leander, TX", "tickets": "https://example.com/tix", "notes": "Free show"}
      ]
    }

Shows in the past are hidden automatically in the visitor's browser.

## Notes
- Leave `email` empty until the address exists; the Contact page then says details are coming soon.
- Keep the `CNAME` file in the repo root; GitHub Pages uses it for madhu.band.
