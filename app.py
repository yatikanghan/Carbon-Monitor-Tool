from flask import Flask, render_template,request

app=Flask(__name__)

@app.route("/", methods=['GET',"POST"])
def index():
    data=False
    if request.method == "POST":
        data=True
        avgelectricitybill=int(request.form.get("avgelectricitybill"))
        avggasbill=int(request.form.get("avggasbill"))
        avgfuelbill=int(request.form.get("avgfuelbill"))

        avgwastegen=int(request.form.get("avgwastegen"))
        avgwastecompose=int(request.form.get("avgwastegen"))

        avgkmtravel=int(request.form.get("avgkmtravel"))
        avgfuelefficiency=int(request.form.get("avgfuelefficiency"))

        return render_template('index.html',avgelectricitybill=avgelectricitybill, avggasbill=avggasbill, avgfuelbill=avgfuelbill, avgwastegen=avgwastegen, avgwastecompose=avgwastecompose, avgkmtravel=avgkmtravel, avgfuelefficiency=avgfuelefficiency)
    else:
        return render_template('index.html')


    
    

app.run(debug=True)

