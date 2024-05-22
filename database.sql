-- Item, Location, ItemLocation, category
CREATE TABLE IF NOT EXISTS category(
    id SERIAL PRIMARY KEY,
    label VARCHAR(50) NOT NULL,
    UNIQUE(label)
);

CREATE TABLE IF NOT EXISTS item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category_id INT REFERENCES category(id) ON UPDATE CASCADE,
    UNIQUE(name, category_id)
);

CREATE TABLE IF NOT EXISTS location (
    id SERIAL PRIMARY KEY,
    address VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    room VARCHAR(10),
    UNIQUE(address, city, room)
);

CREATE TABLE IF NOT EXISTS item_location (
    id SERIAL PRIMARY KEY,
    item_id INT REFERENCES item(id) ON UPDATE CASCADE ON DELETE CASCADE,
    location_id INT REFERENCES location(id) ON UPDATE CASCADE,
    quantity INT NOT NULL
);

-- User and Role
CREATE TABLE IF NOT EXISTS users (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS role (
    id SERIAL PRIMARY KEY,
    label VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_role (
    user_id uuid REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    role_id INT REFERENCES role(id) ON UPDATE CASCADE,
    CONSTRAINT user_role_pkey PRIMARY KEY (user_id, role_id)
);

-- Event, EventStatus and Person
CREATE TABLE IF NOT EXISTS event_status (
    id SERIAL PRIMARY KEY,
    label VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS person (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(265) NOT NULL,
    stand_size INT,
    contact_objective INT NOT NULL,
    date_start TIMESTAMP NOT NULL,
    date_end TIMESTAMP NOT NULL,
    status_id INT REFERENCES event_status(id) ON UPDATE CASCADE,
    location_id INT REFERENCES location(id) ON UPDATE CASCADE,
    item_manager uuid REFERENCES person(id) ON UPDATE CASCADE,
    CONSTRAINT check_dates_event CHECK (date_start <= date_end),
    CONSTRAINT check_dates_now CHECK (date(date_start) >= date(NOW())),
    UNIQUE(name, date_start, date_end, location_id)
);

CREATE TABLE IF NOT EXISTS event_status_history (
    id SERIAL PRIMARY KEY,
    set_on TIMESTAMP NOT NULL,
    event_id INT REFERENCES event(id) ON UPDATE CASCADE ON DELETE CASCADE,
    status_id INT REFERENCES event_status(id) ON UPDATE CASCADE,
    set_by uuid REFERENCES users(id) ON UPDATE CASCADE
);

-- Reserved item
CREATE TABLE IF NOT EXISTS reserved_item (
    item_location_id INT REFERENCES item_location(id) ON UPDATE CASCADE,
    event_id INT REFERENCES event(id) ON UPDATE CASCADE,
    quantity INT NOT NULL,
    status BOOLEAN NOT NULL,
    reserved_on TIMESTAMP NOT NULL,
    reserved_by uuid REFERENCES users(id) ON UPDATE CASCADE,
    CONSTRAINT reserved_keys PRIMARY KEY (item_location_id, event_id)
);

-- Alert and emails
CREATE TABLE IF NOT EXISTS alert (
    id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS alert_email (
    email VARCHAR(30) PRIMARY KEY,
    alert_id INT REFERENCES alert(id) ON UPDATE CASCADE ON DELETE CASCADE
);

set timezone='Europe/Paris';

INSERT INTO location (address, city, room) VALUES ('Palais Neptune', 'Toulon', '007');
INSERT INTO location (address, city, room) VALUES ('Parc Chanot', 'Marseille', '013');
INSERT INTO location (address, city, room) VALUES ('ISEN, Place Georges Pompidou', 'Toulon', '456');

INSERT INTO users(email) VALUES ('marc.etavard@isen.yncrea.fr');
INSERT INTO users(email) VALUES ('alex.olivier@isen.yncrea.fr');
INSERT INTO users(email) VALUES ('definir.a@isen.yncrea.fr');
INSERT INTO users(email) VALUES ('corentin.thibaud@isen.yncrea.fr');
INSERT INTO users(email) VALUES ('jaun.gomez-sanchez@isen.yncrea.fr');
INSERT INTO users(email) VALUES ('dorian.bourdier@isen.yncrea.fr');

INSERT INTO person(last_name, first_name) VALUES ('ETAVARD', 'Marc');
INSERT INTO person(last_name, first_name) VALUES ('OLIVIER', 'Alëx');
INSERT INTO person(last_name, first_name) VALUES ('THIBAUD', 'Corentin');
INSERT INTO person(last_name, first_name) VALUES ('SANCHEZ', 'Juan');
INSERT INTO person(last_name, first_name) VALUES ('BOURDIER', 'Dorian');

INSERT INTO event_status(label) VALUES ('A faire');
INSERT INTO event_status(label) VALUES ('Prêt');
INSERT INTO event_status(label) VALUES ('Récupéré');
INSERT INTO event_status(label) VALUES ('En attente de réception');
INSERT INTO event_status(label) VALUES ('Réceptionné');
INSERT INTO event_status(label) VALUES ('Fini');

INSERT INTO event(name, stand_size, contact_objective, date_start, date_end, status_id, item_manager, location_id) 
VALUES('Salon étudiant Studyrama', 100, 50, NOW()::timestamptz(0), NOW()::timestamptz(0), 1,
       (SELECT id FROM person WHERE last_name = 'ETAVARD'),
       (SELECT id FROM location WHERE city = 'Toulon' AND room = '007'));
INSERT INTO event(name, stand_size, contact_objective, date_start, date_end, status_id, item_manager, location_id) 
VALUES('Salon étudiant Studyrama', 150, 75, '2024-6-11', '2024-6-14', 1,
       (SELECT id FROM person WHERE last_name = 'OLIVIER'),
       (SELECT id FROM location WHERE city = 'Marseille'));

INSERT INTO category(label) VALUES ('Brochures');
INSERT INTO category(label) VALUES ('Kakémonos');
INSERT INTO category(label) VALUES ('Lettres');
INSERT INTO category(label) VALUES ('Goodies');
INSERT INTO category(label) VALUES ('Transats');
INSERT INTO category(label) VALUES ('RDD');

INSERT INTO item(name, category_id) VALUES('Brochures Puissance Alpha Générale', (SELECT id FROM category WHERE label = 'Brochures'));
INSERT INTO item(name, category_id) VALUES('Brochures Puissance Alpha Bachelors', (SELECT id FROM category WHERE label = 'Brochures'));
INSERT INTO item(name, category_id) VALUES('Brochures Ecole FISE', (SELECT id FROM category WHERE label = 'Brochures'));
INSERT INTO item(name, category_id) VALUES('Echarpes RDD 2024', (SELECT id FROM category WHERE label = 'RDD'));

INSERT INTO item(name, category_id) VALUES('Vie Etudiante', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('R&D', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('Ecole Entreprises', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('2 campus', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('Ingé/Bachelors', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('Cyber', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('Chiffres clés', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('Dev Jeux Vidéos', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('DNF', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('BIOST', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('CIN', (SELECT id FROM category WHERE label = 'Kakémonos'));
INSERT INTO item(name, category_id) VALUES('MPSI', (SELECT id FROM category WHERE label ='Kakémonos'));

INSERT INTO item_location(item_id, location_id, quantity) VALUES(1, 3, 280);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(1, 2, 100);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(2, 3, 320);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(3, 3, 20);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(4, 3, 100);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(5, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(6, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(7, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(8, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(9, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(10, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(11, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(12, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(13, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(14, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(15, 3, 1);
INSERT INTO item_location(item_id, location_id, quantity) VALUES(16, 3, 1);

