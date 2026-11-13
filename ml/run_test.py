import pytest
pytest.importorskip("pandas")
import pandas as pd, os




csv_path = os.path.join(os.path.dirname(__file__), 'datasets', 'data', 'raw', 'cardio_train.csv')

print('CSV path:', csv_path)

df = pd.read_csv(csv_path, sep=';')

print('Rows, cols:', df.shape)
