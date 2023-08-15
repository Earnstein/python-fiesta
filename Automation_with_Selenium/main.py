# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
#
#
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# xpath = '//*[@id="section-heading"]'
# driver.get("https://www.billboard.com/charts/hot-100/2010-10-16/")
# title = driver.find_element(By.XPATH, xpath).text
# print(title)
# driver.close()
# driver.quit()
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://symonstorozhenko.wixsite.com/website-1")
    page.locator("#bgLayers_comp-kqx72zu42").get_by_test_id("colorUnderlay").click(button="right")
    page.locator("#comp-kqx72yrn1").click()
    page.get_by_role("button", name="Log In").click()
    page.get_by_test_id("signUp.switchToSignUp").click()
    page.get_by_test_id("siteMembersDialogLayout").get_by_test_id("buttonElement").click()
    page.get_by_test_id("emailAuth").get_by_label("Email").click()
    page.get_by_test_id("emailAuth").get_by_label("Email").fill("hkhfh@gmail.com")
    page.get_by_test_id("emailAuth").get_by_label("Email").press("Tab")
    page.get_by_label("Password").press("CapsLock")
    page.get_by_label("Password").fill("1")
    page.get_by_label("Password").press("CapsLock")
    page.get_by_label("Password").fill("12356")
    page.get_by_test_id("submit").get_by_test_id("buttonElement").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

