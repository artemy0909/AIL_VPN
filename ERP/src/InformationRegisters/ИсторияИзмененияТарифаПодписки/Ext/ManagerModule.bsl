﻿Процедура ОбновитьДанные(Подписка, Тариф, БазоваяСтоимость, СуммаРегулярногоПлатежа) Экспорт
	
	МенеджерЗаписи = СоздатьМенеджерЗаписи();
	
	МенеджерЗаписи.Период = ТекущаяДата();
	МенеджерЗаписи.Подписка = Подписка;
	МенеджерЗаписи.Тариф = Тариф;
	МенеджерЗаписи.БазоваяСтоимость = БазоваяСтоимость;
	МенеджерЗаписи.СуммаРегулярногоПлатежа = СуммаРегулярногоПлатежа;
	
	МенеджерЗаписи.Записать();
	
КонецПроцедуры
