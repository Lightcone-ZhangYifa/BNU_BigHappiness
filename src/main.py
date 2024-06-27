import Spider
import BNU
def main():
    print('trying to login digital DCP...')
    driver = BNU.WebDriver_Init(url=BNU.url['京师大福']
                                , silent=True
                                )
    BNU.login(driver=driver, username=BNU.username, password=BNU.password)
    Spider.generateCSV_title()
    Spider.get_all_items(driver)
    driver.quit()

main()