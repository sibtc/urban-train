TYPE_VEHICLE = (
    ("C", "Carro"),
    ("M", "Moto"),
)

SEXO = (
    ("F", u"FEMININO"),
    ("M", u"MASCULINO"),
)

STATE_CHOICES = (
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", u"Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
)

INATIVO, ATIVO = False, True

STATUS = (
    (ATIVO, "Ativa"),
    (INATIVO, "Inativa"),
)

NAO, SIM = 0, 1
OBRIGATORIO = (
    (NAO, "Não"),
    (SIM, "Sim"),
)

TIPO_LOGRADOURO = (
    ("R", "Rua"),
    ("AV", "Avenida"),
    ("AL", "Alameda"),
    ("A", "Area"),
    ("BL", "Bloco"),
    ("COND", "Condominio"),
    ("EST", "Estrada"),
    ("LGO", "Lago"),
    ("PC", "Praca"),
    ("Q", "Quadra"),
    ("RES", "Residencial"),
    ("ROD", "Rodovia"),
    ("TV", "Travessa"),
    ("VLA", "Viela"),
    ("VL", "Vila"),
    ("AER", "Aeroporto"),
    ("BAL", "Balneario"),
    ("CPO", "Campo"),
    ("CH", "Chacara"),
    ("COL", "Colonia"),
    ("CJ", "Conjunto"),
    ("DT", "Distrito"),
    ("ESP", "Esplanada"),
    ("ETC", "Estacao"),
    ("FAV", "Favela"),
    ("FAZ", "Fazenda"),
    ("FRA", "Feira"),
    ("GAL", "Galeria"),
    ("GJA", "Granja"),
    ("JD", "Jardim"),
    ("LD", "Ladeira"),
    ("LGA", "Lagoa"),
    ("LRG", "Largo"),
    ("LOT", "Loteamento"),
    ("MRO", "Morro"),
    ("NUC", "Nucleo"),
    ("O", "Outros"),
    ("PRQ", "Parque"),
    ("PSA", "Passarela"),
    ("PAT", "Patio"),
    ("PR", "Praia"),
    ("REC", "Recanto"),
    ("ST", "Setor"),
    ("SIT", "Sitio"),
    ("TRC", "Trecho"),
    ("TRV", "Trevo"),
    ("VLE", "Vale"),
    ("VER", "Vereda"),
    ("V", "Via"),
    ("VD", "Viaduto"),
)

REGION_CHOICES = (
    ("S", "SUL"),
    ("SE", "SUDESTE"),
    ("NE", "NORDESTE"),
    ("N", "NORTE"),
    ("CO", "CENTRO OESTE"),
)
