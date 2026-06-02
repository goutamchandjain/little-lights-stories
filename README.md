# 🌟 Little Lights — Full Setup Reference

## What We Built
A library of 15 Indian kids' stories (ages 2–10) covering Hindu, Ramayana, Mahabharata, Jain, Sikh, and Islamic traditions — sent automatically to WhatsApp every day at 6 AM IST via GitHub Actions + Twilio. No laptop needed.

---

## Files

| File | Location | Purpose |
|------|----------|---------|
| `stories_library.html` | outputs folder | Interactive browser app — filter by age & tradition, read stories, copy for WhatsApp |
| `send_story.py` | outputs folder | Python script that sends one story/day via Twilio WhatsApp API |
| `story_tracker.json` | outputs folder + GitHub repo | Tracks which story was last sent so it never repeats |
| `.github/workflows/daily_story.yml` | GitHub repo | GitHub Actions workflow — runs at 6 AM IST daily |

---

## The 15 Stories

| # | Title | Age | Tradition |
|---|-------|-----|-----------|
| 1 | Ganesha and the Greedy Moon | 2–4 | Hindu |
| 2 | Baby Krishna's Butter Secret | 2–4 | Hindu |
| 3 | Guru Nanak's Magic Langar | 2–4 | Sikh |
| 4 | Little Mahavir and the Crying Ant | 2–4 | Jain |
| 5 | Ibrahim Counts the Stars | 2–4 | Islamic |
| 6 | Hanuman's Giant Leap | 5–7 | Ramayana |
| 7 | Eklavya's Silent Teacher | 5–7 | Mahabharata |
| 8 | Mahavir and the Angry Snake | 5–7 | Jain |
| 9 | The Five Brave Ones | 5–7 | Sikh |
| 10 | Yusuf and the Colorful Coat | 5–7 | Islamic |
| 11 | Arjuna's Big Question | 8–10 | Mahabharata |
| 12 | Rama's Hardest Choice | 8–10 | Ramayana |
| 13 | The Merchant Who Let Go | 8–10 | Jain |
| 14 | Mirabai's Unstoppable Song | 8–10 | Hindu |
| 15 | The Langar That Fed an Army | 8–10 | Sikh |

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
- **Workflow:** `.github/workflows/daily_story.yml`
- **Schedule:** `30 0 * * *` = 6:00 AM IST (00:30 UTC)

### GitHub Secrets (set in repo Settings → Secrets → Actions)
| Secret | Where to find the value |
|--------|------------------------|
| `TWILIO_ACCOUNT_SID` | Twilio Console → Account Info |
| `TWILIO_AUTH_TOKEN` | Twilio Console → Account Info |
| `TWILIO_FROM` | Twilio Console → sandbox number (format: `whatsapp:+...`) |
| `TWILIO_TO` | Your WhatsApp number (format: `whatsapp:+...`) |

---

## How It Works

1. Every day at 6 AM IST, GitHub Actions triggers the workflow
2. It runs `send_story.py` on a cloud server (no laptop needed)
3. The script checks `story_tracker.json` to find the next story
4. Sends it to WhatsApp via Twilio API
5. Commits the updated `story_tracker.json` back to the repo
6. Cycles through all 15 stories then repeats from story #1

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
| Node.js 20 deprecation warning | Safe to ignore — goes away after June 16, 2026 |

---

## To Add More Stories

1. Open `send_story.py`
2. Add a new story object to the `STORIES` list following the same format
3. Update `stories_library.html` — add the story to the `STORIES` array in the `<script>` section
4. Commit both files to the GitHub repo

---

*Last updated: June 2026*
