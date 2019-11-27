from __future__ import print_function
from configs import train_path101 as train_path
from configs import test_path101 as test_path
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
import os

cwd = 'C:/Users/tyobr/Documents/Texas_State/Fall_2019/MACHINE_LEARNING/Homework-3'

tensorboard_callback = keras.callbacks.TensorBoard(log_dir='food101runs')

batch_size = 10
num_classes = 10
epochs = 10
data_augmentation = True
save_dir = os.path.join(cwd, 'archive')
model_name = 'kerasfood101.h5'
model_path = os.path.join(save_dir, model_name)

""""
DATA GENERATOR START FROM HERE
"""

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    directory=train_path,
    target_size=(128, 128),
    color_mode='rgb',
    batch_size=10,
    class_mode='categorical',
    shuffle=True,
    seed = 1)

test_generator = test_datagen.flow_from_directory(
        directory=test_path,
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical')

""""
DATA GENERATOR ENDS HERE
"""


""""
MODEL BUILDING START FROM HERE
"""

model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=(128,128,3)))

model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.5))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.25))

model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

""""
MODEL BUILDING ENDS HERE
""""

# initiate RMSprop optimizer
#opt = keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)
opt = keras.optimizers.Adam(lr=0.0001, decay=1e-6)
pretrained_model_path = 'kerasfood101mobilenet.h5'


if os.path.exists(pretrained_model_path):
    print("LOADING OLD MODEL")
    model.load_weights(model_path)
"""
if os.path.exists(model_path):
    print("LOADING OLD MODEL")
    model.load_weights(model_path)
"""
model.compile(loss= 'categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])



model.fit_generator(train_generator,
                    steps_per_epoch=10,
                    epochs=epochs,
                    validation_data=test_generator,
                    validation_steps=10,
                    callbacks=[tensorboard_callback])

model.plot(kind='bar', rot=0)


model.save(model_path)
