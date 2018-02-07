-- Simple users so I can test.
CREATE USER 'super'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'super'@'localhost';
FLUSH PRIVILEGES;
