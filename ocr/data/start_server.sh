#!/bin/bash

# per avere ssh tunneling
# shh -L 8080:localhost:8080 pi@pi.local

# o ti usi direttamente pi.local:8080

php -S localhost:8080 -t /home/pi/Desktop/Visual2022/ocr/data
