import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_LEN = 100

class AIModel:

    def __init__(self):

        with open("tokenizer (1).pkl","rb") as f:
            self.tokenizer = pickle.load(f)

        self.model = load_model("waf_attack_classifier.h5")

        self.labels = ["NORMAL","SQL","XSS"]


    def predict(self,text):

        seq = self.tokenizer.texts_to_sequences([text])

        padded = pad_sequences(seq,maxlen=MAX_LEN)

        pred = self.model.predict(padded)

        index = np.argmax(pred)

        confidence = pred[0][index]

        if confidence < 0.6:
            return "UNKNOWN"

        return self.labels[index]