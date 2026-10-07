import re
import os
import html

md_path = "/Users/nguyenngocphuc/.gemini/antigravity/scratch/book_company_os/02_drafts/FULL_MANUSCRIPT_COMPANY_OS.md"
output_html_path = "/Users/nguyenngocphuc/.gemini/antigravity/scratch/book_company_os/index.html"

with open(md_path, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Clean artifacts
raw_md = raw_md.replace("$\\rightarrow$", "→").replace("$\\Rightarrow$", "⇒").replace("$", "")

chapters = []
for line in raw_md.split('\n'):
    if line.startswith('# '):
        title = line[2:].strip()
        slug = re.sub(r'[^a-zA-Z0-9\u00C0-\u1EF9]+', '-', title).strip('-').lower()
        chapters.append((title, slug))

toc_options = "\n".join([f'<option value="#{slug}">{title}</option>' for title, slug in chapters])

def parse_md_to_html(md_text):
    out = []
    lines = md_text.split('\n')
    in_code = False
    in_ul = False
    in_ol = False
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        
        # Code fence
        if stripped.startswith('```'):
            if in_code:
                out.append('</code></pre>')
                in_code = False
            else:
                if in_ul: out.append('</ul>'); in_ul = False
                if in_ol: out.append('</ol>'); in_ol = False
                out.append('<pre><code>')
                in_code = True
            continue
            
        if in_code:
            out.append(html.escape(line))
            continue
            
        # Divider / HR
        if stripped == '---':
            if in_ul: out.append('</ul>'); in_ul = False
            if in_ol: out.append('</ol>'); in_ol = False
            if in_table: out.append('</table>'); in_table = False
            out.append('<hr>')
            continue
            
        # Headings
        if stripped.startswith('# '):
            if in_ul: out.append('</ul>'); in_ul = False
            if in_ol: out.append('</ol>'); in_ol = False
            title = stripped[2:].strip()
            slug = re.sub(r'[^a-zA-Z0-9\u00C0-\u1EF9]+', '-', title).strip('-').lower()
            out.append(f'<h1 id="{slug}" class="chapter-heading">{title}</h1>')
            continue
        elif stripped.startswith('## '):
            if in_ul: out.append('</ul>'); in_ul = False
            if in_ol: out.append('</ol>'); in_ol = False
            title = stripped[3:].strip()
            out.append(f'<h2 class="section-heading">{title}</h2>')
            continue
        elif stripped.startswith('### '):
            if in_ul: out.append('</ul>'); in_ul = False
            if in_ol: out.append('</ol>'); in_ol = False
            title = stripped[4:].strip()
            out.append(f'<h3 class="subsection-heading">{title}</h3>')
            continue
            
        # Unordered list
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_ul:
                if in_ol: out.append('</ol>'); in_ol = False
                out.append('<ul>')
                in_ul = True
            item = stripped[2:].strip()
            item = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item)
            item = re.sub(r'\*(.*?)\*', r'<em>\1</em>', item)
            item = re.sub(r'`(.*?)`', r'<code>\1</code>', item)
            out.append(f'<li>{item}</li>')
            continue
        else:
            if in_ul:
                out.append('</ul>')
                in_ul = False
                
        # Ordered list
        m_ol = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if m_ol:
            if not in_ol:
                out.append('<ol>')
                in_ol = True
            item = m_ol.group(2).strip()
            item = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item)
            item = re.sub(r'\*(.*?)\*', r'<em>\1</em>', item)
            item = re.sub(r'`(.*?)`', r'<code>\1</code>', item)
            out.append(f'<li>{item}</li>')
            continue
        else:
            if in_ol:
                out.append('</ol>')
                in_ol = False
                
        # Table
        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped[1:-1].split('|')]
            if all(set(c).issubset({'-', ':', ' '}) for c in cells):
                continue # header separator
            if not in_table:
                out.append('<table><thead><tr>')
                for c in cells:
                    c = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', c)
                    out.append(f'<th>{c}</th>')
                out.append('</tr></thead><tbody>')
                in_table = True
            else:
                out.append('<tr>')
                for c in cells:
                    c = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', c)
                    c = re.sub(r'\*(.*?)\*', r'<em>\1</em>', c)
                    c = re.sub(r'`(.*?)`', r'<code>\1</code>', c)
                    out.append(f'<td>{c}</td>')
                out.append('</tr>')
            continue
        else:
            if in_table:
                out.append('</tbody></table>')
                in_table = False

        # Blockquote
        if stripped.startswith('> '):
            text = stripped[2:].strip()
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
            text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
            out.append(f'<blockquote><p>{text}</p></blockquote>')
            continue

        # Blank line
        if not stripped:
            continue
            
        # Regular paragraph
        p = stripped
        p = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p)
        p = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p)
        p = re.sub(r'`(.*?)`', r'<code>\1</code>', p)
        out.append(f'<p>{p}</p>')
        
    if in_ul: out.append('</ul>')
    if in_ol: out.append('</ol>')
    if in_table: out.append('</tbody></table>')
    if in_code: out.append('</code></pre>')
    
    return '\n'.join(out)

