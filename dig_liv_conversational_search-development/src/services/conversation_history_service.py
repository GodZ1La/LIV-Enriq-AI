import firebase_admin
from firebase_admin import firestore
from google.cloud import firestore


db = firestore.Client(database="(default)")
convesational_messages_ref = db.collection('conversational_messages')

def load_conversation_history_front(session_id):
    convesational_messages = convesational_messages_ref.where('session_id','==',session_id).order_by("created_at", direction=firestore.Query.DESCENDING).limit(20).stream()
    return [message.to_dict() for message in convesational_messages]


def load_conversation_history(session_id):
    convesational_messages = convesational_messages_ref.where('session_id','==',session_id).order_by("created_at", direction=firestore.Query.DESCENDING).limit(10).stream()
    
    conversation_buffer = []
    invertbuffer = []
    for message in convesational_messages:
        
        message_data = message.to_dict()
        # assert "content" is a list
        if not isinstance(message_data.get('content'), list):
            message_data['content'] = [message_data.get('content')]

        if(message_data['message_type'] == 'HumanMessage'):
            bufferedMessage = "Usuario: " + message_data.get('content')[0].get('value')
        else:
            bufferedMessage = "Iris: " + message_data.get('content')[0].get('value')
        conversation_buffer.append(bufferedMessage)
    invertbuffer = conversation_buffer[::-1]
    ##if len(invertbuffer) > 0:
    ##    invertbuffer = invertbuffer[:-1]
    return invertbuffer


def format_conversation_history(conversation_history):
    formatted_history = ""
    for message in conversation_history:
        formatted_history += message + "\n"
    return formatted_history


def create_message (user_id, session_id, visitor_id, user_name, content,intent, message_type= "HumanMessage"):
    new_message_data = {
        'user_id': user_id,
        'session_id': session_id,
        'visitor_id':visitor_id,
        'user_name':user_name,
        'message_type': message_type,
        'created_at': firestore.SERVER_TIMESTAMP,
        'content': content,
        'intent': intent,
    }
    new_message_ref = convesational_messages_ref.document()
    new_message_ref.set(new_message_data)
    return new_message_ref.get().to_dict()