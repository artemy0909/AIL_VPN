﻿
Процедура ОбработкаПроведения(Отказ, Режим)
	//{{__КОНСТРУКТОР_ДВИЖЕНИЙ_РЕГИСТРОВ
	// Данный фрагмент построен конструктором.
	// При повторном использовании конструктора, внесенные вручную изменения будут утеряны!!!

	// регистр ПромокодыПериодДействия
	Движения.ПромокодыПериодДействия.Записывать = Истина;
	Для Каждого ТекСтрокаПромокоды Из Промокоды Цикл
		Движение = Движения.ПромокодыПериодДействия.Добавить();
		Движение.Промокод = ТекСтрокаПромокоды.Промокод;
		Движение.ПрайсЛист = Неопределено;
		Движение.ДатаНачала = ТекСтрокаПромокоды.ДействуетОт;
		Движение.ДатаОкончания = ТекСтрокаПромокоды.ДействуетДо;
		Движение.ИспользуетсяОдинРаз = Истина;
	КонецЦикла;

	//}}__КОНСТРУКТОР_ДВИЖЕНИЙ_РЕГИСТРОВ
КонецПроцедуры
