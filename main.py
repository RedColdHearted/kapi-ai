import os

import speech_recognition as sr
from langchain_community.llms.yandex import YandexGPT
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.memory import ConversationBufferMemory


from dotenv import load_dotenv

from executors.manager import ExecutorManager
from utils import get_yc_iam_token

load_dotenv()

DEFAULT_AI_TEMPLATE = """You are an assistant of a desktop application named `Kapi ai`, which is used to talk with the user and launch programs or functions.
After analyzing what the user says, you must issue a response in JSON format:
(
message: <A conversational response to the user, for example: I'm launching YouTube! The language in which you compose the 'message' must be on Russian>,
app: <dict, argument which shows that user needs to run app>,
    (
    name: <The name of the application that the user wants to launch, for example: browser, or calculator. The name should be in English. You must understand that if a user asks to open a social network, then it can be opened in a browser>,
    params: <params that are needed to launch an application, for example to launch YouTube in the browser 'url' : 'https://youtube.com'>,
    )
)
Keep in mind that the user may not want to launch anything but will simply talk to you.
Additionally, answer with JSON serializable types.

list of apps with arguments, if app not in list, answer with empty `app_name`:
    browser(url: str),
    calculator(),
    file_explorer(),

User request: {user_message}"""

#TODO: llm memory

prompt = PromptTemplate.from_template(DEFAULT_AI_TEMPLATE)
llm = YandexGPT(
    iam_token=get_yc_iam_token(),
    model_uri=os.getenv("YC_MODEL_URI"),
    folder_id=os.getenv("YC_FOLDER_ID"),
    temperature=0.4,
    max_tokens=2000,
)
chain = prompt | llm | JsonOutputParser()
apps_manager = ExecutorManager()

def request_llm(user_message: str) -> str:
    chain_result = chain.invoke(user_message)
    if chain_result["app"]:
        apps_manager.run(
            app_name=chain_result["app"]["name"],
            params=chain_result["app"]["params"],
        )
    return chain_result["message"]

def voice_recognition() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

request_llm("открой мне проводник")
