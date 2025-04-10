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
				
	ИначеЕсли СтатусКонфигурации = Перечисления.СтатусКонфигурации.НеПустаяПриДобавлении Тогда
		
		Возврат "Перед добавлением, необходимо очистить конфигурацию";
		
	ИначеЕсли СтатусКонфигурации = Перечисления.СтатусКонфигурации.НеСуществует Тогда
		
		Возврат "Конфигурации с таким именем не существует";
		
	ИначеЕсли СтатусКонфигурации = Перечисления.СтатусКонфигурации.ОшибкаЗапроса Тогда
		
		Возврат "Возникла ошибка при запросе на сервер";
		
	КонецЕсли;
	
КонецФункции

&НаСервере
Процедура ДобавитьКонфигурациюВТаблицу(ИмяКонфигурации, МаксимумСлотов, КоличествоСлотовЗанято, Статус)
	
	
	
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
        Для каждого Идентификатор Из Параметры.ВыделенныеСтроки Цикл
            НайденнаяУдаляемаяСтрока = КонфигурацииСервера.НайтиПоИдентификатору(Идентификатор);
            СтрокиДляУдаления.Добавить(НайденнаяУдаляемаяСтрока);
        КонецЦикла;
        
        Для каждого УдаляемаяСтрока Из СтрокиДляУдаления Цикл
            КонфигурацииСервера.Удалить(УдаляемаяСтрока); 
        КонецЦикла;
    КонецЕсли;
    
КонецПроцедуры

&НаКлиенте
Процедура ОбновитьСтатусыКонфигураций(Команда)
	// TODO
КонецПроцедуры
