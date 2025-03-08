import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
from datetime import datetime
import json
from dateutil import parser

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
  system_instruction="You are a chatbot designed specifically for Jadavpur University. Don't entertain queries apart from university related information and information on courses, department, notices, curriculum. Strictly deny any other query."
  f"If the user asks for any notice of the university, reply in the format 'NOTICE: NOTICE_KEYWORD' strictly, and if the user asks to show recent notices or just notices, reply 'NOTICE_RECENT' stricty and if the user aks for more recent notices reply 'NOTICE_RECENT_MORE', and if the user asks to show notices on some particular date reply in the format 'NOTICE_DATE: DATE-MONTH_NAME-YEAR', eg if it says two months back, you should return that particular month, today's date is {datetime.today()}",
)

def read_json(fileJSON):
    if os.path.exists(fileJSON):
        with open(fileJSON,"r",encoding="utf-8") as f:
            try:return json.load(f)
            except:pass
    return []

def restart():
    global chatHistory
    global notices, recent_notice_fetched
    chatHistory = [
        {
            "role": "model",
            "parts": ["Hi I am ChatJU! How can I help you today?"]
        }
    ]
    notices = read_json("../xtracter/data/notices/notices.json")
    recent_notice_fetched = 0
    # notice_titles = [x['title'] for x in notices]
    # notice_links = [x['link'] for x in notices]
    # notice_docs = [x['docs'] for x in notices]

def fetch_notice(date=None,keyword=None,more=False):
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
        for (i, notice) in enumerate(noticeRelevant):
            output += f"\n\n<code>{i+1}.</code> <b>Title:</b> {notice['title']}\n\
                <b>Link:</b> 🔗 <a target='_blank' href={notice['link']}>{notice['link']}</a>\n\
                <b>Embedded Resources in the link:</b>"
            for docs in notice['docs']:
                output += f"\n🔗 <a target='_blank' href={docs['link']}>{docs['heading']}</a>"
    else:
        output = drawback    
    
    return output

def reply(query):
    global chatHistory
    chat_session = model.start_chat(
        history=chatHistory
    )
    time.sleep(2)
    response = chat_session.send_message(query)
    output = response.text.strip()

    if "NOTICE_DATE: " in output:
        output = fetch_notice(date=output.replace("NOTICE_DATE: ",''))
    elif "NOTICE: " in output:
        output = fetch_notice(keyword=output.replace("NOTICE: ",''))
    elif "NOTICE_RECENT_MORE" == output:
        output = fetch_notice(more=True)
    elif "NOTICE_RECENT" == output:
        output = fetch_notice()


    chatHistory.extend([{"role":"user","parts":[query]}, {"role":"model","parts":[output]}])
    if len(chatHistory)>50:
        chatHistory.pop(0)
        chatHistory.pop(0)
    return output

if __name__ == "__main__":
    restart()
    while ((query := input("User: ").strip()) != 'quit'):
        print("Bot:",reply(query))