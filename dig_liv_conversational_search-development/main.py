from  src.chat import get_parameters,respond
from fastapi import FastAPI
##from .routes import router
from pydantic import BaseModel
from fastapi import APIRouter
import uvicorn
from src.services.sesion_service import get_session_by_userid, create_session, validate_session
from src.services.conversation_history_service import load_conversation_history, format_conversation_history, create_message, load_conversation_history_front
from fastapi.middleware.cors import CORSMiddleware
import json

class CreateSessionRequest(BaseModel):
    user_id: str


class TemplatePath(BaseModel):
    query: str
    sesionId : str
    name:str

class MessageRequestTemplate(BaseModel):
    user_id : str
    session_id : str
    user_query: str
    visitor_id : str
    user_name : str



app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()

@router.post("/conversationalSession")
def conversational_sesion(req: CreateSessionRequest):
    data = req.dict()
    user_id = data.get('user_id') 
    session = validate_session(user_id)
    return session

@router.get("/loadHistory")
def loadConversationHistory(session_id: str):
    conversationalBuffer = load_conversation_history_front(session_id)
    # formatted_conversationBuffer = format_conversation_history(conversationalBuffer)
    # return formatted_conversationBuffer
    response = {"conversational_buffer":conversationalBuffer}
    return response


@router.get("/healthz")  # Default endpoint when you visit "/api"
async def healthcheck():
    return {"response": "OK"}


@router.post("/chat")
async def ask(req: MessageRequestTemplate):
    
    #Step 1. Persist the new message from the User
    data= req.dict()
    print(f' Aquí estoy.. data: {data} con tipo: {type(data)}')
    content = {
        "content_type": "simple_message",
        "value": data.get('user_query') 
    }
    
    human_message = create_message(data.get('user_id'), data.get('session_id'), data.get('visitor_id'),data.get('user_name'), content, "IntentHuman","HumanMessage")
    
    # Step 2. Load the conversation history
    history = load_conversation_history(data.get('session_id'))
    ##print(history)
    formatted_history = format_conversation_history(history)

    # Step 3. Send the request to the chatbot 

    parameters = get_parameters()
    response,intentresponse = respond(parameters,data,formatted_history)
    ##print(f'Salida {response}')
    # Step 4. Persist AI Message
    
    if isinstance(response, str) and isinstance(intentresponse, str):
        strResponse = response
        strResponseIntent = intentresponse
    else:
        strResponse = json.dumps(response)
        strResponseIntent = json.dumps(intentresponse)

    if "recommendation_message" in strResponse.lower():
        content_type = "recommendation_message"
    else:
        content_type = "simple_message"
        
    ai_content= {
        "content_type":content_type,
        "value": strResponse
    }   

    ai_message = create_message(data.get('user_id'),
                                data.get('session_id'),
                                data.get('visitor_id'),data.get('user_name'),
                                ai_content,
                                strResponseIntent.lower(),
                                "AIMessage")
    
    # Step 5. Message containing AI response and human query
    # message = {
    #     "human_message":human_message,
    #     "ai_message":ai_message
    # }

    if type(response) == dict: 
       response["human_message"] = human_message
       response["ai_message"] = ai_message
       return response
    else:
        response_message = {
           "text_message": response,
           "output":{},
           "human_message": human_message,
           "ai_message": ai_message
        }
        return response_message
    
app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)