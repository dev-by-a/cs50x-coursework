SELECT people.name, people.passport_number
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passengers.flight_id = 36;

SELECT city FROM airports WHERE id = 4;
