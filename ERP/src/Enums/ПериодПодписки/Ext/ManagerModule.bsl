﻿Функция РасчитатьКонецПериода(ДатаНачала, ПериодПодписки) Экспорт
	
	Если ПериодПодписки = Месяц Тогда
		
		ДнейВСледующемМесяце = ОбщегоНазначения.ДнейВМесяце(ДатаНачала);
		
		Если День(ДатаНачала) > ДнейВСледующемМесяце Тогда
			
			ДеньОкончания = ДнейВСледующемМесяце;
			
		Иначе
			
			ДеньОкончания = День(ДатаНачала);
			
		КонецЕсли;
		
		Если Месяц(ДатаНачала) <> 12 Тогда
			
			МесяцОкончания = Месяц(ДатаНачала) + 1;
			ГодОкончания = Год(ДатаНачала);
			
		Иначе
			
			МесяцОкончания = 1;
			ГодОкончания = Год(ДатаНачала) + 1;
			
		КонецЕсли;
		
		
		ДатаОкончания = Дата(
			ГодОкончания, МесяцОкончания, ДеньОкончания,
			Час(ДатаНачала), Минута(ДатаНачала), Секунда(ДатаНачала));
		
	ИначеЕсли ПериодПодписки = Год Тогда
		
		ДатаОкончания = ДатаНачала + ОбщегоНазначения.ДниВСекунды(365);
		
	Иначе
		
		ВызватьИсключение "Период подписки не настроен";
		
	КонецЕсли;
	
	Возврат ДатаОкончания;
	
КонецФункции