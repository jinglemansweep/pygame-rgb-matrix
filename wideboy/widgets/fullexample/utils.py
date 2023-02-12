import asyncio
import html
import logging
from datetime import datetime

from wideboy.utils.helpers import get_rss_items
from wideboy.config import DEBUG

logger = logging.getLogger(__name__)


async def update_ticker(loop, ticker, url, interval, update_now=False):
    if not update_now:
        await asyncio.sleep(interval)
    feed = await get_rss_items(loop, url)
    ticker.clear_items()
    now = datetime.now()
    time_fmt = now.strftime("%H:%M")
    header = f"Latest News @ {time_fmt}"
    ticker.add_text_item(header)
    entries = feed.entries
    for idx, item in enumerate(entries):
        content = html.unescape(item["title"])
        if DEBUG:
            content = f"{idx}:{content[:15]}..."
        ticker.add_text_item(content)
    ticker.render_surface()
    logger.info(
        f"ticker:update:rss url={url} entries={len(entries)} interval={interval} update_now={update_now}"
    )
    asyncio.create_task(update_ticker(loop, ticker, url, interval, False))


async def show_ticker(ticker, interval, show_now=False):
    if not show_now:
        await asyncio.sleep(interval)
    logger.info(f"ticker:show interval={interval}")
    ticker.run()
    asyncio.create_task(show_ticker(ticker, interval, False))
