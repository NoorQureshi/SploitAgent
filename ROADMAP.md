# Roadmap & help wanted

Ronin grows through contributions. This is the running list of skills we'd love to add — pick
one, write it (see [CONTRIBUTING.md](CONTRIBUTING.md)), open a PR. Struck-through items are done.

**New to contributing?** Anything tagged 🟢 is a great first skill — a well-understood, single
technique with plenty of public references.

## Web
- ✅ ~~`web-host-header` — host-header injection (password-reset poisoning, routing, cache)~~
- ✅ ~~`web-clickjacking` — framing/UI-redress, and when it's actually impactful~~
- 🟢 `web-open-graph-ssrf` — link-preview/oEmbed SSRF variants
- ✅ ~~`web-websocket` — WebSocket hijacking, message tampering, CSWSH~~
- ✅ ~~`web-rate-limit-bypass` — the many ways rate limits fail (headers, casing, parallelism)~~
- ✅ ~~`web-dependency-confusion` — internal package name takeover~~
- ✅ ~~`web-saml` — SAML assertion/signature-wrapping attacks~~
- `web-dom-clobbering` — DOM clobbering to bootstrap XSS
- `web-postmessage` — cross-window `postMessage` origin flaws

## API
- ✅ ~~`api-versioning` — old/shadow API versions that skipped a fix~~
- `api-websocket` — realtime/subscription authz

## Mobile
- ✅ ~~`mobile-ios-assessment` — iOS static + dynamic (Frida, keychain, IPA)~~
- ✅ ~~`mobile-webview` — Android/iOS WebView JS-bridge & file-access abuse~~

## Cloud
- ✅ ~~`cloud-gcp` — GCP-specific privesc & misconfig depth~~
- ✅ ~~`cloud-azure` — Entra ID / Azure RBAC attacks~~
- ✅ ~~`cloud-docker-registry` — exposed/unauth registries and image secrets~~

## AI / LLM
- ✅ ~~`ai-llm-dos` — unbounded-consumption / cost-amplification (LLM10)~~
- ✅ ~~`ai-supply-chain` — poisoned models/datasets/plugins (LLM03/LLM05)~~

## Code review
- ✅ ~~`code-review-python`, `code-review-nodejs`, `code-review-java`, `code-review-php`,~~
  `code-review-go` — per-language sink/idiom guides
- `code-review-iac` — Terraform/CloudFormation/K8s manifest review
- ✅ ~~`code-review-cicd` — pipeline & GitHub Actions security (poisoned workflows, secrets)~~

## Recon / OSINT
- ✅ ~~`recon-cloud-assets` — finding an org's cloud footprint (buckets, apps, IP ranges)~~
- 🟢 `recon-github-leaks` — deep GitHub/org code-leak hunting

## Defense (blue team)
- ✅ ~~`defense-threat-modeling` — STRIDE/attack-tree modeling for a design~~
- ✅ ~~`defense-log-analysis` — hunting in logs (auth, web, cloud) with concrete queries~~
- ✅ ~~`defense-purple-team` — turning each offensive skill into a detection test~~

## Exploit dev / RE
- `exploit-binary-basics` — intro binary exploitation workflow (pwntools)
- `re-methodology` — reverse-engineering a binary for a bug

## Proposed new domains (need a taxonomy addition — open an issue first)
- `crypto` — cryptographic attacks (padding oracle, weak randomness, JWT-adjacent)
- `smart-contracts` — Solidity/EVM auditing (reentrancy, access control)
- `social-engineering` — phishing infra & pretexting **(authorized engagements only)**

## Library / tooling
- Per-skill `references/` deep-dives (payloads, cheat-sheets) where a `SKILL.md` gets long
- A `checklist`-type skill per domain (see `web-testing-checklist` as the pattern)
- Coverage gaps: see [COVERAGE.md](COVERAGE.md) for which standards are thin

---
Want something not listed? Open an issue describing the technique and its trigger signals.
