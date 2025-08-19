#import os
#os.environ["PYSPARK_PYTHON"] = r"C:\Users\kaique-ramos\AppData\Local\Programs\Python\Python311\python.exe"
#os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\kaique-ramos\AppData\Local\Programs\Python\Python311\python.exe"
#from pyspark.sql import SparkSession
import pandas as pd
import numpy as np
from pathlib import Path
from src.utils.data_cleaning import Clear
from src.models.train_model import TrainModel
from pandas import to_numeric, DataFrame
from src.utils.file_handler import FileHandler
from src.models.predict_model import PredicModel
from src.features.build_features import Features

class ProcessData:
    def __init__(self) -> None:
        self._clear = Clear()
        self._train = TrainModel()
        self._file_handler = FileHandler()
        self._predict_model = PredicModel()
        self._features = Features()

    def process_file(self, path: str = None) -> None:
        self._base = pd.read_csv(path, sep="|", encoding="utf-8", on_bad_lines="skip")
        self._base.columns = self._base.columns.str.strip()

        self._base = self._base.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        self._base[self._base.columns] = self._base[self._base.columns].replace({'None': np.nan, '': np.nan})
        
        self._base = self._base[
                    (self._base['PRODUTO'].notna()) &
                    (self._base['ESTADO'].notna()) &
                    (self._base['NOME'].notna()) &
                    (self._base['IDADE'].notna()) &
                    (self._base['SEXO'].notna()) &
                    (self._base['PRINCIPAL'].notna())
                ]
        
        self._base = self._clear.convert_object_columns(self._base)

        self._parant_path = Path(path).parent

        self._base.to_parquet(
            fr"{self._parant_path}\filtered_data.parquet",
            index=False,
            engine="pyarrow"
        )
    
    def define_type_column(self, columns: list[str] = None,  df: DataFrame = None, type_column: object = None) -> DataFrame:
        for c in columns:
            df[c] = type_column(df[c], errors='coerce')

        return df
    
    def normalize_data(self, path: str = None) -> None:
        self._base = pd.read_parquet(path, engine='pyarrow')
        self._base.columns = self._base.columns.str.strip()

        self._base = self.define_type_column(['PRINCIPAL', 'IDADE', 'ATRASO', 'STATUS_CONFIRMADO'], self._base, to_numeric)
        
        self._base = self._base[self._base['PAGO'] != 'PAGO']

        self._x = self._base.drop(columns=[
            'PAGO', 'ID_CONTR', 'LOCAL_TRAB', 'NOME', 'NUM_CONTRATO',
            'DESCRICAO_PRODUTO', 'PESSOA_JURIDICA', 'PRIM_VENC_ORIGINAL'
        ], errors='ignore')

        self._y = self._base['PAGO']

        self._column_categoric = self._x.select_dtypes(include=['object', 'category']).columns.tolist()
        self._column_numeric = self._x.select_dtypes(include=[np.number]).columns.tolist()
          
        self._x_train, self._x_test, self._y_train, self._y_test, self._X_train_transf, self._X_test_transf, self._response_processor = self._train.train(self._column_numeric, self._column_categoric, self._x, self._y)
        
        self._X_train_bal, self._y_train_bal = self._train.balancing([self._X_train_transf, self._y_train])
        
        
        self._parant_path = Path(path).parent.parent

        self._file_handler.write_pkl(fr'{self._parant_path}\processed\data_already_process.pkl', 
                                    (self._x_train, self._x_test, self._y_train, self._y_test, self._X_train_transf, self._X_test_transf, self._X_train_bal, self._y_train_bal, self._response_processor))
    
    
    def load_data_for_prediction(self, path: str = None):
        self._x_train, self._x_test, self._y_train, self._y_test, self._X_train_transf, self._X_test_transf, self._X_train_bal, self._y_train_bal, self._response_processor = self._file_handler.read_pkl(path)

        self._response_model = self._predict_model.model([self._X_train_bal, self._y_train_bal])

        self._response_predict_model_y = self._predict_model.pred_model(self._response_model, [self._X_test_transf])
       
        return self._response_predict_model_y.astype(int), self._y_test.astype(int)
    

    def load_data_for_calc_probability(self, path: str = None, path_pkl: str = None):
        self._x_train, self._x_test, self._y_train, self._y_test, self._X_train_transf, self._X_test_transf, self._X_train_bal, self._y_train_bal, self._response_processor = self._file_handler.read_pkl(path_pkl)

        self._base = pd.read_parquet(path, engine='pyarrow')

        self._x = self._base.drop(columns=[
            'PAGO', 'ID_CONTR', 'LOCAL_TRAB', 'NOME', 'NUM_CONTRATO',
            'DESCRICAO_PRODUTO', 'PESSOA_JURIDICA', 'PRIM_VENC_ORIGINAL'
        ], errors='ignore')
        
        self._base = self._base[self._base['PAGO'] == '0']

        self._base_x = self._base[self._x.columns].copy()

        self._base['SEXO'] = self._base['SEXO'].astype(str)
        
        self._response_model = self._predict_model.model([self._X_train_bal, self._y_train_bal])

        self._response_probability = self._predict_model.probability(self._response_processor, self._base_x, self._response_model) 
        
        self._base['chance_pagar'] = self._response_probability

        self._base = self._base[['ID_CONTR', 'chance_pagar']]
        
        self._parant_path = Path(path).parent.parent

        self._file_handler.write_txt(fr'{self._parant_path}\processed\visualize.txt', self._base, '|',
                                    ['ID_CONTR', 'chance_pagar'])