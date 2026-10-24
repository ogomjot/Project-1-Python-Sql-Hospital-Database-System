
CREATE DATABASE IF NOT EXISTS hospital;
USE hospital;
 
CREATE TABLE IF NOT EXISTS HOSPITAL (
    patient_id          INT           PRIMARY KEY,
    patient_name        VARCHAR(40)   NOT NULL,
    age                 INT           NOT NULL,
    contact_number      BIGINT        NOT NULL,
    diagnosis           VARCHAR(50)   NOT NULL,
    doctor_treating     VARCHAR(50)   NOT NULL,
    department          VARCHAR(50)   NOT NULL,
    date_of_admission   DATE          NOT NULL,
    date_of_discharging DATE          NOT NULL,
    fees                DECIMAL(10,2) NOT NULL,
    payment_status      VARCHAR(20)   NOT NULL
);
 
