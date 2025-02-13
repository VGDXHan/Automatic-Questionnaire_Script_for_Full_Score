# https://kaoshi.wjx.top/vm/wFcQaPc.aspx#

from playwright.sync_api import sync_playwright

from Interactor import Interactor   
from Solver import Solver
from Params import Params


def main():
    params = Params()
    with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(300000)
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """)
            page.goto(params.url)
            
            interactor = Interactor()
            solver = Solver()
            interactor.storage_all_qa(page)
            solver.solve()
            interactor.finish_questionaire(page)
            interactor.get_score(page)

if __name__ == '__main__':
    main()
 