html_body = parse_md_to_html(raw_md)

full_html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>COMPANY OS - Nguyễn Ngọc Phúc</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
    --bg-page: #f8fafc;
    --bg-surface: #ffffff;
    --text-primary: #0f172a;
    --text-secondary: #334155;
    --text-muted: #64748b;
    --border-color: #e2e8f0;
    --accent: #0284c7;
    --accent-hover: #0369a1;
    --accent-light: #f0f9ff;
    --code-bg: #f1f5f9;
    --quote-border: #0284c7;
    --quote-bg: #f8fafc;
    --font-heading: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-serif: 'Merriweather', Georgia, serif;
    --font-mono: 'JetBrains Mono', Menlo, monospace;
    --max-width: 760px;
}}

@media (prefers-color-scheme: dark) {{
    :root {{
        --bg-page: #0b1120;
        --bg-surface: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: #334155;
        --accent: #38bdf8;
        --accent-hover: #7dd3fc;
        --accent-light: #082f49;
        --code-bg: #111827;
        --quote-border: #38bdf8;
        --quote-bg: #1e293b;
    }}
}}

body.dark-theme {{
    --bg-page: #0b1120 !important;
    --bg-surface: #1e293b !important;
    --text-primary: #f8fafc !important;
    --text-secondary: #cbd5e1 !important;
    --text-muted: #94a3b8 !important;
    --border-color: #334155 !important;
    --accent: #38bdf8 !important;
    --accent-hover: #7dd3fc !important;
    --accent-light: #082f49 !important;
    --code-bg: #111827 !important;
    --quote-border: #38bdf8 !important;
    --quote-bg: #1e293b !important;
}}

body.light-theme {{
    --bg-page: #f8fafc !important;
    --bg-surface: #ffffff !important;
    --text-primary: #0f172a !important;
    --text-secondary: #334155 !important;
    --text-muted: #64748b !important;
    --border-color: #e2e8f0 !important;
    --accent: #0284c7 !important;
    --accent-hover: #0369a1 !important;
    --accent-light: #f0f9ff !important;
    --code-bg: #f1f5f9 !important;
    --quote-border: #0284c7 !important;
    --quote-bg: #f8fafc !important;
}}

* {{
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    margin: 0;
    padding: 0;
    background-color: var(--bg-page);
    color: var(--text-primary);
    font-family: var(--font-serif);
    font-size: 17px;
    line-height: 1.85;
    transition: background 0.2s ease, color 0.2s ease;
}}

/* TOP STICKY BAR */
.top-bar {{
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    background-color: rgba(248, 250, 252, 0.9);
    border-bottom: 1px solid var(--border-color);
    padding: 10px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
}}

body.dark-theme .top-bar {{
    background-color: rgba(11, 17, 32, 0.9) !important;
}}

@media (prefers-color-scheme: dark) {{
    body:not(.light-theme) .top-bar {{
        background-color: rgba(11, 17, 32, 0.9);
    }}
}}

.brand {{
    font-family: var(--font-heading);
    font-weight: 800;
    font-size: 15px;
    color: var(--text-primary);
    text-decoration: none;
    white-space: nowrap;
}}

.brand span {{
    color: var(--accent);
}}

.nav-actions {{
    display: flex;
    align-items: center;
    gap: 8px;
}}

.chapter-select {{
    font-family: var(--font-heading);
    font-size: 12px;
    padding: 6px 8px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background-color: var(--bg-surface);
    color: var(--text-primary);
    max-width: 140px;
    text-overflow: ellipsis;
    outline: none;
}}

.btn-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 6px 10px;
    font-size: 12px;
    font-family: var(--font-heading);
    font-weight: 600;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background: var(--bg-surface);
    color: var(--text-primary);
    cursor: pointer;
    text-decoration: none;
    white-space: nowrap;
}}

.btn-pdf {{
    background: var(--accent);
    color: #ffffff !important;
    border-color: var(--accent);
}}

/* CONTAINER */
.article-container {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 24px 20px 80px 20px;
}}

/* COVER BANNER */
.book-cover-banner {{
    padding: 32px 20px;
    background: var(--bg-surface);
    border-radius: 16px;
    border: 1px solid var(--border-color);
    margin-bottom: 40px;
    border-left: 6px solid var(--accent);
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
}}

.cover-badge {{
    font-family: var(--font-heading);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 10px;
}}

.cover-title {{
    font-family: var(--font-heading);
    font-size: 32px;
    font-weight: 900;
    line-height: 1.15;
    color: var(--text-primary);
    margin: 0 0 10px 0;
}}

.cover-sub {{
    font-family: var(--font-heading);
    font-size: 15px;
    font-weight: 400;
    line-height: 1.5;
    color: var(--text-secondary);
    margin: 0 0 20px 0;
}}

.cover-meta {{
    font-family: var(--font-heading);
    font-size: 13px;
    color: var(--text-muted);
    border-top: 1px solid var(--border-color);
    padding-top: 14px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
    justify-content: space-between;
}}

