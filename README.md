# Raspberry-Pi-Dashboard
A Dashboard for my Raspberry Pi Projects.  

__________________________________________________________

# Summary of Projects on there: 

System Status:  As of now, there is only measuring temperature on there. 

Remote IoT LED:  The first project I put on there, basically allows the user to turn an LED wired to GPIO 17 on via a web dashboard, uses POST command and backend code on the Flask server to do so

Classification Model:  I created an AI classification model with Computer Vision that classifies Lego bricks, into categories:  Full_Brick, 2x2, and Technic Rod.  It is made in Tensorflow, and uses a softmax function in order to predict.  
Requests is used in order to push it and loop it back to the backend.py server so it can read.  It is primarily because I plan on making a Robotic Arm later, and this is just step one of my project.  
In my setup, I have a buildhat, attached to some lego spike prime motors, so it would grab the bricks it would see to sort them.  I hadn't coded those yet, so I will have to wait to see.  For the Computer Vision, it works by capturing the image, as an array, to convert to a 128x128 image for the model to see.  The model then has layers at that size, for processing, using a 3, 3 shape and Conv2D.  It then flattens it, and passed
through dense layers.  After that, its passed as a Dense(3) layer.  For the training data, I wrote a custom Python script for it.  I had it capture images, for each classification class, determined by the user.  It was mostly AI, but that's ok.  I still wrote the code, since I directed AI on how to do it, as AI knew the syntax anyways.  It uses brick_types, and captures images, and as they capture images, for each class, the image is captured as an Array, and then appended to images, along with the current label being appended to labels.  Then, it makes 2 variables named X_train and Y_train, and exports them as a npy file, for the model to read later, as the training data.  For the vision when making a prediction, it uses the same data vectoriziation algorithm, through capturing the image as an array, and then feeding it to the AI.  

Live Camera Feed:  A live camera feed from my Raspberry Pi Camera, I am using a RPI Camera 3.  I put the camera feed server as a separate backend, so yes, the web dashboard does use CORS.  Along with that, due to a conflict,
I merged the wrapper for my tflite classification model with the server, as both the prediction script and my camera feed server both use the camera, as suggested by AI.  The backend for the live camera feed, does contain the code
for the classification model's script, doesn't contain the code for the model itself, its a tflite.  Also, the model was kinda written by an AI, since i asked AI to help me write one, I don't know the exact syntax for it, but I was
able to understand the code and did ultimately act as the software engineer.  It sends a bunch of jpegs for MPEG, to the website's html in order to show a feed.  


________________________________________________________________

Overall, this was mostly a weekend project, I was able to work on it mainly cuz my school is almost over, my homework is mostly completed.  

To make this even more impressive, I'm a 9th grader, and I wrote all this with the help of AI, like a real software engineer, along with deciding some of the logic.  No one always knows the exact syntax, they get AI to write it so
they don't always have to memorize the exact characters to type.  But I mean at the end of the day, its still my work, despite AI having written probably half of the code, since the AI is just the programmer, sure, it suggested 
some logic but at the end of the day, its still my work.  

srry for repetition, i just do that all the time whenever i try to write or say anything.
