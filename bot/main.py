from config import config, Config
from helper import interact

import json
import logging
import nodriver as uc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def load_selectors(path: str):
    with open(path, "r") as f:
        selectors = json.load(f)
    for name, value in selectors.items():
        yield name, value["SELECT"]

async def undetected(keys: Config) -> None:
    browser = await uc.start(
        browser_args=['--disable-web-security', '--disable-site-isolation-trials']
    )
    page = await browser.get(keys.WEBSITE_URL)

    # Interact goes here in a loop
    for name, selector in load_selectors("bot/selectors.json"):
        await interact(page, selector)


def main() -> None:
    logger.info("Kicking off the Bot")
    uc.loop().run_until_complete(undetected(config))


if __name__ == "__main__":
    main()
