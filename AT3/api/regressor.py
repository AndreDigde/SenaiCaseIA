from django.conf import settings
import pickle

class RegressorSingleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            if not cls._instance:
                cls._instance = super(RegressorSingleton, cls).__new__(cls)
                cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        with open(settings.MODEL_PATH, 'rb') as f:
            self.model = pickle.load(f)

    def predict(self, input_data):
        result = self.model.predict([input_data])
        return result[0][0], result[0][1]
