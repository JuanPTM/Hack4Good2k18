CREATE TABLE User (
  user_id  INT     NOT NULL AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  pass     VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE Device
(
    device_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    user_id INT,
    CONSTRAINT Device_User_user_id_fk FOREIGN KEY (user_id) REFERENCES User (user_id)
);
