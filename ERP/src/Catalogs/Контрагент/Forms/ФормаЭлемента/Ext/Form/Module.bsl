﻿
&НаКлиенте
АСИНХ Процедура СекретныйКлючОткрытие(Элемент, СтандартнаяОбработка)
	РезультатВыполнения = Ждать СредстваБуфераОбмена.ПоместитьДанныеАсинх(Новый ЭлементБуфераОбмена(СтандартныйФорматДанныхБуфераОбмена.Текст, Элемент.ТекстРедактирования));
	Если РезультатВыполнения Тогда
		Сообщить("Секретный ключ сохранен в буфер обмена");	
	Иначе
		Сообщить("Ошибка копирования");	
	КонецЕсли;
КонецПроцедуры
