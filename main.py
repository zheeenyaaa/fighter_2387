from fastapi import FastAPI
import routers


app = FastAPI()
app.include_router(routers.router)

# !!!!make prefix api/v1/

@app.get("/health")
async def health():
	return {
		"status": "OK"
	}


