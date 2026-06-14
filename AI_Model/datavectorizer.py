from picamera2 import Picamera2
import numpy as np

capture = Picamera2()

capture.configure(capture.create_still_configuration(main={"size": (128, 128)}))

capture.start()
brick_types = ["full_brick", "2x2_brick", "technic_rod"]
images = []
labels = []
instances = int(input("How many instances for each class? "))

current_label = 0
for current_label, brick_name in enumerate(brick_types):
    for i in range(instances):
        input('Press enter to caputure')
        array = capture.capture_array()
        scaled_frame = array.astype(np.float32) / 255.0
        images.append(scaled_frame)
        labels.append(current_label)
        print(f"captured {i}/{instances}")
    print(f"done with {brick_name}")

capture.stop()

X_train = np.array(images)
Y_train = np.array(labels)
np.save('lego_images.npy', X_train)
np.save('lego_labels.npy', Y_train)
print("\nSuccess! Both arrays are saved to disk and perfectly consistent.")
