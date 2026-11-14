# Artwork attribution

The artist of every artwork on vicentegabrielflores.com is **Vicente Gabriel Flores**. Jinghan, Lawrence, and Leo are titles of works. They are not the artist's name.

Write the metadata below into every new artwork. Do not change the picture, the layout, or the visible caption to do it.

## Raster files

This command writes metadata only. It does not recompress the image. Replace `TITLE` with the art title, then run it on the JPG, WebP, and PNG.

```
exiftool -overwrite_original -charset utf8 \
  -EXIF:Artist="Vicente Gabriel Flores" \
  -XMP-dc:Creator="Vicente Gabriel Flores" \
  -XMP-tiff:Artist="Vicente Gabriel Flores" \
  -IPTC:By-line="Vicente Gabriel Flores" \
  -IPTC:CodedCharacterSet=UTF8 \
  -EXIF:Copyright="© 2026 Vicente Gabriel Flores. All rights reserved." \
  -XMP-dc:Rights="© 2026 Vicente Gabriel Flores. All rights reserved." \
  -IPTC:CopyrightNotice="© 2026 Vicente Gabriel Flores. All rights reserved." \
  -XMP-dc:Title="TITLE" \
  -IPTC:ObjectName="TITLE" \
  -EXIF:ImageDescription="TITLE" \
  -XMP-photoshop:Credit="vicentegabrielflores.com" \
  -IPTC:Credit="vicentegabrielflores.com" \
  -XMP-photoshop:Source="vicentegabrielflores.com" \
  -IPTC:Source="vicentegabrielflores.com" \
  -XMP-xmpRights:WebStatement="https://vicentegabrielflores.com/art.html" \
  path/to/artwork.jpg
```

WebP has no IPTC-IIM segment. On WebP, by-line, object name, credit, source, and copyright notice are stored in the XMP properties the IPTC standard uses for those fields: `XMP-dc:Creator`, `XMP-dc:Title`, `XMP-photoshop:Credit`, `XMP-photoshop:Source`, and `XMP-dc:Rights`. JPEG and PNG receive those XMP properties and the IPTC-IIM tags.

Before committing, decode the file and hash the pixels before and after. The hashes must match. One way to do that is Pillow's `Image.open(path).tobytes()` passed to SHA-256.

## SVG

Keep a `<title>` that names the work, and add this metadata. It is not visible text.

```xml
<title>TITLE</title>
<metadata>
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="https://vicentegabrielflores.com/art.html#anchor">
      <dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">TITLE</dc:title>
      <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">Vicente Gabriel Flores</dc:creator>
      <dc:rights xmlns:dc="http://purl.org/dc/elements/1.1/">© 2026 Vicente Gabriel Flores. All rights reserved.</dc:rights>
    </rdf:Description>
  </rdf:RDF>
</metadata>
```

## Page data

On `art.html`, and on every page that shows the work, add this JSON-LD. Use the date already shown on the page. Point `image` and `contentUrl` at the artwork file. Each `img` alt text gives the title and "by Vicente Gabriel Flores", for example: `Jinghan, gold-leaf painting by Vicente Gabriel Flores`.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "VisualArtwork",
      "name": "TITLE",
      "dateCreated": "YYYY-MM-DD",
      "url": "https://vicentegabrielflores.com/art.html#anchor",
      "image": "https://vicentegabrielflores.com/assets/art/FILE",
      "creator": {
        "@type": "Person",
        "name": "Vicente Gabriel Flores",
        "url": "https://vicentegabrielflores.com"
      },
      "copyrightHolder": {
        "@type": "Person",
        "name": "Vicente Gabriel Flores",
        "url": "https://vicentegabrielflores.com"
      },
      "creditText": "Vicente Gabriel Flores"
    },
    {
      "@type": "ImageObject",
      "name": "TITLE",
      "contentUrl": "https://vicentegabrielflores.com/assets/art/FILE",
      "creator": {
        "@type": "Person",
        "name": "Vicente Gabriel Flores",
        "url": "https://vicentegabrielflores.com"
      },
      "creditText": "Vicente Gabriel Flores",
      "copyrightNotice": "© 2026 Vicente Gabriel Flores. All rights reserved.",
      "license": "https://vicentegabrielflores.com/art.html",
      "acquireLicensePage": "https://vicentegabrielflores.com/art.html"
    }
  ]
}
```
