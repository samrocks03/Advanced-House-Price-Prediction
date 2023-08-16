from flask import Flask, request, jsonify
import pandas as pd
import traceback
import joblib
import sys
import numpy as np

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if model:
        try:
            json_ = request.json
            query = pd.DataFrame.from_dict(json_, orient='index').transpose()


            query_encoded = pd.get_dummies(query)# Perform one-hot encoding on categorical features
            query_encoded = query_encoded.reindex(columns=model_columns) # Reorder columns to match the model's input order
            prediction_log = model.predict(query_encoded)
            
            # Reverse the logarithmic transformation
            prediction = np.exp(prediction_log)
            return jsonify({'prediction': float(prediction[0])})

        except Exception as e:
            return jsonify({'error': str(e)})

    else:
        return jsonify({'error': 'Model not found'})


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])  # This is for a command-line input
    except:
        port = 5000  # If you don't provide any port, the port will be set to 5000

    model = joblib.load("house-price-prediction.pkl")  # Load the trained model
    print('Model loaded')

    # Load the column names used during training
    with open("model_columns.pkl", "rb") as f:
        model_columns = joblib.load(f)
    print('Model columns loaded')

    app.run(port=port, debug=True)
