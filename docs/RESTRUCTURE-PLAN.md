# Ronin Restructure Plan — from CTF framework to the hacking-skills library

> Status: **proposal / for review.** Nothing here is built yet. This is the agreed
> shape before we touch `framework/`.
> Decisions locked with the maintainer: **dual-mode** (CTF/lab + bug-bounty),
> **offensive + defensive** breadth, **keep the multi-CLI portable core**.

## 1. Vision & positioning

Ronin becomes **the** organized, contributable, multi-CLI library of security skills —
the place an AI operator (Claude Code, Codex, Gemini, or a local model) loads *how to
actually do the work* for CTFs, bug bounty, and blue-team tasks.

Why Ronin wins over the reference repos:

| Repo | Strength | Gap Ronin closes |
|---|---|---|
| `0xN0RMXL/BugBountySkills` | Great offensive taxonomy, 600+ files | Not real Agent-Skills (no SKILL.md contract), single-tool, no validation |
| `transilienceai/communitytools` | OWASP/MITRE mapping, validation framework | Heavy, project-coupled, Claude-centric |
| `sickn33/agentic-awesome-skills` | Scale + JSON-schema validation + catalog | General-purpose; security is a thin slice, no engagement methodology |

**Ronin's edge (keep and lean into):**
1. **Tool-neutral core** compiled to `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` + local model — nobody else is portable.
2. **Locked-core vs learning-library** — curated methodology stays stable while the technique library grows safely.
3. **Teach-the-mechanism** house voice — skills explain *why*, not just *what*.
4. **Scope discipline first** — now extended to a real dual-mode authorization model.

## 2. Design principles (non-negotiables)

- **One source of truth.** Everything lives in `framework/`; entry files are generated. Never edit generated files.
- **Domain taxonomy, not a flat list.** The current flat `tools-*`/`tech-*` naming does not scale to hundreds of skills.
- **The skill *type* is metadata, not a filename prefix.** Arsenal / technique / methodology / checklist / reference become frontmatter fields.
- **Every skill is schema-validated.** A versioned JSON schema + CI gate keeps contributions consistent and the library upgradeable.
- **Generated indexes are generated, not hand-maintained.** Catalog, coverage matrices, and discovery symlinks are build outputs.
- **Portable first.** Any new mechanism must survive the compile to Codex/Gemini/local, not just Claude.

## 3. The dual-mode safety model (the new #1 rule)

The hard rule stops being "labs only" and becomes **"operate only inside a confirmed
authorization envelope, and the envelope type is explicit."**

Two modes, each with its own boundary artifact:

- **CTF/lab mode** — boundary is `scope.txt` (lab VPN ranges: `10.129.x.x`, `10.10.x.x`, declared exam range). Unchanged discipline.
- **Bug-bounty mode** — boundary is a **program scope + rules of engagement**: `scope.txt` (in-scope domains/assets, explicit out-of-scope), `roe.md` (rate limits, allowed test types, no-DoS, disclosure policy, safe-harbor link). Ronin refuses to act on any asset not matched by in-scope patterns, and honors out-of-scope as a hard block.

Every skill declares which modes it is valid in (`modes: [ctf, bugbounty, defense]`), so
a destructive lab technique never auto-loads during a live bug-bounty engagement, and
defensive skills are clearly separated from offensive ones.

## 4. Proposed repository structure

