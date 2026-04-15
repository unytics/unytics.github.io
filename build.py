# /// script
# dependencies = ["markdown"]
# ///
"""Build script for unytics.io — generates homepage + blog HTML from templates and markdown."""

import glob
import http.server
import os
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
SITE_URL = "https://unytics.io"
BOOKING_URL = "https://outlook.office.com/bookwithme/user/af9126dab77a4875999901a41b929b48@audioptic.fr/meetingtype/ThLax7Qcxk24NOanCTiBWg2?anonymous&ismsaljsauthenabled&ep=mlink"

I18N = {
    "en": {
        "lang": "en",
        "nav_pitfalls": "Pitfalls",
        "nav_solutions": "Solutions",
        "nav_case_studies": "Case Studies",
        "nav_offers": "Offers",
        "nav_cta": "Free Data Call",
        "skip_link_text": "Skip to main content",
        "copyright_text": "All rights reserved.",
        "toast_text": "Email copied to clipboard!",
        "home_url": "/",
        "blog_index_url": "/blog/",
        "og_locale": "en_US",
        "og_locale_alt": "fr_FR",
        "en_active": "active",
        "fr_active": "",
    },
    "fr": {
        "lang": "fr",
        "nav_pitfalls": "Pi\u00e8ges",
        "nav_solutions": "Solutions",
        "nav_case_studies": "Cas Clients",
        "nav_offers": "Offres",
        "nav_cta": "Appel Data Gratuit",
        "skip_link_text": "Aller au contenu principal",
        "copyright_text": "Tous droits r\u00e9serv\u00e9s.",
        "toast_text": "Email copi\u00e9 dans le presse-papier !",
        "home_url": "/fr/",
        "blog_index_url": "/blog/fr/",
        "og_locale": "fr_FR",
        "og_locale_alt": "en_US",
        "en_active": "",
        "fr_active": "active",
    },
}

HOMEPAGE_EN_HEAD_EXTRA = """\
<meta name="keywords" content="fractional head of data, fractional data leadership, data consulting, data apps, data team scaling, BigQuery, fraud prevention, self-service data platform, data leadership, scale-up, data engineering, serverless architecture">

    <!-- Structured Data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Unytics",
        "description": "Fractional Head of Data for scale-ups. Strategic leadership and execution: Revenue-generating Data Apps, team scaling, self-service platforms. Ex-Head of Data at Nickel (0 to 40 people, 800+ users).",
        "url": "https://unytics.io",
        "founder": {
            "@type": "Person",
            "name": "Paul Marcombes",
            "jobTitle": "Fractional Head of Data",
            "sameAs": "https://linkedin.com/in/paul-marcombes/"
        },
        "areaServed": "Worldwide",
        "serviceType": ["Fractional Head of Data", "Data Apps", "Data Team Scaling", "Serverless Data Architecture", "Fraud Prevention", "Self-Service Data Platform"]
    }
    </script>"""

HOMEPAGE_FR_HEAD_EXTRA = """\
<meta name="keywords" content="head of data \u00e0 temps partiel, head of data fractionn\u00e9, conseil data, data apps, croissance \u00e9quipe data, BigQuery, pr\u00e9vention fraude, plateforme data self-service, leadership data, scale-up, ing\u00e9nierie des donn\u00e9es, architecture serverless">

    <!-- Structured Data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Unytics",
        "description": "Head of Data \u00e0 temps partiel pour scale-ups. Leadership strat\u00e9gique et ex\u00e9cution : Data Apps g\u00e9n\u00e9ratrices de revenus, croissance d'\u00e9quipe, plateformes self-service. Ex-Head of Data Nickel (0 \u00e0 40 personnes, 800+ utilisateurs).",
        "url": "https://unytics.io/fr/",
        "founder": {
            "@type": "Person",
            "name": "Paul Marcombes",
            "jobTitle": "Head of Data \u00e0 temps partiel",
            "sameAs": "https://linkedin.com/in/paul-marcombes/"
        },
        "areaServed": "Worldwide",
        "serviceType": ["Head of Data \u00e0 temps partiel", "Data Apps", "Croissance \u00e9quipe data", "Architecture data serverless", "Pr\u00e9vention fraude", "Plateforme data self-service"]
    }
    </script>"""

