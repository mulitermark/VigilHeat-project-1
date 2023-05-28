# VigilHeat-project
for software technology course

## Prerequisites

- Python 3
- git

## Setup

Clone the repository

```bash
git clone https://github.com/JIAOJIAOMEI/VigilHeat-project.git
cd VigilHeat-project
```
If you want to run people_counter_checkoutline.py,
then run the following steps:
```bash
cd VigilHeat-project
cd src
python people_counter_checkoutline.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel --input test_2.mp4 --output output_2.mp4
```
if you want to use the code for your own video, please make sure that you check the shape of your video and change the code accordingly, and adjust the black vertical line in the code accordingly.
![img.png](MVP%20Scope%2Fimg.png)
### Linux

Create a virtual environment and install the requirements

```bash
source setup.sh
```

To deactivate the virtual environment

```bash
deactivate
```

### Development

To update the requirements. Be sure to activate the virtual environment first.

```bash
pip freeze > requirements.txt
```

### reference
https://github.com/saimj7/People-Counting-in-Real-Time
