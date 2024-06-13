import firebase_admin
from firebase_admin import firestore
from google.cloud import firestore


db = firestore.Client(database="(default)")
convesational_sessions_ref = db.collection('convesational_sessions')

def get_session_by_userid (user_id: str):
    
    convesational_sessions = convesational_sessions_ref.where('user_id','==',user_id).stream()
    session_data = None 

    for session in convesational_sessions:
        session_data = session.to_dict()
        session_data['id'] = session.id
        session_data["session_id"] = session_data["id"]
        del session_data["id"]
        print(f"Sesion ID: {session.id}")
        print(f"User ID: {session_data['user_id']}")
        print(f"Fecha y hora de creación: {session_data['created_at']}")
        # print(f"Lock de conversación: {session_data['convesational_lock']}")
        
    return session_data

def validate_session(user_id):
    # Revisar si el usuario ya tiene una sesión creada
    session = get_session_by_userid(user_id)
    # En caso de que no, se crea una nueva sesión
    if session == None:
        print("No se encontro la sesión")
        session= create_session(user_id)
    return session

def create_session (user_id: str):
    new_session_data = {
        'user_id': user_id,
        'created_at': firestore.SERVER_TIMESTAMP,
        'conversational_lock': 'false'
    }

    new_session_ref = convesational_sessions_ref.document()
    new_session_ref.set(new_session_data)
    print(f"New session created with ID: {new_session_ref.id}")
    #new_session_data['id'] = new_session_ref.id 
    return new_session_ref.get().to_dict()

#def load_convesation_memmory():
#    db = firestore.Client(database="(default)")