from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
import httpx
import asyncio
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import os
import uuid
from datetime import datetime

app = FastAPI(title="Ollama Chat Interface")

OLLAMA_BASE_URL = "http://localhost:11434"
CONFIG_FILE = "config.json"
PROMPTS_FILE = "saved_prompts.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        "model": "llama3.2",
        "temperature": 0.7,
        "top_p": 0.9,
        "system_prompt": "You are a helpful assistant.",
        "max_tokens": 4096,
        "stream": True,
        "num_ctx": 2048,
        "repeat_penalty": 1.1
    }

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def load_prompts():
    if os.path.exists(PROMPTS_FILE):
        with open(PROMPTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_prompts(prompts):
    with open(PROMPTS_FILE, 'w') as f:
        json.dump(prompts, f, indent=2)

class ChatMessage(BaseModel):
    message: str
    model: str = "llama3.2"
    system_prompt: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    num_ctx: Optional[int] = None
    repeat_penalty: Optional[float] = None

class ModelSwitchRequest(BaseModel):
    model: str

class ConfigRequest(BaseModel):
    model: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    system_prompt: Optional[str] = None
    max_tokens: Optional[int] = None
    stream: Optional[bool] = None
    num_ctx: Optional[int] = None
    repeat_penalty: Optional[float] = None

class SavePromptRequest(BaseModel):
    name: str
    prompt: str
    description: Optional[str] = None

class UsePromptRequest(BaseModel):
    prompt_id: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.get("/board", response_class=HTMLResponse)
async def board_page():
    """Sirve la página del pizarrón de stickers"""
    try:
        with open("static/board.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Board page not found")

@app.get("/board2", response_class=HTMLResponse)
async def board2_page():
    """Sirve la página del pizarrón avanzado v2"""
    try:
        with open("static/board2.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Board v2 page not found")

@app.post("/chat")
async def chat(request: ChatMessage):
    config = load_config()
    
    async def generate_stream():
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                payload = {
                    "model": request.model or config.get("model", "llama3.2"),
                    "prompt": request.message,
                    "stream": True,
                    "options": {
                        "temperature": request.temperature if request.temperature is not None else config.get("temperature", 0.7),
                        "top_p": request.top_p if request.top_p is not None else config.get("top_p", 0.9),
                        "num_ctx": request.num_ctx if request.num_ctx is not None else config.get("num_ctx", 2048),
                        "repeat_penalty": request.repeat_penalty if request.repeat_penalty is not None else config.get("repeat_penalty", 1.1)
                    }
                }
                
                # Priorizar system_prompt del request sobre el global
                system_prompt_to_use = request.system_prompt if request.system_prompt is not None else config.get("system_prompt")
                
                if system_prompt_to_use:
                    prompts = load_prompts()
                    
                    for prompt_id, prompt_data in prompts.items():
                        if prompt_data["prompt"] == system_prompt_to_use:
                            payload["system"] = f"[ID:{prompt_id}] {system_prompt_to_use}"
                            break
                    else:
                        payload["system"] = system_prompt_to_use
                
                async with client.stream(
                    "POST",
                    f"{OLLAMA_BASE_URL}/api/generate",
                    json=payload
                ) as response:
                    if response.status_code != 200:
                        yield f"data: {{\"error\": \"Error communicating with Ollama\"}}\n\n"
                        return
                    
                    async for chunk in response.aiter_lines():
                        if chunk:
                            try:
                                data = json.loads(chunk)
                                if "response" in data:
                                    yield f"data: {{\"response\": \"{data['response'].replace('"', '\\"')}\"}}\n\n"
                                if data.get("done", False):
                                    yield "data: {\"done\": true}\n\n"
                                    break
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.RequestError as e:
            yield f"data: {{\"error\": \"Connection error: {str(e)}\"}}\n\n"
    
    return StreamingResponse(generate_stream(), media_type="text/plain")

@app.get("/models")
async def list_models():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Error fetching models")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

@app.post("/switch-model")
async def switch_model(request: ModelSwitchRequest):
    config = load_config()
    config["model"] = request.model
    save_config(config)
    return {"message": f"Model switched to {request.model}"}

@app.get("/config")
async def get_config():
    return load_config()

@app.post("/config")
async def update_config(request: ConfigRequest):
    config = load_config()
    
    if request.model is not None:
        config["model"] = request.model
    if request.temperature is not None:
        config["temperature"] = request.temperature
    if request.top_p is not None:
        config["top_p"] = request.top_p
    if request.system_prompt is not None:
        config["system_prompt"] = request.system_prompt
    if request.max_tokens is not None:
        config["max_tokens"] = request.max_tokens
    if request.stream is not None:
        config["stream"] = request.stream
    if request.num_ctx is not None:
        config["num_ctx"] = request.num_ctx
    if request.repeat_penalty is not None:
        config["repeat_penalty"] = request.repeat_penalty
    
    save_config(config)
    return {"message": "Configuration updated successfully", "config": config}

@app.get("/prompts")
async def get_prompts():
    prompts = load_prompts()
    return {"prompts": prompts}

@app.post("/prompts")
async def save_prompt(request: SavePromptRequest):
    prompts = load_prompts()
    prompt_id = str(uuid.uuid4())
    
    prompts[prompt_id] = {
        "id": prompt_id,
        "name": request.name,
        "prompt": request.prompt,
        "description": request.description or "",
        "created_at": datetime.now().isoformat(),
        "last_used": None
    }
    
    save_prompts(prompts)
    return {"message": "Prompt saved successfully", "prompt_id": prompt_id, "prompt": prompts[prompt_id]}

@app.post("/prompts/use")
async def use_prompt(request: UsePromptRequest):
    prompts = load_prompts()
    
    if request.prompt_id not in prompts:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    prompt = prompts[request.prompt_id]
    prompt["last_used"] = datetime.now().isoformat()
    
    config = load_config()
    config["system_prompt"] = prompt["prompt"]
    save_config(config)
    save_prompts(prompts)
    
    return {"message": f"Prompt '{prompt['name']}' applied successfully", "prompt": prompt}

@app.delete("/prompts/{prompt_id}")
async def delete_prompt(prompt_id: str):
    prompts = load_prompts()
    
    if prompt_id not in prompts:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    deleted_prompt = prompts.pop(prompt_id)
    save_prompts(prompts)
    
    return {"message": f"Prompt '{deleted_prompt['name']}' deleted successfully"}

@app.get("/prompts/{prompt_id}")
async def get_prompt(prompt_id: str):
    prompts = load_prompts()
    
    if prompt_id not in prompts:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    return {"prompt": prompts[prompt_id]}

@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_ollama(path: str, request):
    try:
        async with httpx.AsyncClient() as client:
            url = f"{OLLAMA_BASE_URL}/api/{path}"
            
            if request.method == "GET":
                response = await client.get(url, params=request.query_params)
            elif request.method == "POST":
                body = await request.body()
                response = await client.post(url, content=body, headers={"Content-Type": "application/json"})
            elif request.method == "PUT":
                body = await request.body()
                response = await client.put(url, content=body, headers={"Content-Type": "application/json"})
            elif request.method == "DELETE":
                response = await client.delete(url)
            
            return response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)