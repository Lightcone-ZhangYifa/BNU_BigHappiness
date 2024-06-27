import Spider
import BNU

def main():
    print('reading configuration from file...')
    Spider.read_config()
    print('trying to login digital DCP...')
    driver = BNU.WebDriver_Init(url=BNU.url['京师大福']
                                , silent=True
                                )
    BNU.read_info()
    BNU.login(driver=driver, username=BNU.username, password=BNU.password)
    if Spider.current_page == 1 and Spider.current_item == 0:
        Spider.generateCSV_title()
    Spider.get_all_items(driver)
    driver.quit()

main()
