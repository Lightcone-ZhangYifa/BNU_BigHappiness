import Spider
import BNU
import theme


def BigHappiness():
    theme.Processing('reading configuration from file...')
    Spider.read_config()
    theme.Processing('initializing WebDriver engine...')
    driver = BNU.WebDriver_Init(url=BNU.url['京师大福']
                                , silent=True
                                )
    theme.Processing('trying to login digital DCP...')

    BNU.login(driver=driver)
    driver.get(url=BNU.url['京师大福'])
    if Spider.current_page == 1 and Spider.current_item == 0:
        Spider.exportCSV_title()
    Spider.get_all_items(driver)
    print()
    theme.Successfully('-' * 10 + '[  Get all items successfully.  ]' + '-' * 10)
    driver.quit()

BigHappiness()
