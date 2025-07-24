import pandas as pd 
import websocket
import asyncio
import numpy as np
import json
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from database import Base, engine, get_db, localSession
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Candlesticks
from websocket_ import on_close, on_error, on_open, websocket_manager
import threading

manager = websocket_manager()
binance_data_queue = asyncio.Queue()


    

origins = ["*"]

async def lifespan(app: FastAPI):

    loop = asyncio.get_event_loop()
    def on_message(ws, message):
        data = json.loads(message)
        db = localSession()
        k = data["k"]
        try:
            if k["x"] == True:
                
                new_data = Candlesticks(
                    open = float(k["o"]),
                    high = float(k["h"]),
                    low = float(k["l"]),
                    close = float(k["c"]),
                    volume = float(k["v"])               
                )
                db.add(new_data)
                db.commit()
                db.refresh(new_data)
                print("the data was added nicely into the database ")
                try:
                    message = json.dumps(k)
                    asyncio.run_coroutine_threadsafe(binance_data_queue.put(message), loop)
                    print("the message was added to the que")
                except RuntimeError as e:
                    print("could not put the message in the que")
        
        except Exception as e:
            db.rollback()
            print(f"there was an error during insertion of the data. {e}")
        finally:
            db.close()
    print("The app is starting.")
    BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
    ws = websocket.WebSocketApp(BINANCE_WS_URL, on_close=on_close, on_open=on_open, on_message=on_message, on_error=on_error)
    print("initializing the websocket thread")


    
    
    try:
        ws_task = threading.Thread(target=ws.run_forever, daemon=True).start()
        print("finished initializign the threads")
        Base.metadata.create_all(bind=engine)
        print("the table created")
        
    except Exception as e:
        print(f"There was an error: {e}")
    
    try:
        yield
    finally: 
        print("The app is now closing ")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/get_data/")
async def get_data(db: Session = Depends(get_db)):
    return {
        "data": "this is the data"
    }

@app.websocket("/ws")
async def live_data(websocket: WebSocket):
    await manager.connect(websocket=websocket)
    try:
        while True:
            data = await binance_data_queue.get()
            await manager.send_to(data, websocket)
            binance_data_queue.task_done()
            await asyncio.sleep(2)
            print("you are connected and ready for another one ")
    except WebSocketDisconnect as e: 
        manager.disconnect(websocket)
        print("the websocket was disconnected.")
    except Exception as e:
        print(f"There was an error during the sending. {e}")
    


