from datetime import datetime
from pathlib import Path


def write_blog_created_event(post_id: int, author_id: int) -> None:
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    message = (
        f"{datetime.utcnow().isoformat()}Z | blog_created | post_id={post_id} | author_id={author_id}\n"
    )
    with (log_dir / "blog_events.log").open("a", encoding="utf-8") as logfile:
        logfile.write(message)
