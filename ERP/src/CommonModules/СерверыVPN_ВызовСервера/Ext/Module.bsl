﻿
Процедура УдалитьКонфигурацию(СерверСсылка, ИмяКонфигурации) Экспорт
	
	Запрос = Новый Запрос;
	Запрос.Текст = 
		"ВЫБРАТЬ
		|	СлотыКонфигураций.ИдСлота КАК ИдСлота
		|ИЗ
		|	РегистрСведений.СлотыКонфигураций КАК СлотыКонфигураций
		|ГДЕ
		|	СлотыКонфигураций.Сервер = &СерверСсылка
		|	И СлотыКонфигураций.ИмяКонфигурации = &ИмяКонфигурации";
	
	Запрос.УстановитьПараметр("ИмяКонфигурации", ИмяКонфигурации);
	Запрос.УстановитьПараметр("СерверСсылка", СерверСсылка);
	РезультатЗапроса = Запрос.Выполнить();
	ИдУдаленныхСлотов = РезультатЗапроса.Выгрузить().ВыгрузитьКолонку("ИдСлота");
	
	НаборЗаписей = РегистрыСведений.СлотыКонфигураций.СоздатьНаборЗаписей();
	НаборЗаписей.Отбор.Сервер.Установить(СерверСсылка);
	НаборЗаписей.Отбор.ИмяКонфигурации.Установить(ИмяКонфигурации);
	НаборЗаписей.Записать();
	
	Ответ = WGD_Соединение.УдалитьСлоты(ИмяКонфигурации, СерверСсылка, ИдУдаленныхСлотов);
	
	Если НЕ Ответ.status Тогда
		ВызватьИсключение СтрШаблон("Не удалось удалить слоты конфигурации на сервере. Сервер вернул ошибку: '%1'", Ответ.message);
	КонецЕсли;
	
КонецПроцедуры

Функция ЗарезервиватьСлот(КонтрагентСсылка, РегионСсылка=Неопределено, НазваниеПользователя=Неопределено) Экспорт
	
	ОптимальнаяКонфигурация = ВыбратьОптимальнуюКонфигурацию(РегионСсылка);
	
	Если ОптимальнаяКонфигурация = Неопределено Тогда
		Возврат Неопределено;	
	КонецЕсли;
	
	НаборЗаписей = РегистрыСведений.СлотыКонфигураций.СоздатьНаборЗаписей();  			
	НаборЗаписей.Отбор.Сервер.Установить(ОптимальнаяКонфигурация.Сервер);
	НаборЗаписей.Отбор.ИмяКонфигурации.Установить(ОптимальнаяКонфигурация.ИмяКонфигурации);
	НаборЗаписей.Отбор.Статус.Установить(Перечисления.СтатусСлотаКонфигурации.Свободен);
	НаборЗаписей.Прочитать();
	Запись = НаборЗаписей[0];
	МенеждерЗаписи = РегистрыСведений.СлотыКонфигураций.СоздатьМенеджерЗаписи();
	ЗаполнитьЗначенияСвойств(МенеждерЗаписи, Запись);
	НаборЗаписей.Удалить(Запись);
	МенеждерЗаписи.Статус = Перечисления.СтатусСлотаКонфигурации.Используется;
	МенеждерЗаписи.Пользователь = КонтрагентСсылка;
	МенеждерЗаписи.НазваниеПользователя = НазваниеПользователя;
	МенеждерЗаписи.Записать();
	
	Возврат Новый Структура(
		"ИмяФайла,Файл,Сервер,ИмяКонфигурации,ИдСлота", 
	    ЗаполнитьНазваниеФайлаСлучайныймиЦифрами(Запись.Сервер.РегионСервера.ИдентификаторДляФайла) + ".conf",
		Запись.ФайлКонфигурации,
		Запись.Сервер,
		Запись.ИмяКонфигурации,
		Запись.ИдСлота
	);
	
