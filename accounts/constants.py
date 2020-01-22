import re

INATIVO, ATIVO = False, True
STATUS = (
    (ATIVO, 'Ativa'),
    (INATIVO, 'Inativa'),
)

NAO, SIM = 0,1
OBRIGATORIO = (
    (NAO, 'Não'),
    (SIM, 'Sim'),
)

MASCULINO, FEMININO, INDEFINIDO = 'M', 'F', 'I'
SEXO = (
    (MASCULINO, 'MASCULINO'),
    (FEMININO, 'FEMININO'),
    (INDEFINIDO, 'INDEFINIDO'),
)
