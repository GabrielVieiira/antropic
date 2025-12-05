from django.db import models


class NivelCargo(models.TextChoices):
    OPERACIONAL = 'OPERACIONAL', 'Operacional'
    TECNICO = 'TECNICO', 'Técnico'
    SUPERVISAO = 'SUPERVISAO', 'Supervisão'
    COORDENACAO = 'COORDENACAO', 'Coordenação'
    GERENCIA = 'GERENCIA', 'Gerência'
    DIRETORIA = 'DIRETORIA', 'Diretoria'


class Parentesco(models.TextChoices):
    FILHO = 'FILHO', 'Filho(a)'
    CONJUGE = 'CONJUGE', 'Cônjuge'
    IRMAO = 'IRMAO', 'Irmão(ã)'
    PAIS = 'PAIS', 'Pais'
    OUTROS = 'OUTROS', 'Outros'


class TipoEquipe(models.TextChoices):
    MANUAL = 'MANUAL', 'Manual'
    MECANIZADA = 'MECANIZADA', 'Mecanizada'


class TipoContrato(models.TextChoices):
    CLT = 'CLT', 'CLT'
    PJ = 'PJ', 'Pessoa Jurídica'
    ESTAGIARIO = 'ESTAGIARIO', 'Estagiário'
    TEMPORARIO = 'TEMPORARIO', 'Temporário'
    APRENDIZ = 'APRENDIZ', 'Jovem Aprendiz'


class StatusFuncionario(models.TextChoices):
    ATIVO = 'ATIVO', 'Ativo'
    AFASTADO = 'AFASTADO', 'Afastado'
    FERIAS = 'FERIAS', 'Em Férias'
    DEMITIDO = 'DEMITIDO', 'Demitido'


class Turno(models.TextChoices):
    DIURNO = 'DIURNO', 'Diurno'
    NOTURNO = 'NOTURNO', 'Noturno'
    INTEGRAL = 'INTEGRAL', 'Integral'
    FLEXIVEL = 'FLEXIVEL', 'Flexível'


class TipoConta(models.TextChoices):
    CORRENTE = 'CORRENTE', 'Conta Corrente'
    POUPANCA = 'POUPANCA', 'Conta Poupança'
