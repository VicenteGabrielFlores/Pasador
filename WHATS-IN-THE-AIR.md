# What's in the Air / Lo que hay en el aire

Daily checklist for the next edition. This is a flat static site. Prepare a pull request to `main` for review. Do not merge, deploy, or change GitHub Pages settings.

The author name on every new page is **Vicente Gabriel Flores**. Do not add any other name. Do not invent editions, facts, artworks, statistics, or memories. Keep the supplied English and Spanish together on one page, and keep the poem's line breaks. Do not add a newsletter form, analytics, or a post to X or email.

## Files for one new day

1. Copy `whats-in-the-air-2026-11-06.html` to `whats-in-the-air-YYYY-MM-DD.html`.
2. Prepend one card at the top of the list in `whats-in-the-air.html` (newest first).
2b. In index.html, replace both `/whats-in-the-air-YYYY-MM-DD.html` hrefs in the Air tile and the EN/ES titles with the new edition; set `/` lastmod. `tests/home_air_link.py` fails if the homepage does not link the newest edition file in the repo.
3. Prepend one `<entry>` in `whats-in-the-air.xml` and set the feed `<updated>` to that edition.
4. Add the new page to `sitemap.xml` and leave it there. Do not add `whats-in-the-air.xml` to `sitemap.xml`. Rebuild `news-sitemap.xml` so it lists only editions dated within the last 2 days (48 hours): each new edition replaces older entries. The news sitemap file stays in the repo; do not list it in `sitemap-index.xml` or `robots.txt`. Set `<lastmod>` on the new page, on `whats-in-the-air.html`, and on the `sitemap.xml` entry in `sitemap-index.xml`. Set `<lastmod>` on `/` when step 2b changes the homepage.
5. Leave `robots.txt` as it is unless a real restriction is required. `Allow: /` already covers these URLs. Keep the `Sitemap` lines for `sitemap.xml` and `sitemap-index.xml`. Do not add `news-sitemap.xml` back to `robots.txt`. Do not remove the other rules.
6. Home and Poems already link to the archive. A new edition does not need its own navigation item. The shared menu already links the archive. Leave that menu in place, including Author, Art, La Toma, Articles, Davos, Crónicas, and Familia.

## URL and metadata

- Page: `/whats-in-the-air-YYYY-MM-DD.html`
- Canonical: `https://vicentegabrielflores.com/whats-in-the-air-YYYY-MM-DD.html`
- Unique `<title>`: poem title, the date, and `What's in the Air`
- Unique meta description drawn from that edition. One clear sentence. No keyword list.
- `og:type` is `article`. `og:url` matches the canonical URL. `og:title` and `twitter:title` are exactly `What's in the Air`, written in the tag as `What&#39;s in the Air` so a share card does not stop at the apostrophe. The document `<title>` stays unique. Description and the existing `og-image.jpg` are set. Same image for the Twitter card.
- Keep `<meta name="twitter:site" content="@pasadornovel">` and `<meta name="twitter:creator" content="@pasadornovel">` on the archive and on every edition.
- `BlogPosting` JSON-LD, not `NewsArticle`. `genre` is `Literary commentary`. `headline` is the English poem title. `alternativeHeadline` is the Spanish poem title. `datePublished` and `dateModified` are the edition date (`YYYY-MM-DD`); if `dateModified` is missing, set it to that same date. Do not add a clock time. `inLanguage` is `en` and `es`. `author` is only `{"@id":"https://vicentegabrielflores.com/#author"}`. `isPartOf` keeps `{"@id":"https://vicentegabrielflores.com/whats-in-the-air.html#series"}`. `hasPart` is a `CreativeWork` with `genre` `Poetry` and `name` set to the English title, a slash, and the Spanish title. Keep `image` and `mainEntityOfPage`. Do not add a publisher Organization.
- The archive page stays `@type` `Blog`. Each item in its `blogPost` array is a `BlogPosting` with the same genre, dates, author `@id`, and poem `hasPart`.
- Do not repeat the full Person on an edition or on the archive. The one Person, `@id` `https://vicentegabrielflores.com/#author`, is on `author.html` and the homepage. Its `sameAs` includes `https://x.com/pasadornovel` and `https://www.amazon.com/author/vicentegabrielflores`. Do not give the author a second `@id`.
- Near the byline, and again at the end of the edition, keep the link `Follow on X / Sígueme en X: @pasadornovel` to `https://x.com/pasadornovel`. The archive keeps the same link under the introduction and at the end of the list. Copying the previous edition file keeps these lines; do not delete them when replacing the day's text.
- The visible author name, on the edition byline and on the archive card, is a link to `https://vicentegabrielflores.com/author.html`. On the archive, the author link stays outside the edition link. A card cannot contain a second link inside the first.
- The archive footer and every edition footer keep `mailto:cronista@vicentegabrielflores.com` beside `@pasadornovel`. That address is already public on the homepage for rights, representation, and press inquiries. Do not add a phone number, a postal address, or a new editorial-policy paragraph.
- Do not add an outbound link inside a synopsis sentence or a poem. If the day's supplied sources note gives the exact URLs, add them only in a compact sources list after the signature. Do not rewrite the poem or the synopsis to sound like a news report.
- After both languages and the written byline, place `vicente-gabriel-flores-signature.png` once, across the text column, with space above it. Alt text: `Handwritten signature of Vicente Gabriel Flores`. Do not repeat it, do not set it beside a stanza, and do not use the portrait or a letter as the signature.
- If a URL for that day's X Article was not supplied, do not add one. Do not post to X.
- Visible `<time datetime="YYYY-MM-DD">` matches that date. The manuscript's timezone is America/Chicago. Do not invent a clock time. In the Atom feed only, use `YYYY-MM-DDT00:00:00-06:00` (or `-05:00` while Chicago is on daylight time) as the calendar-day boundary.
- English prose and poem live in `<section lang="en">`. Spanish lives in `<section lang="es">`.
- On the archive page, add the same edition at the start of the `Blog` JSON-LD `blogPost` array, as a `BlogPosting`.
- Archive card: date, both poem titles, the linked author name, and the edition's own opening sentences. The poem titles and “Read this edition” link to the edition URL. The author name links to `https://vicentegabrielflores.com/author.html`.

