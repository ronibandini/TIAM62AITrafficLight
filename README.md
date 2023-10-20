# TIAM62AITrafficLight

AI traffic lights with Texas Instruments AM62A and Edge Impulse.
A model is trained to recognize motorcycle riders with and without helmets. 
That model is loaded into AM62A. 
A regular webcam will send pictures for local inference.
Inference values will be sent to a server.
A separate WiFi device - Unihiker with Debian/Python - will query the server to determine if red traffic light will switch to green.


