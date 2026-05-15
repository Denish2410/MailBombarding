from dotenv import load_dotenv
import os
load_dotenv()

import smtplib
import time
import logging
import random
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from pathlib import Path

# =============================================================
#  ✏️  CONFIGURATION
# =============================================================

GMAIL_ADDRESS   = "[EMAIL_ADDRESS]"
GMAIL_APP_PASS  = "[APP_PASSWORD]"

EXCEL_FILE      = "testing.xlsx"
SHEET_NAME      = 0

FIRST_NAME_COL  = "First Name"
EMAIL_COL       = "Work Email"

PDF_ATTACHMENT  = None          # Set to "brochure.pdf" to attach a PDF, or leave None

DELAY_SECONDS   = 5        # Base seconds between emails (random ±3s added automatically)

# =============================================================
#  ✏️  EMAIL CONTENT
# =============================================================

EMAIL_SUBJECT = "Your subject here..."

# Plain-text fallback (for email clients that don't render HTML)
EMAIL_BODY_PLAIN = """\
Your body message here....
"""

# HTML version — renders styled signature exactly like your Gmail signature
EMAIL_BODY_HTML = """\
Your body HTML here....
"""

# =============================================================
#  🚀  SCRIPT — No need to edit below this line
# =============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler("email_log.txt", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


def load_contacts(filepath: str, sheet) -> pd.DataFrame:
    """Load and validate the Excel file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {filepath}")
    df = pd.read_excel(path, sheet_name=sheet, dtype=str)
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=[EMAIL_COL, FIRST_NAME_COL])
    df[EMAIL_COL]      = df[EMAIL_COL].str.strip()
    df[FIRST_NAME_COL] = df[FIRST_NAME_COL].str.strip()
    log.info(f"Loaded {len(df)} valid contacts from '{filepath}'")
    return df


def build_email(to_name: str, to_email: str) -> MIMEMultipart:
    """Construct a personalized MIME email with plain+HTML and optional PDF attachment."""

    # Use 'related' envelope to support inline images
    related = MIMEMultipart("related")

    # 'alternative' tells clients: pick the best version you support (HTML preferred)
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(EMAIL_BODY_PLAIN.format(**{"First Name": to_name}), "plain", "utf-8"))
    alt.attach(MIMEText(EMAIL_BODY_HTML.format(**{"First Name": to_name}),  "html",  "utf-8"))
    
    related.attach(alt)

    # Attach the inline logo image
    logo_path = Path("Image/unicornLogo.jpeg")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<unicorn_logo>")
            img.add_header("Content-Disposition", "inline", filename=logo_path.name)
            related.attach(img)
    else:
        log.warning(f"Logo not found at '{logo_path}'. Cannot attach inline image.")

    # If PDF attached, wrap in a 'mixed' envelope
    if PDF_ATTACHMENT:
        pdf_path = Path(PDF_ATTACHMENT)
        if pdf_path.exists():
            outer = MIMEMultipart("mixed")
            outer["From"]    = GMAIL_ADDRESS
            outer["To"]      = to_email
            outer["Subject"] = EMAIL_SUBJECT
            outer.attach(related)
            with open(pdf_path, "rb") as f:
                part = MIMEApplication(f.read(), Name=pdf_path.name)
                part["Content-Disposition"] = f'attachment; filename="{pdf_path.name}"'
                outer.attach(part)
            return outer
        else:
            log.warning(f"PDF not found at '{PDF_ATTACHMENT}' — sending without attachment")

    # No PDF — just use the related envelope
    related["From"]    = GMAIL_ADDRESS
    related["To"]      = to_email
    related["Subject"] = EMAIL_SUBJECT
    return related


def send_emails():
    """Main: load contacts, connect to Gmail, send all emails."""
    if not GMAIL_ADDRESS or not GMAIL_APP_PASS:
        log.error("GMAIL_ADDRESS or GMAIL_APP_PASS not found. Check your .env file.")
        return

    df = load_contacts(EXCEL_FILE, SHEET_NAME)

    sent_count    = 0
    failed_count  = 0
    skipped_count = 0

    log.info("Connecting to Gmail SMTP...")
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASS.replace(" ", ""))
        log.info("Login successful ✓")
    except smtplib.SMTPAuthenticationError:
        log.error("Authentication failed. Check your Gmail address and App Password.")
        return
    except Exception as e:
        log.error(f"Could not connect to Gmail: {e}")
        return

    log.info(f"Starting to send {len(df)} emails...\n")

    for idx, row in df.iterrows():
        name  = row[FIRST_NAME_COL]
        email = row[EMAIL_COL]

        # Basic email format validation
        if "@" not in email or "." not in email.split("@")[-1]:
            log.warning(f"[{idx+1}] Skipped invalid email: {email}")
            skipped_count += 1
            continue

        try:
            msg = build_email(name, email)
            server.sendmail(GMAIL_ADDRESS, email, msg.as_string())
            log.info(f"[{idx+1}/{len(df)}] ✓ Sent to {name} <{email}>")
            sent_count += 1
        except Exception as e:
            log.error(f"[{idx+1}/{len(df)}] ✗ Failed for {name} <{email}>: {e}")
            failed_count += 1

        # Random delay — mimics human behaviour, avoids spam detection
        if idx < len(df) - 1:
            delay = DELAY_SECONDS + random.uniform(-3, 3)
            delay = max(3, delay)       # never go below 3 seconds
            time.sleep(delay)

    server.quit()

    log.info("\n" + "="*50)
    log.info(f"  DONE — Sent: {sent_count} | Failed: {failed_count} | Skipped: {skipped_count}")
    log.info(f"  Full log saved to: email_log.txt")
    log.info("="*50)


if __name__ == "__main__":
    send_emails()