"""
/home/procidic/IoT_proj/backend.py
The backend for the dashboard, to control the computer, so logically, the computer has to be the backend.  
Allows the frontend to control the raspberry pi, along with providing a backend server.  
"""
from flask import Flask, render_template, request, jsonify  # This is everything we need!  
from gpiozero import LED
from time import sleep
import subprocess

app = Flask(__name__)  # Define the app
led = LED(17) # The LED is attached to GPIO pin 17!
latest_ai_predict = {"predicted_name": "AI OFFLINE", "confidence": 0.0}
@app.route('/')  # USER IS VISITING THE DASHBOARD!!!! 
def home(): # ok, load the home page... 
    return render_template('index.html') # This, is home.  

@app.route('/temp', methods=['GET']) # If the frontend, asked for the temperature
def get_temp(): # This is our standard procedure.
    temperature = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True) # Ok, run vcgencmd measure_temp
    # and write down the return value as a string.  
    print(temperature.stdout)  # Ok, lets let the programmer see
    temp_variable = temperature.stdout.strip() # remove the pesky \n
    return_temp = temp_variable[5:len(temp_variable)-2] # And only return the number, we can have integers since its predictable, 
    # always will have a temp= thing which is 5 characters, and at the end, there are 2 characters.  
    print(return_temp)
    return jsonify(temperature=return_temp)  # lets send it to the frontend
    

@app.route('/data', methods=['POST'])
def recieveLEDcmd():  #Recieves the data for if the user wanted to turn on LED
    data = request.get_json() # Hey, did the user turn it on?  
    button_pressed = data.get('LED_On')  # I'm not sure, but I got the data, lemme check...

    # If they actually are true, then...
    if button_pressed == True: 
        led.on()  # Turn the LED  the raspberry pi is connected to on for 6 seconds!  btw the Pi is the backend technically
        sleep(6)
        led.off() #Ok, now turn it off
        return jsonify(status="Success!") # Tell the user we were successful!
    elif button_pressed == False: # if they didn't, then just keep it off.   
        led.off()
    
    return jsonify(status="Unknown") # if something's went wrong, then just say unknown.  

@app.route('/api/updated_prediction', methods=['POST'])
def update_AI_prediction():
    global latest_ai_predict

    latest_ai_predict = request.get_json()
    print(f"Received AI update: {latest_ai_predict.get('predicted_name')}")

    return jsonify(status="Success")

@app.route('/api/get_prediction', methods=['GET'])
def get_AI_prediction():
    global latest_ai_predict
    return jsonify(latest_ai_predict)

# Ok, if the program runs, just host it with 0.0.0.0 DNS on the port 5000, on the current IP address.  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
