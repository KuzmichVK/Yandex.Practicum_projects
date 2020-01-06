Дашборд для Яндекс.Дзен

Он помогает ответить на вопросы:
- Cколько взаимодействий пользователей с карточками происходит в системе с разбивкой по темам карточек?
- Как много карточек генерируют источники с разными темами?
- Насколько хорошо пользователи конвертируются из показов карточек в просмотры статей?

Установка
Ubuntu(Linux):
sudo apt update - обновил ОС
sudo apt install postgres - установил postgres 
sudo apt install postgresql postgresql-contrib - установил postgresql 
sudo service postgresql start - запустил postgresql 
sudo apt install python3-pip - установил python3
pip3 install dash==1.4.1 - установил dash
sudo apt-get install sqlite3 libsqlite3-dev - установил sqlite3 
sudo apt install python3-pandas - установил библиотеку pandas 
sudo apt install python3-sqlalchemy - установил библиотеку sqlalchemy
sudo apt-get install python3-psycopg2 - установил библиотеку psycopg2

Пример использования:
- Сравнение популярности разных тем среди пользователей.
- Сравнение популярности разных тем среди источников.
- Подсчет людей, которые просмотрят контент по воронке.

Настройка:
- Для доступа к БД:
	имя - automation-test
	login - test_admin
	публичный ip - 84.201.169.81
	parol - test_admin
	user - my_user
	password - my_user_password
- Для создания табличек и раздача прав:
	CREATE TABLE dash_engagement(record_id serial PRIMARY KEY, 
	                             dt TIMESTAMP, 
        	                     item_topic VARCHAR(128), 
                	             event VARCHAR(128), 
                        	     age_segment VARCHAR(128),
			             unique_users BIGINT);
	GRANT ALL PRIVILEGES ON TABLE dash_engagement TO my_user;
	GRANT USAGE, SELECT ON SEQUENCE dash_engagement_record_id_seq TO my_user;

	CREATE TABLE dash_visits(record_id serial PRIMARY KEY, 
        	                 item_topic VARCHAR(128), 
                	         source_topic VARCHAR(128), 
                        	 age_segment VARCHAR(128),
                                 dt TIMESTAMP, 
			         visits INT);
	GRANT ALL PRIVILEGES ON TABLE dash_visits TO my_user;
	GRANT USAGE, SELECT ON SEQUENCE dash_visits_record_id_seq TO my_user;

- Для запуска пайплайна:
	python3 zen_pipeline.py --start_dt='2019-09-24 18:00:00' --end_dt='2019-09-24 19:00:00'

- Для регулярного запуска пайплайна:
	15 3 * * * python3 -u -W ignore /home/test_admin/zen_pipeline.py --start_dt='2019-09-24 18:00:00' --end_dt='2019-09-24 19:00:00' 2>&1
