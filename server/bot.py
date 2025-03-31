import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
from datetime import datetime
import json
from dateutil import parser
from fuzzywuzzy import fuzz
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="learnlm-1.5-pro-experimental",
  generation_config=generation_config,
  system_instruction=f'''
        You are a chatbot designed specifically for Jadavpur University. Don't entertain queries apart from university related information and information on courses, department, notices, curriculum. Strictly deny any other query.

        Wherever you enclose a text like **TEXT** replace it with <b>TEXT</b> and wherever you use * for listing things replace it with ●

        If the user asks for any notice of the university, reply in the format 'NOTICE: NOTICE_KEYWORD' strictly,
        If the user asks to show recent notices or just notices, reply 'NOTICE_RECENT' stricty,
        If the user aks for more recent notices reply 'NOTICE_RECENT_MORE' strictly,
        If the user asks to show notices on some particular date reply in the format 'NOTICE_DATE: DD-MM-YYYY', eg if it says two months back, you should return appropriate month, today's date is {datetime.today()}

        If user asks for location of university provide LINK='https://www.google.com/maps/place/Jadavpur+University/@22.4977988,88.3714421,17.35z/data=!4m6!3m5!1s0x3a0271237f28abe9:0xd047bab0c8bfb11c!8m2!3d22.4988822!4d88.3714123!16zL20vMDQ2dm0?entry=ttu&g_ep=EgoyMDI1MDMwNC4wIKXMDSoASAFQAw%3D%3D'

        If user asks about campus maps provide LINK='https://jadavpuruniversity.in/campus-map/' and campus map image '<img src='./src/pictures/Campus-Map.jpg' alt='campus-map' size=50/>'

        Few Campus Map Details:
        Main Entrance & Administrative Zone: Aurobindo Bhavan, Sansad Building, Alumni Building
        Academic & Research Blocks: UG & PG Science & Arts Buildings, Physics & Telecommunication Building, Bio-Science Building, Metallurgy, Civil, Mechanical, Chemical, and Electrical Buildings, High Voltage Building & Testing Lab, Food Tech Building
        Libraries & Learning Resources: Central Library, Departmental Libraries
        Cultural & Co-Curricular Spaces: OAT (Open Air Theatre), TSG/TSA (Triguna Sen Auditorium), Gandhi Bhavan
        Technical & Practical Training Centers: Computer Centre, School of Printing, Central Glass & Ceramic Research Institute, Blue Earth Workshop 
        Student & Faculty Amenities: FETSU, Cheap Store
        Other Important Areas: Darshan Bhavan, Jadavpur Vidyapith

        If your reply contains any LINK enclose it like '🔗 <a href='LINK' target='_blank'>INFO_ASKED_BY_USER</a>'

        If user asks for names of departments of a particular faculty{os.listdir("../xtracter/data/syllabus")} provide them the required list in a structured format
        If user doesn't mention faculty name provide them list of 5 departments using the provided list for each faculty.
        These are list of department from each faculty:
        arts: {os.listdir("../xtracter/data/syllabus/arts")}
        engineering-technology: {os.listdir("../xtracter/data/syllabus/engineering-technology")}
        interdisciplinary-studies-law-and-management: {os.listdir("../xtracter/data/syllabus/interdisciplinary-studies-law-and-management")}
        science: {os.listdir("../xtracter/data/syllabus/science")}
        Even if the user doesn't completely name the faculty, you should understand what he is trying to see and show him

        If user asks about general knowledge of a particular department reply strictly in the format 'ABOUT: FACULTY_NAME/DEPARTMENT_NAME'
        If user asks about courses of a particular department reply strictly in the format 'COURSES: FACULTY_NAME/DEPARTMENT_NAME'
        If user asks about the syllabus or courses of some particular course like ug, pg, bachelor, master, extra departmental, phd, doctorate, doctoral, diploma, certificate course etc. but doesn't tell the department, ask them the department and if they tell the department too then reply strictly in the format 'SYLLABUS: FACULTY_NAME/DEPARTMENT_NAME|COURSE_NAME'
  '''
)

