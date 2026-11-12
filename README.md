# Minseung Choi — Personal Homepage

Three views (Home, Experience, Languages) with English, Chinese, and Korean text. Built as a static site for GitHub Pages.

## Digital Humanities coursework

[李杜诗句互文](https://lanos7469.github.io/li-du/) compares similar lines in Li Bai and Du Fu's poetry.

## Preview locally

Open `index.html` in a browser, or run `python3 -m http.server 8765` and visit `http://localhost:8765/`.

## Update the site from Excel

`content/homepage_content.xlsx` is the editable content list. Each row identifies its page and exact location on the site. The English, Chinese, and Korean columns control the displayed text. The Asset / link column controls image paths and link targets.

1. Edit an existing row in the workbook and save it. To add or remove a project bullet, add or remove a row with `UI location` set to `Project bullet list` and a unique ID. Use the `Order` column to arrange the list.
2. Run `python3 scripts/export_content.py` to regenerate `content-data.js`.
3. Review the website, then commit and push both the workbook and generated data file.

For a completely new section or field, also add a matching `data-i18n` element in `index.html`. Image files live in `assets/`.

The CV was provided as source material. Its original PDF is not included because it contains information excluded from the public site.

## Publish with GitHub Pages

Open **Settings → Pages**, choose **Deploy from a branch**, select `main` and `/ (root)`, then save. The public address is `https://lanos7469.github.io/`.
