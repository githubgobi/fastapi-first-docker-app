import time


def send_welcome_email(email: str):
    # simulate sending email
    time.sleep(2)
    print(f"Welcome email sent to {email}", flush=True)

    # If print(f"Welcome email sent to {email}") is not appearing, it usually happens because the background task runs inside Uvicorn (or a container) where stdout behaves differently.