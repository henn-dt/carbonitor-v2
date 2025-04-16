-- Grant privileges for all hosts
ALTER USER 'myuser'@'%' IDENTIFIED WITH mysql_native_password BY 'mypassword';
GRANT ALL PRIVILEGES ON carbonitor_db.* TO 'myuser'@'%';
FLUSH PRIVILEGES;