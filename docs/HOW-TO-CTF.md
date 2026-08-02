# How to do a CTF with Ronin

A skimmable playbook for working a box with **Ronin**, the tool-agnostic CTF/HTB
AI-assistant framework. This assumes you've finished setup (see
[SETUP.md](./SETUP.md)) and have your tool open in the repo.

**Authorized-lab practice only.** Ronin is built for HackTheBox, TryHackMe, Pro
Labs, and CPTS/OSCP exam environments — nothing else.

---

## 0. The one rule: scope

Ronin only ever acts against a target you have **confirmed is authorized** — a lab
VPN range such as `10.129.x.x` / `10.10.x.x`, or a declared exam range.

Before you start:

```bash
sudo openvpn lab.ovpn          # connect the lab VPN first
# then spawn the box in the HTB/THM web UI and confirm it's up
ping -c1 10.129.x.x            # sanity-check reachability
```

When you kick off the engagement, **tell the agent the target IS your authorized
lab**. It records it in `<box>/scope.txt` and treats that file as a hard boundary
for every phase and every sub-agent. Never point Ronin at production, third-party,
or public infrastructure — if a target isn't clearly in a lab range, the agent
stops and asks you to confirm before it does anything.

---

## 1. Start a box

In the repo, launch your tool:

```bash
claude          # or: codex   |   gemini   |   the local advisor
```

Then give it a prompt in roughly this shape:

> "Let's work an HTB box, target `10.129.x.x` — it's my authorized lab. Set up the
> engagement and start."

The agent scaffolds the box directory for you:

```
<box>/
  scope.txt      # the confirmed target — the boundary
  notes.md       # timestamped teaching log — source of truth for the report
  state.md       # live status: ports, creds, foothold, current lead
  rabbitholes.md # dead-ends + why each was ruled out
  recon/ web/ loot/ screenshots/ ...
```

---

## 2. The loop (what actually happens)

Ronin walks these phases. Your job at each is to **approve actions and steer the
next lead**.

1. **Enumerate** *(recon role)* — port/service scan + per-service enum → a
   prioritized lead list. *You:* pick which lead to chase first.
2. **Attack surface** — leads get routed by type:
   - web services → **web role**
   - Active Directory / domain → **ad role**
   - everything else → worked directly with the matching `tools-*` skill.
3. **Foothold** — get a shell, stabilize it, grab the **user flag**.
4. **Escalate** *(privesc role)* — hunt root / SYSTEM.
5. **Multi-host / pivot** — enumerate internal reachability, then repeat steps 1–4
   for each internal host.
6. **Report** *(report role)* — compile `notes.md` → `report.md`.

**Working principle:** when stuck, the answer is almost always *enumerate more*.

**Pace.** Default is **one lead at a time** — the agent proposes, you approve. Say
*"work it fully autonomously"* to let it run the loop on its own. Even autonomous,
it stays scope-bounded and still asks before high-impact or irreversible actions.

---

## 3. Working with the agent well

- **Approve / deny each tool action.** The agent explains every command's flags and
  *why that tool* over the alternatives — read those, that's the learning.
- **`notes.md` is a teaching log**, not a command dump. Every step follows the
  five beats:

  ```
  1. Goal / why now      — what you're trying to learn, and what pointed you here
  2. Tool & exact syntax — the command + a one-line gloss of the flags that matter
  3. Result              — the relevant output, trimmed
  4. Why it worked       — the mechanism (why the IDOR exists, why the cap = root)
  5. Next lead           — the single concrete action this unlocks
  ```

  Read it to understand *why the box fell*, not just that it did.
- **Dead-ends go in `rabbitholes.md`** with the reason each was ruled out — so you
  never re-walk them.
- **Multi-tool note:** parallel sub-agents run only in Claude Code. In
  Codex / Gemini / the local advisor it's **one agent doing the phases
  sequentially** — same playbook, same roles, just not concurrent.

---

## 4. Capturing new skills (the learning loop)

**This is what makes Ronin get sharper every box.** When a box teaches a reusable
technique, tell the agent:

> "capture this as a skill"

The **learn role** writes a new skill from `TECHNIQUE-TEMPLATE.md`, tagged with the
**trigger signals** that should auto-apply it later, and indexes it:

```
framework/skills/tech-<slug>/SKILL.md   # the new technique
framework/skills/README.md              # index entry (auto-updated)
```

Then rebuild so every tool picks it up:

```bash
./adapters/build.sh all
```

**Know the two halves of the framework — the distinction matters:**

- **Locked core** — the methodology, the roles, and the reference skills
  (`tools-*`, `htb-insane`). This is **stable**. Don't edit it mid-engagement.
  `bin/lock.sh` can make it read-only so you can't corrupt it by accident.
- **Learning library** (`framework/skills/tech-*`) — the **only** part that grows
  during CTFs.

So the framework gets smarter each box **without ever touching its stable core**.

---

## 5. Finishing

- Both flags captured → ask for the report:

  > "compile the report"

  The **report role** turns `notes.md` into `<box>/report.md` — a CPTS/OSCP-style,
  reproducible writeup.
- **Your loot, flags, and notes are gitignored** — they stay local. The only things
  worth committing / PR-ing are **framework improvements**: new `tech-*` skills.

---

## 6. Tips

- **Keep the VPN alive.** If the box goes unreachable mid-run, reset or re-spawn it
  in the web UI, reconnect, and resume — the agent picks up from `state.md`.
- **Big / Insane boxes:** the `htb-insane` skill kicks in with rabbit-hole
  discipline and explicit chaining structure so long paths don't lose the thread.
- Trust the loop: a fresh scan beats guessing at exploits.

---

**See also:** [SETUP.md](./SETUP.md) · [LOCAL-MODELS.md](./LOCAL-MODELS.md)
