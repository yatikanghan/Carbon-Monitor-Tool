from flask import Flask, render_template,request
import matplotlib.pyplot as plt
import io

app=Flask(__name__)
avgelectricitybill=None
@app.route("/")
def index():

    return render_template('index.html')

@app.route("/report", methods=['GET',"POST"])
def report():
    if request.method == "POST":
        
        avgelectricitybill=float(request.form.get("avgelectricitybill"))
        avggasbill=float(request.form.get("avggasbill"))
        avgfuelbill=float(request.form.get("avgfuelbill"))

        avgwastegen=float(request.form.get("avgwastegen"))
        avgwastecompose=float(request.form.get("avgwastecompose"))

        avgkmtravel=float(request.form.get("avgkmtravel"))
        avgfuelefficiency=float(request.form.get("avgfuelefficiency"))

        Energysector=(avgelectricitybill)*(12)*(0.0005)+(avggasbill)*(12)*(0.0053)+(avgfuelbill)*(12)*(2.32)
        Wastesector=(avgwastegen)*(12)*(0.57)-(avgwastecompose)
        Travelsector=(avgkmtravel)*(1/avgfuelefficiency)*(2.31)

        labels=['Energy Usage', 'Waste Management', 'Business Travel']
        values=[Energysector,Wastesector,Travelsector]
        chart_path=generate_pie_chart(values,labels)

        return render_template('report.html',avgelectricitybill=avgelectricitybill, avggasbill=avggasbill, avgfuelbill=avgfuelbill, avgwastegen=avgwastegen, avgwastecompose=avgwastecompose, avgkmtravel=avgkmtravel, avgfuelefficiency=avgfuelefficiency, Energysector=Energysector, Wastesector=Wastesector, Travelsector=Travelsector, chart_path=chart_path)
    else:
        return render_template('index.html')
    
def generate_pie_chart(values,labels):
    myexplode = [0.03, 0.03, 0.03]
    plt.pie(values, labels=labels, autopct='%1.1f%%', explode=myexplode, colors=['red', 'blue', 'green'])
    plt.title('Carbon Footprint kgCO2')
    chart_path = 'static/chart.png'
    plt.savefig(chart_path)
    plt.close()
    return chart_path


app.run(debug=True)

