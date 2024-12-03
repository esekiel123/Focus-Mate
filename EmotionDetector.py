from __future__ import print_function
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping

# Parámetros de configuración
img_width, img_height = 48, 48  # Tamaño de las imágenes de entrada
batch_size = 32
epochs = 50
num_classes = 7  # Número de clases de emociones (7: Happy, Sadness, Surprise, etc.)

# Definición del modelo
def create_model():
    model = Sequential()
    
    # Primera capa convolucional
    model.add(Conv2D(64, (3, 3), padding='same', input_shape=(img_width, img_height, 1)))  # Entrada con 1 canal (grayscale)
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    # Segunda capa convolucional
    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    # Tercera capa convolucional
    model.add(Conv2D(256, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Aplanar la salida de las capas convolucionales para conectarlo con capas densas
    model.add(Flatten())

    # Capa densa completamente conectada
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))  # Regularización para evitar sobreajuste

    # Capa de salida
    model.add(Dense(num_classes))  # Salida con 7 clases (emociones)
    model.add(Activation('softmax'))  # Función softmax para clasificación multiclase

    # Compilación del modelo
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])
    
    return model

# Creación del modelo
model = create_model()
model.summary()

# Definir las rutas de los conjuntos de datos (ajustar a las rutas de tu conjunto de datos)
train_data_dir = 'data/train'
validation_data_dir = 'data/validation'

# Preprocesamiento de imágenes y aumento de datos
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',  # Para clasificación multiclase
    color_mode='grayscale'  # Las imágenes son en escala de grises
)

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',  # Para clasificación multiclase
    color_mode='grayscale'  # Las imágenes son en escala de grises
)

# Callbacks para mejorar el entrenamiento
checkpoint = ModelCheckpoint('emotion_model.h5', monitor='val_loss', save_best_only=True, verbose=1)
early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, verbose=1)

# Entrenamiento del modelo
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size,
    callbacks=[checkpoint, early_stop, reduce_lr]
)

