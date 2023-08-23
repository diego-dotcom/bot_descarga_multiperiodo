from datetime import datetime, timedelta


def obtener_rangos_meses_completos(fecha_inicio, fecha_final):
    fecha_inicio = datetime.strptime(fecha_inicio, '%d/%m/%Y')
    fecha_final = datetime.strptime(fecha_final, '%d/%m/%Y')

    rangos_meses = []
    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_final:
        primer_dia_mes = fecha_actual.replace(day=1)

        if primer_dia_mes.month == 12:
            ultimo_dia_mes = primer_dia_mes.replace(
                year=primer_dia_mes.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            siguiente_mes = primer_dia_mes.month % 12 + 1
            siguiente_ano = primer_dia_mes.year if siguiente_mes != 1 else primer_dia_mes.year + 1
            ultimo_dia_mes = primer_dia_mes.replace(
                year=siguiente_ano, month=siguiente_mes, day=1) - timedelta(days=1)

        if ultimo_dia_mes > fecha_final:
            ultimo_dia_mes = fecha_final

        rangos_meses.append([primer_dia_mes.strftime(
            '%d/%m/%Y'), ultimo_dia_mes.strftime('%d/%m/%Y')])

        fecha_actual = ultimo_dia_mes + timedelta(days=1)

    return rangos_meses
