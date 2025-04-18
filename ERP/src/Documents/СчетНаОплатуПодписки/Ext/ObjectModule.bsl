﻿
Процедура ОбработкаЗаполнения(ДанныеЗаполнения, СтандартнаяОбработка) Экспорт
	//{{__КОНСТРУКТОР_ВВОД_НА_ОСНОВАНИИ
	// Данный фрагмент построен конструктором.
	// При повторном использовании конструктора, внесенные вручную изменения будут утеряны!!!
	Если ТипЗнч(ДанныеЗаполнения) = Тип("ДокументСсылка.Подписка") Тогда
		// Заполнение шапки
		ДатаФормирования = ТекущаяДата();
		КрайнийСрокОплаты = ДатаФормирования + ОбщегоНазначения.НеделиВСекунды(1);
		Контрагент = ДанныеЗаполнения.Клиент;
		Подписка = ДанныеЗаполнения.Ссылка;
		БазоваяСтоимость = ДанныеЗаполнения.БазоваяСтоимость;
		СуммаДокумента = ДанныеЗаполнения.СуммаРегулярногоПлатежа;
		Тариф = ДанныеЗаполнения.Тариф;
	КонецЕсли;
	//}}__КОНСТРУКТОР_ВВОД_НА_ОСНОВАНИИ
КонецПроцедуры

Функция СчетИстек() Экспорт
	
	Возврат КрайнийСрокОплаты < ТекущаяДата();
	
КонецФункции

Процедура ОбработкаПроведения(Отказ, Режим)
	//{{__КОНСТРУКТОР_ДВИЖЕНИЙ_РЕГИСТРОВ
	// Данный фрагмент построен конструктором.
	// При повторном использовании конструктора, внесенные вручную изменения будут утеряны!!!

	// регистр БалансСчетовПользователей Расход
	Движения.БалансСчетовПользователей.Записывать = Истина;
	Движение = Движения.БалансСчетовПользователей.Добавить();
	Движение.ВидДвижения = ВидДвиженияНакопления.Расход;
	Движение.Период = Дата;
	Движение.Контрагент = Контрагент;
	Движение.Сумма = СуммаДокумента;

	//}}__КОНСТРУКТОР_ДВИЖЕНИЙ_РЕГИСТРОВ
КонецПроцедуры