## Feed

`whats-in-the-air.xml` is an Atom feed of real editions only, newest first. Each entry's `<id>` and `<link>` are the edition's canonical URL. Put both languages in `<content type="html">`. There is one feed. Do not keep a second copy. Do not list this feed in `sitemap.xml`. Every public page keeps `<link rel="alternate" type="application/atom+xml" title="What's in the Air" href="https://vicentegabrielflores.com/whats-in-the-air.xml">` in `<head>`.

## News sitemap

`news-sitemap.xml` uses the `news` namespace (`http://www.google.com/schemas/sitemap-news/0.9`). `news:name` is `Vicente Gabriel Flores`. `news:publication_date` is the edition date, with no clock time. `news:title` is the English poem title (`headline`). Newest first.

Google News reads only articles from the last 48 hours. Keep an edition here only while its date is today or yesterday in America/Chicago, the date-only form of that window. Each new edition replaces the file's older entries. Do not leave an edition once its date is more than two days old. Older editions stay in `sitemap.xml`.

`news:language` is `en`. Each edition is one bilingual page whose document language is English, and the news sitemap allows a single language code on a URL, so `es` is not a second tag beside it. A future edition whose page language is Spanish (`<html lang="es">`, with no English section) uses `es`.

`news-sitemap.xml` stays in the repository. `robots.txt` does not name it, and `sitemap-index.xml` does not list it. Do not add it back to either file.

## Foreground color

Copying the previous edition keeps its color tokens. Leave them. Body copy, both languages of the poem, navigation, links, captions, and the footer use a brighter cream and antique gold on the black page, measured to WCAG AA. Do not return that text to the older dim brown or dim gold, and do not change the type size to make it readable. Do not edit book-cover images or `og-image.jpg`.

## Checks before the pull request

- The poem lines match the supplied text, including breaks. *The Brave Bulls* stays italic when the supplied text italicizes it.
- The election and news sentences stay as supplied, with their source attribution left in the body.
- Internal links resolve: archive, edition, home, poems, articles, feed.
- The new URL is in `sitemap.xml`. It is in `news-sitemap.xml` only while its date is today or yesterday in America/Chicago.
- `robots` meta on the new page is `index, follow, max-image-preview:large`, matching the rest of the site. Do not add `noindex`.
- No analytics snippet, no newsletter field, no claim about search ranking.
- Desktop and mobile: the navigation opens, the edition is readable, the follow link wraps inside the screen, and the poem lines wrap without a horizontal scrollbar.

Open the pull request for review. Merging is what publishes the site.

## Artwork

If an edition shows an artwork, credit it as described in [ART-ATTRIBUTION.md](ART-ATTRIBUTION.md). The artist is Vicente Gabriel Flores. Jinghan, Lawrence, and Leo are titles of works.
