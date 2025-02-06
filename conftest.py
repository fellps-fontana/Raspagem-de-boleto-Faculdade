import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def set_up_page(browser):
    context = browser.new_context(base_url='https://estudante.sesisenai.org.br', )
    page = context.new_page()
    yield page
    context.close()


