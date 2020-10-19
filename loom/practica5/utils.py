import re

numero_ronmano_pattern = '^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'


def remover_digitos(palabra):
    return ''.join([i for i in palabra if not i.isdigit()]).strip()


def remover_caracteres(palabra):
    return ''.join([s for s in palabra.split() if s.isdigit()])


def remover_caracteres_especiales(palabra):
    return ''.join(filter(lambda x: x.isalpha() or x.isspace() or x.isdigit(), palabra))


def es_numero_romano(palabra):
    return re.search(numero_ronmano_pattern, palabra)
