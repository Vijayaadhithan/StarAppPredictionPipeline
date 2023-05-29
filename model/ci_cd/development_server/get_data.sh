#!/bin/bash
python3 get_git_data.py
# If the following works comment out above and do the following:
#get_data_1.py
#get_data_2.py
#also change this one
python3 data_preprocessing.py
python3 model_prediction.py
