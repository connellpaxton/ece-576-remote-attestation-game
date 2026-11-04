# Meridian CleanRoom

Welcome to the Meridian CleanRoom, a simulated Trusted Execution Environment (TEE) that protects sensitive medical data through attestation.

In this excercise, you will learn about the basic components and properties of attestation by verifying yourself with the server.
In each stage you will attest, using insecurities you observe in the server to receive approval whether it should be granted or not.
After gaining access to the system, you will receive a flag to show successful completetion, but for full credit in the rubric, you
must also fully explain how you got to your solution, and provide a fix that will close the security hole.

## Prerequisites

Before starting, install:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/downloads)

The docker container packages all of the other dependencies in the project and ensures a uniform starting point for all players.


## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/connellpaxton/ece-576-remote-attestation-game
cd ece-576-remote-attestation-game
```

### 2. Start Docker

Build and start the local containers; this may take a few minutes the first time.
```bash
docker compose up -d --build
```

If port 8080 is already in use, start the site on another local port, for example `SITE_PORT=8081 docker compose up -d --build`.


### 3. Open the site

Visit:
http://localhost:8080

This will bring you to the faux medical site, which you will attempt to login to. Use `http://localhost:8081` if you selected `SITE_PORT=8081`.

### 4. Open the Player Terminal

The player terminal provides a uniform environment for all of the players.
```bash
docker compose exec player sh
```
It provides `curl` (a program for sending HTTP(S) requests) and `jq` (a program for parsing JSON responses) for interacting with the server.

---

## Communicating with the Server

The Meridian CleanRoom website provides an HTTP API.

Inside the player container, the server is available at:

```text
http://localhost:8080
```
But we can refer to it using the environment variable `$SITE`.

_Note that if the variable is undefined (or you get no response from the following commands), you may have forgotten to enter the docker shell, or ran the commands from the wrong terminal._


### Basic Commands

**Request a challenge:**

```bash
curl -s "$SITE/stage/1/challenge?user=YOUR_NAME" | jq
```

Choose a local name (letters, numbers, dots, underscores, and hyphens; up to 32 characters) and replace `YOUR_NAME`. The response includes the caller's local IP; the name and IP personalize flags for this run. If omitted, the user defaults to `student`.

**Request an attestation quote:**

```bash
curl -s "$SITE/stage/1/quote?nonce=VALUE&workload=allowed" | jq
```

Replace `VALUE` with the nonce provided by the server, and use the same `user` value when requesting a new challenge for each stage.

**Save a response to a file:**

```bash
curl -s "$SITE/stage/1/challenge?user=YOUR_NAME" > challenge.json
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
USER=YOUR_NAME
CHALLENGE=$(curl -fsS "$SITE/stage/1/challenge?user=$USER")
NONCE=$(printf '%s' "$CHALLENGE" | jq -r '.nonce')
QUOTE=$(curl -fsS "$SITE/stage/1/quote?nonce=$NONCE&workload=allowed")
curl -fsS -X POST "$SITE/stage/1/verify" \
  -H "Content-Type: application/json" \
  -d "$QUOTE" | jq
```

Replace `YOUR_NAME` with your chosen local name. Each stage needs its own fresh challenge; the challenge response also shows the local IP used to personalize the flag.

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

Flags are personalized using the user name you choose when requesting a challenge and the local IP address of the requesting client.

Record the flags you obtain during the lab. These locally generated flags serve as challenge-completion indicators; your instructor will explain how submissions are assessed.

## Submissions

For each completed stage, submit:

- Your chosen user name
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

---

## Lab Rules

Any assistance you receive from any tool or other person should be included in your report to the instructor.
