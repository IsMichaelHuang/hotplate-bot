from dotenv import load_dotenv

import os
import nodriver as uc

async def main(**kargs):
    url = kargs["website"]
    phone = kargs["number"]

    browser = await uc.start(
        browser_args=['--disable-web-security', '--disable-site-isolation-trials']
    )
    page = await browser.get(url)
    await page.sleep(5)

    # Selecting the first current drop and interacting with it
    container = await page.select("div.c-bZNrxE.c-bZNrxE-iVNpjU-css")
    await container.click()
    await page.sleep(3)

    # Select the first item and interact with it
    container = await page.select("div.c-fuYhmF.c-fuYhmF-iPJLV-css")
    await container.click()
    await page.sleep(3)

    # Select the plus sign for the first occurance
    container = await page.select_all("div.c-bZNrxE.c-bZNrxE-ilkRvoX-css")
    delta = container[1]
    await delta.click()
    await page.sleep(3)

    # Add to Cart
    button = await page.select("button.c-bYwOQu.c-bYwOQu-dWXYMB-size-large.c-bYwOQu-gTzoIO-shape-rounded.c-bYwOQu-iczyIrr-css")
    await button.click()
    await page.sleep(3)

    # Checkout
    button = await page.select("button.c-cAlLHX.c-cAlLHX-idzJAYQ-css")
    await button.click()
    await page.sleep(3)

    # Confirm Checkout
    button = await page.select("a.c-bYwOQu.c-bYwOQu-dWXYMB-size-large.c-bYwOQu-iHjjLf-shape-square.c-bYwOQu-ihuiYjp-css")
    await button.click()
    await page.sleep(3)

    # Enter Phone number
    button = await page.select("input")
    await button.send_keys(phone)
    await page.sleep(3)

    # Wait for manual verification input
    while True:
        success = await page.select("div.bg-success9.text-white.flex.items-center.justify-center.rounded-full.h-5.w-5.shrink-0.transition-all")
        if success:
            print("Success detected! Resuming script...")
            break
    await page.sleep(2)

    # Confirm time
    button = await page.select("button.c-bYwOQu.c-bYwOQu-dWXYMB-size-large.c-bYwOQu-iHjjLf-shape-square.c-bYwOQu-ikAydxt-css")
    await button.click()

    await page.sleep(3)
    stripe_iframe = await page.select("iframe[title='Secure payment input frame']")
    print(f"Stripe iframe: {stripe_iframe}")

    def fill_input(name, value):
        return f"""
            var iframe = document.querySelector("iframe[title='Secure payment input frame']");
            var input = iframe.contentDocument.querySelector("input[name='{name}']");
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(input, '{value}');
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        """

    await page.evaluate(fill_input("number", "1111111111111111"))
    print("Card number entered")
    await page.evaluate(fill_input("expiry", "0911"))
    print("Expiry entered")
    await page.evaluate(fill_input("cvc", "420"))
    print("CVC entered")
    await page.evaluate(fill_input("postalCode", "12345"))
    print("Postal entered")
    await page.sleep(3)

    # Confirm checkout
    button = await page.select("button.c-bYwOQu.c-bYwOQu-dWXYMB-size-large.c-bYwOQu-iHjjLf-shape-square.c-bYwOQu-ikAydxt-css.grow") 
    await button.click()
    await page.sleep(3)

    await page.save_screenshot("test.png")
    await browser.stop()


if __name__ == "__main__":
    load_dotenv()
    website = os.getenv("WEBSITE_URL")
    number = os.getenv("NUMBER")
    uc.loop().run_until_complete(main(website=website, number=number))

