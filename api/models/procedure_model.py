from pydantic import BaseModel
 
class TextInputModel(BaseModel):
    message: str
    
class ChatResponseModel(BaseModel):
    assistant: str