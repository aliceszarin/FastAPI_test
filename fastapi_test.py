from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Optional
import uvicorn
import nest_asyncio

nest_asyncio.apply()
app = FastAPI()

class Item(BaseModel):
    nome: str
    idade: int
    hobbies: Optional [str] = None
    
class UpdateItem(BaseModel):
     nome: Optional[str] = None
     idade: Optional[int] = None
     hobbies: Optional[str] = None

inventory = {}
# inventory = {
#         1: {
#             "nome": "João",
#             "idade": 23,
#             "sexo": "male"
            
#         }
#     }

#Esse {item_id} pode ser qualquer coisa:
    
def validacao_item_id(item_id):
    if item_id > 0:
        return item_id
    else:
        raise HTTPException(status_code=400, detail="Item ID inválido")
        
@app.get('/pesquisar/{item_id}')
def pegar_item(item_id: int):
    validacao_item_id(item_id)
    if item_id in inventory:
        return inventory[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item NOT FOUND")

@app.post("/criar/{item_id}") #{item_id} é um path parameter
#REQUEST BODY
async def novo_dado(item_id: int, item: Item):
    validacao_item_id(item_id)
    if item_id in inventory:
        raise HTTPException(status_code=409, detail="CONFLICT, Item já existe")

    inventory [item_id] = item
    # inventory [item_id] = {"nome":item.nome, "idade": item.idade, "sexo": item.sexo  }
    return inventory[item_id]
 
@app.put("/alterar/{item_id}")
async def alterar_dado(item_id: int, item: UpdateItem):
    validacao_item_id(item_id)
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item NOT FOUND")
    
    if item.nome != None:
        inventory[item_id].nome = item.nome
        
    if item.idade != None:
        inventory[item_id].idade = item.idade
    
    if item.hobbies != None:
        inventory[item_id].hobbies = item.hobbies
        
    return inventory[item_id] 
                  
@app.delete("/deletar/{item_id}")
async def deletar_dado(item_id: int = Path(..., description="DELETA OF US")):
    validacao_item_id(item_id)
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item NOT FOUND") 
    else:
        del inventory[item_id]

# INICIALIZAR API
uvicorn.run(app, host='0.0.0.0', port= 8002)
