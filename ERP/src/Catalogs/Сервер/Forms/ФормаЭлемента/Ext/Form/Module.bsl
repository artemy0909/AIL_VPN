﻿
&НаКлиенте
Процедура ДобавитьНовуюКонфигурацию(Команда)
	
	ОтобразитьПредупреждение = ДобавитьНовуюКонфигурациюНаСервере();
	
	Если ОтобразитьПредупреждение <> Неопределено Тогда
		
		ПредупреждениеАсинх(ОтобразитьПредупреждение,,"Не удалось добавить конфигурацию");
		
	КонецЕсли;
	
КонецПроцедуры

&НаСервере
Функция ДобавитьНовуюКонфигурациюНаСервере()	
	
	КонфигурацияУжеЕсть = ?(
		КонфигурацииСервера.НайтиСтроки(Новый Структура("ИмяКонфигурации", ИмяНовойКонфигурации)).Количество() <> 0,
		Истина, Ложь
	);
	
	Если КонфигурацияУжеЕсть Тогда
			
		Возврат "Конфигурация с таким именем уже есть";
		
	КонецЕсли;

	СтатусКонфигурации = WGD_Соединение.ПолучитьСтатусКонфигурации(ИмяНовойКонфигурации, Объект.Ссылка, Истина);
	Если СтатусКонфигурации = Перечисления.СтатусКонфигурации.Ок ИЛИ
			СтатусКонфигурации = Перечисления.СтатусКонфигурации.Выключена Тогда
			
		ДобавитьКонфигурациюВТаблицу(ИмяНовойКонфигурации, ЛимитСлотовНовойКонфигурации, 0, СтатусКонфигурации);
		//РегистрыСведений.КонфигурацииСервера.ДобавитьНовуюКонфигурацию(Объект.Ссылка, ИмяНовойКонфигурации, ЛимитСлотовНовойКонфигурации);
		// TODO Проверить все тут
	ИначеЕсли СтатусКонфигурации = Перечисления.СтатусКонфигурации.НеПустаяПриДобавлении Тогда
		
		Возврат "Перед добавлением, необходимо очистить конфигурацию";
		
	ИначеЕсли СтатусКонфигурации = Перечисления.СтатусКонфигурации.НеСуществует Тогда
		
		Возврат "Конфигурации с таким именем не существует";
		
	ИначеЕсли СтатусКонфигурации = Перечисления.СтатусКонфигурации.ОшибкаЗапроса Тогда
		
		Возврат "Возникла ошибка при запросе на сервер";
		
	КонецЕсли;
	
КонецФункции

&НаСервере
Процедура ДобавитьКонфигурациюВТаблицу(ИмяКонфигурации, МаксимумСлотов, СлотовЗанято, Статус)
	
	НоваяСтр = КонфигурацииСервера.Добавить();
	НоваяСтр.ИмяКонфигурации = ИмяКонфигурации;
	НоваяСтр.Слоты = СтрШаблон("%1 из %2", СлотовЗанято, МаксимумСлотов);
	НоваяСтр.Статус = Статус;
	
КонецПроцедуры

&НаКлиенте
Процедура КонфигурацииСервераПередУдалением(Элемент, Отказ)
	    
    Отказ = Истина;
    ПараметрыОповещения = Новый Структура("ВыделенныеСтроки", Элемент.ВыделенныеСтроки);
    ОповещениеПриОтветеНаВопрос = Новый ОписаниеОповещения(
		"РезультатОтветаНаВопросОбУдаленииКонфигурацииСервера", ЭтаФорма, ПараметрыОповещения);
	ПоказатьВопрос(
		ОповещениеПриОтветеНаВопрос,
		"Вы уверены? Удаление конфигурации может привести к нежелательным последствиям", // TODO изменение текста в зависимости от того есть подписчики на конфигурации, или нет
		РежимДиалогаВопрос.ДаНет,,,"Подтверждение удаления");
    
КонецПроцедуры

&НаКлиенте
Процедура РезультатОтветаНаВопросОбУдаленииКонфигурацииСервера(Результат, Параметры) Экспорт
    
    Если Результат = КодВозвратаДиалога.Да Тогда
		
		СтрокиДляУдаления = Новый Массив;
        Для Каждого Идентификатор Из Параметры.ВыделенныеСтроки Цикл
            НайденнаяУдаляемаяСтрока = КонфигурацииСервера.НайтиПоИдентификатору(Идентификатор);
            СтрокиДляУдаления.Добавить(НайденнаяУдаляемаяСтрока);
        КонецЦикла;
        
		Для Каждого УдаляемаяСтрока Из СтрокиДляУдаления Цикл
			СерверыVPN_ВызовСервера.УдалитьКонфигурацию(Объект.Ссылка, УдаляемаяСтрока.ИмяКонфигурации);
            КонфигурацииСервера.Удалить(УдаляемаяСтрока);
		КонецЦикла;
		
    КонецЕсли;
    
КонецПроцедуры

&НаКлиенте
Процедура ОбновитьСтатусыКонфигураций(Команда)
	КонфигурацииСервера.Очистить();
    ЗаполнитьТаблицуКонфигураций();
КонецПроцедуры

&НаСервере
Процедура ПриСозданииНаСервере(Отказ, СтандартнаяОбработка)
	
	Если Не Объект.Ссылка.Пустая() Тогда
		
    	ЗаполнитьТаблицуКонфигураций();
		
	КонецЕсли;
	
КонецПроцедуры

&НаСервере
Процедура ЗаполнитьТаблицуКонфигураций()
	
	Конфигурации = РегистрыСведений.КонфигурацииСервера.ВсеКонфигурацииСервера(Объект.Ссылка);
	
	Для Каждого Стр Из Конфигурации Цикл
		
		СлотовЗанято = РегистрыСведений.СлотыКонфигураций.КоличествоСлотовЗанято(Объект.Ссылка, Стр.ИмяКонфигурации);
		Статус = WGD_Соединение.ПолучитьСтатусКонфигурации(Стр.ИмяКонфигурации, Объект.Ссылка);
		
		ДобавитьКонфигурациюВТаблицу(Стр.ИмяКонфигурации, Стр.МаксимумСлотов, СлотовЗанято, Статус);	
		
	КонецЦикла;
	
КонецПроцедуры
