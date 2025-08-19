from src.features.build_features import Features
from sklearn.linear_model import LogisticRegression

class PredicModel:
    def __init__(self) -> None:
        self._feature = Features()

    def model(self, data: list = None) -> object:
        self._model = LogisticRegression(max_iter=1000, random_state=42)
        self._model.fit(data[0], data[1])
    
        return self._model
    
    def pred_model(self, model: object, data: list = None):
        self._y_pred = model.predict(data[0])

        return self._y_pred
    
    def probability(self, response_processor: object = None, data: list = None, model: object = None):
        
        self._X_unknown_transf = response_processor.transform(data)

        self._probability = model.predict_proba(self._X_unknown_transf)[:, 1]
        
        return self._probability