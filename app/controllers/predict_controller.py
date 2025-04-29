from app.utils.image_preprocess import preprocess_image_from_path
from app.models.model import predict

async def test_predict():
    img_path = r"C:\Users\nimes\Desktop\Screenshot 2025-04-27 132600.png" # Change to your actual image path
    img_array = preprocess_image_from_path(img_path)
    prediction, label = predict(img_array)
    return {"prediction": float(prediction), "label": label}
