from fastapi import FastAPI

from questions.router import router as router_users

app = FastAPI(
    debug=True,
    title='Bewise.ai v.1',
    description='API добавления и вывода вопросов'
)

app.include_router(
    router_users
)