/* HEADINGS */
h1.chapter-heading {{
    font-family: var(--font-heading);
    font-size: 24px;
    font-weight: 800;
    line-height: 1.35;
    color: var(--text-primary);
    margin-top: 54px;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--accent);
    scroll-margin-top: 60px;
}}

h2.section-heading {{
    font-family: var(--font-heading);
    font-size: 19px;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 36px;
    margin-bottom: 14px;
    line-height: 1.4;
    scroll-margin-top: 60px;
}}

h3.subsection-heading {{
    font-family: var(--font-heading);
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 24px;
    margin-bottom: 10px;
    line-height: 1.4;
}}

p {{
    margin-top: 0;
    margin-bottom: 18px;
    text-align: left;
    word-break: break-word;
}}

blockquote {{
    margin: 20px 0;
    padding: 14px 18px;
    background: var(--quote-bg);
    border-left: 4px solid var(--quote-border);
    border-radius: 0 8px 8px 0;
    font-style: italic;
    color: var(--text-secondary);
}}

blockquote p:last-child {{
    margin-bottom: 0;
}}

ul, ol {{
    padding-left: 20px;
    margin-bottom: 20px;
}}

li {{
    margin-bottom: 6px;
}}

code {{
    font-family: var(--font-mono);
    font-size: 0.88em;
    padding: 2px 5px;
    background: var(--code-bg);
    border-radius: 4px;
    color: var(--accent);
}}

pre {{
    background: var(--code-bg);
    padding: 14px;
    border-radius: 8px;
    overflow-x: auto;
    font-family: var(--font-mono);
    font-size: 13px;
    line-height: 1.5;
    border: 1px solid var(--border-color);
    margin: 20px 0;
}}

pre code {{
    padding: 0;
    background: transparent;
    color: var(--text-primary);
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
    font-size: 14px;
    font-family: var(--font-heading);
    display: block;
    overflow-x: auto;
}}

th, td {{
    padding: 8px 12px;
    border: 1px solid var(--border-color);
    text-align: left;
}}

th {{
    background: var(--code-bg);
    font-weight: 700;
}}

hr {{
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 40px 0;
}}

strong {{
    font-weight: 700;
    color: var(--text-primary);
}}

.floating-tools {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 30px;
    padding: 4px 10px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    display: flex;
    gap: 6px;
    z-index: 99;
}}

.floating-tools button {{
    background: none;
    border: none;
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 13px;
    color: var(--text-primary);
    cursor: pointer;
    padding: 4px 6px;
}}
</style>
</head>
<body>

<header class="top-bar">
    <a href="#" class="brand">COMPANY <span>OS</span></a>
    
    <div class="nav-actions">
        <select class="chapter-select" onchange="if(this.value) location.href=this.value;">
            <option value="">-- Chọn chương --</option>
            {toc_options}
        </select>
        <button class="btn-icon" onclick="toggleTheme()" title="Đổi giao diện">🌓</button>
        <a class="btn-icon btn-pdf" href="./COMPANY_OS_NGUYEN_NGOC_PHUC.pdf" target="_blank">📄 PDF</a>
    </div>
</header>

<main class="article-container">

    <div class="book-cover-banner">
        <div class="cover-badge">CẨM NANG KIẾN TRÚC VẬN HÀNH</div>
        <h1 class="cover-title">COMPANY OS</h1>
        <div class="cover-sub">Xây Dựng Hệ Điều Hành Doanh Nghiệp Tinh Gọn Bằng Low-Code & AI Thực Chiến</div>
        <div class="cover-meta">
            <div>✍️ Tác giả: <strong>Nguyễn Ngọc Phúc</strong></div>
            <div>📖 Quy mô: 21.715 từ • 12 Chương</div>
        </div>
    </div>

    <article id="book-content">
        {html_body}
    </article>

</main>

<div class="floating-tools">
    <button onclick="changeFontSize(-1)">A-</button>
    <button onclick="changeFontSize(1)">A+</button>
    <button onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">↑</button>
</div>

<script>
function toggleTheme() {{
    const body = document.body;
    if (body.classList.contains('dark-theme')) {{
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        localStorage.setItem('theme', 'light');
    }} else if (body.classList.contains('light-theme')) {{
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
    }} else {{
        const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (isDark) {{
            body.classList.add('light-theme');
            localStorage.setItem('theme', 'light');
        }} else {{
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        }}
    }}
}}

function changeFontSize(delta) {{
    const content = document.getElementById('book-content');
    const currentSize = parseFloat(window.getComputedStyle(content).fontSize);
    const newSize = Math.max(14, Math.min(24, currentSize + delta));
    content.style.fontSize = newSize + 'px';
    localStorage.setItem('book_font_size', newSize);
}}

(function() {{
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {{
        document.body.classList.add(savedTheme + '-theme');
    }}
    const savedFontSize = localStorage.getItem('book_font_size');
    if (savedFontSize) {{
        document.getElementById('book-content').style.fontSize = savedFontSize + 'px';
    }}
}})();
</script>

</body>
</html>
'''

with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Web reader HTML generated successfully at:", output_html_path)
