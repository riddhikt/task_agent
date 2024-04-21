from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from uagents import Model
import google.generativeai as genai
import uvicorn

AGENT_ADDRESS = "agent1qgkeu08u8xyve9acze25js5gd6yyt5czwny83wve5z5r5l726mh3jg00ce3"


class Message(Model):
    message: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
genai.configure(api_key='AIzaSyANvgl8Qc8lW3bPOxtcFzj7yFgkjbPBxZE')
description_model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")


@app.post("/task-generation")
async def task_generation(req: Message):
    try:
        print("the request is - ", req)
        print(type(req))
        prompt = f"""you are an agent that will give me 10 tasks based on the addiction I will give you, make sure 
        the tasks can be crosschecked by clicking a photo because i would be checking if the user has completed the 
        task or not. also with every task give a suggestion what the photo could be. for example if you have given 
        the task as drink water, the expected image would be "a selfie of you drinking water" and a description why 
        this task benefit the user. Also give me all of these in json format where there are just tasks, 
        expected photo, and description it requires. Now i will tell you what addiction the user is facing: {Message}"""
        response = description_model.generate_content([prompt])
        # Remove unwanted backticks and trim whitespace
        clean_response = response.text
        clean_response = clean_response.replace("```json", "").replace("```", "").strip()
        # Convert the cleaned string to a JSON object
        response_json = json.loads(clean_response)
        return response_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return "Hello from the task generation Agent"


if __name__ == "__main__":
    uvicorn.run("task_agent:app", host="0.0.0.0", port=8002, reload=True)
