from fastapi import FastAPI
from notes_service.api.router import router


app = FastAPI(title="notes service")

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
