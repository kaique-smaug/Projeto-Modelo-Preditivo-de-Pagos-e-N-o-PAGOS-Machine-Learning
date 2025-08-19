from src.config_scripts.sql.sql_insertion import InsertSQL

class LoadConnection:

    def get_instance(self, query: str = None) -> object:
        self._instance_insertSql = InsertSQL(query)
        
        return self._instance_insertSql