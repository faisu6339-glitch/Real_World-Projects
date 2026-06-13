
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
import os

# Dataset Path
TRAIN_DIR = "asl_alphabet_train"

# Image Generator
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Training Dataset
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(64,64),
    batch_size=32,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

# Validation Dataset
val_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(64,64),
    batch_size=32,
    class_mode='categorical',
    subset='validation',
    shuffle=True
)

# Print Classes
print("Classes Found:")
print(train_generator.class_indices)

print("Number of Classes:")
print(train_generator.num_classes)

# CNN Model
model = Sequential()

# Layer-1
model.add(Conv2D(
    32,
    (3,3),
    activation='relu',
    input_shape=(64,64,3)
))

model.add(MaxPooling2D(2,2))

# Layer-2
model.add(Conv2D(
    64,
    (3,3),
    activation='relu'
))

model.add(MaxPooling2D(2,2))

# Layer-3
model.add(Conv2D(
    128,
    (3,3),
    activation='relu'
))

model.add(MaxPooling2D(2,2))

# Flatten
model.add(Flatten())

# Dense
model.add(Dense(256, activation='relu'))

model.add(Dropout(0.5))

# Output Layer
model.add(Dense(
    train_generator.num_classes,
    activation='softmax'
))

# Compile
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Summary
model.summary()

# Train
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=5
)

# Create models folder
os.makedirs("models", exist_ok=True)

# Save Model
model.save("models/sign_language_model.h5")

print("Model Saved Successfully!")
