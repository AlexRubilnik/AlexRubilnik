def furnace1_errors_list(err_query):
    # Принимает массив ошибок faults1, faults2, faults3, faults4
    # Возвращает расшифрованный список ошибок в текстовом виде
    errors = list()

    #FAULTS1
    if err_query.faults1 & 1:
        pass #errors.append("1: ")
    if err_query.faults1 & 2:
        pass #errors.append("2: ")
    if err_query.faults1 & 4:
        errors.append("3: Ошибка давления воздуха (PSL300)")
    if err_query.faults1 & 8:
        errors.append("4: Высокое давление ПГ")
    if err_query.faults1 & 16:
        errors.append("5: Высокое давление О2")
    if err_query.faults1 & 32:
        errors.append("6: Низкое давление ПГ")
    if err_query.faults1 & 64:
        errors.append("7: Низкое давление О2")
    if err_query.faults1 & 128:
        errors.append("8: Ошибка измерения ПГ")
    if err_query.faults1 & 256:
        errors.append("9: Ошибка измерения О2")
    if err_query.faults1 & 512:
        errors.append("10: Ошибка соотношения О2/СН4")
    if err_query.faults1 & 1024:
        errors.append("11: MPA4112 Ошибка пилотной горелки")
    if err_query.faults1 & 2048:
        errors.append("12: MPA4112 Ошибка основной горелки")
    if err_query.faults1 & 4096:
        errors.append("13: VPM Ошибка контроля герметичности")
    if err_query.faults1 & 8192:
        pass #errors.append("14: ")
    if err_query.faults1 & 16384:
        pass #errors.append("15: ")
    if err_query.faults1 & 32768:
        errors.append("16: Горелка не в положении розжига")
    
    #FAULTS2
    if err_query.faults2 & 1:
        errors.append("17: Ошибка шкафа управления")
    if err_query.faults2 & 2:
        errors.append("18: Несоответствие расхода О2 уставке")
    if err_query.faults2 & 4:
        errors.append("19: Несоответствие расхода ПГ уставке")
    if err_query.faults2 & 8:
        errors.append("20: Ошибка KV100")
    if err_query.faults2 & 16:
        errors.append("21: Ошибка регулятора расхода FCV101")
    if err_query.faults2 & 32:
        errors.append("22: Ошибка регулятора расхода FCV201")
    if err_query.faults2 & 64:
        errors.append("23: Неправильная конфигурация блока клапанов")
    if err_query.faults2 & 128:
        errors.append("24: Отсутствует питание 24В")
    if err_query.faults2 & 256:
        pass #errors.append("25: ")
    if err_query.faults2 & 512:
        errors.append("26: Ошибка частотника воздуходувки")
    if err_query.faults2 & 1024:
        errors.append("27: Ошибка измерения температуры печи")
    if err_query.faults2 & 2048:
        errors.append("28: Уставка заданного значения Lambda")
    if err_query.faults2 & 4096:
        errors.append("29: Дистанционное задание мощности")
    if err_query.faults2 & 8192:
        errors.append("30: Расход воздушного дутья не соответствует уставке")
    if err_query.faults2 & 16384:
        errors.append("31: Высокая концентрация ПГ в воздухе рабочей зоны")
    if err_query.faults2 & 32768:
        errors.append("32: Отказ детектора ПГ")

    #FAULTS3
    if err_query.faults3 & 1:
        errors.append("33: Высокая концентрация О2 в воздухе рабочей зоны")
    if err_query.faults3 & 2:
        errors.append("34: Отказ детектора О2")
    if err_query.faults3 & 4:
        errors.append("35: Ошибка ПЛК клиента")
    if err_query.faults3 & 8:
        errors.append("36: Авария системы дымоудаления (ПЛК клиента)")
    if err_query.faults3 & 16:
        errors.append("37: Авария вращения печи (ПЛК клиента)")
    if err_query.faults3 & 32:
        pass #errors.append("38: ")
    if err_query.faults3 & 64:
        errors.append("39: Отказ системы мониторинга клиента (ПЛК клиента)")
    if err_query.faults3 & 128:
        errors.append("40: Ошибка КАЗ")
    if err_query.faults3 & 256:
        errors.append("41: Нажата аварийная кнопка")
    if err_query.faults3 & 512:
        errors.append("42: Внешний аварийный сигнал (ПЛК клиента)")
    if err_query.faults3 & 1024:
        errors.append("43: Нажата внешняя аварийная кнопка")
    if err_query.faults3 & 2048:
        errors.append("44: Ошибка КА 4")
    if err_query.faults3 & 4096:
        errors.append("45: Ошибка расходометра воздуха")
    if err_query.faults3 & 8192:
        errors.append("46: Соотношение мощности к О2 обогащению")
    if err_query.faults3 & 16384:
        errors.append("47: Отказ реле КА1/КА2")
    if err_query.faults3 & 32768:
        errors.append("48: Отказ KY300")

    #FAULTS4
    if err_query.faults4 & 1:
        errors.append("49: Модуль сигналов выхода в режиме защиты")

    return errors


