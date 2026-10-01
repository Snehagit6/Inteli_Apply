import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def send_email_report(
    report_path: Path | None = None,
    screenshot_path: Path | None = None,
) -> None:
    load_dotenv(PROJECT_ROOT / ".env")

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("MAIL_FROM", smtp_user or "")
    recipients = [address.strip() for address in os.getenv("MAIL_TO", "").split(",") if address.strip()]

    if not smtp_user or not smtp_password or not sender or not recipients:
        logger.warning("Email report skipped: SMTP_USERNAME, SMTP_PASSWORD, and MAIL_TO are required")
        return

    report_path = report_path or PROJECT_ROOT / "reports" / "pytest-report.html"
    screenshot_path = screenshot_path or PROJECT_ROOT / "ui_screen" / "naukri_job_search.png"
    msg = EmailMessage()
    msg["Subject"] = "Naukri pytest report"
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg.set_content("The Naukri pytest report and screenshot are attached.")

    attachments = (
        (report_path, "text", "html"),
        (screenshot_path, "image", "png"),
    )
    for attachment_path, maintype, subtype in attachments:
        if not attachment_path.exists():
            logger.warning("Email attachment not found: {}", attachment_path)
            continue
        msg.add_attachment(
            attachment_path.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            filename=attachment_path.name,
        )

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
            smtp.login(smtp_user, smtp_password)
            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        logger.error("Email report skipped: Gmail rejected the SMTP credentials")
        return
    except (smtplib.SMTPException, OSError) as error:
        logger.error("Email report skipped: {}", error)
        return

    logger.info("Email report sent to {}", ", ".join(recipients))


if __name__ == "__main__":
    send_email_report()
    