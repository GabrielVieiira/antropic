from django.core.exceptions import ValidationError

def validar_cnpj(cnpj):
    if not cnpj or len(cnpj) != 14 or not cnpj.isdigit():
        raise ValidationError("CNPJ deve conter exatamente 14 dígitos numéricos.")
    
    if len(set(cnpj)) == 1:
        raise ValidationError("CNPJ inválido: todos os dígitos são iguais.")
    
    def calcular_digito(cnpj_base, pesos):
        soma = sum(int(cnpj_base[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digito1 = calcular_digito(cnpj[:12], pesos1)
    
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digito2 = calcular_digito(cnpj[:13], pesos2)
    
    if int(cnpj[12]) != digito1 or int(cnpj[13]) != digito2:
        raise ValidationError("CNPJ inválido: dígitos verificadores incorretos.")