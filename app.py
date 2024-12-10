from flask import Flask, render_template,request, send_file, session
import matplotlib.pyplot as plt
import io
from reportlab.pdfgen import canvas

app=Flask(__name__)


errors = {}
app.secret_key = "123456789"

@app.route("/")
def index():
    errors = {}
    return render_template('index.html', errors=errors)

@app.route("/report", methods=['GET',"POST"])
def report():
    errors = {}
    if request.method == "POST":

        companyname=request.form.get("companyname")
        avgelectricitybill=float(request.form.get("avgelectricitybill"))
        avggasbill=float(request.form.get("avggasbill"))
        avgfuelbill=float(request.form.get("avgfuelbill"))

        avgwastegen=float(request.form.get("avgwastegen"))
        avgwastecompose=float(request.form.get("avgwastecompose"))

        avgkmtravel=float(request.form.get("avgkmtravel"))
        avgfuelefficiency=float(request.form.get("avgfuelefficiency"))

        

        
        # ------------------
        if not companyname or len(companyname.strip()) < 2:
            errors["companyname"] = "Company name must be at least 2 characters long."
        if avgelectricitybill is None or avgelectricitybill <= 0:
            errors["avgelectricitybill"] = "Electricity bill must be a non-negative number."
        if avggasbill is None or avggasbill <= 0:
            errors["avggasbill"] = "Natural gas bill must be a non-negative number."
        if avgfuelbill is None or avgfuelbill <= 0:
            errors["avgfuelbill"] = "Fuel bill must be a non-negative number."
        if avgwastegen is None or avgwastegen <= 0:
            errors["avgwastegen"] = "Waste generated must be a non-negative number."
        if avgwastecompose is None or not (0 <= avgwastecompose <= 100):
            errors["avgwastecompose"] = "Waste composed must be between 0 and 100."
        if avgkmtravel is None or avgkmtravel <= 0:
            errors["avgkmtravel"] = "Kilometers traveled must be a non-negative number."
        if avgfuelefficiency is None or avgfuelefficiency <= 0:
            errors["avgfuelefficiency"] = "Fuel efficiency must be a positive number."

        # If no errors, process data
        if not errors:
            Energysector=(avgelectricitybill)*(12)*(0.0005)+(avggasbill)*(12)*(0.0053)+(avgfuelbill)*(12)*(2.32)
            Wastesector=(avgwastegen)*(12)*(0.57)-(avgwastecompose)
            Travelsector=(avgkmtravel)*(1/avgfuelefficiency)*(2.31)

            session["companyname"]=companyname
            session["ebill"]=avgelectricitybill
            session["gbill"]=avggasbill
            session["fbill"]=avgfuelbill
            session["wgen"]=avgwastegen
            session["wcom"]=avgwastecompose
            session["tyear"]=avgkmtravel
            session["feff"]=avgfuelefficiency
            session["carbonenergy"]=Energysector
            session["carbonwaste"]=Wastesector
            session["carbontravel"]=Travelsector
            
            
             


            
            labels=['Energy Usage', 'Waste Management', 'Business Travel']
            values=[Energysector,Wastesector,Travelsector]
            chart_path=generate_pie_chart(values,labels)
            HighImpact=None
            MediumImpact=None
            LowImpact=None
            
            if Energysector <= Wastesector:
                MediumImpact = ["Waste Management", Wastesector]
                LowImpact = ["Energy Usage", Energysector]

                if Wastesector <= Travelsector:
                    HighImpact = ["Business Travel", Travelsector]
                else:
                    HighImpact = ["Waste Management", Wastesector]
            else:
                HighImpact = ["Energy Usage", Energysector]

            # Compare Energy and Travel to determine Medium and Low
            if Energysector <= Travelsector:
                MediumImpact = ["Business Travel", Travelsector]
                LowImpact = ["Waste Management", Wastesector]
            else:
                MediumImpact = ["Waste Management", Wastesector]
                LowImpact = ["Business Travel", Travelsector]
        

            return render_template('report.html',avgelectricitybill=avgelectricitybill, avggasbill=avggasbill, avgfuelbill=avgfuelbill, avgwastegen=avgwastegen, avgwastecompose=avgwastecompose, avgkmtravel=avgkmtravel, avgfuelefficiency=avgfuelefficiency, Energysector=Energysector, Wastesector=Wastesector, Travelsector=Travelsector, chart_path=chart_path, HighImpact=HighImpact,MediumImpact=MediumImpact,LowImpact=LowImpact)
        return render_template('index.html', errors=errors)
        # ------------------





        
    
def generate_pie_chart(values,labels):
    myexplode = [0.03, 0.03, 0.03]
    plt.pie(values, labels=labels, autopct='%1.1f%%', explode=myexplode, colors=['red', 'blue', 'green'])
    plt.title('Carbon Footprint kgCO2')
    chart_path = 'static/chart.png'
    plt.savefig(chart_path)
    plt.close()
    return chart_path



@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    


    pdf_path = 'details.pdf'
    chart_path = 'static/chart.png'
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, "Carbon Footprint Monitor")
    c.drawString(100, 730, f"Company Name : {session.get("companyname")}")
    c.drawString(100, 680, f"Monthly Gas Bill : {session.get("gbill")}")
    c.drawString(100, 700, f"Monthly Electricity Bill : {session.get("ebill")}")
    c.drawString(100, 660, f"Monthly Fuel Bill : {session.get("fbill")}")
    c.drawString(100, 640, f"Monthly Waste Generated : {session.get("wgen")}")
    c.drawString(100, 620, f"Monthly Waste Composed or Recycled Percentage : {session.get("wcom")}%")
    c.drawString(100, 600, f"Employee Travel for Business Purpose : {session.get("tyear")}")
    c.drawString(100, 580, f"Average Fuel efficiency per 100 km : {session.get("feff")}\n\n")
    c.drawString(100, 560, f"Energy Sector Carbon Footprint : {session.get("carbonenergy")}")
    c.drawString(100, 540, f"Waste Sector Carbon Footprint : {session.get("carbonwaste")}")
    c.drawString(100, 520, f"Travel Sector Carbon Footprint : {session.get("carbontravel")}")
    # c.drawString(100, 690, f"Argument 3: {args[2]}")
    c.drawImage(chart_path, 100, 100, width=400, height=300)
    c.save()

    return send_file(pdf_path, as_attachment=True)


app.run(debug=True) 