from fastapi import FastAPI

from src.routes.main_router import main_router

app = FastAPI()

app.include_router(main_router)


def main() -> None:
    print("Hello from Skills-manager !")


if __name__ == "__main__":
    main()
