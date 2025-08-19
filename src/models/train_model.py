from src.features.build_features import Features
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

class TrainModel:
    def __init__(self) -> None:
        self._normalize = Features()

    def train(self, column_numeric: list[int, float] = None, column_categoric: list[str] = None, x: list = None, y: list = None):
        self._response_processor = self._normalize.processor(column_numeric, column_categoric)

        self._x_train, self._x_test, self._y_train, self._y_test = train_test_split(
            x, y, test_size=0.3, stratify=y, random_state=42
        )

        self._X_train_transf = self._response_processor.fit_transform(self._x_train)
        self._X_test_transf = self._response_processor.transform(self._x_test)

        return self._x_train, self._x_test, self._y_train, self._y_test, self._X_train_transf, self._X_test_transf, self._response_processor
    
    def balancing(self, data: list = None):
        self._balance = SMOTE(sampling_strategy='minority')
        self._X_train_bal, self._y_train_bal = self._balance.fit_resample(data[0], data[1])

        return self._X_train_bal, self._y_train_bal
    
        

