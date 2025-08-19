from src.data.db.load_connection import LoadConnection

class DataLoader:
    #def __init__(self, query: str = None) -> None:
        #self._response_load_conection = LoadConnection().get_instance()
    
    def get_load_connection(self, query: str = None) -> object:
        return LoadConnection().get_instance(query)
        
    def fetch_data(self, query: str = None) -> list:
        self._response_get_load_connection = self.get_load_connection(query)
        
        
        self._response_data, _ = self._response_get_load_connection.mysql_query()
        
        
        if len(self._response_data) > 0:
            return self._response_data
        
        else: return []
    