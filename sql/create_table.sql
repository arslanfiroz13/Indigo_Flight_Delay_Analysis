-- 1️⃣ Database create karo
CREATE DATABASE IF NOT EXISTS indigo_flight_analysis;

-- 2️⃣ Database use karo
USE indigo_flight_analysis;

-- 3️⃣ Table create karo
CREATE TABLE IF NOT EXISTS indigo_flights (
    flight_id INT,
    airline VARCHAR(50),
    origin VARCHAR(50),
    destination VARCHAR(50),
    departure_delay INT,
    arrival_delay INT,
    distance INT,
    date DATE
);