from sklearn.metrics import (
    confusion_matrix, classification_report,
    f1_score, roc_auc_score
)
import matplotlib.pyplot as plt
#from pathlib import Path
import seaborn as sns
import plotly.figure_factory as ff
from pandas import DataFrame

class Visualize:

    def confusion(self, data: list = None) -> confusion_matrix:
        print("Matriz de Confusão:")
        return confusion_matrix(data[0], data[1])
    
    def classification(self, data: list = None) -> classification_report:
        print("\nRelatório de Classificação:")
        return classification_report(data[0], data[1])
    
    def f1(self, data: list = None) -> f1_score:
        print("F1 Score:")
        return f1_score(data[0], data[1])
    
    def roc_auc(self, data: list = None) -> roc_auc_score:
        print("ROC AUC:")
        return roc_auc_score(data[0], data[1])

    def confusion_v2(self, data: list = None, path: str = None) -> None:
        cm = confusion_matrix(y_true=data[0], y_pred=data[1])
        z = cm.tolist()

        fig = ff.create_annotated_heatmap(
            z,
            x=["Predito 0", "Predito 1"],
            y=["Real 0", "Real 1"],
            colorscale='Blues',
            showscale=True
        )
        fig.update_layout(title='Matriz de Confusão')
        fig.write_html(f'{path}\\confusion.html')

        
    def classification_v2(self, data: list = None, path: str = None) -> classification_report:
        #Gera o relatório como dicionário
        report_dict = classification_report(data[0], data[1], output_dict=True)

        # Converte para DataFrame para facilitar formatação
        df = DataFrame(report_dict).transpose()

        # Salva em HTML (DataFrame já tem método pra isso)
        df.to_html(f"{path}\\classification_report.html", float_format="%.4f", border=1)

        print("\nRelatório de Classificação salvo em HTML.")

    
    def f1_v2(self, data: list = None, path: str = None) -> f1_score:
        score = f1_score(data[0], data[1])

        html_content = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>F1 Score</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>F1 Score</h2>
            <table>
                <tr><th>F1 Score</th></tr>
                <tr><td>{score:.4f}</td></tr>
            </table>
        </body>
        </html>
        """

        with open(f"{path}\\f1_score.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def roc_auc_v2(self, data: list = None, path: str = None) -> roc_auc_score:
        score = roc_auc_score(data[0], data[1])

        html_content = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>ROC AUC Score</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>ROC AUC Score</h2>
            <table>
                <tr><th>ROC AUC</th></tr>
                <tr><td>{score:.4f}</td></tr>
            </table>
        </body>
        </html>
        """

        with open(f"{path}\\roc_auc_score.html", "w", encoding="utf-8") as f:
            f.write(html_content)
