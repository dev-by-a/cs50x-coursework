-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports
WHERE year = 2025 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Read the interview transcripts from witnesses on the day of the theft
SELECT name, transcript FROM interviews
WHERE year = 2025 AND month = 7 AND day = 28;

-- Ruth saw theif leave in a car within 10 min of theft; check bakery scurity logs for cars leaving
SELECT * FROM bakery_security_logs
WHERE year = 2025 AND month = 7 AND day = 28
AND hour = 10 AND minute >= 15 AND minute <=25;

-- Eugene saw theif at ATM on Leggett Street withdrawing money that morning
SELECT * FROM atm_transactions
WHERE year = 2025 AND month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

-- Raymond heard thief make a call under 1 minute before leaving the bakery
SELECT * FROM phone_calls
WHERE year = 2025 AND month = 7 AND day = 28
AND duration < 60;

-- Cross-reference license plate, ATM withdrawal, and phone call to find common suspect
SELECT people.name, people.phone_number, people.license_plate, bank_accounts.account_number
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE people.license_plate IN ('5P2BI95','94KL13X','6P58WS2','4328GD8','G412CB7','L93JTIZ','322W7JE','0NTHK55')
AND bank_accounts.account_number IN (28500762,28296815,76054385,49610811,16153065,25506511,81061156,26013199)
AND people.phone_number IN ('(130) 555-0289','(499) 555-9472','(367) 555-5533','(286) 555-6063','(770) 555-1861','(031) 555-6622','(826) 555-1652','(338) 555-6650');

-- Find Diana's passport number
SELECT passport_number FROM people WHERE name = 'Diana';

-- Find Diana's flight using her passport number
SELECT flight_id FROM passengers
WHERE passport_number = (SELECT passport_number FROM people WHERE name = 'Diana');

SELECT * FROM flights
WHERE id IN (18, 24, 54)
AND year = 2025 AND month = 7 AND day = 29;

SELECT * FROM airports WHERE id IN (8, 6);

SELECT name FROM people WHERE phone_number = '(725) 555-3243';

