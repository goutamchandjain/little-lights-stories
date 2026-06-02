# Little Lights — GitHub Actions Setup

Follow these steps once. After that, stories send automatically every day at 6 AM IST — no laptop needed.

---

## Step 1: Create a GitHub repository

1. Go to https://github.com/new
2. Name it: `little-lights-stories`
3. Set it to **Private**
4. Click **Create repository**

---

## Step 2: Upload the files

Upload these two files to the repo root:
- `send_story.py`  ← the story sender script
- `story_tracker.json`  ← tracks which story was last sent

And create this folder structure:
```
.github/
  workflows/
    daily_story.yml   ← the automation workflow
```

The easiest way: use GitHub's web UI — click "Add file → Upload files" for send_story.py,
then "Add file → Create new file" for the workflow at `.github/workflows/daily_story.yml`.

---

## Step 3: Add secrets (your Twilio credentials)

In your repo → Settings → Secrets and variables → Actions → New repository secret

Add these three secrets:

| Name | Value |
|------|-------|
| `TWILIO_ACCOUNT_SID` | AC9ec0af02600f5bfdf16037f455a8afd5 |
| `TWILIO_AUTH_TOKEN` | dae232912aeec2795e13ec719b9bd3d7 |
| `TWILIO_FROM` | whatsapp:+14155238886 |
| `TWILIO_TO` | whatsapp:+919886303637 |

---

## Step 4: Done!

GitHub Actions will run the script every day at 6:00 AM IST (00:30 UTC).
You can also trigger it manually anytime: Actions tab → Daily Story → Run workflow.

---

## Troubleshooting

- **Story not arriving?** Check Actions tab for errors in the latest run.
- **"Story already sent today"?** The tracker.json in the repo is up to date — wait for tomorrow.
- **Want to send immediately?** Go to Actions → Daily Little Lights Story → Run workflow → Run workflow.