```
ronin/
  ronin                         ← CLI: doctor · install · build · validate · catalog · start · local · new · lock
  setup.sh
  framework/                    ← SINGLE SOURCE OF TRUTH
    methodology.md                the loop · dual-mode scope rule · note-taking standard      🔒 locked
    roles/                        phase playbooks (recon·web·ad·privesc·report·learn + bb·defense) 🔒 locked
    skills/
      recon/        <slug>/SKILL.md    passive/active enum, OSINT, subdomains, fingerprinting
      web/          <slug>/SKILL.md    XSS, SQLi, SSRF, SSTI, IDOR, auth, deserialization…
      api/          <slug>/SKILL.md    REST/GraphQL/gRPC, BOLA, mass assignment
      mobile/       <slug>/SKILL.md    Android/iOS
      cloud/        <slug>/SKILL.md    AWS/GCP/Azure, K8s, containers
      network/      <slug>/SKILL.md    services, pivoting, tunneling
      ad/           <slug>/SKILL.md    Active Directory / Kerberos
      ai-ml/        <slug>/SKILL.md    LLM/AI attacks (prompt injection, jailbreak, extraction)
      code-review/  <slug>/SKILL.md    SAST, secrets, language-specific sinks
      exploit-dev/  <slug>/SKILL.md    PoC, chaining, impact amplification
      privesc/      <slug>/SKILL.md    Linux + Windows local privesc
      defense/      <slug>/SKILL.md    detection-engineering, hardening, DFIR/IR   ← defensive breadth
      payloads/     <slug>/SKILL.md    polyglots, WAF bypass, wordlist pointers
      reporting/    <slug>/SKILL.md    writeups, H1/Bugcrowd templates, CVSS
      automation/   <slug>/SKILL.md    pipelines, nuclei templates, monitoring
      tradecraft/   <slug>/SKILL.md    htb-insane discipline, scope/RoE, rabbit-holes
      _templates/                      per-type SKILL.md templates
  schemas/
    skill.schema.json             ← versioned skill contract (validation source)
  adapters/
    build.sh                      → entry files + discovery symlinks + catalog
    local/ronin-advisor.py
  bin/
    lock.sh · unlock.sh
    migrate/                      ← schema migration scripts (upgradeability)
  docs/
    SETUP · HOW-TO-CTF · HOW-TO-BUGBOUNTY · LOCAL-MODELS · SCHEMA · CONTRIBUTING-SKILLS
  CATALOG.md                     ← GENERATED (git-ignored), browsable index
  data/                          ← GENERATED (git-ignored): skills_index.json, coverage.json
  CLAUDE.md   .claude/           ← GENERATED entry file + discovery symlinks
  AGENTS.md   GEMINI.md          ← GENERATED entry files
```

**Nested-canonical + flat-discovery.** Skills live nested by domain (browsable, scalable).
`build.sh` generates flat discovery symlinks under `.claude/skills/<name>` pointing at the
canonical nested files, so Claude Code discovery still works. Slugs are **domain-prefixed**
(`web-ssrf-gopher-redis-rce`, `recon-subdomain-enum`) so names stay globally unique and greppable.

## 5. Skill file contract (the upgradeable schema)

Every `SKILL.md` opens with validated frontmatter:

```yaml
---
name: web-ssrf-gopher-redis-rce        # globally unique, domain-prefixed slug
description: >                          # the auto-load trigger line — concrete signals
  SSRF → internal unauth Redis → RCE via gopher://. Load when SSRF is confirmed and
  Redis/6379 is reachable. …
domain: web                            # one of the taxonomy folders
type: technique                        # technique | arsenal | methodology | checklist | reference
stability: learning                    # locked | learning
modes: [ctf, bugbounty]                # ctf | bugbounty | defense
severity: high                         # optional (bug-bounty triage)
owasp: [A10:2021-SSRF]                  # optional mappings ↓ power the coverage matrix
owasp_llm: []
mitre: [T1190]
cwe: [CWE-918]
tools: [curl, redis-cli]
learned_on: AEGIS                       # optional provenance
schema_version: 1
---
```

Body sections standardized per type (enforced softly by template, checked by linter):
`When it applies · Why it works (mechanism) · Method (exact commands + flag gloss) ·
Gotchas / what fails · Verify success · References`.

`schema_version` + `schemas/skill.schema.json` + `bin/migrate/` make future format changes
a mechanical upgrade instead of a manual rewrite.

## 6. Cross-cutting indices (generated)

