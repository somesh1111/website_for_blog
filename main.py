from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from blog_generator import BlogGenerator
from stock_data import StockDataExtractor

app = FastAPI()

templates = Jinja2Templates(directory="templates")

API_KEY = "AIzaSyBUycb8lBogwVm2MsSD2UsQ7ExF3yknAys"

blog_ai = BlogGenerator(API_KEY)

# Google sheet setup
CREDS_FILE = "credentials.json"
SHEET_ID = "1FP2CZs8GHkzbVNWLmrjz91JdMck8q4tvWxsZ8BB_AZQ"

stock_extractor = StockDataExtractor(CREDS_FILE, SHEET_ID)
stock_extractor.load_data()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "blog": None}
    )


@app.post("/generate")
def generate_blog(request: Request, notification: str = Form(...)):

    # get company history from sheet
    stock_history = stock_extractor.get_company_history(notification)

    blog = blog_ai.generate_blog(notification, stock_history)

    blog = blog.replace("\n", "<br>")

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "blog": blog}
    )