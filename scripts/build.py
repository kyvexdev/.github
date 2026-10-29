"""Builds the images on the kyvexdev organization page (profile/README.md).

    python scripts/build.py

Writes profile/assets/: header.svg (animated), tech.svg and discord.svg. Every image embeds the brand
fonts (Sora, JetBrains Mono), so GitHub shows them exactly. Run it by hand after changing an image and
commit the result. Products aren't listed here: the page links to kyvexdev.com, which is always current.
"""
import base64
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'profile', 'assets')

BG, PANEL, BORDER, STRONG = '#000000', '#111111', '#262626', '#333333'
TEXT, MUTED, CYAN = '#EDEDED', '#8F8F8F', '#22D3EE'

K_ICON = f'<rect width="16" height="72" fill="{TEXT}"/><polygon points="66,0 46,0 22,36 46,72 66,72 42,36" fill="{CYAN}"/>'


def font_face():
    def b64(name):
        return base64.b64encode(open(os.path.join(HERE, 'fonts', name), 'rb').read()).decode()
    return (f"@font-face{{font-family:'Sora';font-weight:100 900;src:url(data:font/woff2;base64,{b64('Sora.woff2')}) format('woff2')}}"
            f"@font-face{{font-family:'JBM';font-weight:700;src:url(data:font/woff2;base64,{b64('JetBrainsMono-700.woff2')}) format('woff2')}}"
            ".s{font-family:'Sora',sans-serif}.m{font-family:'JBM',monospace;font-weight:700}")


