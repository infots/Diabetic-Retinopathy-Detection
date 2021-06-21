Setup Steps to follow for this project to install on local machine
1) Create virtual env
	conda create -n new_proj python=3.6
	conda activate new_proj
2) Install all depencies using pip command
	First change dir to DR using cd command
	pip install -r requirements.txt
3) Then run the project on local
	python deploy.py
4) Open any browser and type local machine address http://127.0.0.1:5000
5) Click on browser button and upload image
6) Click on submit button and you will get predicted result.


Refer website for data :
https://www.kaggle.com/dimitreoliveira/aptos-blindness-detection-eda-and-keras-resnet50/data?select=train.csv

