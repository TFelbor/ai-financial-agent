import uvicorn
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", 
                host="0.0.0.0", 
                port=8000, 
                reload=True,
                workers=1)  # Set to 1 during development for easier debugging