HOMEPAGE_CONFIG = {
    "en": {
        "title": "Unytics - Fractional Head of Data | Turn Your Data Team Into a Revenue Driver",
        "description": "Fractional Head of Data for scale-ups. Strategic leadership and execution: Revenue-generating Data Apps (\u20ac2M+ fraud prevention), team growth from 0 to 40 people, 800+ self-service users. By Paul Marcombes, ex-Head of Data at Nickel.",
        "canonical_url": f"{SITE_URL}/",
        "og_type": "website",
        "hreflang_en": f"{SITE_URL}/",
        "hreflang_fr": f"{SITE_URL}/fr/",
        "content_file": "homepage/en.html",
        "output_file": "index.html",
        "head_extra": HOMEPAGE_EN_HEAD_EXTRA,
    },
    "fr": {
        "title": "Unytics - Head of Data \u00e0 temps partiel | Transformez votre \u00e9quipe data en g\u00e9n\u00e9rateur de revenus",
        "description": "Head of Data \u00e0 temps partiel pour scale-ups. Leadership strat\u00e9gique et ex\u00e9cution : Data Apps g\u00e9n\u00e9ratrices de revenus (\u20ac2M+ pr\u00e9vention fraude), croissance d'\u00e9quipe de 0 \u00e0 40 personnes, 800+ utilisateurs autonomes. Par Paul Marcombes, ex-Head of Data Nickel.",
        "canonical_url": f"{SITE_URL}/fr/",
        "og_type": "website",
        "hreflang_en": f"{SITE_URL}/",
        "hreflang_fr": f"{SITE_URL}/fr/",
        "content_file": "homepage/fr.html",
        "output_file": "fr/index.html",
        "head_extra": HOMEPAGE_FR_HEAD_EXTRA,
    },
}


