"""
Helper utilities for the Hotplate bot.

Provides reusable async functions for interacting with browser elements,
abstracting common patterns like selecting, clicking, and waiting.
"""

import logging
import nodriver as uc

logger = logging.getLogger(__name__)


async def interact(page: uc.Tab, selector: str, debug: bool = False, sleep: int = 3) -> bool:
    """
    Select an element by CSS selector, click it, and optionally screenshot.

    Returns True if the element was found and clicked, False otherwise.
    """
    element = await page.select(selector)
    if not element:
        logger.warning("Element not found: %s", selector)
        return False

    await element.click()
    logger.info("Clicked element: %s", selector)

    if debug:
        await page.save_screenshot("debug.png")
        logger.debug("Screenshot saved: debug.png")

    await page.sleep(sleep)
    return True
