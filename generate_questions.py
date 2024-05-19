"""
    Generates questions to questions folder
    By default only updates files staratingwith '-' or not existing files
    Add console argument 'all' to update all the questions
"""

import human_format_cat_gen

import os
from dotenv import load_dotenv
import unicodedata
import re
import json
import aiohttp
import asyncio
import sys


QUESTION_DIR = "questions"
QUESTIONS_COUNT = 15


# convert given value into form which can be in a filename
def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKC', value)
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

async def get_questions_from_api(client_session, category):
    API_URL = os.getenv("API_URL")
    API_KEY = os.getenv("API_KEY")
    headers = {"X-Api-Key": API_KEY}

    data = {
        "topic": category,
        "limit": QUESTIONS_COUNT,
    }

    response = await client_session.post(f'{API_URL}/get_question_by_topic', json=data, headers=headers)

    if (response.status == 200):
        response_json = await response.json()
        questions_data = response_json["answers"]
        questions = []

        for i in range(len(questions_data)):
            questions.append({
                "question": questions_data[i]["question"],
                "right_answer": questions_data[i]["answer"],
            })

        return questions
    else:
        print("Response Log:", await response.text())
        raise Exception("Error getting response, status code NOT 200") 


async def generate(regenerate_all=False):
    if os.path.exists(".env"):
        load_dotenv(".env", override=True)

    categories_dict = human_format_cat_gen.generate()

    if not os.path.exists(QUESTION_DIR):
        os.makedirs(QUESTION_DIR)

    client_session = aiohttp.ClientSession() 
    for human_form, full_form in categories_dict.items():
        filename_form = slugify(full_form)

        regenerate_cur = regenerate_all
        if(os.path.exists(os.path.join(QUESTION_DIR, "-" + f"{filename_form}.json"))):
            os.remove(os.path.join(QUESTION_DIR, "-" + f"{filename_form}.json"))
            regenerate_cur = True
        elif not os.path.exists(os.path.join(QUESTION_DIR, f"{filename_form}.json")):
            regenerate_cur = True

        if(regenerate_cur):
            file_contents = {
                "category_full_form": full_form,
                "category_human_form": human_form,
                "category_filename_form": filename_form,
                "questions": await get_questions_from_api(client_session, full_form)
            }

            with open(os.path.join(QUESTION_DIR, f"{filename_form}.json"), "w", encoding="utf-8") as f:
                json.dump(file_contents, f, ensure_ascii=False, indent=4)

    await client_session.close()


if __name__ == "__main__":
    regenerate_all = False
    if(len(sys.argv) > 1 and sys.argv[1] == "all"):
        regenerate_all = True

    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate(regenerate_all))