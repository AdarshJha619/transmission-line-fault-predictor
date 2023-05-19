import flask
import pickle
import pandas as pd
import numpy as np

with open('/Users/namraquasim/Documents/GitHub/tx line fault detector/Transmission Line Fault Detection.pkl', 'rb') as f:
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
        prediction = prediction["Fault_Type"].map({0:'LLL Fault (Between phase A,B and C)', 1:'LLLG Fault (Between phase A,B,C and Ground)', 2:'LLG Fault (Between phase A,B anf Ground)',
                      3:'LG Fault (Between phase A and Ground)', 4:'LL Fault (Between phase A and B)',
                      5:'No Fault'})
        print(prediction)              
        return flask.render_template('main.html', original_input={'Current in phase A ':ia, 'Current in phase B ':ib ,'Current in phase C ':ic , 
                                     'Voltage in phase A ':va, 'Voltage in phase B ':vb , 'Voltage in phase C ':vc },
                                    result=prediction[0]
                                    )

if __name__=='__main__':
    app.run(debug="True")
