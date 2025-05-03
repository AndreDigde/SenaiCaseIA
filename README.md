# Case de IA, Senai #

Os scripts de AT1 e AT2 foram desenvolvido no `Python 3.12`, e a aplicação web utiliza em seus containers a versão `3.10`.

## AT1 ##

Em AT1 existe somente um script de nome `first_analysis.py`, no qual plota gráficos de dispersão de cada variável com uma saída e salva em arquivo, e também de variável com outra variável. O arquivo de dependências para executar esse script é o `requirements.txt` da raíz do projeto. Para executar basta utilizar o comando no diretório do script:

`python first_analysis.py`

## AT2 ##

No diretório AT2 contém 3 scripts. O `regression_train.py` é um arquivo somente para ser importado, nele há métodos para remover outliers dos dados com o método Z-score, embaralhar os dados e separar entre treino e teste, treinar regressões em lote, avaliar o resultado dos treinos, calcular o desempenho dos modelos e salvar os resultados em `csv`. São os modelos implementados no script `LinearRegression`, `SVR`, `GaussianProcessRegressor`, `MLPRegressor` e `RandomForestRegressor`. Também há uma função para remover dados outliers com o método Z-score.

O script `eval_models.py` monta os lotes de treino, e automatiza o treinamento e avaliação dos modelos. Para executar o scritp, bastar utilizar o comando abaixo:

`python eval_models.py`

Por último tem o script `create_model.py`, no qual treina e salva um modelo definido para ser utilizado na aplicação web. Além de salvar as métricas de avaliação do modelo. Para executar, use o comando:

`python create_model.py`

O arquivo de dependências para executar esse script é o `requirements.txt` da raíz do projeto.

## AT3 ##

AT3 é o sistema web que importa o modelo treinado e expões uma api para poder utilizá-la. Estão implementados um CRUD das predições do modelo, um CRUD de usuário e um sistema de autenticação com `JWT`. Todos os endpoints, excetos os de autentição, estão protegidos e necessita de token válido. O projeto está conteinerizado em `Docker`, basta executar o comando abaixo no diretório `AT3` para configurar e subir o ambiente utilizando o `Docker`:

`docker compose up`

Pode acontecer do container do banco de dados não estar pronto antes do container da aplicação, nesse caso execute o comando anterior novamente para que a aplicação suba corretamente.

Com o sistema executando, para acessar localmente utilize a URL `http://localhost:8000/`, nesse endereço consta a documentação da API feita pelo `Swagger`. No `Swagger` há disponível uma interface gráfica para utilizar os end-points, no qual estão agrupados por funcionalidade e há exemplos de utilização.
