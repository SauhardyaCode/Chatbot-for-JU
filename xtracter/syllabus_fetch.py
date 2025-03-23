from base_code import *
import time

faculties = ("arts","science","engineering-technology","interdisciplinary-studies-law-and-management")

departmentWrapDIV = "jet-listing-grid__items"
subjectCardWrapDIV = "jet-engine-listing-overlay-wrap"
subjectCardDIV = "jet-listing-dynamic-field__content"

courseWrapDIV = departmentWrapDIV
courseCardDIV = "jet-listing-grid__item"
headingCourseH2 = "elementor-heading-title"

def clean(string):
    return string.lower().replace(' & ','-').replace(' ','-')

try:
    for faculty in faculties:
        url = f"https://jadavpuruniversity.in/department/faculty-of-{faculty}"
        driver.get(url)
        print("Loading Page...")
        time.sleep(3)

        department = driver.find_element(By.CLASS_NAME, departmentWrapDIV)
        subjects = department.find_elements(By.XPATH, f".//div[contains(@class, '{subjectCardWrapDIV}')]")
        subjects_data = []

        for subject in subjects:
            linkToSite = subject.get_attribute('data-url')
            infoElemArr = subject.find_elements(By.CLASS_NAME, subjectCardDIV)
            name = infoElemArr[0].text.strip()
            details = infoElemArr[1].get_attribute("innerHTML").strip()
            subjects_data.append({'name': name, 'details': details, 'link': linkToSite})

        for subj in subjects_data:
            name = subj['name']
            details = subj['details']
            linkToSite = subj['link']

            path = f"./data/syllabus/{faculty}/{clean(name)}"
            os.makedirs(path, exist_ok=True)

            with open(f"{path}/about.json", "w", encoding="utf-8") as f:
                json.dump({'name':name,'description':details}, f, indent=4, ensure_ascii=False)
            
            time.sleep(2)
            course_url = linkToSite
            driver.get(course_url)
            data = []

            try:
                courseWrap = driver.find_elements(By.CLASS_NAME, courseWrapDIV)[1]
            except IndexError:
                print(f"No course data available for: {name}")
            else:
                courses = courseWrap.find_elements(By.CLASS_NAME, courseCardDIV)

                for course in courses:
                    heading = course.find_element(By.XPATH, f".//h2[contains(@class, '{headingCourseH2}')]").text.strip()
                    try:
                        duration = course.find_element(By.XPATH,
                        ".//div[@class='elementor-widget-container' and starts-with(normalize-space(text()), 'Duration:')]"
                        ).text.replace("Duration:",'').strip()
                    except:
                        duration = None
                    try:
                        intake = course.find_element(By.XPATH,
                        ".//div[@class='elementor-widget-container' and starts-with(normalize-space(text()), 'Intake:')]"
                        ).text.replace("Intake:",'').strip()
                    except:
                        intake = None

                    link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
                    data.append({'course':heading, 'duration':duration, 'intake':intake, 'link':link})

            print(f"Writing on {path}/courses.json")
            with open(f"{path}/courses.json","w",encoding="utf-8") as f:
                json.dump(data,f,indent=4,ensure_ascii=False)

    print("Scrapping Successful!")

except Exception as e:
    print("Loading Failed!",e)

finally:
    driver.quit()