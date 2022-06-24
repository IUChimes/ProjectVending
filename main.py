from fastapi import FastAPI
from routers.auth import router as authRouter
from routers.user import router as userRouter
from routers.product import router as productRouter
from routers.vendor import router as vendorRouter

app = FastAPI()
app.include_router(authRouter)
app.include_router(userRouter)
app.include_router(productRouter)
app.include_router(vendorRouter)