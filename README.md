# VigilHeat-project
for software technology course

The project description for "Team is Ready for Action" was originally written by Mei Jiaojiao, with MVP part added by Arriagada Silva Sebastián Ignacio and personal information added by the rest of the team. 
The Market, Users & KPI section was also initially drafted by Mei Jiaojiao and later modified by the rest of the team. 

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