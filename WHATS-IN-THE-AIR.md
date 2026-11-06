# What's in the Air / Lo que hay en el aire

Daily checklist for the next edition. This is a flat static site. Prepare a pull request to `main` for review. Do not merge, deploy, or change GitHub Pages settings.

The author name on every new page is **Vicente Gabriel Flores**. Do not add any other name. Do not invent editions, facts, artworks, statistics, or memories. Keep the supplied English and Spanish together on one page, and keep the poem's line breaks. Do not add a newsletter form, analytics, or a post to X or email.

## Files for one new day

1. Copy `whats-in-the-air-2026-11-06.html` to `whats-in-the-air-YYYY-MM-DD.html`.
2. Prepend one card at the top of the list in `whats-in-the-air.html` (newest first).
3. Prepend one `<entry>` in `whats-in-the-air.xml` and set the feed `<updated>` to that edition.
4. Add the new page to `sitemap.xml`, and set `<lastmod>` on the new page, on `whats-in-the-air.html`, and on `whats-in-the-air.xml`.
5. Leave `robots.txt` as it is unless a real restriction is required. `Allow: /` already covers these URLs. Do not remove existing rules.
6. Home and Poems already link to the archive. A new edition does not need a new navigation item. Articles keeps its own row; do not add a link there unless it still fits on one line at 390px and 1280px.

## URL and metadata

- Page: `/whats-in-the-air-YYYY-MM-DD.html`
- Canonical: `https://vicentegabrielflores.com/whats-in-the-air-YYYY-MM-DD.html`
- Unique `<title>`: poem title, the date, and `What's in the Air`
- Unique meta description drawn from that edition. One clear sentence. No keyword list.
- `og:type` is `article`. `og:url` matches the canonical URL. Title, description, and the existing `og-image.jpg` are set. Same for the Twitter card.
- Keep `<meta name="twitter:site" content="@pasadornovel">` and `<meta name="twitter:creator" content="@pasadornovel">` on the archive and on every edition.
- `BlogPosting` JSON-LD: `author.name` is `Vicente Gabriel Flores`, `datePublished` and `dateModified` are the edition date (`YYYY-MM-DD`). `headline` is the poem title. `alternativeHeadline` is the Spanish poem title. `inLanguage` is `en` and `es`.
- Every author `Person` includes `"sameAs": ["https://x.com/pasadornovel"]`.
- Near the byline, and again at the end of the edition, keep the link `Follow on X / Sígueme en X: @pasadornovel` to `https://x.com/pasadornovel`. The archive keeps the same link under the introduction and at the end of the list. Copying the previous edition file keeps these lines; do not delete them when replacing the day's text.
- If a URL for that day's X Article was not supplied, do not add one. Do not post to X.
- Visible `<time datetime="YYYY-MM-DD">` matches that date. The manuscript's timezone is America/Chicago. Do not invent a clock time. In the Atom feed only, use `YYYY-MM-DDT00:00:00-06:00` (or `-05:00` while Chicago is on daylight time) as the calendar-day boundary.
- English prose and poem live in `<section lang="en">`. Spanish lives in `<section lang="es">`.
- On the archive page, add the same edition at the start of the `Blog` JSON-LD `blogPost` array.
- Archive card: date, both poem titles, the author name, and the edition's own opening sentences. Link the card to the edition URL.

## Feed

`whats-in-the-air.xml` is an Atom feed of real editions only, newest first. Each entry's `<id>` and `<link>` are the edition's canonical URL. Put both languages in `<content type="html">`. There is one feed. Do not keep a second copy.

## Foreground color

Copying the previous edition keeps its color tokens. Leave them. Body copy, both languages of the poem, navigation, links, captions, and the footer use a brighter cream and antique gold on the black page, measured to WCAG AA. Do not return that text to the older dim brown or dim gold, and do not change the type size to make it readable. Do not edit book-cover images or `og-image.jpg`.

## Checks before the pull request

- The poem lines match the supplied text, including breaks.
- The election and news sentences stay as supplied, with their source attribution left in the body.
- Internal links resolve: archive, edition, home, poems, articles, feed.
- The new URL is in `sitemap.xml`.
- `robots` meta on the new page is `index, follow`, matching the rest of the site.
- No analytics snippet, no newsletter field, no claim about search ranking.
- Desktop and mobile: the navigation opens, the edition is readable, the follow link wraps inside the screen, and the poem lines wrap without a horizontal scrollbar.

Open the pull request for review. Merging is what publishes the site.
