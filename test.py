from dotenv import load_dotenv

import os
import nodriver as uc

async def main(**kargs):
    url = kargs["website"]

    browser = await uc.start()
    page = await browser.get(url)
    await page.sleep(3)
    await page.save_screenshot("test.png")
    await browser.stop()

if __name__ == "__main__":
    load_dotenv()
    website = os.getenv("WEBSITE_URL")
    uc.loop().run_until_complete(main(website=website))