КонецФункции

Функция ПодключитьКонфигурацию(ИмяКонфигурации, СерверСсылка, ЛимитСлотов) Экспорт
	
	СтатусКонфигурации = WGD_Соединение.ПолучитьДанныеКонфигурации(ИмяКонфигурации, СерверСсылка, Истина);
	
	Если СтатусКонфигурации = Перечисления.СтатусКонфигурации.Ок ИЛИ
			СтатусКонфигурации = Перечисления.СтатусКонфигурации.Выключена Тогда		
			
		Попытка
			ДанныеГенерации = WGD_Соединение.ГенерироватьСлотыКонфигурации(ИмяКонфигурации, СерверСсылка, ЛимитСлотов);
		Исключение
			Возврат Перечисления.СтатусКонфигурации.ОшибкаЗапроса;	
		КонецПопытки;
		
		Если НЕ ДанныеГенерации.status Тогда
			Возврат Перечисления.СтатусКонфигурации.ОшибкаЗапроса;	
		КонецЕсли;
		
		ДанныеСлотов = WGD_Соединение.ПолучитьВсеСлотыКонфигурации(СерверСсылка, ИмяКонфигурации);
		Если Не ДанныеСлотов.status Тогда
			Возврат Перечисления.СтатусКонфигурации.ОшибкаЗапроса;				
		КонецЕсли;
		
		РегистрыСведений.СлотыКонфигураций.ДобавитьСлотыИзОтветаСервера(ДанныеСлотов.data, ДанныеГенерации.data, СерверСсылка, ИмяКонфигурации);
		
	КонецЕсли;
	
	Возврат СтатусКонфигурации;
	
КонецФункции

Функция ВыбратьОптимальнуюКонфигурацию(РегионСсылка=Неопределено)
	
	Серверы = Неопределено;
	
	Если РегионСсылка <> Неопределено Тогда
		
		СерверыВыборка = Справочники.Сервер.Выбрать(,,Новый Структура("РегионСервера", РегионСсылка));

		Серверы = Новый Массив;
		
		Пока СерверыВыборка.Следующий() Цикл
			Серверы.Добавить(СерверыВыборка.Ссылка);	
		КонецЦикла;		
	КонецЕсли;
	
	ДанныеОСерверах = РегистрыСведений.СлотыКонфигураций.ПолучитьИнформациюОКонфигурациях(Серверы);
	
	СтатусыСерверов = Новый Соответствие;
	Для Каждого Стр Из ДанныеОСерверах Цикл
		
		СтатусСервера = СтатусыСерверов.Получить(Стр.Сервер);
		
		Если СтатусСервера = Неопределено Тогда
			Попытка
				СтатусСервера_Массив = WGD_Соединение.ПолучитьСтатусыКонфигурацийСервера(Стр.Сервер);			
			Исключение
				Продолжить;	
			КонецПопытки;
			СтатусСервера = ОбщегоНазначения.ПреобразованиеМассивВТаблицуЗначений(СтатусСервера_Массив.data);
			СтатусыСерверов.Вставить(Стр.Сервер, СтатусСервера);
		КонецЕсли;
		
		ДанныеКонфигурации = СтатусСервера.Найти(Стр.ИмяКонфигурации, "Name");
		
		Если ДанныеКонфигурации.status Тогда
			Возврат Новый Структура("ИмяКонфигурации,Сервер",
				Стр.ИмяКонфигурации, Стр.Сервер
			);
		КонецЕсли;	
		
	КонецЦикла;
	
	Возврат Неопределено;
		
КонецФункции

Функция ЗаполнитьНазваниеФайлаСлучайныймиЦифрами(ИдентификаторДляФайла)
	
	Возврат ИдентификаторДляФайла + "_" + ОбщегоНазначения.ГенерироватьСлучайнуюПоследовательностьБуквЦифр(4, Истина);
	
КонецФункции
