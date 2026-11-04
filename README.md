# Meridian CleanRoom — Attestation Security Lab

Welcome to the Meridian CleanRoom cybersecurity lab!

In this lab, you will investigate a simulated Trusted Execution Environment (TEE) that protects sensitive medical data through attestation.

Your goal is to explore the system, identify security weaknesses, and capture flags.

## Prerequisites

Before starting, install:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/downloads)
- [GitHub CLI](https://cli.github.com/)

You will also need a GitHub account.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/tinacheng2/meridian-cleanroom-lab.git
cd meridian-cleanroom-lab
```

### 2. Log In to GitHub

```bash
gh auth login
```

Follow the prompts to authenticate through your browser.

### 3. Configure Your GitHub Username

Your GitHub username will be used as your student identifier.

**Windows PowerShell:**

```powershell
"GITHUB_USERNAME=$(gh api user --jq '.login')" | Set-Content .env
```

**macOS/Linux:**

```bash
echo "GITHUB_USERNAME=$(gh api user --jq '.login')" > .env
```

### 4. Start Docker

Make sure Docker Desktop is running.

```bash
docker compose pull site
docker compose up -d --build
```

### 5. Open Meridian CleanRoom

Visit:

http://localhost:8080

### 6. Open the Player Terminal

```bash
docker compose exec player sh
```

The player terminal provides `curl` and `jq` for interacting with the server.

---

## Communicating with the Server

Meridian CleanRoom provides an HTTP API.

Inside the player container, the server is available at:

```text
http://site:8080
```

You can use the `$SITE` environment variable instead of typing the full address.

### Basic Commands

**Request a challenge:**

```bash
curl -s "$SITE/stage/1/challenge" | jq
```

**Request an attestation quote:**

```bash
curl -s "$SITE/stage/1/quote?nonce=VALUE&workload=allowed" | jq
```

Replace `VALUE` with the nonce provided by the server.

**Save a response to a file:**

```bash
curl -s "$SITE/stage/1/challenge" > challenge.json
```

**Display saved JSON:**

```bash
jq . challenge.json
```

**Extract a specific field:**

```bash
jq -r '.nonce' challenge.json
```

**Submit JSON to the server:**

```bash
curl -s -X POST "$SITE/stage/1/verify" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}' | jq
```

Replace the sample JSON with the data required by the endpoint.

### API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/stage/<stage>/challenge` | GET | Request a challenge nonce |
| `/stage/<stage>/quote` | GET | Request an attestation quote |
| `/stage/<stage>/verify` | POST | Submit an attestation quote |
| `/captured-quote` | GET | Retrieve captured attestation evidence |
| `/stage/4/firmware/status` | GET | View platform firmware status |
| `/stage/4/firmware/archive` | GET | Examine archived firmware |
| `/stage/4/firmware/install` | POST | Submit a firmware package |

Some endpoints behave differently depending on the stage.

---

## Lab Challenges

### Stage 1 — Valid Quote

Explore how attestation quotes are generated and verified.

**Objective:** Submit a valid quote and obtain the Stage 1 flag.

### Stage 2 — Replay Attack

Investigate how the verifier handles previously captured attestation evidence.

**Objective:** Find a way to reuse an earlier quote.

### Stage 3 — Measurement Bypass

Explore how the verifier checks workload measurements.

**Objective:** Determine whether an unauthorized workload can pass verification.

### Stage 4 — TCB Rollback

Meridian CleanRoom recently updated its platform, but some security policies may be outdated.

**Objective:** Investigate whether outdated firmware can be used to bypass attestation security.

---

## Flags

Each stage contains a flag formatted as:

```text
CTF{stage1_...}
CTF{stage2_...}
CTF{stage3_...}
CTF{stage4_...}
```

Flags are personalized using your configured GitHub username.

Record the flags you obtain during the lab. These locally generated flags serve as challenge-completion indicators; your instructor will explain how submissions are assessed.

## Submissions

For each completed stage, submit:

- Your GitHub username
- Stage number
- Captured flag
- A brief explanation of your approach
- Relevant terminal output showing your result

Follow your instructor's directions for submission.

---

## Troubleshooting

**Check running containers:**

```bash
docker compose ps
```

**View server logs:**

```bash
docker compose logs site
```

**Restart the lab:**

```bash
docker compose down
docker compose up -d
```

**Stop and remove the lab containers:**

```bash
docker compose down
```

**Check your GitHub login:**

```bash
gh auth status
```

**Check your configured username:**

Windows PowerShell:

```powershell
Get-Content .env
```

macOS/Linux:

```bash
cat .env
```

If `gh` is not recognized after installation, close and reopen your terminal.

---

## Lab Rules

This lab is intended for cybersecurity education.

The environment uses simulated attestation and synthetic medical data.

Perform testing only against the provided Meridian CleanRoom Docker environment. Do not attempt these techniques against systems without authorization.