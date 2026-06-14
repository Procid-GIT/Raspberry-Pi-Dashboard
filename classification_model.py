import tensorflow as tf
import numpy as np

x_train = np.load('lego_images.npy')
y_train = np.load('lego_labels.npy')
print("Data successfully loaded")

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(128, 128, 3)),
    tf.keras.layers.Conv2D(32, (3, 3), activation ='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(3)
])


loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer = tf.keras.optimizers.Adam()

print("preparing model training...")
model.compile(optimizer=optimizer, loss=loss_fn, metrics=['accuracy'])

print("training AI Model...")
model.fit(x_train, y_train, epochs=10, batch_size=4)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
print("Preparing for conversion to tflite... ")
tflite_model = converter.convert()
with open('robotArm.tflite', 'wb') as f:
    f.write(tflite_model)
print("AI successfully written to disk.")