def slugify(filename: str) -> str:
    """Convert a markdown filename to a URL-safe slug."""
    name = Path(filename).stem
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9\-]", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse optional YAML frontmatter from markdown text.

    Returns (metadata_dict, body_text).
    """
    metadata = {}
    body = text

    if text.startswith("---\n") or text.startswith("---\r\n"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            frontmatter_lines = parts[1].strip().splitlines()
            for line in frontmatter_lines:
                if ":" in line:
                    key, _, value = line.partition(":")
                    value = value.strip()
                    # Strip surrounding quotes
                    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                        value = value[1:-1]
                    metadata[key.strip()] = value
            body = parts[2].strip()

    # Fallback: extract title from first H1
    if "title" not in metadata:
        h1_match = re.match(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1_match:
            metadata["title"] = h1_match.group(1).strip()

    # Fallback: extract description from first paragraph
    if "description" not in metadata:
        lines = body.split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                metadata["description"] = stripped[:160]
                break

    return metadata, body


def render_template(template: str, context: dict) -> str:
    """Replace {{key}} placeholders in template with context values."""
    result = template
    for key, value in context.items():
        result = result.replace("{{" + key + "}}", str(value))
    # Clean up trailing spaces in class attributes (from empty placeholders)
    result = re.sub(r'class="([^"]*?)\s+"', r'class="\1"', result)
    return result


def read_template() -> str:
    """Read the layout template."""
    return (ROOT / "templates" / "layout.html").read_text(encoding="utf-8")


def build_homepage(lang: str, template: str) -> None:
    """Build a homepage HTML file from the template and content fragment."""
    config = HOMEPAGE_CONFIG[lang]
    i18n = I18N[lang]

    content = (ROOT / config["content_file"]).read_text(encoding="utf-8")

    context = {**i18n, **config, "content": content}
    html = render_template(template, context)

    output_path = ROOT / config["output_file"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"  {config['output_file']}")


def build_post(md_path: Path, lang: str, template: str) -> dict:
    """Build a single blog post HTML page. Returns post metadata for the index."""
    text = md_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(text)

    slug = metadata.get("slug") or slugify(md_path.name)
    title = metadata.get("title", slug)
    description = metadata.get("description", "")
    date = metadata.get("date", "")

    i18n = I18N[lang]

    # Convert markdown to HTML
    html_body = markdown.markdown(body, extensions=["fenced_code", "tables"])

    # Remove the H1 from the rendered body since we display it in the header
    html_body = re.sub(r"<h1>.*?</h1>\s*", "", html_body, count=1)

    # Build article content
    back_label = "&larr; Blog" if lang == "en" else "&larr; Blog"
    date_display = date
    article_html = f"""
        <article class="blog-post">
            <div class="container">
                <a href="{i18n['blog_index_url']}" class="blog-back-link">{back_label}</a>
                <div class="blog-post-header">
                    {"<p class='blog-post-date'>" + date_display + "</p>" if date_display else ""}
                    <h1>{title}</h1>
                </div>
                <div class="blog-post-content">
                    {html_body}
                </div>
            </div>
        </article>"""

    # Build hreflang URLs
    if lang == "en":
        hreflang_en = f"{SITE_URL}/blog/{slug}/"
        hreflang_fr = f"{SITE_URL}/blog/fr/{slug}/"
        canonical_url = hreflang_en
    else:
        hreflang_en = f"{SITE_URL}/blog/{slug}/"
        hreflang_fr = f"{SITE_URL}/blog/fr/{slug}/"
        canonical_url = hreflang_fr

    context = {
        **i18n,
        "title": f"{title} | Unytics Blog",
        "description": description,
        "canonical_url": canonical_url,
        "og_type": "article",
        "hreflang_en": hreflang_en,
        "hreflang_fr": hreflang_fr,
        "content": article_html,
        "head_extra": "",
    }

    html = render_template(template, context)

    # Write output
    if lang == "en":
        output_path = ROOT / "blog" / slug / "index.html"
    else:
        output_path = ROOT / "blog" / "fr" / slug / "index.html"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"  {output_path.relative_to(ROOT)}")

    return {
        "title": title,
        "description": description,
        "date": date,
        "slug": slug,
        "md_filename": md_path.name,
    }


def build_blog_index(posts: list[dict], lang: str, template: str) -> None:
    """Build the blog listing page."""
    i18n = I18N[lang]

    # Sort by date descending
    sorted_posts = sorted(posts, key=lambda p: p.get("date", ""), reverse=True)

    # Generate cards HTML
    cards = []
    for post in sorted_posts:
        if lang == "en":
            post_url = f"/blog/{post['slug']}/"
        else:
            post_url = f"/blog/fr/{post['slug']}/"

        date_html = f'<p class="blog-card-date">{post["date"]}</p>' if post.get("date") else ""
        desc_html = f"<p>{post['description']}</p>" if post.get("description") else ""
        cards.append(
            f"""                <a href="{post_url}" class="blog-card">
                    {date_html}
                    <h2>{post['title']}</h2>
                    {desc_html}
                </a>"""
        )

    cards_html = "\n".join(cards)

    content = f"""
        <section class="blog-listing">
            <div class="container">
                <h1>Blog</h1>
                <div class="blog-cards">
{cards_html}
                </div>
            </div>
        </section>"""

    if lang == "en":
        canonical_url = f"{SITE_URL}/blog/"
        hreflang_en = f"{SITE_URL}/blog/"
        hreflang_fr = f"{SITE_URL}/blog/fr/"
    else:
        canonical_url = f"{SITE_URL}/blog/fr/"
        hreflang_en = f"{SITE_URL}/blog/"
        hreflang_fr = f"{SITE_URL}/blog/fr/"

    blog_description = {
        "en": "Insights on data leadership, engineering, and AI by Paul Marcombes.",
        "fr": "R\u00e9flexions sur le leadership data, l'ing\u00e9nierie et l'IA par Paul Marcombes.",
    }

    context = {
        **i18n,
        "title": "Blog | Unytics",
        "description": blog_description[lang],
        "canonical_url": canonical_url,
        "og_type": "website",
        "hreflang_en": hreflang_en,
        "hreflang_fr": hreflang_fr,
        "content": content,
        "head_extra": "",
    }

    html = render_template(template, context)

    if lang == "en":
        output_path = ROOT / "blog" / "index.html"
    else:
        output_path = ROOT / "blog" / "fr" / "index.html"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"  {output_path.relative_to(ROOT)}")


def build_all() -> None:
    """Build all pages: homepages + blog."""
    template = read_template()

    # Build homepages
    print("Building homepages...")
    for lang in ("en", "fr"):
        build_homepage(lang, template)

    # Discover English blog posts
    en_md_files = sorted(ROOT.glob("blog/*.md"))
    if not en_md_files:
        print("No blog posts found in blog/*.md")
        return

    # Build blog posts
    print("Building blog posts...")
    en_posts = []
    fr_posts = []

    for md_path in en_md_files:
        # Build English version
        post_meta = build_post(md_path, "en", template)
        en_posts.append(post_meta)

        # Build French version (required)
        fr_md_path = ROOT / "blog" / "fr" / md_path.name
        if not fr_md_path.exists():
            print(f"  ERROR: Missing French translation: {fr_md_path.relative_to(ROOT)}")
            sys.exit(1)

        fr_meta = build_post(fr_md_path, "fr", template)
        fr_posts.append(fr_meta)

    # Build blog indexes
    print("Building blog indexes...")
    build_blog_index(en_posts, "en", template)
    build_blog_index(fr_posts, "fr", template)

    print("Done!")


def serve(port: int = 8000) -> None:
    """Start a local HTTP server."""
    import functools

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    with http.server.HTTPServer(("", port), handler) as httpd:
        print(f"\nServing at http://localhost:{port}")
        print(f"  Homepage EN: http://localhost:{port}/")
        print(f"  Homepage FR: http://localhost:{port}/fr/")
        print(f"  Blog EN:     http://localhost:{port}/blog/")
        print(f"  Blog FR:     http://localhost:{port}/blog/fr/")
        print("\nPress Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


def main() -> None:
    args = sys.argv[1:]

    if not args:
        build_all()
    elif args[0] == "serve":
        build_all()
        port = 8000
        if "--port" in args:
            port_idx = args.index("--port") + 1
            if port_idx < len(args):
                port = int(args[port_idx])
        serve(port)
    else:
        print(f"Usage: uv run build.py [serve [--port PORT]]")
        sys.exit(1)


if __name__ == "__main__":
    main()
