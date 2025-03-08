from base_code import *
import time

path = "./data/notices"
link_only_data = read_json(f"{path}/notices_linkOnly.json")

full_data = read_json(f"{path}/notices.json")

dataToDump = []
for data in link_only_data:
    linkToPDF = data['link']

    exists = False
    for item in full_data:
        if linkToPDF == item['link']:
            dataToDump.append(item)
            print(f"Skipping Link: {linkToPDF}")
            exists = True

    if not exists:
        try:
            driver.get(linkToPDF)
            pdfBox = driver.find_element(By.CLASS_NAME, "link_color").find_elements(By.TAG_NAME, "a")
            data['docs'] = []

            for pdf in pdfBox:
                heading = pdf.text.strip()
                link = pdf.get_attribute("href")
                data['docs'].append({'heading': heading, 'link': link})

            print(f"Scrapped Link: {linkToPDF}")
            dataToDump.append(data)
            time.sleep(1)

        except Exception as e:
            print(f"Error scrapping {linkToPDF}",e)

with open(f"{path}/notices.json","w",encoding="utf-8") as f:
    json.dump(dataToDump,f,indent=4,ensure_ascii=False)

driver.quit()