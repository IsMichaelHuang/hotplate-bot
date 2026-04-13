import nodriver as uc

async def main():
    browser = await uc.start()
    page = await browser.get("https://www.hotplate.com/bakeryinabasket")
    await page.sleep(3)
    await page.save_screenshot("test.png")
    await browser.stop()

if __name__ == "__main__":
    uc.loop().run_until_complete(main())

