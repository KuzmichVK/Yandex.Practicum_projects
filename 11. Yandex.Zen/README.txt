������� ��� ������.����

�� �������� �������� �� �������:
- C������ �������������� ������������� � ���������� ���������� � ������� � ��������� �� ����� ��������?
- ��� ����� �������� ���������� ��������� � ������� ������?
- ��������� ������ ������������ �������������� �� ������� �������� � ��������� ������?

���������
Ubuntu(Linux):
sudo apt update - ������� ��
sudo apt install postgres - ��������� postgres 
sudo apt install postgresql postgresql-contrib - ��������� postgresql 
sudo service postgresql start - �������� postgresql 
sudo apt install python3-pip - ��������� python3
pip3 install dash==1.4.1 - ��������� dash
sudo apt-get install sqlite3 libsqlite3-dev - ��������� sqlite3 
sudo apt install python3-pandas - ��������� ���������� pandas 
sudo apt install python3-sqlalchemy - ��������� ���������� sqlalchemy
sudo apt-get install python3-psycopg2 - ��������� ���������� psycopg2

������ �������������:
- ��������� ������������ ������ ��� ����� �������������.
- ��������� ������������ ������ ��� ����� ����������.
- ������� �����, ������� ���������� ������� �� �������.

���������:
- ��� ������� � ��:
	��� - automation-test
	login - test_admin
	��������� ip - 84.201.169.81
	parol - test_admin
	user - my_user
	password - my_user_password
- ��� �������� �������� � ������� ����:
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

- ��� ������� ���������:
	python3 zen_pipeline.py --start_dt='2019-09-24 18:00:00' --end_dt='2019-09-24 19:00:00'

- ��� ����������� ������� ���������:
	15 3 * * * python3 -u -W ignore /home/test_admin/zen_pipeline.py --start_dt='2019-09-24 18:00:00' --end_dt='2019-09-24 19:00:00' 2>&1