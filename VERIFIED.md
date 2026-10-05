# Cloud demo verification

Verified at 2026-10-05T13:58:38.364026+00:00 in GitHub Codespaces using its default Docker-enabled environment.

Image: `sha256:9617f7e8df6bf92ef431ac8897ef813fa574aa8e5674746fc55ca0e71639ae1c`

```text
PASS: packaged model smoke test
PASS: runtime environment flag and env file
PASS: bind-mounted input and persistent output
PASS: port mapping, health, API predictions and invalid input
ALL DEMO CHECKS PASSED
```

Cache demo: dependency installation stayed cached after a source change; source copy rebuilt; original source was restored. The private HTTP demo is served on container port 8000, mapped to host port 8080.

The small CPU model is illustrative; GPU execution and production deployment were not tested.
