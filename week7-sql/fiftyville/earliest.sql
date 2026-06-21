SELECT * FROM flights
WHERE origin_airport_id = 8
AND year = 2025 AND month = 7 AND day = 29
ORDER BY hour, minute
LIMIT 1;
