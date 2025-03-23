from base_code import *
import time
import os

path = "./data/syllabus"
syllabusDataID = "c89a251"
curriculumDataID = "f483f6c"

for faculty in os.listdir(path):
    for dept in os.listdir(f"{path}/{faculty}"):
        fileToEdit = f"{path}/{faculty}/{dept}/courses.json"
        details = read_json(fileToEdit)
        data = []
        for detail in details:
            url = detail['link']
            if 'syllabus' in detail:
                print(f"Skipping Link: {url}")
                data.append(detail)
                continue

            try:
                driver.get(url)
                time.sleep(3)

                # syllabus
                link_arr1 = []
                try:
                    embedded = driver.find_element(By.XPATH, f"//div[@data-id='{syllabusDataID}']")
                except:
                    pass
                else:
                    titles = [x.text for x in embedded.find_elements(By.TAG_NAME, "strong")]
                    link_elems = embedded.find_elements(By.TAG_NAME, "a")
                    if len(titles)!=len(link_elems):
                        titles = [x.text for x in link_elems]
                    links = [x.get_attribute("href") for x in link_elems]
                    for i in range(len(links)):
                        link_arr1.append({'title': titles[i], 'link': links[i]})

                # curriculum
                link_arr2 = []
                try:
                    embedded = driver.find_element(By.XPATH, f"//div[@data-id='{curriculumDataID}']")
                except:
                    pass
                else:
                    titles = [x.text for x in embedded.find_elements(By.TAG_NAME, "strong")]
                    link_elems = embedded.find_elements(By.TAG_NAME, "a")
                    if len(titles)!=len(link_elems):
                        titles = [x.text for x in link_elems]
                    links = [x.get_attribute("href") for x in link_elems]
                    for i in range(len(links)):
                        link_arr2.append({'title': titles[i], 'link': links[i]})

                detail['syllabus'] = link_arr1
                detail['curriculum'] = link_arr2
                data.append(detail)
                print(f"Scrapped Link: {url}")

            except Exception as e:
                print(f"Error Scrapping {url}")

        print(f'Writing on {fileToEdit}')
        with open(fileToEdit,'w',encoding='utf-8') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

driver.quit()