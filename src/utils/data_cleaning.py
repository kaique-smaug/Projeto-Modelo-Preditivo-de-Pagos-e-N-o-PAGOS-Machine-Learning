from pandas import to_numeric, DataFrame

class Clear:

    def convert_object_columns(self, df: DataFrame) -> DataFrame:
        for col in df.columns:
            if df[col].dtype == "object":
                
                if to_numeric(df[col], errors="coerce").notna().all():
                    df[col] = to_numeric(df[col], errors="coerce").astype("Int64")
                
                else:
                    df[col] = df[col].astype(str)
        
        return df