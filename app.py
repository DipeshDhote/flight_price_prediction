
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