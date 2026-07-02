[![GitHub license](https://img.shields.io/github/license/marlof/ScORCH)](https://github.com/marlof/ScORCH/blob/master/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/marlof/ScORCH)](https://github.com/marlof/ScORCH/issues) [![CI](https://github.com/marlof/ScORCH/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/marlof/ScORCH/actions/workflows/ci.yml)

# ScORCH

**Auditable job orchestration in pure bash. No agents, no database, no daemons to babysit.**

ScORCH turns your existing scripts into controlled, repeatable, audited jobs that anyone on the team — or any upstream system — can trigger safely. It records *who* ran *what*, *when*, with *which parameters*, and *what happened*: the evidence trail that SOX Section 404 and change-management audits actually ask for.

> *"Simplicity is a great virtue but it requires hard work to achieve it and education to appreciate it."* — Edsger W. Dijkstra

## Why ScORCH?

Most orchestration tools want to own your world: an agent on every host, a database, a message bus, a web of YAML. ScORCH takes the opposite bet:

- **The filesystem is the database.** Jobs are files. Job *states* are symlink directories (`new/`, `queued/`, `running/`, `failed/`, `manual/`...). State transitions are atomic `mv` operations. Your monitoring tool is `ls`.
- **Human-in-the-loop is a first-class state.** Jobs can pause in `manual/` and wait for a person to approve, fix, or intervene — not an afterthought bolted onto a fire-and-forget engine.
- **Bring your own tools.** ScORCH doesn't care whether you deploy with Ansible, provision with Terraform, or manage config with Puppet. It orchestrates *around* them and keeps the audit trail they don't.
- **One dependency: bash 4+.** No build step. Runs on anything from a production RHEL estate to a Raspberry Pi.

Born in financial-sector release management before "DevOps" had a name, refined across government and enterprise estates since.

## Quick start

Install the latest version into the current directory:

```bash
wget https://s3.eu-west-2.amazonaws.com/autoscorchdownload.com/install && chmod a+x install && ./install
```

Run `./scorch`, press **`n`** (new job), and ScORCH loads the available plugins:

```
    INSTALL:        AZURECLI        OK
    INSTALL:       TERRAFORM        OK
      LOCAL:         VAGRANT        OK
       TEST:            TEST        OK

 help <plugin>    at any time for additional parameters
 info <plugin>    for further information
```

Paste a request template (the `.` on its own line terminates input):

```
Action : DRINK-TEA
Size   : Mug
Milk   : 1
.
```

That's a job. Select it by number and you get the full context menu:

```
Amend rules | Copy | View | Edit | Log | tail | Queue | Tasks | Delete | Filter | eXit :
```

**`Tasks`** shows what the job will do before you queue it. **`Queue`** hands it to the dispatcher. **`Log`** shows what happened. Start with the DEMO plugins — `DRINK-TEA` is a safe end-to-end walkthrough.

## How it works

```
 request        job file           dispatcher          outcome
 (template) --> jobs/active/  -->  jobs/queued/  -->  jobs/completed/
                     |                  |              jobs/failed/ --> jobs/fixing/
                jobs/new/          jobs/running/       jobs/manual/  (human gate)
                (symlink)          (symlink)
```

A job is a self-contained file in `jobs/active/`. Its lifecycle state is expressed as a symlink in exactly one state directory at a time. The dispatcher picks up `queued/` jobs; failures land in `failed/` and move to `fixing/` once acknowledged; anything needing a human waits in `manual/`. Every transition is logged with timestamp and user.

Because state is just files and symlinks:

- `ls jobs/failed/` is your incident queue
- `grep` is your job search
- backup/restore is `tar`
- completed history feeds `jobs.csv`, queryable with the bundled `scorchdb` CMDB tool

## Plugins

Plugins convert a request template into an ordered task list. They live in `plugins/<GROUP>/SP_<NAME>` and are plain bash — if you can write a script, you can write a plugin. Ready-made examples ship in `plugins/DEMO/` (tea-making to Kafka), `plugins/INSTALL/` (Terraform, Azure CLI, Java, Nexus) and `plugins/PI/` (PiVPN, OpenCanary).

Site-specific plugins go in `plugins/CUSTOM/` and survive upgrades. Plugin loading includes a security scan that flags dangerous patterns (`curl | sh`, unguarded `rm -rf`, raw `eval`) before anything is sourced.

Triggering from CI or other systems uses the same engine, headless:

```bash
scorch -a JBOSS -o "RELEASE:6.4" -o "ENVIRONMENT:PROD-STG" -s
```

## Directory structure

```
scorch/
+--bin/            Utility scripts (scorchdb, netboxq, qjira, keepsafe, ...)
+--etc/            Config, users, motd
+--functions/      ScORCH function library
+--jobs/
|  +--active/      The job files themselves
|  +--new/ queued/ running/ completed/ failed/ fixing/
|  +--manual/ pending/ starting/ archived/ deleted/
|                  One symlink per job, one state at a time
+--plugins/
|  +--DEMO/ INSTALL/ LOCAL/ PI/
|  +--CUSTOM/      Your site-local plugins (upgrade-safe)
+--projects/       Obrar project spaces (common/ + per-project)
+--python/         Faster job-listing helpers
+--var/            Logs, locks, job history (jobs.csv)
```

## The suite

| Tool | Purpose |
|------|---------|
| `scorch` | Interactive TUI + headless CLI job orchestration |
| `obrar` | Deployment framework driven from project spaces (`projects/`) |
| `bin/scorchdb` | Query completed-job history as a CSV database |
| `bin/keepsafe` | Encrypted credential storage (OpenSSL) |
| `bin/*` | Helpers: Jira, NetBox, MS Teams notifications, AWS lookups |

## Open source vs Enterprise

The open-source release (Apache 2.0) is the single-script `scorch` with embedded functions — everything described above. The Enterprise edition (see `EnterpriseLicense.txt`) adds authentication/security, audit and report modules, alternative paths, and admin tooling, delivered as a tar with the fully commented function library. Details: [autoscorch.com](http://www.autoscorch.com).

## Requirements

- bash 4+
- Standard POSIX userland (awk, grep, sed)
- That's it. No root required for a per-user install.

## Contributing

Issues and PRs welcome. Run `shellcheck` and `tests/` before submitting; the house style is documented in the `scorch` header (Hungarian-notation variable prefixes: `str_`, `b_`, `fn_`, `dir_`, `file_`).
