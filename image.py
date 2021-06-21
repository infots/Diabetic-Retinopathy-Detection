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

src_dir = "static/img"
dst_dir = "static/img1"

app = Flask(__name__)
app.secret_key = "super secret key"

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


@app.route('/', methods=['GET', 'POST'])
def upload():
	flash('')
	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'])
		for jpgfile in glob.iglob(os.path.join(src_dir, "*.*")):
			shutil.copy(jpgfile, dst_dir)

		# loading saved model
		model = models.load_model("./vgg16_model.h5")
		from keras.preprocessing.image import ImageDataGenerator
		test_datagen = ImageDataGenerator(rescale=1. / 255)
		itr1 = test_set1 = test_datagen.flow_from_directory(
			'static',
			target_size=(224, 224),
			batch_size=377,
			class_mode='categorical')
		X1, y1 = itr1.next()
		arr = model.predict(X1, batch_size=377, verbose=1)
		arr = np.argmax(arr, axis=1)

		idxe = 0
		print(arr)
		for idx in arr:
			if (arr[idx] == 1):
				idxe = idx
				break
		flash(str(idxe))
		idxe = arr[0]
		flash(str(arr))
		if (idxe == 0):
			flash('label 1')
		elif (idxe == 1):
			flash('label 2')
		elif (idxe == 2):
			flash('label 3')
		elif (idxe == 3):
			flash('label 4')
		else:
			flash('label 5')

		K.clear_session()
		os.remove('static/img/' + filename)
		return render_template('image.html', user_image='static/img1/' + filename)
	return render_template('image.html')


if __name__ == '__main__':
	app.run(debug=True)