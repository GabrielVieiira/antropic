from apps.contratos.models import ContratoContratante, ContratoFiliais

def listar_contratos_contratante(contratante_id):
    return ContratoContratante.objects.filter(contratante_id=contratante_id, ativo=True)

def buscar_contrato_por_numero(numero_interno):
    return ContratoContratante.objects.filter(numero_contrato_interno=numero_interno).first()

def listar_subcontratos_por_contrato(contrato_id):
    return ContratoFiliais.objects.filter(contrato_id=contrato_id)

def buscar_subcontrato_por_filial(filial_id):
    return ContratoFiliais.objects.filter(filial_id=filial_id)