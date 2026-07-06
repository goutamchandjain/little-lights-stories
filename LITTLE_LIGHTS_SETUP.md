# 🌟 Little Lights — Full Setup Reference

## What We Built
A library of **100 stories** for kids ages 2–10, mixing **Religion, Science, Fiction, Drama, and Fun** — sent automatically to WhatsApp every day at 6 AM IST via GitHub Actions + Twilio. No laptop needed.

Every story ends with a **"Think About It"** question written specifically for that story's context, so kids are left to reflect, not just entertained.

---

## Files

| File | Location | Purpose |
|------|----------|---------|
| `stories_library.html` | repo root | Interactive browser app — filter by age & category, search, read stories, copy for WhatsApp |
| `send_story.py` | repo root | Python script that sends one story/day via Twilio WhatsApp API |
| `story_tracker.json` | repo root | Tracks which story was last sent so it never repeats until the full cycle finishes |
| `.github/workflows/main.yml` | repo root | GitHub Actions workflow — runs at 6 AM IST daily |

---

## The 100 Stories — by Category

| Category | Count | Ages covered | Flavor |
|----------|-------|---------------|--------|
| 🕉️ Religion | 15 | 2–10 | Hindu, Ramayana, Mahabharata, Jain, Sikh, Islamic traditions |
| 🔬 Science | 21 | 2–10 | Wonder-driven: weather, the body, space, animals, physics, the brain |
| 📖 Fiction | 22 | 2–10 | Original fantasy & imagination — dragons, robots, magic with a message |
| 🎭 Drama | 21 | 2–10 | Real-life feelings — friendship, family, honesty, change, resilience |
| 🎈 Fun | 21 | 2–10 | Silly, laugh-out-loud stories that still end with a light reflective question |

Every story is tagged with an `age` band (2–4, 5–7, or 8–10) and a `category`. Open `stories_library.html` to browse, search, and filter the full set — click any card to read the full story plus its Think About It question and lesson.

---

## Credentials & Accounts

### Twilio
- **Console:** https://console.twilio.com
- Find your **Account SID** and **Auth Token** on the Twilio Console dashboard
- **From number:** the Twilio WhatsApp sandbox number (shown in Console → Messaging → Try it out → Send a WhatsApp message)
- **To number:** your WhatsApp number in `whatsapp:+<country_code><number>` format

> ⚠️ Twilio sandbox requires the recipient to periodically re-send the join code to the sandbox number if messages stop arriving.

### GitHub Actions
- **Repo:** https://github.com/goutamchandjain/little-lights-stories
- **Workflow:** `.github/workflows/main.yml`
- **Schedule:** `30 0 * * *` = 6:00 AM IST (00:30 UTC)

### GitHub Secrets (set in repo Settings → Secrets → Actions)
| Secret | Where to find the value |
|--------|------------------------|
| `TWILIO_ACCOUNT_SID` | Twilio Console → Account Info |
| `TWILIO_AUTH_TOKEN` | Twilio Console → Account Info |
| `TWILIO_FROM` | Twilio Console → sandbox number (format: `whatsapp:+...`) |
| `TWILIO_TO` | Your WhatsApp number (format: `whatsapp:+...`) |

*(These secrets are unchanged — no action needed if the daily send was already working.)*

---

## How It Works

1. Every day at 6 AM IST, GitHub Actions triggers the workflow
2. It runs `send_story.py` on a cloud server (no laptop needed)
3. The script checks `story_tracker.json` to find the next story
4. Sends it to WhatsApp via Twilio API
5. Commits the updated `story_tracker.json` back to the repo
6. Cycles through all 100 stories (mixing every category in original order) then repeats from story #1

Since the original 15 religion stories kept their same IDs (1–15) and the new 85 stories were appended after them (16–100), the existing tracker position carries over automatically — delivery continues without skipping or repeating a story.

---

## Manual Controls

**Send a story right now from Terminal:**
```bash
TWILIO_ACCOUNT_SID=<your_sid> TWILIO_AUTH_TOKEN=<your_token> \
TWILIO_FROM=<from_number> TWILIO_TO=<to_number> \
python3 send_story.py
```

**Trigger manually from GitHub:**
Actions tab → Daily Little Lights Story → Run workflow → Run workflow

**Force-send the next story (reset tracker date):**
Edit `story_tracker.json` in the GitHub repo, change `last_sent_date` to `"2000-01-01"`, commit — then run the workflow.

**Skip to a specific story:**
Edit `story_tracker.json`, set `last_sent_index` to one less than the story number you want (e.g. set to `4` to send story #5 next), change `last_sent_date` to `"2000-01-01"`, commit.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Story already sent today" | Reset `last_sent_date` in `story_tracker.json` to a past date |
| 401 Twilio error | Check GitHub Secrets are saved correctly |
| Stories stopped arriving on WhatsApp | Re-send the Twilio sandbox join code to the sandbox number |
| GitHub Actions 403 push error | Ensure `permissions: contents: write` is in the workflow YAML |

---

## To Add More Stories

1. Open `send_story.py`
2. Add a new story dict to the `STORIES` list — include `id`, `category`, `title`, `age`, `tradition`, `text`, `think`, `moral`
3. Keep the formatted WhatsApp message (title + text + think + moral) under 1600 characters
4. Regenerate `stories_library.html` (or manually add the same entry to its embedded `STORIES` array)
5. Commit both files to the GitHub repo

---

*Last updated: July 2026 — expanded from 15 to 100 stories across Religion, Science, Fiction, Drama, and Fun.*