def svg(w, h, body, css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>{font_face()}{css}</style>{body}</svg>')


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


# Header: the wordmark draws in, DEVELOPMENT fades up, the tagline types out, a cyan line sweeps under it,
# and a trail of three cyan chevrons (the K's arm) runs on the right.
def header():
    w, h = 1280, 340
    css = """
.bar{transform-box:fill-box;transform-origin:50% 100%;animation:grow .6s cubic-bezier(.2,.8,.2,1) both}
.arm{animation:slide .6s .35s cubic-bezier(.2,.8,.2,1) both}
.l{animation:fade .45s both}
.l1{animation-delay:.7s}.l2{animation-delay:.82s}.l3{animation-delay:.94s}.l4{animation-delay:1.06s}
.dev{animation:fade .6s 1.3s both}
.type{animation:type 1.9s 1.8s steps(43) both}
.cur{animation:follow 1.9s 1.8s steps(43) both,blink 1s 3.7s steps(1) infinite}
.sweep{transform-box:fill-box;transform-origin:0 50%;animation:sweep 1.4s 4s cubic-bezier(.6,0,.2,1) both}
.ch{opacity:.12;animation:run 2.4s linear infinite}.c2{animation-delay:.3s}.c3{animation-delay:.6s}
@keyframes grow{from{transform:scaleY(0)}}
@keyframes slide{from{transform:translateX(-40px);opacity:0}}
@keyframes fade{from{opacity:0;transform:translateY(8px)}}
@keyframes type{from{width:0}to{width:602px}}
@keyframes blink{50%{opacity:0}}
@keyframes follow{from{transform:translateX(-598px)}}
@keyframes sweep{from{transform:scaleX(0)}}
@keyframes run{0%,100%{opacity:.12}20%{opacity:1}45%{opacity:.12}}
"""
    word = (f'<g transform="translate(96 78) scale(1.3)">'
            f'<rect class="bar" x="0" y="0" width="16" height="72" fill="{TEXT}"/>'
            f'<polygon class="arm" points="66,0 46,0 22,36 46,72 66,72 42,36" fill="{CYAN}"/>'
            f'<polygon class="l l1" points="75,0 94,0 107,22 120,0 139,0 115,40 115,72 99,72 99,40" fill="{TEXT}"/>'
            f'<polygon class="l l2" points="148,0 166,0 181,46 196,0 214,0 190,72 172,72" fill="{TEXT}"/>'
            f'<g class="l l3" fill="{TEXT}"><rect x="223" y="0" width="16" height="72"/><rect x="223" y="0" width="50" height="15"/>'
            f'<rect x="223" y="28.5" width="44" height="15"/><rect x="223" y="57" width="50" height="15"/></g>'
            f'<g class="l l4" fill="{TEXT}"><polygon points="282,0 300,0 348,72 330,72"/><polygon points="330,0 348,0 300,72 282,72"/></g></g>')
    chev = ''.join(f'<g class="ch c{i + 1}" transform="translate({930 + i * 92} 106) scale(1.75)">'
                   f'<polygon points="0,0 20,0 44,36 20,72 0,72 24,36" fill="{CYAN}"/></g>' for i in range(3))
    tag = 'Software, scripts and tools, built to last.'
    body = (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="20" fill="{BG}" stroke="{BORDER}"/>'
            f'{chev}{word}'
            f'<text class="m dev" x="98" y="214" font-size="15" letter-spacing="9" fill="{MUTED}">DEVELOPMENT</text>'
            f'<defs><clipPath id="t"><rect class="type" x="96" y="240" width="760" height="44"/></clipPath></defs>'
            f'<text class="s" clip-path="url(#t)" x="96" y="272" font-size="26" font-weight="600" fill="{TEXT}" textLength="590" lengthAdjust="spacingAndGlyphs">{html.escape(tag)}</text>'
            f'<rect class="cur" x="696" y="248" width="3" height="30" fill="{CYAN}"/>'
            f'<rect class="sweep" x="96" y="306" width="1088" height="3" rx="1.5" fill="{CYAN}"/>')
    write('header.svg', svg(w, h, body, css))


# Line icons (2px stroke, square caps) on a 20 x 20 grid, one per language or tool.
TECH_ICONS = {
    'LUA': '<circle cx="9" cy="11" r="6.5"/><circle cx="16" cy="4" r="2.2"/>',
    'JAVASCRIPT': '<path d="M7 3H5.5A1.5 1.5 0 0 0 4 4.5V8l-2 2 2 2v3.5A1.5 1.5 0 0 0 5.5 17H7"/><path d="M13 3h1.5A1.5 1.5 0 0 1 16 4.5V8l2 2-2 2v3.5a1.5 1.5 0 0 1-1.5 1.5H13"/>',
    'HTML': '<path d="M7 5L2 10l5 5"/><path d="M13 5l5 5-5 5"/><path d="M11.5 3l-3 14"/>',
    'CSS': '<path d="M8 2.5L6 17.5"/><path d="M14 2.5L12 17.5"/><path d="M3 7h15"/><path d="M2 13h15"/>',
    'PYTHON': '<rect x="1.5" y="3" width="17" height="14" rx="2"/><path d="M5 8l3 2.5L5 13"/><path d="M10 13h5"/>',
    'SQL / MYSQL': '<ellipse cx="10" cy="4.5" rx="7" ry="2.5"/><path d="M3 4.5v11c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-11"/><path d="M3 10c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5"/>',
    'GIT': '<circle cx="5" cy="4" r="2"/><circle cx="5" cy="16" r="2"/><circle cx="15" cy="7" r="2"/><path d="M5 6v8"/><path d="M15 9c0 3.5-4 3.5-8.5 5.5"/>',
}


def tech_svg():
    items = list(TECH_ICONS)
    w, h, gap, parts = 1280, 52, 14, []
    widths = [74 + len(t) * 9.2 for t in items]
    total = sum(widths) + gap * (len(items) - 1)
    x = (w - total) / 2
    for i, t in enumerate(items):
        first = False  # every chip the same
        ink = '#000' if first else TEXT
        parts.append(f'<rect x="{x + .5}" y=".5" width="{widths[i] - 1}" height="{h - 1}" rx="10" fill="{CYAN if first else PANEL}" stroke="{CYAN if first else STRONG}"/>'
                     f'<g transform="translate({x + 20} 16)" fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter">{TECH_ICONS[t]}</g>'
                     f'<text class="m" x="{x + 52}" y="31" font-size="14" letter-spacing="1.5" fill="{ink}">{t}</text>')
        x += widths[i] + gap
    write('tech.svg', svg(w, h, ''.join(parts)))


def discord_svg():
    w, h = 300, 60
    icon = ('<g transform="translate(26 18)" fill="none" stroke="#000" stroke-width="2.2" stroke-linecap="square">'
            '<path d="M2 3h20v13H9l-5 4v-4H2z"/><path d="M7 9h10"/><path d="M7 12.5h6"/></g>')
    body = (f'<rect width="{w}" height="{h}" rx="12" fill="{CYAN}"/>{icon}'
            f'<text class="s" x="64" y="37" font-size="18" font-weight="800" fill="#000">Join the Discord</text>'
            f'<path d="M262 24l8 6-8 6" fill="none" stroke="#000" stroke-width="2.4" stroke-linecap="square"/>')
    write('discord.svg', svg(w, h, body))


def main():
    header()
    tech_svg()
    discord_svg()
    print('built: header.svg, tech.svg, discord.svg')


if __name__ == '__main__':
    main()
