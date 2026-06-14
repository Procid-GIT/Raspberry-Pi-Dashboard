const turnonLED = document.getElementById("LED"); /* Finds LED Div class so it can play around */

/* Yes, really, all this 
   bs happens inside one addEventListener function, so only happens when user clicks it, 
   Just so to let the backend know to turn on LEd, since the webpage is for controling the raspberry pi,
   which is the backend, so it does control the backend.*/
turnonLED.addEventListener('click', async (e) => {
    e.preventDefault();
    console.log("LED toggled on");
    const payload = {
        LED_On: true,  /* LED is officially toggled on, now the message is just packaged like a json*/
    };
    try { /* Here, we are gonna attempt to deliver. */
        turnonLED.textContent = "...";
        const data = await fetch('/data', {  /* Data link raspberrypi/data it will send it along that road
                                             , Post just means its sending to the server.   */
            method: 'POST',  
            headers: { 'Content-Type': 'application/json'},  /* This package is a certified JSON */
            body: JSON.stringify(payload)  /* Well, if it is a JSON, then S T R I N G I F Y it into one. */
        });
        if (!data.ok) {  /* Standard procedure used, when maybe the destination has a problem */
            throw new Error(`Sorry, but the Pi said ${data.status} today :/`);
        }
        const stats = await data.json();  /* REFRESH, Where is the data??? HAS IT GONE ANYWHERE */
        console.log("Response Data, Success, ", stats);  /*  OH, turns out its just fine! */
        turnonLED.textContent = "Sent";  /* Let's let the user know it was delivered succsesfully. */
        turnonLED.classList.remove('error');
        turnonLED.classList.add('active');
        setTimeout(() => {
            turnonLED.textContent = "Turn on LED";
            turnonLED.classList.remove('active');
        }, 2000);
    } catch (error) {  /* If, maybe there was an accident?  */
        const errorMsg = error.message || String(error);  /* Lets put it in a variable, and then tell the console the variable! */
        console.error('Sir, idk what happened but it says ', errorMsg);
        turnonLED.textContent = "Error :/"; /* Sorry sir, but something happened... */
        turnonLED.classList.remove('active');
        turnonLED.classList.add('error');
        setTimeout(() => {
            turnonLED.textContent = "Turn on LED";
            turnonLED.classList.remove('error');
        }, 2000);
    }
});

const measure_temp = document.getElementById("temp-display");
setInterval(get_temp, 2000);

async function get_temp() {
    try {
        const temp = await fetch('/temp');
    
        if (!temp.ok) {
            throw new Error(`Sorry, but could not get temp cuz of ${temp.status}.`);
        }

        const temp_data = await temp.json();
        const temperature_final = temp_data.temperature;
        console.log(temperature_final);
        measure_temp.textContent = `${temperature_final}`;
        measure_temp.classList.toggle('temp_normal', temperature_final < 60.0);
        measure_temp.classList.toggle('temp_medium', temperature_final >= 60.0 && temperature_final < 80.0);
        measure_temp.classList.toggle('temp_danger', temperature_final >= 80.0);
    } catch (error) {
        // code goes here
        console.error('Error fetching temperature', error)
        measure_temp.textContent = "NaN";
    }
};

const ai_prediction = document.getElementById("prediction");
setInterval(get_pred, 1000);

async function get_pred() {
    try {
        const prediction = await fetch('/api/get_prediction');

        if (!prediction.ok) {
            throw new Error(`Sorry, we could not get the prediction cuz of ${prediction.status}.`);
        }
        const pred_data = await prediction.json();
        const classify = pred_data.predicted_name;
        const confidence = pred_data.confidence;
        console.log(classify, confidence);
        ai_prediction.textContent = `I predict I'm seeing ${classify}, \n ${confidence}% confidence`;
        ai_prediction.classList.remove('error');
        ai_prediction.classList.add('normal');
    } catch (error) {
        console.error('Error, could not get AI prediction', error);
        ai_prediction.textContent = "3rr0r X_X";
        ai_prediction.classList.remove('normal');
        ai_prediction.classList.add('error');
    }
}