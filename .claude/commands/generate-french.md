---
description: Generate French translation of index.html with proper structure and paths
---

Translate the English website (index.html) to French:

1. Read /home/pmarcombes/unytics.github.io/index.html
2. Create /home/pmarcombes/unytics.github.io/fr/index.html with:
   - Translate ALL visible text (headings, paragraphs, buttons, nav, etc.)
   - Translate meta tags: title, description, og:*, twitter:*, keywords
   - Set lang="fr" on <html>
   - Update canonical to: https://unytics.io/fr/
   - Update og:url to: https://unytics.io/fr/
   - Set og:locale to fr_FR, og:locale:alternate to en_US
   - Add hreflang tags (en, fr, x-default)
   - Update ALL asset paths to use ../ prefix:
     * CSS: href="../static/style.css"
     * JS: src="../static/script.js"
     * Images: src="../assets/..."
     * Favicon: href="../assets/favicon.ico"
   - Set French button to active class, English button to inactive
   - Keep anchor links, class names, IDs, data attributes unchanged
   - Keep external links unchanged (calendar, LinkedIn, etc.)

Translation style: Professional, business-appropriate French. Translate:
- "Fractional Head of Data" as "Head of Data à temps partiel".
- "Data Apps" as "Data Apps".
- "Framework" as "Framework".

Keep technical terms and names in English where appropriate.

Note: Do NOT create /fr/404.html - GitHub Pages only supports one 404.html at root level.
