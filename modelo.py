import pandas as pd
import random 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib

dados = []

for _ in range(1000):
    valor = random.uniform(10.0, 15000.0)

    if valor > 8000:
        fraude = 1 if random.random() > 0.1 else 0 
    else:
        fraude = 1 if random.random() > 0.95 else 0 
        
    dados.append({'valor': valor, 'fraude': fraude})

df = pd.DataFrame(dados)

X = df[['valor']]
y = df['fraude']

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

modelo = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
modelo.fit(X_treino, y_treino)

y_pred = modelo.predict(X_teste)
acuracia = accuracy_score(y_teste, y_pred)
print(f"Acurácia no Teste: {acuracia * 100:.2f}%")

arquivo_modelo = 'modelo_antifraude.pkl'
joblib.dump(modelo, arquivo_modelo)