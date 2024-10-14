from consulta_webservice import consultar_webservice

# Chama a função para obter os dados
dados_consulta = consultar_webservice()

# Agora você pode usar os dados obtidos da consulta
print(dados_consulta['op'])
print(dados_consulta['nomeproduto'])
print(dados_consulta['serial'])
print(dados_consulta['so_instalacao'])
# ... (continua para acessar outros dados conforme necessário)
