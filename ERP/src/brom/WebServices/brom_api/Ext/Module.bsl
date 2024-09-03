Функция DebugPing()
	Возврат "";
КонецФункции

Функция DebugEcho(param)
	значение = brom_API.ИзЗначенияБром(param);
	Возврат brom_API.ВЗначениеБром(значение, Строка(значение));
КонецФункции

Функция GetSystemInfo()
	Возврат brom_API.ПолучитьИнформациюОСистеме(); 
КонецФункции

Функция GetObjectList(type, name, settings)
	Возврат brom_API.ПолучитьСписокОбъектов(type, name, settings);
КонецФункции

Функция ExecuteRequest(request, settings)
	Возврат brom_API.ПолучитьРезультатЗапроса(request, settings);
КонецФункции

Функция ExecuteRequestBatch(request, settings)
	Возврат brom_API.ПолучитьРезультатПакетаЗапросов(request, settings);
КонецФункции

Функция GetObject(reference, settings)
	Возврат brom_API.ПолучитьОбъект(reference, settings);
КонецФункции

Функция GetSessionParameter(name)
	Возврат brom_API.ПолучитьЗначениеПараметраСеанса(name);
КонецФункции

Функция GetConstant(name, settings)
	Возврат brom_API.ПолучитьЗначениеКонстанты(name, settings);
КонецФункции

Функция SetConstant(name, value)
	Возврат brom_API.УстановитьЗначениеКонстанты(name, value);
КонецФункции

Функция GetConstantList(settings)
	Возврат brom_API.ПолучитьЗначенияКонстант(settings);
КонецФункции

Функция ExecuteCode(code, param)
	Возврат brom_API.ВыполнитьКод(code, param);
КонецФункции

Функция PostObject(object, settings)
	Возврат brom_API.ОпубликоватьОбъект(object, settings);
КонецФункции

Функция DeleteObject(object)
	Возврат brom_API.УдалитьОбъект(object);
КонецФункции

Функция ExecuteMethod(module, method, params)
	Возврат brom_API.ВыполнитьМетод(module, method, params);
КонецФункции

Функция GetMetadata(nodes, pack_size, pack_index)
	Возврат brom_API.ПолучитьМетаданные(nodes, pack_size, pack_index);
КонецФункции

Функция GetMetadataNames(parents)
	Возврат brom_API.ПолучитьИменаПодчиненныхУзловМетаданных(parents);	
КонецФункции