class GeneralFunctions():
    def activateBot(self):
        self.bot = BotFunctions()
        
    def reply(self, query):
        global chatHistory
        chat_session = model.start_chat(
            history=chatHistory
        )
        time.sleep(2)
        response = chat_session.send_message(query)
        output = response.text.strip()

        if "NOTICE_DATE: " in output:
            output = self.bot.fetch_notice(date=output.replace("NOTICE_DATE: ",''))
        elif "NOTICE: " in output:
            output = self.bot.fetch_notice(keyword=output.replace("NOTICE: ",''))
        elif "NOTICE_RECENT_MORE" == output:
            output = self.bot.fetch_notice(more=True)
        elif "NOTICE_RECENT" == output:
            output = self.bot.fetch_notice()
        elif "ABOUT: " in output:
            output = self.bot.fetch_about(path=output.replace("ABOUT: ",'').lower())
        elif "COURSES: " in output:
            output = self.bot.fetch_courses(path=output.replace("COURSES: ",'').lower())
        elif "SYLLABUS: " in output:
            output = self.bot.fetch_syllabus(*output.replace("SYLLABUS: ",'').lower().split('|'))


        chatHistory.extend([{"role":"user","parts":[query]}, {"role":"model","parts":[output]}])
        if len(chatHistory)>40:
            chatHistory.pop(0)
            chatHistory.pop(0)
        return output

    def read_json(self, fileJSON):
        if os.path.exists(fileJSON):
            with open(fileJSON,"r",encoding="utf-8") as f:
                try:return json.load(f)
                except:pass
        return []

    def restart(self):
        global chatHistory
        global notices, recent_notice_fetched
        chatHistory = [
            {
                "role": "model",
                "parts": ["Hi I am ChatJU! How can I help you today?"]
            }
        ]
        notices = self.read_json("../xtracter/data/notices/notices.json")
        recent_notice_fetched = 0

    def convertCoursesToHTML(self, courses):
        code = ""
        for course in courses:
            duration = course['duration']
            intake = course['intake']
            syllabus = course['syllabus']
            curriculum = course['curriculum']
            absent_msg = "N/A"
            code += f"\n\n<b><code>{course['course']}</code></b>\n<b>Duration:</b> {duration if duration else absent_msg}\n<b>Intake:</b> {intake if intake else absent_msg}\n"

            code += "<b>Syllabus:</b> "
            if len(syllabus)>1:
                for link in syllabus:
                    code += f"\n● <a href='{link['link']}' target='_blank'>{link['title']}</a>"
            elif len(syllabus):
                code += f"<a href='{syllabus[0]['link']}' target='_blank'>{syllabus[0]['title']}</a>"
            else:
                code+=absent_msg

            code += "\n<b>Curriculum:</b> "
            if len(curriculum)>1:
                for link in curriculum:
                    code += f"\n● <a href='{link['link']}' target='_blank'>{link['title']}</a>"
            elif len(curriculum):
                code += f"<a href='{curriculum[0]['link']}' target='_blank'>{curriculum[0]['title']}</a>"
            else:
                code+=absent_msg
        return code

    def convertNoticesToHTML(self, notices):
        code=""
        for (i, notice) in enumerate(notices):
            code += f"\n\n<code>{i+1}.</code> <b>{notice['title']}</b>\n\
                <span>🔗 <a target='_blank' href={notice['link']}>{notice['link']}</a></span>\n"
            if notice['docs']:
                code += "Embedded Resources in the link:"
                for docs in notice['docs']:
                    code += f"\n<span>🔗 <a target='_blank' href={docs['link']}>{docs['heading']}</a></span>"
        return code

    def convrtAboutToHTML(self, data):
        return f"<b>Department of {data['name']}</b>\n\n{data['description']}"

