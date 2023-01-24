# Air-Board
Have you ever wondered if you could write in air? <br/>
With airboard you can do so. Airboard uses web-cam to track hand movements of a user, and draws the figure accordingly.


## 2) Setting up project locally
### To create virtual environment
```
python -m venv <ENVIRONMENT_NAME>
```
    
for e.g.
```bash
python -m venv env
```

### To activate virtual environment

```bash
<ENVIRONMENT_NAME>\Scripts\activate
``` 

### To install dependencies

```bash
pip install -r requirements.txt
```

### To create / update requirements.txt

```bash
pip freeze > requirements.txt
```

### Project Status
This project is currently in the development stage. <br/>
The <code>/templates</code> folder contains some basic frontend template. And <code>VirtualPainter.py</code> file contains all the code that is used for detecting a hand movements from image frames, and drawing it on a canvas. Now the problem with this approach is that with the current status, we can't deploy our project in real world. Because, we need to grab images from the client side, and then send it to our backend, where it can track  the hand movement and send it back to the client, where we can represent the marked movements. 
<br/>
So we need to design a backend server in <code>flask</code> that can accept images from client, and then perform computations and return the processed image. We will also need to make necessary changes on the frontend side, that can accept user images using a webcam, and then send it to our backend server.