- **`CATALOG.md`** — the human-browsable table of every skill (domain, type, modes, triggers). Generated by `ronin catalog`, git-ignored.
- **Coverage matrix** — OWASP Top 10 / OWASP LLM Top 10 / MITRE ATT&CK / CWE Top 25 coverage computed from frontmatter mappings (transilience's best idea). Rendered as badges + a docs page.
- **`ATTACK_INDEX`** — maps an attack/vuln class → the skills that cover it, for fast routing.
- **`data/skills_index.json`** — machine index for the CLI, MCP, and any future web catalog.

## 7. Contribution & automation

- **`ronin new skill --domain web --type technique --slug ssrf-...`** scaffolds from the right `_templates/` file.
- **`ronin validate`** runs the JSON-schema check + section linter locally; **CI runs the same** and fails on drift or invalid frontmatter.
- **Generated ≠ committed.** Entry files (`CLAUDE.md`/`AGENTS.md`/`GEMINI.md`) stay committed (users need them on clone). Heavy indexes (`CATALOG.md`, `data/*.json`, discovery symlinks) are generated + git-ignored, so PRs stay source-only and never conflict on generated noise.
- **Issue/PR templates + labels** (`good-first-skill`, `domain:web`, `needs-mechanism`) to make contributing obvious.
- **Locked-core rule preserved:** methodology, roles, and reference arsenals require `bin/unlock.sh` + explicit PR rationale; the technique library is the open, welcoming contribution path.

## 8. Multi-CLI compile changes

`build.sh` extends to: walk the nested taxonomy, emit the same three entry files, generate
discovery symlinks, and produce the catalog/index. The single-agent entry files (Codex/Gemini/local)
get a **skills index by domain** instead of the current flat list; Claude gets subagents +
Skill tool as today. Portability stays the acceptance test for any new mechanism.

## 9. Migration of the existing 8 skills (Phase 0, no content loss)

| Today | New home | type / stability |
|---|---|---|
| `tools-recon` | `recon/recon-arsenal` | arsenal / locked |
| `tools-web` | `web/web-arsenal` | arsenal / locked |
| `tools-privesc` | `privesc/privesc-arsenal` | arsenal / locked |
| `tools-ad-pivot` | `ad/ad-pivot-arsenal` | arsenal / locked |
| `htb-insane` | `tradecraft/htb-insane` | methodology / locked |
| `tech-gopher-redis-rce` | `web/web-ssrf-gopher-redis-rce` | technique / learning |
| `tech-mongo-agg-facet-bypass` | `api/api-mongo-agg-facet-bypass` | technique / learning |
| `tech-webauthn-software-authenticator` | `web/web-webauthn-software-authenticator` | technique / learning |
| `roles/htb-*` | `roles/` (unchanged, + new `bb`, `defense` roles) | methodology / locked |

Each migrated file gains the new frontmatter fields; body content is preserved.

## 10. Phased roadmap

- **Phase 0 — Foundations.** Add `schemas/skill.schema.json`, `_templates/`, taxonomy folders; migrate the 8 existing skills; extend `build.sh` (nested walk + symlinks + catalog); add `ronin validate` / `ronin catalog`; wire CI. *Outcome: same content, new backbone, green CI.*
- **Phase 1 — Dual-mode safety.** Update `methodology.md` + roles for CTF vs bug-bounty envelopes; add `roe.md`/program-scope handling; add `modes` gating. Add `docs/HOW-TO-BUGBOUNTY.md`.
- **Phase 2 — Seed content.** Author/adapt core skills across every domain (web, api, recon, cloud, ai-ml, defense…) so each folder is credibly populated. Prioritize OWASP Top 10 + LLM Top 10 coverage.
- **Phase 3 — Indices & automation.** ATTACK_INDEX, coverage matrix + badges, richer CI (mapping validation, dead-link checks).
- **Phase 4 — Fame layer.** README revamp with live catalog table + coverage badges; GitHub Pages docs site; issue/PR templates + `good-first-skill`; Discussions; launch posts.

## 11. Open questions to resolve before Phase 0

1. Domain-prefixed slugs vs bare slugs (recommend prefixed for uniqueness/grep).
2. Whether `defense` is one folder or splits into `detection` / `hardening` / `dfir`.
3. Keep committing `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` (recommend yes) vs generate-on-setup.
4. Bring in an MCP CVE-enrichment server (transilience-style) now or defer to a later phase.
