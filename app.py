import flask
import pickle
import pandas as pd
import numpy as np

with open('Transmission Line Fault Detection.pkl', 'rb') as f:
    model = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=["GET", "POST"])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
        ia = flask.request.form['currentA']
        ib = flask.request.form['currentB']
        ic = flask.request.form['currentC']
        va = flask.request.form['voltageA']
        vb = flask.request.form['voltageB']
        vc = flask.request.form['voltageC']
        


        input_variables = pd.DataFrame([[ia, ib, ic, va, vb, vc]], columns=['Ia', 'Ib', 'Ic', 'Va', 'Vb', 'Vc'], dtype=object)
        print(ia,ib,ic,va,vb,vc)
        
        prediction = model.predict(input_variables)
        prediction = pd.DataFrame(prediction, columns=['Fault_Type'])
        prediction = prediction["Fault_Type"].map({0:'line A line B line C fault', 1:'Line A line B line C to ground fault', 2:'line A line B and ground fault',
                      3:'line A and ground fault', 4:'line B line C fault',
                      5:'No Fault'})
        print(prediction)              
        return flask.render_template('main.html', original_input={'currentA ':ia, 'currentB ':ib ,'currentC ':ic , 
                                     'voltageA ':va, 'voltageB ':vb , 'voltageC ':vc },
                                    result=prediction[0]
                                    )

if __name__=='__main__':
    app.run(debug="True")
