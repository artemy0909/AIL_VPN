﻿&НаКлиенте
Процедура ГенерироватьПромокоды(Команда)
	ГенерироватьПромокодыНаСервере();
КонецПроцедуры

&НаСервере
Процедура ГенерироватьПромокодыНаСервере()
	Для Кол = 0 По КоличествоПромокодов Цикл
		НовыйСтр = Объект.Промокоды.Добавить();
		НовыйСтр.Промокод = ОбщегоНазначения.ГенерироватьСлучайнуюПоследовательностьБуквЦифр(32, Истина);
		НовыйСтр.ДействуетОт = ТекущаяДата();
		НовыйСтр.ДействуетДо = ?(НЕ ОбщегоНазначения.ДатаЗаполнена(ДействуютДо),
			ОбщегоНазначения.ДатаОкончанияВремен(), ДействуютДо);
	КонецЦикла;
КонецПроцедуры

