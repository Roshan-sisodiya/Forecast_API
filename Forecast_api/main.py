from Controller import MainController
from fastapi import FastAPI
from fastapi import APIRouter
import uvicorn


app = FastAPI()
# Startup event → open Redis pool
@app.on_event("startup")
async def startup_event():
    print("🚀 Application Started")
    #await RedisClient.open()


# Shutdown event → close Redis pool
@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Application Stopping")
    #await RedisClient.close()


# Register routers
app.include_router(MainController.router, prefix="/api", tags=["index"])


def main():
    print("Application Started")
    uvicorn.run(app, host="0.0.0.0",port=5001)




if __name__ == "__main__":
    main()
