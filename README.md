<div align="center">

# MailBombarding

**A simple, personalised bulk email sender for Gmail.**

Read contacts from an Excel sheet, personalise each message, add an inline logo and an optional PDF, and send with randomised pacing to keep things friendly to spam filters.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Gmail SMTP](https://img.shields.io/badge/Gmail-SMTP-EA4335?logo=gmail&logoColor=white)](https://support.google.com/mail/answer/7126229)
[![Status](https://img.shields.io/badge/status-ready%20to%20use-brightgreen)](#)

</div>

---

## Features

- **Personalised greetings** using a `{First Name}` placeholder in plain-text and HTML bodies
- **Inline logo** embedded directly in the HTML email
- **Optional PDF attachment** sent with every message
- **Randomised delays** between sends to reduce spam-filter risk
- **Full logging** of every send to `email_log.txt`
- **Skips incomplete rows** automatically (missing name or email)

## Project Structure

```text
your-project/
├── bulk_email_sender.py   # main script
├── .env                   # Gmail credentials (you create this)
├── testing.xlsx           # contacts spreadsheet
├── email_log.txt          # generated after the first run
├── Image/
│   └── your-logo.jpeg     # inline logo used in emails
└── your_file.pdf          # optional attachment
```

## Requirements

- Python **3.8** or newer
- The following packages:

```bash
pip install pandas openpyxl python-dotenv
```

## Quick Start

### 1. Create your `.env` file

In the same folder as `bulk_email_sender.py`, create a file named exactly `.env`:

```env
GMAIL_ADDRESS=you@gmail.com
GMAIL_APP_PASS=xxxx xxxx xxxx xxxx
```

> **Important:** `GMAIL_APP_PASS` must be a 16-character **App Password**, not your normal Gmail password. See [Getting a Gmail App Password](#getting-a-gmail-app-password).

### 2. Prepare your contacts spreadsheet

Save `testing.xlsx` in the project folder with at least these two columns (names are case-sensitive):

| First Name | Work Email         |
|------------|--------------------|
| Alice      | alice@example.com  |
| Bob        | bob@company.org    |

Rows with a missing name or email are skipped.

### 3. Add your logo *(optional)*

Create an `Image/` folder and place your logo inside it. If the logo is missing, the script will warn you and still send the emails without the image.

### 4. Write your email

Open `bulk_email_sender.py` and edit the settings near the top:

```python
EMAIL_SUBJECT   = "Your subject here"
EMAIL_BODY_PLAIN = "Hi {First Name}, here is the plain-text version of my message."
EMAIL_BODY_HTML  = "<p>Hi {First Name}, here is the <strong>HTML</strong> version.</p>"
```

### 5. Attach a PDF *(optional)*

```python
PDF_ATTACHMENT = "your_file.pdf"   # set to None to send without an attachment
```

### 6. Set the send delay

```python
DELAY_SECONDS = 5   # base pause between emails; actual delay is randomised ±3 s (minimum 3 s)
```

Increase this value if you are sending to many contacts.

## Running the Script

From the project folder, run:

```bash
python bulk_email_sender.py
```

The script will connect to Gmail SMTP, read your contacts, send each personalised email, print a live status line for every send, and write a full log to `email_log.txt`.

## Getting a Gmail App Password

Google requires an App Password when 2-Step Verification is enabled, which it must be for App Passwords to work.

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security) and turn on **2-Step Verification** if it is not already on.
2. Visit [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
3. Choose **App: Mail** and **Device: Other**, then give it a name.
4. Click **Generate** and copy the 16-character password.
5. Paste it into your `.env` file (with or without spaces).

## Troubleshooting

| Problem | Fix |
|---------|-----|
| **Authentication failed** | Check `GMAIL_ADDRESS` and `GMAIL_APP_PASS` in `.env`. Make sure 2-Step Verification is on, and regenerate the App Password if needed. |
| **Excel file not found** | Confirm `testing.xlsx` is in the same folder as the script, or update `EXCEL_FILE` at the top of the script. |
| **Logo not found** | The folder must be named exactly `Image/` and the file name must match the one the script expects, including case. |
| **Emails going to spam** | Increase `DELAY_SECONDS` (try 10–15), warm up the account with a few manual emails, and avoid spam-trigger words. |
| **KeyError on `{First Name}`** | A placeholder in your body does not match `First Name` exactly. Check spelling and capitalisation. |

## Important Notes

- Gmail free accounts can send roughly **500 emails per day**. Google Workspace accounts can send up to **2,000 per day**.
- Always test with 1–2 real contacts before a full send.
- **Never share your App Password or commit `.env` to Git.** Add `.env` to your `.gitignore`.
- This script does **not** track opens or clicks. It is a simple one-way sender.

---

<div align="center">

Made for simple, personal bulk emailing. Send responsibly.

</div>