import numpy as np
from keras.applications import inception_v3

def to_model_image(image):
    img = np.copy(image)
    img /= 255.0
    img -= 0.5
    img *= 2.0
    return img

def predict_classes(model, image, top_count=5):
    input_image_extended = np.expand_dims(image, axis=0)
    predictions = model.predict(input_image_extended)
    predicted_classes = inception_v3.decode_predictions(predictions, top=top_count)
    results = []
    for i in range(top_count):
        _, name, confidence = predicted_classes[0][i]
        results.append({'className': name, 'probability': float(confidence)})
    return results

