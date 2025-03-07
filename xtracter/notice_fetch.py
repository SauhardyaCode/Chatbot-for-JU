from base_code import *
import time

noticeFileJSON = "./data/notices/notices_linkOnly.json"
try:
    url = "https://jadavpuruniversity.in/notifications/"
    driver.get(url)

    print("Loading page...")

    try:
        totalPages = int(driver.find_element(By.CLASS_NAME, "jet-listing-grid__items").get_attribute("data-pages"))
    except ValueError as e:
        print(e)
        totalPages = 200

    # Find all notice blocks
    for i in range(totalPages):
        data = read_json(noticeFileJSON)
        time.sleep(1)

        containers = driver.find_elements(By.CLASS_NAME, "elementor-widget-theme-post-title")
        for container in containers:
            a_tag = container.find_element(By.TAG_NAME,"a")
            title = a_tag.text.strip()
            link = a_tag.get_attribute("href")
            notice = {"title": title, "link": link}
            if notice not in data:
                data.append(notice)
        
        navigationLinks = driver.find_elements(By.CLASS_NAME, "jet-filters-pagination__link")
        for link in navigationLinks:
            if link.text.strip() == "Next":
                link.click()
        
        time.sleep(3)
        print(f"Code Scraped [Page: {i+1}]")

        with open(noticeFileJSON,"w",encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("Scrapping Successful!")

except Exception as e:
    print("Loading Failed! ",e)

finally:
    driver.quit()