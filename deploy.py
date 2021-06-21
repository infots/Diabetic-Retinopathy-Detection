from flask import Flask, render_template, request, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import flash
from flask import session
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras import backend as K
import os
import glob
import shutil
from keras import models
from keras.preprocessing.image import ImageDataGenerator

src_dir = "static/img"
dst_dir = "static/img1"

app = Flask(__name__)
app.secret_key = "super secret key"

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

# loading saved model
model = models.load_model("./new_final_model.h5")

@app.route('/', methods=['GET', 'POST'])
def upload():
	flash('')

	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'])
		for jpgfile in glob.iglob(os.path.join(src_dir,"*.*")):
				shutil.copy(jpgfile, dst_dir)

		test_datagen = ImageDataGenerator(rescale=1. / 255)
		itr1 = test_set1 = test_datagen.flow_from_directory(
			'static',
			target_size=(512,512),
			batch_size=1)
		X1, y1 = itr1.next()
		arr = model.predict(X1, batch_size=1, verbose=1)
		print(arr)
		arr = np.argmax(arr, axis=1)
		if (arr == 0):
			flash('No DR')
		elif (arr == 1):
			flash('Mild DR')
		elif (arr == 2):
			flash('Moderate DR')
		elif (arr == 3):
			flash('Sever DR')
		else:
			flash('Proliferative DR')

		K.clear_session()
		os.remove('static/img/' + filename)
		return render_template('page.html', user_image='static/img1/' + filename)
	return render_template('page.html')




if __name__ == '__main__':
	app.run(debug=True)
