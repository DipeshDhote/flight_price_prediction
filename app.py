
# from fastapi import FastAPI, Form, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel
# from src.flight_price_prediction.pipelines.prediction_pipeline import PredictPipeline, CustomData
# import datetime

# app = FastAPI()

# templates = Jinja2Templates(directory="templates")

# class PredictRequest(BaseModel):
#     Airline: str
#     Date_of_Journey: str
#     Source: str
#     Destination: str
#     Dep_Time: str
#     Arrival_Time: str
#     Total_Stops: float
#     Duration_In_Minutes: int

# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/pred", response_class=HTMLResponse)
# async def form(request: Request):
#     return templates.TemplateResponse("form.html", {"request": request})

# @app.post("/predict", response_class=HTMLResponse)
# async def post_predict(request: Request,
#                         Airline: str = Form(...),
#                         Date_of_Journey: str = Form(...),
#                         Source: str = Form(...),
#                         Destination: str = Form(...),
#                         Dep_Time: str = Form(...),
#                         Arrival_Time: str = Form(...),
#                         Total_Stops: float = Form(...),
#                         Duration_In_Minutes: int = Form(...)):
#     data = CustomData(
#         Airline=Airline,
#         Date_of_Journey=Date_of_Journey,
#         Source=Source,
#         Destination=Destination,
#         Dep_Time=Dep_Time,
#         Arrival_Time=Arrival_Time,
#         Total_Stops=Total_Stops,
#         Duration_In_Minutes=Duration_In_Minutes
#     )

#     print(data)
#     pred_df = data.get_data_as_data_frame()
#     print(pred_df)
#     print("Before Prediction")

#     predict_pipeline = PredictPipeline()
#     print("Mid Prediction")
#     results = predict_pipeline.predict(pred_df)
#     print("After Prediction")

#     return templates.TemplateResponse('result.html', {"request": request, "results": results[0]})

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


from flask import Flask, request, render_template
from src.flight_price_prediction.pipelines.prediction_pipeline import PredictPipeline, CustomData
from src.flight_price_prediction.logger import logging
from src.flight_price_prediction.exception import CustomException

application = Flask(__name__)

app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("form.html")
    
    else:
        data = CustomData(
            Airline = (request.form.get('Airline')),
            Date_of_Journey = str(request.form.get('Date_of_Journey')),
            Source = (request.form.get('Source')),
            Destination = (request.form.get('Destination')),
            Dep_Time = (request.form.get('Dep_Time')),
            Arrival_Time = (request.form.get('Arrival_Time')),
            Total_Stops = float(request.form.get('Total_Stops')),
            Duration_In_Minutes = int(request.form.get('Duration_In_Minutes')),
        )
        logging.info("reading custom data is completed")
        print(data)
        pred_df = data.get_data_as_data_frame()
        logging.info("converted data into dataframe")
        print(pred_df)
        print("Before Prediction")

        predict_pipeline = PredictPipeline()
        print("Mid Prediction")
        results = predict_pipeline.predict(pred_df)
        logging.info("prediction has been completed")
        print("After Prediction")
        return render_template('result.html', results=results[0])

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)