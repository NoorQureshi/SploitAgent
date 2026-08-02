#!/usr/bin/env python3
"""
Ronin local advisor — drive a LOCAL model (Ollama / LM Studio / any OpenAI-compatible
endpoint) with the Ronin framework loaded as its system prompt. Fully offline, no deps
beyond the Python standard library.

This is *advisor mode*: the model guides you through the box using Ronin's methodology,
roles, and skills — it does NOT execute commands. You run them and paste results back.
(For a local model that runs commands itself, point Codex at your local endpoint —
see docs/LOCAL-MODELS.md.)

Authorized lab practice only (HTB / TryHackMe / Pro Labs / CPTS-OSCP).

Usage:
  python3 adapters/local/ronin-advisor.py --provider ollama   --model qwen2.5-coder:14b
  python3 adapters/local/ronin-advisor.py --provider lmstudio --model <loaded-model-name>
  python3 adapters/local/ronin-advisor.py --base-url http://host:port/v1 --model <m> --api-key <k>

In-session commands:
  /skill <name>   inject a skill file (e.g. /skill tools-recon) as extra context
  /skills         list available skills
  /reset          clear the conversation (keeps the system prompt)
  /save <file>    write the transcript to a file
  /quit           exit
"""
import argparse, json, os, sys, urllib.request, urllib.error

PROVIDERS = {
    "ollama":   {"base_url": "http://localhost:11434/v1", "api_key": "ollama"},
    "lmstudio": {"base_url": "http://localhost:1234/v1",  "api_key": "lm-studio"},
}
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def load_system_prompt():
    # Prefer the generated single-agent brain; fall back to composing from source.
    for p in (os.path.join(ROOT, "AGENTS.md"), os.path.join(ROOT, "GEMINI.md")):
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                return f.read()
    meth = os.path.join(ROOT, "framework", "methodology.md")
    if os.path.isfile(meth):
        with open(meth, encoding="utf-8") as f:
            return f.read()
    sys.exit("Could not find AGENTS.md or framework/methodology.md — run ./adapters/build.sh all first.")

def list_skills():
    sk = os.path.join(ROOT, "framework", "skills")
    return sorted(d for d in os.listdir(sk) if os.path.isdir(os.path.join(sk, d)))

def load_skill(name):
    p = os.path.join(ROOT, "framework", "skills", name, "SKILL.md")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()

def chat(base_url, api_key, model, messages, timeout=600):
    body = json.dumps({"model": model, "messages": messages, "temperature": 0.2, "stream": False}).encode()
    req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", data=body,
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + api_key})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return data["choices"][0]["message"]["content"]

def main():
    ap = argparse.ArgumentParser(description="Ronin local advisor (Ollama / LM Studio / OpenAI-compatible)")
    ap.add_argument("--provider", choices=list(PROVIDERS), help="ollama | lmstudio")
    ap.add_argument("--base-url", help="OpenAI-compatible base URL (e.g. http://localhost:11434/v1)")
    ap.add_argument("--api-key", help="API key (any string for local servers)")
    ap.add_argument("--model", required=True, help="model name loaded in the local server")
    args = ap.parse_args()

    prov = PROVIDERS.get(args.provider, {})
    base_url = args.base_url or prov.get("base_url")
    api_key = args.api_key or prov.get("api_key") or "local"
    if not base_url:
        sys.exit("Specify --provider ollama|lmstudio or --base-url.")

    system = load_system_prompt() + (
        "\n\n---\nYou are running as a LOCAL ADVISOR. You cannot execute commands yourself — "
        "give the operator the exact next command (with a one-line flag gloss and why), then wait "
        "for them to paste the output before continuing. Enforce the scope rule strictly: refuse to "
        "proceed until the operator confirms the target is an authorized lab. Keep notes in the "
        "five-beat teaching style.")
    messages = [{"role": "system", "content": system}]

    print(f"🥷 Ronin advisor · {base_url} · model={args.model}")
    print("   advisor mode: I guide, you run the commands. Authorized labs only.")
    print("   commands: /skill <name>  /skills  /reset  /save <file>  /quit\n")
    while True:
        try:
            line = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); break
        if not line:
            continue
        if line in ("/quit", "/exit"):
            break
        if line == "/reset":
            messages = messages[:1]; print("[conversation reset]"); continue
        if line == "/skills":
            print("  " + "  ".join(list_skills())); continue
        if line.startswith("/skill "):
            name = line.split(None, 1)[1].strip()
            content = load_skill(name)
            if content is None:
                print(f"[no such skill: {name}] try /skills"); continue
            messages.append({"role": "user", "content": f"Reference skill '{name}':\n\n{content}"})
            print(f"[injected skill: {name}]"); continue
        if line.startswith("/save "):
            fn = line.split(None, 1)[1].strip()
            with open(fn, "w", encoding="utf-8") as f:
                for m in messages[1:]:
                    f.write(f"## {m['role']}\n{m['content']}\n\n")
            print(f"[saved transcript -> {fn}]"); continue

        messages.append({"role": "user", "content": line})
        try:
            reply = chat(base_url, api_key, args.model, messages)
        except urllib.error.URLError as e:
            print(f"[connection error: {e.reason}]")
            print(f"[is the local server running? ollama: `ollama serve` · LM Studio: start the local server]")
            messages.pop(); continue
        except Exception as e:
            print(f"[error: {e}]"); messages.pop(); continue
        messages.append({"role": "assistant", "content": reply})
        print(f"\nronin> {reply}\n")

if __name__ == "__main__":
    main()
