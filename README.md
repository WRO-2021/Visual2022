# Visual:dizzy: 2022
>Optical Character Recognition for robocup junior 2022/2023


The buonarroti team here is working in order to reach the world tournament of robocup junior.
 These files should run on our raspberri pi, in the [photos](ocr/photos/) 
 dir there are files that capture and saves the photos in the [data](ocr/data/images/) dir, 
 they are made in such a way that you can import these files and their functions from other files
 (es. [here](arduino_connection/worker.py))
  so we don't need to rewrite code.:+1:


  Directory map:ledger::
  - [ocr](ocr/):rocket:: files for the training and preparation of the result
    - [data](ocr/data/): [images](ocr/data/images/) folder and some files that are used to label the images, 
    the [.html](ocr/data/index.html) show the images in a carousel and can download a json with the catalogation, 
    if [save.php](ocr/data/save.php) is also running(with the ```php``` command, 
    as shown in the [start server](ocr/data/start_server.sh)) the json can be directly copied in the right place([json](ocr/data/images/data.json))
    - [neural network](ocr/neuralnetwork/):microscope:: [training](ocr/neuralnetwork/primaNN.ipynb) and [definition](ocr/neuralnetwork/CNN.py) of the CNN used for the recognition, it works for both b&w and rgb images.
    The [saves](ocr/neuralnetwork/saves/) dir has the dump of the models and the encoders used.
    - [photos](ocr/photos/):eyes::
    as already said, files for photo capture and storing. [check cameras](ocr/photos/checCameras.py) detect the opencv index of the connected cameras.
 - [arduino connection](arduino_connection/):vertical_traffic_light:: the [worker](arduino_connection/worker.py) is the main file for the running robot, it uses the trained model to take photos and communicate via serial port(USB) with the arduino when it ask if there are victims detected.


 The team:frog::
 * [SamueleFacenda](https://github.com/SamueleFacenda):mushroom:
 * [ALEPASSERINI](https://github.com/ALEPASSERINI):cactus:
 * [Zampagnone](https://github.com/Zampagnone):palm_tree:
