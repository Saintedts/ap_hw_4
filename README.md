## Функционал: 

0. '/': Выводим листинг валюты.
1. '/get_currencies': Получать курс основных валют к рублю (доллары, евро, юани, шекели) кешируется на 5 минут. 
2. '/get_currencie/{coin}': Получать одну валюту к рублю из списка (берется из кешируемого списка выше).
3. '/get_total_rub/{coin}/{total}': Переводить сумму валюты в рубли (берется из кешируемого списка выше). 
4. '/get_total_coin/{coin}/{total}': Переводить сумму рубли в сумму валюты (берется из кешируемого списка выше). 
5. '/status': Выводит дату и точное время. 

* to run redis: redis-server
* to run fastapi: uvicorn main:app --reload
* to run docker-compose: docker-compose up --build
