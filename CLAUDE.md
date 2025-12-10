# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static marketing website for Unytics (unytics.io), hosted on GitHub Pages. The site showcases fractional Head of Data services, data applications portfolio, and open-source tools. It's a bilingual website supporting English and French.

## Site Structure

- **Root**: English version (`index.html`)
- **`/fr/`**: French version (`fr/index.html`)
- **`/static/`**: Shared CSS and JavaScript files (`style.css`, `script.js`)
- **`/assets/`**: All images, logos, and static assets
- **404 page**: `404.html` at root only (GitHub Pages limitation)
- **SEO files**: `sitemap.xml`, `sitemap_index.xml`, `robots.txt`, `CNAME`

## Key Architecture Patterns

### Language System

The site implements client-side language detection and switching:
- Browser language auto-detection on first visit
- localStorage persistence of language preference
- Manual language selection overrides auto-detection
- Language switcher buttons in navigation
- French URLs use `/fr/` prefix with proper hreflang tags

### Path Resolution

French pages (`fr/index.html`) use relative paths with `../` prefix:
- CSS: `href="../static/style.css"`
- JS: `src="../static/script.js"`
- Assets: `src="../assets/filename.ext"`
- Root pages use direct paths without `../` prefix:
- CSS: `href="static/style.css"`
- JS: `src="static/script.js"`
- Assets: `src="assets/filename.ext"` or `/assets/filename.ext`

### JavaScript Features (static/script.js)

Single shared JavaScript file handles:
- Language detection, switching, and preference storage
- Mobile menu toggle
- Accordion functionality for case study details
- Email copy-to-clipboard with toast notifications
- Dynamic content based on current page language

## Custom Slash Commands

The `.claude/commands/` directory contains workflow automation:

- **`/screenshot`**: Copies most recent screenshot from Windows Screenshots folder (`/mnt/c/Users/conta/Pictures/Screenshots/`) to `assets/`, with optional renaming
- **`/download`**: Copies most recent file from Windows Downloads folder (`/mnt/c/Users/conta/Downloads/`) to `assets/`, with optional renaming
- **`/generate-french`**: Translates English `index.html` to French with proper structure, paths, and metadata

## Content Update Workflow

**IMPORTANT**: When the user requests content updates to the website:
1. **Always update the English version first** (`index.html` at root)
2. **Then update the French version** (`fr/index.html`)
3. Both versions must be kept in sync with equivalent translations

This ensures both language versions stay consistent and up-to-date.

## Translation Guidelines

When creating or updating French translations:
- Translate "Fractional Head of Data" as "Responsable des Données Fractionné"
- Keep technical terms and product names in English where appropriate
- Update all meta tags: title, description, og:*, twitter:*, keywords
- Set `lang="fr"` on `<html>` tag
- Update canonical URL to `https://unytics.io/fr/`
- Set `og:locale` to `fr_FR`, `og:locale:alternate` to `en_US`
- Ensure French button has `active` class, English button does not
- **Never translate**: class names, IDs, data attributes, anchor links, external URLs

## SEO Considerations

- Both language versions have full hreflang implementation
- Sitemap includes both language versions with proper annotations
- Meta tags are fully localized per language
- Canonical URLs point to correct language version
- Social media metadata (Open Graph, Twitter Cards) is localized

## Asset Management

All images live in `/assets/`:
- Logos for open-source tools (SVG format)
- Portfolio screenshots (PNG format)
- Profile photos (JPG format)
- Favicon (ICO and SVG formats)

When adding new assets, use the `/screenshot` or `/download` commands to copy from Windows filesystem.

## Development Workflow

This is a static site with no build process:
- Direct HTML/CSS/JS editing
- Changes are immediately reflected when files are committed
- GitHub Pages automatically serves updates
- Test locally by opening HTML files in browser

## GitHub Pages Hosting

- Custom domain: `unytics.io` (configured via CNAME)
- Repository: `unytics.github.io`
- Branch: `master`
- Root directory serves English site
- Subdirectories serve alternate languages
- Single 404.html at root handles all not-found scenarios
