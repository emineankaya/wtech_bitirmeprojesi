from fastapi import FastAPI, UploadFile, File 
from fastapi.responses import FileResponse 
from fastapi.responses import HTMLResponse
# HTMLResponse'ı içe aktarın
from keras.models import load_model
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from PIL import Image
import numpy as np
from typing import List, Optional
import io


from keras.models import load_model


app = FastAPI()

# Modeli yükle
model = load_model("C:\\Users\\emine\\OneDrive\\Masaüstü\\catanddog\\my_model.keras")



class Item(BaseModel):
    files: List[UploadFile] = File(...)

def process_image(contents, target_size=(224, 224)):
    img = Image.open(io.BytesIO(contents))
    img = img.resize(target_size)
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.post("/predict/", summary="Upload and predict clothing items")
async def predict(files: List[UploadFile] = File(...)):
    """
    Bu endpoint, yüklenen bir veya daha fazla kıyafet görüntüsünün sınıfını tahmin etmek için kullanılır.
    
    ### Giriş
    - **files**: Yüklenen bir veya daha fazla görüntü dosyası.
    
    ### Çıkış
    - **predictions**: Giriş görüntülerinin sınıf tahminleri. Her bir tahmin, bir sınıf etiketiyle birlikte bir olasılık dağılımını içeren bir liste olarak döndürülür.
    
    """

    processed_images = []
    for file in files:
        contents = await file.read()
        processed_image = process_image(contents)
        processed_images.append(processed_image)


    class_names = {
        0: "elbise\black_dress",
        1: "black_pants",
        2: "black_shirt",
        3: "black_shoes",
        4: "black_shorts",
        5: "blue_dress",
        6: "blue_pants",
        7: "blue_shirt",
        8: "blue_shoes",
        9: "blue_shorts",
        10: "brown_dress",
        11: "brown_pants",
        12: "brown_shirt",
        13: "brown_shoes",
        14: "brown_shorts",
        15: "red_dress",
        16: "red_pants",
        17: "red_shirt",
        18: "red_shoes",
        19: "red_shorts",
        20: "white_dress",
        21: "white_pants",
        22: "white_shirt",
        23: "white_shoes",
        24: "white_shorts"
      
    }
    predictions_with_class_names = []

    # predictions: modelin tahminlerinin olduğu liste
    for processed_image in processed_images:
        prediction = model.predict(processed_image)
        class_index = np.argmax(prediction[0])
        class_name = class_names[class_index]
        probability = np.max(prediction[0])
        predictions_with_class_names.append({"class_name": class_name, "probability": probability})

    return {"predictions": predictions_with_class_names}        
