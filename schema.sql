DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS places;

CREATE TABLE places (
  id      INT          NOT NULL AUTO_INCREMENT,
  city    VARCHAR(100) NOT NULL,
  county  VARCHAR(100) DEFAULT NULL,
  country VARCHAR(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_city_county_country (city, county, country)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE people (
  id              INT          NOT NULL AUTO_INCREMENT,
  given_name      VARCHAR(100) NOT NULL,
  family_name     VARCHAR(100) NOT NULL,
  date_of_birth   DATE         DEFAULT NULL,
  place_of_birth  INT          DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (place_of_birth) REFERENCES places (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
