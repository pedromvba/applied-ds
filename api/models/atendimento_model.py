from pydantic import BaseModel
 
class AtendimentoInputModel(BaseModel):
    origem: str
    raio: int
    
class AtendimentoResponseModel(BaseModel):
    atendimento: str
    tempo_viagem: str