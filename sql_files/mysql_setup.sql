CREATE TABLE if not exists Congress(
    congress_id INT,
    start_date DATE,
    end_date DATE,
    URL varchar(255),
    PRIMARY KEY (congress_id)
);

CREATE TABLE if not exists Person(
    person_id INT AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    sex ENUM("male", "female"),
    birth_date DATE,
    death_date DATE,
    age_at_death INT,
    URL varchar(255) NOT NULL,
    PRIMARY KEY (person_id),
    UNIQUE (URL)
);

CREATE TABLE if not exists State(
    state_id INT AUTO_INCREMENT,
    state_name varchar(255) NOT NULL,
    PRIMARY KEY (state_id)
);

CREATE TABLE if not exists Chamber(
    chamber_id INT AUTO_INCREMENT,
    seat_type ENUM('Senator', 'Representative'),
    PRIMARY KEY (chamber_id)
);

CREATE TABLE if not exists Party(
    party_id INT AUTO_INCREMENT,
    party_name varchar(255) NOT NULL,
    URL varchar(255) NOT NULL,
    PRIMARY KEY (party_id)
);

CREATE TABLE if not exists Congressperson(
    congress_id INT,
    person_id INT,
    state_id INT,
    chamber_id INT,
    party_id INT,
    age_at_congress INT,
    PRIMARY KEY (congress_id, person_id),
    Foreign Key (congress_id) REFERENCES Congress(congress_id) ON DELETE CASCADE,
    Foreign Key (person_id) REFERENCES Person(person_id) ON DELETE CASCADE,
    Foreign Key (state_id) REFERENCES State(state_id) ON DELETE CASCADE,
    Foreign Key (chamber_id) REFERENCES Chamber(chamber_id) ON DELETE CASCADE,
    Foreign Key (party_id) REFERENCES Party(party_id) ON DELETE CASCADE
);