#!/usr/bin/env python3
"""Ronin skills indexer.

Scans framework/skills/<domain>/<slug>/SKILL.md, then:
  symlinks  -> (re)create flat .claude/skills/<name> discovery symlinks
  catalog   -> write CATALOG.md (browsable) + data/skills_index.json (machine)
  index     -> print a compact domain-grouped markdown index to stdout
  validate  -> check frontmatter against the required schema keys/enums
  all       -> symlinks + catalog

No third-party deps: a minimal frontmatter parser handles our controlled files.
"""
import sys, os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "framework", "skills")

REQUIRED = ["name", "description", "domain", "type", "stability", "modes", "schema_version"]
DOMAINS = ["recon","web","api","mobile","cloud","network","ad","ai-ml","code-review",
           "exploit-dev","privesc","defense","payloads","reporting","automation","tradecraft"]
TYPES = ["technique","arsenal","methodology","checklist","reference"]
STABILITY = ["locked","learning"]
MODES = ["ctf","bugbounty","defense"]
DOMAIN_TITLES = {
    "recon":"Reconnaissance","web":"Web application","api":"API","mobile":"Mobile",
    "cloud":"Cloud & containers","network":"Network & services","ad":"Active Directory",
    "ai-ml":"AI / LLM","code-review":"Source-code review","exploit-dev":"Exploit development",
    "privesc":"Privilege escalation","defense":"Defense / blue-team","payloads":"Payloads",
    "reporting":"Reporting","automation":"Automation","tradecraft":"Tradecraft & discipline",
}

def parse_frontmatter(path):
    text = open(path, encoding="utf-8").read().split("\n")
    if not text or text[0].strip() != "---":
        return None
    end = None
    for i in range(1, len(text)):
        if text[i].strip() == "---":
            end = i; break
    if end is None:
        return None
    fm, i = {}, 1
    lines = text[1:end]
    j = 0
    while j < len(lines):
        line = lines[j]
        m = re.match(r'^([A-Za-z0-9_]+):\s*(.*)$', line)
        if not m:
            j += 1; continue
        key, val = m.group(1), m.group(2).strip()
        if val in (">", "|", ">-", "|-"):  # folded/literal block
            block = []
            j += 1
            while j < len(lines) and (lines[j].startswith("  ") or lines[j].strip() == ""):
                block.append(lines[j].strip()); j += 1
            fm[key] = " ".join(x for x in block if x).strip()
            continue
        if val.startswith("[") and val.endswith("]"):  # inline list
            inner = val[1:-1].strip()
            fm[key] = [x.strip() for x in inner.split(",")] if inner else []
        else:
            fm[key] = val
        j += 1
    return fm

def collect():
    skills = []
    for p in sorted(glob.glob(os.path.join(SKILLS, "*", "*", "SKILL.md"))):
        fm = parse_frontmatter(p)
        reldir = os.path.relpath(os.path.dirname(p), ROOT)
        skills.append({"path": p, "reldir": reldir, "fm": fm or {}})
    return skills

def short_desc(fm):
    d = (fm.get("description") or "").strip()
    d = re.sub(r'\s+', ' ', d)
    d = re.sub(r'^One line:\s*', '', d, flags=re.I)
    # first sentence, capped
    cut = d.find(". ")
    if 0 < cut < 160:
        return d[:cut+1]
    return (d[:150] + "…") if len(d) > 150 else d

def cmd_validate():
    skills = collect(); errors = []
    seen = {}
    for s in skills:
        fm, where = s["fm"], s["reldir"]
        if not fm:
            errors.append(f"{where}: no/invalid frontmatter"); continue
        for k in REQUIRED:
            if k not in fm:
                errors.append(f"{where}: missing '{k}'")
        n = fm.get("name","")
        if n:
            if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', n):
                errors.append(f"{where}: name '{n}' not kebab-case")
            if n in seen:
                errors.append(f"{where}: duplicate name '{n}' (also {seen[n]})")
            seen[n] = where
        if fm.get("domain") not in DOMAINS:
            errors.append(f"{where}: domain '{fm.get('domain')}' not in taxonomy")
        if fm.get("type") not in TYPES:
            errors.append(f"{where}: type '{fm.get('type')}' invalid")
        if fm.get("stability") not in STABILITY:
            errors.append(f"{where}: stability '{fm.get('stability')}' invalid")
        modes = fm.get("modes") or []
        if not isinstance(modes, list) or not modes or any(m not in MODES for m in modes):
            errors.append(f"{where}: modes {modes} invalid (subset of {MODES}, non-empty)")
        # folder domain should match declared domain
        folder_domain = s["reldir"].split(os.sep)[2] if len(s["reldir"].split(os.sep))>2 else ""
        if folder_domain and fm.get("domain") and folder_domain != fm.get("domain"):
            errors.append(f"{where}: folder domain '{folder_domain}' != frontmatter domain '{fm.get('domain')}'")
    if errors:
        print("SKILL VALIDATION FAILED:", file=sys.stderr)
        for e in errors: print("  - "+e, file=sys.stderr)
        return 1
    print(f"validated {len(skills)} skills — OK")
    return 0

