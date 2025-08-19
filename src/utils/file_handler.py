from pathlib import Path
from shutil import copyfileobj
from pickle import dump, load
from pandas import DataFrame

class FileHandler:
    def __init__(self) -> None:
        #self._header = [
        #    'ID_CONTR', 'NUM_CONTRATO', 'NOME', 'ESTADO', 'PRINCIPAL', 'PRODUTO', 'PESSOA_JURIDICA', 
        #    'SEXO', 'LOCAL_TRAB', 'IDADE', 'PRIM_VENC_ORIGINAL','PAGO', 'ATRASO', 'STATUS_CONFIRMADO', 'chance pagar'
        #]
        pass

    def read_sql_txt(self, path: str = None) -> str:
        with open(path, 'r', encoding="utf-8") as f:
            self._response_file = f.read()

        return  self._response_file

    def create_txt_file(self, path_file: str = None) -> None:
        self._path = Path(path_file)
        
        if not self._path.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)  # cria pastas pai se não existirem
            self._path.touch()
    
    def size_file(self, path: str = None) -> int:
        with open(path, 'r', encoding="utf-8") as f:
            self.__total_lines = len(f.readline())

        return self.__total_lines
    
    def delete_data(self, path):
        with open(path, "r+", encoding="utf-8") as f:  # r+ = leitura e escrita
            f.truncate(0) 

    def write_txt(self, path: str = None, data: DataFrame = None, delimiter: str = '|', header: list = None) -> None:
        self.create_txt_file(path)
        
        if Path(path).exists():
            self.delete_data(path)

        # Se header não for fornecido, pega do DataFrame
        if header is None:
            header = list(data.columns)

        num_cols = len(header)

        if isinstance(data, list):
            # Converte DataFrame para lista de listas, garantindo tamanho igual ao header
            lines = [header] + [list(map(str, row))[:num_cols] + ['']*(num_cols - len(row)) for row in data]
        else:
            lines = [header] + [list(map(str, row))[:num_cols] + ['']*(num_cols - len(row)) for row in data.values.tolist()]

        # Calcula largura máxima de cada coluna
        col_widths = [max(len(str(field)) for field in col) for col in zip(*lines)]

        with open(path, 'w', encoding='utf-8') as f:
            for line in lines:
                # Garante que cada linha tem o tamanho de col_widths
                line_extended = line + ['']*(len(col_widths) - len(line))
                formatted_line = f" {delimiter} ".join(f"{field:<{col_widths[i]}}" for i, field in enumerate(line_extended))
                f.write(formatted_line + '\n')

    
    def join_files(self, entry_files: list[str] = None, output_files: str = None) -> None:
        with open(output_files, 'wb') as outfile:
            for file in entry_files:
                with open(file, 'rb') as infile:
                    copyfileobj(infile, outfile)
    
    def write_pkl(self, path: str = None, data: tuple = None) -> None:
         with open(path, 'wb') as f:
            dump(data, f)

    def read_pkl(self, path: str = None) -> list:
        with open(path, 'rb') as f:
          self._x_train, self._x_test, self._y_train, self._y_test, self._X_train_transf, self._X_test_transf, self._X_train_bal, self._y_train_bal, self._response_processor  = load(f)
        
        return self._x_train, self._x_test, self._y_train, self._y_test, self._X_train_transf, self._X_test_transf, self._X_train_bal, self._y_train_bal, self._response_processor
        