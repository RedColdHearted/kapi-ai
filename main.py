import os

import speech_recognition as sr
from langchain_community.llms.yandex import YandexGPT
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

from executors.manager import ExecutorManager
from utils import RecognizedData, get_yc_iam_token

load_dotenv()

DEFAULT_AI_TEMPLATE = """You are an assistant of a desktop application named Kapi ai, which is used to talk with the user and launch programs or functions or websites.
After analyzing what the user says, you must issue a response in JSON format:
(
    message: <A conversational response to the user, for example: I'm launching YouTube! The language in which you compose the 'message' must be on Russian>,
    app: <dict, argument which shows that user needs to run app>,
        (
        name: <The name of the application that the user wants to launch, for example: browser, or calculator. The name should be in English. You must understand that if a user asks to open a social network, then it can be opened in a browser>,
        params: <params that are needed to launch an application, for example to launch YouTube in the browser 'url' : 'https://youtube.com...'>,
        )
)
Keep in mind that the user may not want to launch anything but will simply talk to you.
Additionally, answer with JSON serializable types.

list of apps with arguments, if app not in list, answer with empty app_name:
    browser(url: str) comment: if user asking to pen any YT chanel or search by name than you should open with corresponding link,
    calculator(),
    file_explorer(),

User request: {user_message}
"""

#TODO: llm memory

prompt = PromptTemplate.from_template(DEFAULT_AI_TEMPLATE)
llm = YandexGPT(
    iam_token=get_yc_iam_token(),
    model_uri=os.getenv("YC_MODEL_URI"),
    folder_id=os.getenv("YC_FOLDER_ID"),
    temperature=0.6,
    max_tokens=2000,
)
chain = prompt | llm | JsonOutputParser()
apps_manager = ExecutorManager()

def request_llm(user_message: str) -> str:
    ai_answer = chain.invoke({"user_message": user_message})
    if ai_answer["app"]:
        apps_manager.run(
            app_name=ai_answer["app"]["name"],
            params=ai_answer["app"]["params"],
        )
    return ai_answer

def record_and_recognize() -> RecognizedData:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Speak")
        audio_data = recognizer.listen(source, phrase_time_limit=50)
    try:
        text = recognizer.recognize_google(audio_data, language='ru-RU')
        return RecognizedData(text=text)
    except sr.UnknownValueError:
        return RecognizedData(err="Speech recognition failed.")
    except sr.RequestError as err:
        return RecognizedData(err=f"Speech recognition service error: {err}")

while True:
    # recognized_data = record_and_recognize()
    new_message = input("Введите что-то: ")
    print(request_llm(new_message))
