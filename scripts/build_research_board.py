#!/usr/bin/env python3
"""Build the offline research board from canonical Markdown (standard library only).

Run from any directory: python3 scripts/build_research_board.py
Do not edit the generated HTML. Unknown table shapes fail before replacing output.
"""
from __future__ import annotations

import hashlib
import html
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / 'wiki'
SOURCE = WIKI / 'research/trading/research_index.md'
OUTPUT = SOURCE.with_suffix('.html')
TOKEN = re.compile(r'\[\[([^\]]+)\]\]|\[([^\]]+)\]\(([^)]+)\)|\*\*(.+?)\*\*|`([^`]+)`')
MISSING: set[str] = set()


def inline(value: str) -> str:
    result, end = [], 0
    for match in TOKEN.finditer(value):
        result.append(html.escape(value[end:match.start()]))
        wiki, label, url, bold, code = match.groups()
        if wiki:
            target, _, alias = wiki.partition('|')
            path, _, fragment = target.partition('#')
            resolved = WIKI / (path + '.md')
            if not resolved.is_file():
                candidates = list(WIKI.rglob(Path(path).name + '.md'))
                if len(candidates) == 1:
                    resolved = candidates[0]
            label = html.escape(alias or path)
            if resolved.is_file():
                href = quote(os.path.relpath(resolved, OUTPUT.parent))
                if fragment:
                    href += '#' + quote(fragment)
                result.append(f'<a href="{href}">{label}</a>')
            else:
                MISSING.add(target)
                result.append(f'<span class="missing" title="Source page missing: {html.escape(target, quote=True)}">{label} <small>page unavailable</small></span>')
        elif url:
            parsed = urlsplit(url)
            local = (OUTPUT.parent / unquote(parsed.path)).resolve()
            safe_local = not parsed.scheme and not parsed.netloc and local.is_relative_to(ROOT) and local.is_file()
            if url.startswith(('https://', 'http://')) or safe_local:
                result.append(f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>')
            else:
                result.append(html.escape(match.group()))
        elif bold:
            result.append('<strong>' + inline(bold) + '</strong>')
        else:
            result.append('<code>' + html.escape(code) + '</code>')
        end = match.end()
    result.append(html.escape(value[end:]))
    return ''.join(result)


def prose(value: str) -> str:
    blocks = []
    for block in value.strip().split('\n\n'):
        lines = block.splitlines()
        if not lines:
            continue
        if all(line.startswith('- ') for line in lines):
            blocks.append('<ul>' + ''.join('<li>' + inline(line[2:]) + '</li>' for line in lines) + '</ul>')
        elif all(re.match(r'^\d+\. ', line) for line in lines):
            blocks.append('<ol>' + ''.join('<li>' + inline(re.sub(r'^\d+\. ', '', line)) + '</li>' for line in lines) + '</ol>')
        else:
            blocks.append('<p>' + inline(' '.join(lines)) + '</p>')
    return ''.join(blocks)


def table(section: str, columns: int) -> tuple[str, list[list[str]]]:
    lines = section.strip().splitlines()
    intro = '\n'.join(line for line in lines if not line.startswith('|'))
    rows = []
    for line in (line for line in lines if line.startswith('|')):
        # A wikilink's alias delimiter is not a table delimiter.
        cells = [cell.strip() for cell in re.split(r'\|(?![^\[]*\]\])', line.strip().strip('|'))]
        if len(cells) != columns:
            raise ValueError(f'Expected {columns} cells: {line}')
        rows.append(cells)
    if len(rows) < 2 or not all(re.fullmatch(r':?-+:?', c) for c in rows[1]):
        raise ValueError('Missing table header/separator')
    return intro, rows[2:]


def main() -> None:
    raw = SOURCE.read_text(encoding='utf-8')
    if '\n## Current focus\n' in raw:
        build_home(raw)
        return
    chunks = re.split(r'^## (.+)\n', raw, flags=re.M)
    sections = dict(zip(chunks[1::2], chunks[2::2]))
    intro, active = table(sections['Active research programs'], 6)
    _, assets = table(sections['Shared research assets'], 2)
    horizon_intro, horizon = table(sections['Horizon programs'], 3)
    lanes = sorted({re.sub(r'\*\*|`', '', row[1]).split(' → ')[0] for row in active})
    cards = []
    for number, row in enumerate(active, 1):
        name, lane, evidence, action, dependency, links = row
        lane_key = re.sub(r'\*\*|`', '', lane).split(' → ')[0]
        cards.append(f'''<article class="card" data-item data-kind="active" data-lane="{html.escape(lane_key, quote=True)}">
<div class="card-top"><span class="eyebrow">PROGRAM {number:02}</span><span class="lane">{inline(lane_key)}</span></div>
<h3>{inline(name)}</h3><div class="next"><h4>Next action</h4><p>{inline(action)}</p></div>
<details><summary>Evidence &amp; dependencies</summary><div class="detail-body"><h4>Current evidence / state</h4><p>{inline(evidence)}</p><h4>Human dependency</h4><p>{inline(dependency)}</p><h4>Research lane</h4><p>{inline(lane)}</p></div></details>
<div class="issue-links">{inline(links)}</div></article>''')
    asset_cards = ''.join(f'<article class="card resource" data-item data-kind="assets"><h3>{inline(name)}</h3><p>{inline(role)}</p></article>' for name, role in assets)
    horizon_cards = ''.join(f'<article class="card resource" data-item data-kind="horizon"><span class="eyebrow">{inline(state)}</span><h3>{inline(name)}</h3><h4>Resume condition</h4><p>{inline(resume)}</p></article>' for name, state, resume in horizon)
    principles = ''.join(f'<details class="principle"><summary>{title}</summary>{prose(sections[title])}</details>' for title in ['Operating objective', 'Research system model', 'Board operating rules'])
    # Exclude the maintenance instructions from the original purpose text.
    original_intro = chunks[0].split('##')[0]
    purpose = '\n\n'.join(block for block in original_intro.split('\n\n') if block.startswith(('Purpose:', 'Related process:')))
    output = TEMPLATE.replace('@@CARDS@@', '\n'.join(cards)).replace('@@ASSETS@@', asset_cards).replace('@@HORIZON@@', horizon_cards)
    values = {
        'LANES': ''.join(f'<option value="{html.escape(lane, quote=True)}">{html.escape(lane.capitalize())}</option>' for lane in lanes),
        'ACTIVE_COUNT': str(len(active)), 'ASSET_COUNT': str(len(assets)), 'HORIZON_COUNT': str(len(horizon)),
        'INTRO': prose(intro), 'HORIZON_INTRO': prose(horizon_intro), 'PRINCIPLES': principles,
        'PURPOSE': prose(purpose), 'HASH': hashlib.sha256(raw.encode()).hexdigest()[:12],
        'MISSING': str(len(MISSING)),
    }
    for key, value in values.items():
        output = output.replace('@@' + key + '@@', value)
    if re.search(r'@@[A-Z_]+@@', output):
        raise ValueError('Unfilled template field')
    OUTPUT.write_text(output, encoding='utf-8')
    print(f'Built {OUTPUT.relative_to(ROOT)}: {len(active)} programs, {len(assets)} resources, {len(horizon)} horizon programs.')
    for path in sorted(MISSING):
        print(f'Source link unavailable: {path}')


def build_home(raw: str) -> None:
    """Render the fresh-start home without importing the historical portfolio."""
    chunks = re.split(r'^## (.+)\n', raw, flags=re.M)
    sections = dict(zip(chunks[1::2], chunks[2::2]))
    required = {'Current focus', 'Starting work', 'History, when useful'}
    if set(sections) != required:
        raise ValueError('Research home sections changed; update the renderer explicitly')
    output = HOME_TEMPLATE
    for marker, heading in [('FOCUS', 'Current focus'), ('START', 'Starting work'), ('HISTORY', 'History, when useful')]:
        output = output.replace('@@' + marker + '@@', prose(sections[heading]))
    output = output.replace('@@HASH@@', hashlib.sha256(raw.encode()).hexdigest()[:12])
    OUTPUT.write_text(output, encoding='utf-8')
    print(f'Built {OUTPUT.relative_to(ROOT)}: fresh start, no inherited commitments.')


HOME_TEMPLATE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Research Home · Money Machine</title><style>
:root{color-scheme:light;--ink:#20342e;--muted:#64716a;--line:#dce2d8;--accent:#226147}
*{box-sizing:border-box}body{margin:0;background:#f6f7f1;color:var(--ink);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:860px;margin:auto;padding:48px 28px 70px}header{display:flex;justify-content:space-between;gap:20px;align-items:center;padding-bottom:22px;border-bottom:1px solid var(--line)}.brand{font-weight:750;letter-spacing:-.5px}.tag,.eyebrow{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted)}.intro{padding:64px 0 30px}h1{font-size:50px;line-height:1.12;letter-spacing:-2px;margin:10px 0 18px}.lead{font-size:18px;color:var(--muted);max-width:560px}h2{font-size:14px;margin:0 0 20px;color:var(--muted);font-weight:600}p{margin:0 0 16px}.focus{padding:30px;background:white;border:1px solid var(--line);border-radius:12px;margin:10px 0 28px}.focus p:first-of-type{font-size:26px;letter-spacing:-.5px}.focus p:last-child{color:var(--muted);font-size:15px;margin-bottom:0}.start{padding:8px 4px 20px;font-size:15px;max-width:680px}a{color:var(--accent);text-underline-offset:4px}a:focus-visible,summary:focus-visible{outline:3px solid #ad7828;outline-offset:5px}details{border-top:1px solid var(--line);padding:22px 4px;font-size:14px}summary{cursor:pointer;color:var(--accent);font-weight:600}details[open] summary{margin-bottom:20px}li{margin:10px 0}footer{margin-top:34px;font-size:12px;color:var(--muted)}footer p{margin:8px 0}code{font-size:12px;background:#eaf0e5;padding:2px 5px;border-radius:3px;overflow-wrap:anywhere}@media(max-width:600px){main{padding:24px 20px 40px}.intro{padding-top:40px}h1{font-size:39px}.tag{font-size:9px}.focus{padding:24px}.focus p:first-of-type{font-size:23px}}
</style></head><body><main>
<header><span class="brand">Money Machine</span><span class="tag">Research home</span></header>
<div class="intro"><span class="eyebrow">A fresh start</span><h1>Room for what’s next.</h1><p class="lead">Start with what you want to work on now. There’s nothing here you need to catch up on first.</p></div>
<section class="focus" aria-labelledby="focus-heading"><h2 id="focus-heading">Current focus</h2>@@FOCUS@@</section>
<section class="start" aria-label="Starting work">@@START@@</section>
<details><summary>Past work, if you need it</summary>@@HISTORY@@</details>
<footer><a href="research_index.md">Edit the source</a> · <a href="../../sessions/current-checkpoint.md">Current checkpoint</a>
<details><summary>About this page</summary><p>The fresh-start decision was approved on October 6, 2026. This is a local view of the Markdown research home.</p><p>After editing the source, run <code>python3 scripts/build_research_board.py</code> from the repository root, then reload this page.</p><p>Source snapshot: <code>@@HASH@@</code></p></details></footer>
</main></body></html>'''


TEMPLATE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Research Board · Money Machine</title>
<style>
:root{color-scheme:light;--ink:#20342e;--muted:#64716a;--line:#dce2d8;--paper:#f6f7f1;--accent:#226147;--soft:#eaf0e5}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--accent);text-underline-offset:3px}button,input,select{font:inherit}button,summary,select{cursor:pointer}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #ad7828;outline-offset:4px}[hidden]{display:none!important}.skip{position:absolute;left:20px;top:-80px;background:white;padding:12px;z-index:5}.skip:focus{top:10px}
.shell{max-width:1480px;margin:auto;display:grid;grid-template-columns:228px minmax(0,1fr);min-height:100vh}.sidebar{border-right:1px solid var(--line);padding:36px 24px;position:sticky;top:0;height:100vh;display:flex;flex-direction:column;gap:32px}.brand{font-size:12px;font-weight:800;letter-spacing:1.8px}.brand b{display:block;font-size:22px;letter-spacing:-.7px}.sidebar small{color:var(--muted)}nav{display:grid;gap:8px}nav button{text-align:left;padding:12px;border:0;border-radius:7px;background:transparent;color:var(--muted);display:flex;justify-content:space-between;gap:10px}nav button[aria-pressed=true]{background:var(--ink);color:white}nav span{opacity:.7}.side-bottom{margin-top:auto;display:grid;gap:10px;font-size:13px}.side-bottom a{text-decoration:none}main{min-width:0;padding:44px 44px 60px}.eyebrow{font-size:10px;letter-spacing:1.5px;font-weight:750;color:var(--muted);text-transform:uppercase}h1{font-size:44px;letter-spacing:-1.8px;line-height:1.1;margin:12px 0}h2{font-size:23px;letter-spacing:-.5px;margin:0}h3{font-size:21px;line-height:1.3;letter-spacing:-.45px;margin:18px 0}h3 a{text-decoration:none}h3 a:hover{text-decoration:underline}h4{font-size:10px;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);margin:0 0 6px}p{margin:0 0 14px}.lead{color:var(--muted);max-width:650px;font-size:16px}.notice{margin:26px 0;padding:13px 17px;border-left:3px solid #bca564;background:#f0eddf;font-size:13px;color:#605635}.notice p{margin:0}.toolbar{display:flex;gap:12px;margin:26px 0 22px}.search{flex:1;min-width:120px}.search span,.filter span{display:block;font-size:11px;letter-spacing:.7px;text-transform:uppercase;color:var(--muted);margin-bottom:5px}input,select{border:1px solid #cbd4c8;border-radius:7px;background:white;padding:11px 13px;color:var(--ink);width:100%}select{max-width:280px}.section-head{display:flex;justify-content:space-between;gap:20px;align-items:center;margin:26px 0 16px}.section-head p{margin:0;color:var(--muted);font-size:12px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;align-items:start}.card{background:white;border:1px solid var(--line);border-radius:10px;padding:23px;overflow-wrap:anywhere}.card-top{display:flex;justify-content:space-between;gap:10px;align-items:center}.lane{font-size:10px;border-radius:4px;padding:3px 7px;background:var(--soft);color:#426449}.next{padding-top:2px}.next p{font-size:14px;line-height:1.65}details{border-top:1px solid var(--line);margin-top:17px;padding-top:12px}summary{font-size:13px;color:var(--accent);font-weight:600}.detail-body{padding-top:18px;font-size:13px}.issue-links{border-top:1px solid var(--line);margin-top:15px;padding-top:13px;font-size:12px;line-height:1.9}.resource p{font-size:14px}.resource h3{margin-top:9px}.section-intro{font-size:13px;color:var(--muted);max-width:800px}.missing small{display:inline-block;font-size:10px;background:#f7eedb;color:#7c612e;padding:1px 5px;border-radius:3px;letter-spacing:0;font-weight:400}.principle{padding:18px;background:white;border:1px solid var(--line);border-radius:8px}.principle summary{font-size:16px}.principle p,.principle li{font-size:14px}.principle[open] summary{margin-bottom:18px}li{margin:10px 0}code{font-size:12px;background:var(--soft);padding:2px 5px;border-radius:3px;overflow-wrap:anywhere}.empty{padding:40px;text-align:center;border:1px dashed var(--line);border-radius:10px}.empty button{border:0;background:var(--accent);color:white;padding:10px 18px;border-radius:6px}footer{margin-top:35px;border-top:1px solid var(--line);padding-top:17px;font-size:12px;color:var(--muted)}footer details{border:0;padding:0;margin-top:10px}footer p{margin-top:12px}.no-script{padding:15px;background:#f0eddf}
@media(min-width:1400px){main{padding-left:56px;padding-right:56px}}@media(max-width:1000px){.shell{grid-template-columns:190px minmax(0,1fr)}main{padding:32px 24px}.sidebar{padding:32px 18px}.grid{grid-template-columns:1fr}}@media(max-width:650px){.shell{display:block}.sidebar{height:auto;position:static;border-right:0;border-bottom:1px solid var(--line);padding:20px;gap:18px}.brand b{display:inline;font-size:17px;margin-right:10px}.sidebar nav{display:flex;flex-wrap:wrap;gap:5px}.sidebar nav button{font-size:12px;padding:8px 10px}.side-bottom{display:none}main{padding:24px 18px}h1{font-size:36px}.toolbar{flex-direction:column}select{max-width:none}.card{padding:20px}.section-head{align-items:start}.card-top{flex-wrap:wrap}}@media print{.sidebar,.toolbar,.notice,footer{display:none}.shell{display:block}main{padding:0}.grid{display:block}.card{break-inside:avoid;margin-bottom:15px}details{display:block}}
</style></head><body>
<a href="#main" class="skip">Skip to research</a><div class="shell">
<aside class="sidebar"><div class="brand"><b>Money Machine</b>RESEARCH WORKSPACE</div>
<nav aria-label="Board sections"><button type="button" data-view="active" aria-pressed="true">Active programs <span>@@ACTIVE_COUNT@@</span></button><button type="button" data-view="assets" aria-pressed="false">Shared resources <span>@@ASSET_COUNT@@</span></button><button type="button" data-view="horizon" aria-pressed="false">On the horizon <span>@@HORIZON_COUNT@@</span></button><button type="button" data-view="principles" aria-pressed="false">Operating context</button></nav>
<div class="side-bottom"><small>CONNECTED NOTES</small><a href="../../sessions/current-checkpoint.md">Current checkpoint ↗</a><a href="../../index.md">Knowledge index ↗</a><a href="research_index.md">Board source ↗</a><small>Local view · Markdown-backed</small></div></aside>
<main id="main"><header><span class="eyebrow">RESEARCH / PORTFOLIO</span><h1>Pick up the thread.</h1><p class="lead">Find a program, see the next action, and open the evidence when you need it.</p></header>
<div class="notice"><p><strong>Research status needs reconciliation.</strong> This view preserves the board’s wording. Some entries lag behind the <a href="../../sessions/current-checkpoint.md">current checkpoint</a>; check the linked notes before starting work.</p></div>
<noscript><p class="no-script">JavaScript is disabled. All sections are shown; search and filters require JavaScript.</p></noscript>
<div class="toolbar" hidden><label class="search"><span>Search this section</span><input id="search" type="search" placeholder="Program, issue, evidence, or dependency…" autocomplete="off"></label><label class="filter"><span>Research lane</span><select id="lane"><option value="">All lanes</option>@@LANES@@</select></label></div>
<section data-section="active"><div class="section-head"><h2>Active programs</h2><p data-count aria-live="polite"></p></div><details class="section-intro"><summary>How to read availability</summary>@@INTRO@@</details><div class="grid" style="margin-top:16px">@@CARDS@@</div></section>
<section data-section="assets"><div class="section-head"><h2>Shared resources</h2><p data-count aria-live="polite"></p></div><div class="grid">@@ASSETS@@</div></section>
<section data-section="horizon"><div class="section-head"><h2>On the horizon</h2><p data-count aria-live="polite"></p></div><div class="section-intro">@@HORIZON_INTRO@@</div><div class="grid">@@HORIZON@@</div></section>
<section data-section="principles"><div class="section-head"><h2>Operating context</h2></div><div class="section-intro">@@PURPOSE@@</div>@@PRINCIPLES@@</section>
<div class="empty" hidden><h3>No matching items</h3><p>Try a broader search or another lane.</p><button type="button" id="reset">Clear filters</button></div>
<footer>Source: <a href="research_index.md">Research Board Markdown</a> · Status: in progress · Snapshot <code>@@HASH@@</code>
<details><summary>Keep this view in sync</summary><p>Edit the Markdown board, then run <code>python3 scripts/build_research_board.py</code> from the repository root and reload this file. The snapshot identifies the source content; it is not a claim of current research status.</p><p>Research links open local Markdown files. @@MISSING@@ source targets are unavailable and labeled on the board. Linear links open their original issues.</p></details></footer>
</main></div><script>
(() => {
  const buttons = [...document.querySelectorAll('[data-view]')];
  const sections = [...document.querySelectorAll('[data-section]')];
  const search = document.querySelector('#search');
  const lane = document.querySelector('#lane');
  const empty = document.querySelector('.empty');
  let view = 'active';
  function render() {
    const query = search.value.trim().toLocaleLowerCase();
    let shown = 0;
    sections.forEach(section => {
      section.hidden = section.dataset.section !== view;
      if (section.hidden) return;
      const items = [...section.querySelectorAll('[data-item]')];
      items.forEach(item => {
        item.hidden = !(item.textContent.toLocaleLowerCase().includes(query) && (view !== 'active' || !lane.value || item.dataset.lane === lane.value));
        if (!item.hidden) shown++;
      });
      const count = section.querySelector('[data-count]');
      if (count) count.textContent = `${shown} of ${items.length} shown`;
    });
    document.querySelector('.toolbar').hidden = view === 'principles';
    document.querySelector('.filter').hidden = view !== 'active';
    empty.hidden = shown > 0 || view === 'principles';
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === view)));
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    view = button.dataset.view; search.value = ''; lane.value = ''; render();
  }));
  search.addEventListener('input', render);
  lane.addEventListener('change', render);
  document.querySelector('#reset').addEventListener('click', () => {search.value = ''; lane.value = ''; render(); search.focus();});
  render();
})();
</script></body></html>'''

if __name__ == '__main__':
    main()