def cmd_symlinks():
    dest = os.path.join(ROOT, ".claude", "skills")
    if os.path.islink(dest):
        os.unlink(dest)
    os.makedirs(dest, exist_ok=True)
    # clear old symlinks
    for e in os.listdir(dest):
        fp = os.path.join(dest, e)
        if os.path.islink(fp):
            os.unlink(fp)
    n = 0
    for s in collect():
        name = s["fm"].get("name") or os.path.basename(s["reldir"])
        target = os.path.relpath(s["reldir"], os.path.join(".claude","skills"))
        link = os.path.join(dest, name)
        os.symlink(target, link); n += 1
    print(f"  linked {n} skills -> .claude/skills/")
    return 0

def cmd_catalog():
    skills = collect()
    by_domain = {}
    for s in skills:
        by_domain.setdefault(s["fm"].get("domain","(none)"), []).append(s)
    # CATALOG.md
    out = ["# Ronin skills catalog", "",
           f"> Generated by `adapters/gen_index.py`. **Do not edit by hand.** {len(skills)} skills.",
           "", "For authorized security practice only (CTF/lab + bug-bounty + defensive).", ""]
    for d in DOMAINS:
        items = by_domain.get(d)
        if not items: continue
        out.append(f"## {DOMAIN_TITLES.get(d,d)} (`{d}`)")
        out.append("")
        out.append("| skill | type | modes | severity | summary |")
        out.append("|---|---|---|---|---|")
        for s in sorted(items, key=lambda x: x["fm"].get("name","")):
            fm = s["fm"]
            modes = ",".join(fm.get("modes") or [])
            out.append(f"| `{fm.get('name','')}` | {fm.get('type','')} | {modes} | {fm.get('severity','')} | {short_desc(fm)} |")
        out.append("")
    open(os.path.join(ROOT,"CATALOG.md"),"w",encoding="utf-8").write("\n".join(out))
    # data/skills_index.json
    os.makedirs(os.path.join(ROOT,"data"), exist_ok=True)
    idx = [{k:s["fm"].get(k) for k in ["name","domain","type","stability","modes","severity","owasp","owasp_llm","owasp_api","mitre","cwe"]} | {"path": s["reldir"]} for s in skills]
    json.dump({"count":len(skills),"skills":idx}, open(os.path.join(ROOT,"data","skills_index.json"),"w"), indent=2)
    print(f"  wrote CATALOG.md ({len(skills)} skills) + data/skills_index.json")
    return 0

def cmd_index():
    """Compact domain-grouped index for embedding in AGENTS.md/GEMINI.md."""
    skills = collect()
    by_domain = {}
    for s in skills:
        by_domain.setdefault(s["fm"].get("domain","(none)"), []).append(s)
    lines = []
    for d in DOMAINS:
        items = by_domain.get(d)
        if not items: continue
        lines.append(f"**{DOMAIN_TITLES.get(d,d)}** (`{d}`)")
        for s in sorted(items, key=lambda x: x["fm"].get("name","")):
            fm = s["fm"]
            lines.append(f"- `{fm.get('name','')}` — {short_desc(fm)}")
        lines.append("")
    sys.stdout.write("\n".join(lines))
    return 0

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "all":
        return cmd_symlinks() or cmd_catalog()
    return {"symlinks":cmd_symlinks,"catalog":cmd_catalog,"index":cmd_index,"validate":cmd_validate}.get(cmd, lambda:2)()

if __name__ == "__main__":
    sys.exit(main())