def furnace2_errors_list(err_query):
    # Принимает массив ошибок faults1, faults2
    # Возвращает расшифрованный список ошибок в текстовом виде
    errors = list()

    #FAULTS1
    if err_query.faults1 & 1:
        errors.append("1: Низкое давление ПГ")
    if err_query.faults1 & 2:
        errors.append("2: Низкое давление О2")
    if err_query.faults1 & 4:
        errors.append("3: Низкое давление воздуха")
    if err_query.faults1 & 8:
        errors.append("4: Высокое давление ПГ")
    if err_query.faults1 & 16:
        errors.append("5: Высокое давление О2")
    if err_query.faults1 & 32:
        errors.append("6: Ошибка измерения давления ПГ")
    if err_query.faults1 & 64:
        errors.append("7: Ошибка измерения давления О2")
    if err_query.faults1 & 128:
        errors.append("8: Ошибка измерения расхода ПГ")
    if err_query.faults1 & 256:
        errors.append("9: Ошибка измерения расхода О2")
    if err_query.faults1 & 512:
        errors.append("10: Ошибка контроля герметичности")
    if err_query.faults1 & 1024:
        errors.append("11: Ошибка соотношения ПГ/О2")
    if err_query.faults1 & 2048:
        errors.append("12: Ошибка пилотной горелки")
    if err_query.faults1 & 4096:
        errors.append("13: Ошибка основной горелки")
    if err_query.faults1 & 8192:
        errors.append("14: Ошибка шкафа управления")
    if err_query.faults1 & 16384:
        errors.append("20: Ошибка конфигурации")
    if err_query.faults1 & 32768:
        errors.append("15: Несоответствие расхода ПГ уставке")
    
    #FAULTS2
    if err_query.faults2 & 1:
        errors.append("16: Несоответствие расхода О2 уставке")
    if err_query.faults2 & 2:
        errors.append("18: Limit S. valves KV100-KV200")
    if err_query.faults2 & 4:
        errors.append("Ошибка глаза")
    if err_query.faults2 & 8:
        errors.append("Отклонение от заданной температуры")
    if err_query.faults2 & 16:
        errors.append("Ошибка измерения температуры")
    if err_query.faults2 & 32:
        errors.append("19: Limit S. valves PCV100-PCV200")
    if err_query.faults2 & 64:
        errors.append("21: Ошибка питания")
    if err_query.faults2 & 128:
        errors.append("22: Температура О2 слишком низкая")
    if err_query.faults2 & 256:
        errors.append("23: Воздуходувка не готова")
    if err_query.faults2 & 512:
        errors.append("24: Несоответствие расхода воздуха уставке")
    if err_query.faults2 & 1024:
        errors.append("17: Ошибка чтения по UDP")
    if err_query.faults2 & 2048:
        errors.append("27: Слишком много ошибок розжига")
    if err_query.faults2 & 4096:
        pass #errors.append("29: ")
    if err_query.faults2 & 8192:
        pass #errors.append("30: ")
    if err_query.faults2 & 16384:
        pass #errors.append("31: ")
    if err_query.faults2 & 32768:
        pass #errors.append("32: ")    

    return errors
        