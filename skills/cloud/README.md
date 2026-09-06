# Cloud & containers — `cloud` skills

AWS/GCP/Azure and Kubernetes/containers: metadata/IMDS abuse, object-storage misconfig, IAM escalation, exposed control planes.

Add a skill here:
```bash
cp -r skills/_templates/technique.md skills/cloud/<slug>/SKILL.md
# edit frontmatter (domain: cloud) + body, then:
python3 tools/catalog.py
```

Naming: domain-prefixed kebab-case, e.g. `cloud-<thing>`. See the full table in [`CATALOG.md`](../../CATALOG.md).
