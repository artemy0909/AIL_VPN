﻿Функция НайтиАктивную(Контрагент) Экспорт
	
	Запрос = Новый Запрос;
	Запрос.Текст = 
		"ВЫБРАТЬ ПЕРВЫЕ 1
		|	Подписка.Ссылка КАК Ссылка
		|ИЗ
		|	Документ.Подписка КАК Подписка
		|ГДЕ
		|	Подписка.Статус = ЗНАЧЕНИЕ(Перечисление.СтатусПодписки.Активна)";
	
	РезультатЗапроса = Запрос.Выполнить();
	ВыборкаДетальныеЗаписи = РезультатЗапроса.Выбрать();
	ВыборкаДетальныеЗаписи.Следующий();
	Возврат ВыборкаДетальныеЗаписи.Ссылка;
	
КонецФункции