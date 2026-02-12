from src.core.seguranca import gerar_hash_senha, verificar_senha

senha_do_usuario = "minha_senha_secreta"

# 1. Gerando o hash
hash_gerado = gerar_hash_senha(senha_do_usuario)
print(f"Senha original: {senha_do_usuario}")
print(f"Senha criptografada no banco: {hash_gerado}")

# 2. Tentando validar
teste_correto = verificar_senha("minha_senha_secreta", hash_gerado)
print(f"A senha bate? {teste_correto}")

teste_errado = verificar_senha("senha_errada", hash_gerado)
print(f"A senha errada bate? {teste_errado}")