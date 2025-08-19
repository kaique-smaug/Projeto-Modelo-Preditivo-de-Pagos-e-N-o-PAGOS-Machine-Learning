from src.data.load_data import DataLoader
from src.utils.paths import Paths
from src.utils.file_handler import FileHandler
from src.data.process_data import ProcessData
from src.visualization.visualize import Visualize

def main():
    dataloader = DataLoader()
    path = Paths()
    file_handler = FileHandler()
    process_data = ProcessData()
    visualize = Visualize()
    
    response_data_loader = dataloader.fetch_data(file_handler.read_sql_txt(fr'{path.get_project_root()}\querys\PAGOS.txt'))     
    file_handler.write_txt(fr'{path.get_project_root()}\data\raw\response_query_paids.txt', response_data_loader, '|',
    [
            'ID_CONTR', 'NUM_CONTRATO', 'NOME', 'ESTADO', 'PRINCIPAL', 'PRODUTO', 'PESSOA_JURIDICA', 
            'SEXO', 'LOCAL_TRAB', 'IDADE', 'PRIM_VENC_ORIGINAL','PAGO', 'ATRASO', 'STATUS_CONFIRMADO'])
    
    response_data_loader = dataloader.fetch_data(file_handler.read_sql_txt(fr'{path.get_project_root()}\querys\BASE_GERAL.txt'))     
    file_handler.write_txt(fr'{path.get_project_root()}\data\raw\response_query_general.txt', response_data_loader, '|',
    ['ID_CONTR', 'NUM_CONTRATO', 'NOME', 'ESTADO', 'PRINCIPAL', 'PRODUTO', 'PESSOA_JURIDICA', 
        'SEXO', 'LOCAL_TRAB', 'IDADE', 'PRIM_VENC_ORIGINAL','PAGO', 'ATRASO', 'STATUS_CONFIRMADO'])
    
    file_handler.join_files(
        [fr'{path.get_project_root()}\data\raw\response_query_paids.txt', fr'{path.get_project_root()}\data\raw\response_query_general.txt'],
        fr'{path.get_project_root()}\data\interim\joinfiles.txt')
    
    process_data.process_file(fr'{path.get_project_root()}\data\interim\joinfiles.txt')
    
    process_data.normalize_data(fr'{path.get_project_root()}\data\interim\filtered_data.parquet')
    
    responsew_predict_y, responde_y_test =  process_data.load_data_for_prediction(fr'{path.get_project_root()}\data\processed\data_already_process.pkl')
    
    process_data.load_data_for_calc_probability(fr'{path.get_project_root()}\data\interim\filtered_data.parquet',
                                                                fr'{path.get_project_root()}\data\processed\data_already_process.pkl')
    
    visualize.confusion_v2([responde_y_test, responsew_predict_y], r'\\canada\mis_interno\Kaique\Robos\Previsao_cliente_rec\reports\figures')
    
    visualize.classification_v2([responde_y_test, responsew_predict_y], r'\\canada\mis_interno\Kaique\Robos\Previsao_cliente_rec\reports\metrics')
    
    visualize.f1_v2([responde_y_test, responsew_predict_y], r'\\canada\mis_interno\Kaique\Robos\Previsao_cliente_rec\reports\metrics')
    
    visualize.roc_auc_v2([responde_y_test, responsew_predict_y], r'\\canada\mis_interno\Kaique\Robos\Previsao_cliente_rec\reports\metrics')
    
if __name__ == '__main__':
    main()