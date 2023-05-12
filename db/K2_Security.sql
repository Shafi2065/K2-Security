USE K2_Security;

CREATE TABLE User (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255),
    is_manager BOOLEAN NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Shift (
    id INT NOT NULL AUTO_INCREMENT,
    start_time DATETIME,
    end_time DATETIME,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Schedule (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    shift_id INT NOT NULL,
    start_time DATETIME,
    end_time DATETIME,
    PRIMARY KEY (id),
    KEY user_id (user_id),
    KEY shift_id (shift_id),
    CONSTRAINT schedule_ibfk_1 FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT schedule_ibfk_2 FOREIGN KEY (shift_id) REFERENCES Shift (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Salary (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    date DATE,
    salary DECIMAL(10,2),
    hours_worked DECIMAL(10,2),
    paid DECIMAL(10,2),
    PRIMARY KEY (id),
    KEY user_id (user_id),
    CONSTRAINT salary_ibfk_1 FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE TimeOffRequest (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    reason TEXT,
    PRIMARY KEY (id),
    KEY user_id (user_id),
    CONSTRAINT time_off_ibfk_1 FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
