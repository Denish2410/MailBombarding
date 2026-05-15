================================================================
  MAILBOMBARDING (BULK EMAIL SENDER) — README
================================================================

WHAT THIS DOES
--------------
Reads a list of contacts from an Excel file and sends each one
a personalized HTML email via Gmail SMTP. 
It supports:
  - Personalized salutations (First Name)
  - Inline logo image (Image)
  - Optional PDF attachment
  - Randomized delay between sends to avoid spam filters
  - Full logging to email_log.txt


================================================================
  FOLDER STRUCTURE
================================================================

your-project/
│
├── bulk_email_sender.py      ← main script
├── .env                      ← Gmail credentials (you create this)
├── testing.xlsx              ← contacts spreadsheet
├── email_log.txt             ← auto-generated after first run
│
├── Image/
│   └── your image      ← inline logo used in emails
│
└── (optional) your_file.pdf  ← if you want a PDF attachment


================================================================
  REQUIREMENTS
================================================================

Python 3.8 or higher

Required Python packages:
  - pandas
  - openpyxl      (for reading .xlsx files)
  - python-dotenv

Install them all at once by running:

    pip install pandas openpyxl python-dotenv


================================================================
  SETUP — STEP BY STEP
================================================================

STEP 1 — Create your .env file
--------------------------------
In the same folder as bulk_email_sender.py,
 create a file named exactly:   .env

Paste this inside it (replace with your real values):

    GMAIL_ADDRESS=you@gmail.com
    GMAIL_APP_PASS=xxxx xxxx xxxx xxxx

  ⚠  GMAIL_APP_PASS is a 16-character App Password, NOT your
     normal Gmail password. See "Getting a Gmail App Password"
     section below.


STEP 2 — Prepare your Excel file (testing.xlsx)
-------------------------------------------------
The spreadsheet must have at least these two columns
(column names are case-sensitive):

    | First Name | Work Email          |
    |------------|---------------------|
    | Alice      | alice@example.com   |
    | Bob        | bob@company.org     |

  - Save it as testing.xlsx in the project folder.
  - Rows with a missing name or email are skipped automatically.


STEP 3 — Add your logo
------------------------
Create a folder called Image/ inside the project folder and
place your logo file there:

    Image

If the file is missing the script will warn you but still send
the emails (just without the inline image).


STEP 4 — Edit the email content
---------------------------------
Open bulk_email_sender.py and fill in these sections near the
top of the file:

    EMAIL_SUBJECT    = "Your subject here..."
    EMAIL_BODY_PLAIN = "Plain-text version of your message"
    EMAIL_BODY_HTML  = "<p>HTML version of your message</p>"

You can personalise with {First Name} anywhere in the body:

    EMAIL_BODY_PLAIN = "Hi {First Name}, ..."


STEP 5 — (Optional) Attach a PDF
----------------------------------
If you want to attach a PDF to every email, set:

    PDF_ATTACHMENT = "your_file.pdf"

Leave it as  None  to send without any attachment.


STEP 6 — Adjust the send delay
--------------------------------
DELAY_SECONDS controls the base pause between emails.
Default is 5 seconds (actual delay is randomised ±3 s,
minimum 3 s). Increase this if you are sending many emails
to reduce spam-filter risk.

    DELAY_SECONDS = 5


================================================================
  HOW TO RUN
================================================================

Open a terminal, navigate to the project folder, then run:

    python bulk_email_sender.py

The script will:
  1. Connect to Gmail SMTP
  2. Read contacts from testing.xlsx
  3. Send each contact a personalised email
  4. Print a live status line for every send
  5. Write a full log to email_log.txt


================================================================
  GETTING A GMAIL APP PASSWORD
================================================================

Google requires an App Password when 2-Step Verification is on
(which it must be for App Passwords to work).

  1. Go to  https://myaccount.google.com/security
  2. Under "How you sign in to Google", click 2-Step Verification
     and enable it if not already on.
  3. Go back to Security → search for "App passwords"
     (or visit https://myaccount.google.com/apppasswords)
  4. Choose App: Mail  |  Device: Other → give it a name
  5. Click Generate — copy the 16-character password shown.
  6. Paste it (with or without spaces) into your .env file.

  ⚠  Never share your App Password or commit .env to Git.
     Add .env to your .gitignore file.


================================================================
  TROUBLESHOOTING
================================================================

"Authentication failed"
  → Double-check GMAIL_ADDRESS and GMAIL_APP_PASS in .env.
  → Make sure 2-Step Verification is ON in your Google account.
  → Re-generate the App Password and update .env.

"Excel file not found"
  → Confirm testing.xlsx is in the same folder as the script.
  → Check the EXCEL_FILE variable at the top of the script.

"Logo not found"
  → Make sure the folder is named exactly  Image/  (capital I)
    and the file is  yourimage.jpeg  (matching case).

Emails going to spam
  → Increase DELAY_SECONDS (try 10–15).
  → Warm up your Gmail account by sending a few manual emails first.
  → Avoid spam trigger words in your subject/body.

KeyError on {First Name}
  → Your EMAIL_BODY_PLAIN or EMAIL_BODY_HTML contains a curly-
    brace placeholder that doesn't match "First Name" exactly.
  → Check spelling and capitalisation.


================================================================
  IMPORTANT NOTES
================================================================

- Gmail free accounts can send roughly 500 emails per day.
  Google Workspace accounts allow up to 2,000 per day.
- Always test with 1–2 real contacts before a full send.
- Keep a backup of your .env file somewhere safe and private.
- This script does NOT track opens or clicks. It is a simple
  one-way sender only.

================================================================# MailForge
