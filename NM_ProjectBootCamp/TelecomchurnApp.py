from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    gender = request.form['gender']
    seniorCitizen = request.form['seniorCitizen']
    partner = request.form['partner']
    dependents = request.form['dependents']
    tenure = request.form['tenure']
    phoneService = request.form['phoneService']
    multipleLines = request.form['multipleLines']
    internetService = request.form['internetService']
    onlineSecurity = request.form['onlineSecurity']
    onlineBackup = request.form['onlineBackup']
    deviceProtection = request.form['deviceProtection']
    techsupport = request.form['techsupport']
    streamingTV = request.form['streamingTV']
    streamingmovies =request.form['streaming_movies']     
    contract = request.form['contract']
    paperlessbilling = request.form['paperless_billing']
    paymentmethod = request.form['payment_method']
    monthlycharges = request.form['monthly_charges']
    totalcharges = request.form['total_charges']
    churn = request.form['churn']

    user_input = pd.DataFrame({'gender': [gender], 'SeniorCitizen': [seniorCitizen], 'Partner': [partner], 'Dependents': [dependents], 'tenure': [tenure], 'PhoneService': [phoneService], 'MultipleLines': [multipleLines], 'InternetService': [internetService], 'OnlineSecurity': [onlineSecurity], 'OnlineBackup': [onlineBackup], 'DeviceProtection': [deviceProtection], 'TechSupport': [techsupport], 'StreamingTV': [streamingTV], 'StreamingMovies': [streamingmovies], 'Contract': [contract], 'PaperlessBilling': [paperlessbilling], 'PaymentMethod': [paymentmethod], 'MonthlyCharges': [monthlycharges], 'TotalCharges': [totalcharges], 'Churn': [churn], }) 

    user_input['Churn'].replace(to_replace='Yes', value=1, inplace=True)
    user_input['Churn'].replace(to_replace='No',  value=0, inplace=True)

    user_input['gender'] = user_input['gender'].astype('object')
    user_input['SeniorCitizen'] = user_input['SeniorCitizen'].astype('object')
    user_input['Partner'] = user_input['Partner'].astype('object')
    user_input['Dependents'] = user_input['Dependents'].astype('object')
    user_input['tenure'] = user_input['tenure'].astype('int64')
    user_input['PhoneService'] = user_input['PhoneService'].astype('object')
    user_input['MultipleLines'] = user_input['MultipleLines'].astype('object')
    user_input['InternetService'] = user_input['InternetService'].astype('object')
    user_input['OnlineSecurity'] = user_input['OnlineSecurity'].astype('object')
    user_input['OnlineBackup'] = user_input['OnlineBackup'].astype('object')
    user_input['DeviceProtection'] = user_input['DeviceProtection'].astype('object')
    user_input['TechSupport'] = user_input['TechSupport'].astype('object')
    user_input['StreamingTV'] = user_input['StreamingTV'].astype('object')
    user_input['StreamingMovies'] = user_input['StreamingMovies'].astype('object')
    user_input['Contract'] = user_input['Contract'].astype('object')
    user_input['PaperlessBilling'] = user_input['PaperlessBilling'].astype('object')
    user_input['PaymentMethod'] = user_input['PaymentMethod'].astype('object')
    user_input['MonthlyCharges'] = user_input['MonthlyCharges'].astype('float64')
    user_input['TotalCharges'] = user_input['TotalCharges'].astype('float64')
    user_input['Churn'] = user_input['Churn'].astype('int64')

    df_dummies_user_input = pd.get_dummies(user_input)

    y = df_dummies_user_input['Churn'].values
    X = df_dummies_user_input.drop(columns = ['Churn'])

    df = pd.DataFrame({'SeniorCitizen':[],'tenure':[],'MonthlyCharges':[],'TotalCharges':[],'gender_Female':[],'gender_Male':[],'Partner_No':[],'Partner_Yes':[],'Dependents_No':[],'Dependents_Yes':[],'PhoneService_No':[],'PhoneService_Yes':[],'MultipleLines_No':[],'MultipleLines_No phone service':[],'MultipleLines_Yes':[],'InternetService_DSL':[],'InternetService_Fiber optic':[],'InternetService_No':[],'OnlineSecurity_No':[],'OnlineSecurity_No internet service':[],'OnlineSecurity_Yes':[],'OnlineBackup_No':[],'OnlineBackup_No internet service':[],'OnlineBackup_Yes':[],'DeviceProtection_No':[],'DeviceProtection_No internet service':[],'DeviceProtection_Yes':[],'TechSupport_No':[],'TechSupport_No internet service':[],'TechSupport_Yes':[],'StreamingTV_No':[],'StreamingTV_No internet service':[],'StreamingTV_Yes':[],'StreamingMovies_No':[],'StreamingMovies_No internet service':[],'StreamingMovies_Yes':[],'Contract_Month-to-month':[],'Contract_One year':[],'Contract_Two year':[],'PaperlessBilling_No':[],'PaperlessBilling_Yes':[],'PaymentMethod_Bank transfer (automatic)':[],'PaymentMethod_Credit card (automatic)':[],'PaymentMethod_Electronic check':[],'PaymentMethod_Mailed check':[],})

    X = pd.concat([df, X]).reindex(columns=df.columns)
    X.fillna(0, inplace=True)
    with open('model_scalar.pkl', 'rb') as f:
        scaler = pickle.load(f)


    X_scaled_row = scaler.transform(X)

    with open("model_GB.pkl", "rb") as f:
        loaded_model = pickle.load(f)

    prediction_test = loaded_model.predict(X_scaled_row)

    if prediction_test[0] == 1:
        Result_Text = "Customer will churn. Better connect with customer ASAP."
    else:
        Result_Text = "Customer will NOT churn. Make sure to stay in touch with customer."
   
    return render_template('prediction.html', prediction=Result_Text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)