class BotFunctions():
    def __init__(self):
        self.general = GeneralFunctions()

    def fetch_notice(self, date=None, keyword=None, more=False):
        global notices, recent_notice_fetched
        noticeRelevant = []

        if date:
            for notice in notices:
                text = notice['title'].replace('-',' ').replace(':',' ').replace('=',' ')
                if "07.03.2025" in text:print(text)
                words = text.split()
                extracted_dates = []
                for word in words:
                    try:
                        parsed_date = parser.parse(word, fuzzy=False, dayfirst=True)
                        extracted_dates.append(parsed_date)
                    except:
                        pass
                parsed_date = parser.parse(date, fuzzy=False, dayfirst=True)

                if parsed_date in extracted_dates:
                    noticeRelevant.append(notice)
                    if len(noticeRelevant)>10:
                        break

            output = "Here are few notices related to the given date:\n"
            drawback = "Sorry, I can't find any notice corresponding to the mentioned date."

        elif keyword:
            for notice in notices:
                threshold = 0.8
                if (fuzz.partial_ratio(keyword.lower(), notice['title'].lower()) > threshold):
                    noticeRelevant.append(notice)
                    if len(noticeRelevant)>10:
                        break

            output = "Here are few notices matching your search:\n"
            drawback = "Sorry, I can't find any notice corresponding to your search."

        else:
            if more:
                recent_notice_fetched += 10
                output = "Here are some few more recent notices:\n"
            else:
                recent_notice_fetched = 10
                output = "Here are some few recent notices:\n"

            noticeRelevant = notices[recent_notice_fetched-10:recent_notice_fetched]
            drawback = "Sorry, no more notices found!"
        
        if noticeRelevant:
            output += self.general.convertNoticesToHTML(noticeRelevant)
        else:
            output = drawback
        
        return output

    def fetch_about(self, path):
        if path:
            data = self.general.read_json(f"../xtracter/data/syllabus/{path}/about.json")
            output = self.general.convrtAboutToHTML(data)
        else:
            output = "Sorry, can't find anything related to your question!"
        return output

    def fetch_courses(self, path):
        if path:
            name = self.general.read_json(f"../xtracter/data/syllabus/{path}/about.json")['name']
            courses = self.general.read_json(f"../xtracter/data/syllabus/{path}/courses.json")
            output = f"The list of courses available in the <b>Department of {name}</b> are as follows:"
            output += self.general.convertCoursesToHTML(courses)
        else:
            output = "Sorry, can't find anything related to your question!"
        return output

    def fetch_syllabus(self, path, course_name):
        isBachelor = lambda x: 'bachelor' in x.lower() or 'BA' in x or 'B.' in x
        isMaster = lambda x: 'master' in x.lower() or x.startswith('M') or 'idc/mdc ' in x.lower()
        isDoctor = lambda x: 'doctor' in x.lower() or 'Ph.D' in x
        isExtraDept = lambda x: 'extra departmental' in x.lower();
        isDiploma = lambda x: 'diploma' in x.lower() or 'PG ' in x

        if path:
            dept_name = self.general.read_json(f"../xtracter/data/syllabus/{path}/about.json")['name']
            data = self.general.read_json(f"../xtracter/data/syllabus/{path}/courses.json")
            COURSES = {'bachelor': [x for x in data if isBachelor(x['course'])],
                    'master': [x for x in data if isMaster(x['course'])],
                    'doctor': [x for x in data if isDoctor(x['course'])],
                    'extra dept': [x for x in data if isExtraDept(x['course'])],
                    'diploma': [x for x in data if isDiploma(x['course'])]}

            regexBachelor = r"\b(bachelors?|b\.?a\.?|b\.?sc\.?|b\.?e\.?|b\.?tech\.?|u\.?g|under[^a-zA-Z0-9]*grad|under[^a-zA-Z0-9]*graduate|b\.?pharm|b\.?ed|b\.?p\.?ed)\b"
            regexMaster = r"\b(masters?|m\.?a\.?|m\.?sc\.?|m\.?e\.?|m\.?tech\.?|m\.?pharm|m\.?phil|mca|pg|post[^a-zA-Z0-9]*graduate|post[^a-zA-Z0-9]*grad|inter[^a-zA-Z0-9]*disciplinary|multi[^a-zA-Z0-9]*disciplinary|idc|mdc)\b"
            regexDoctor = r"\b(ph\.?d\.?|doctorate|doctoral|dphil|research\s?(?:program(?:me|mes|s)*|degrees?|course|stud(?:ies|y)|opportunit(?:ies|y)|fellowships?|scholarships?))\b"
            regexExtraDept = r"\b(extra[^a-zA-Z0-9]*departmental[^a-zA-Z0-9]*?(?:courses?|subjects?|program(?:me|mes|s)*|electives?)*)\b"
            regexDiploma = r"\b(diploma|pg\s?(?:certificate|cert)|post\s?graduate\s?(?:certificate|diploma))\b"

            REGEX = {'bachelor':regexBachelor,'master':regexMaster,'doctor':regexDoctor,'extra dept':regexExtraDept,'diploma':regexDiploma}
            relevant = []

            for course, regex in REGEX.items():
                if re.match(regex,course_name,re.IGNORECASE):
                    relevant.extend(COURSES[course])

            output = f"The list of courses, you asked for, available in the <b>Department of {dept_name}</b> are as follows:"
            if relevant:
                output += self.general.convertCoursesToHTML(relevant)
            else:
                output = f"No matching courses could be found in the Department of {dept_name}"
        else:
            output = "Sorry, can't find anything related to your question!"
        return output

if __name__ == "__main__":
    generalObject = GeneralFunctions()
    generalObject.restart()
    while ((query := input("User: ").strip()) != 'quit'):
        print("Bot:",generalObject.reply(query))