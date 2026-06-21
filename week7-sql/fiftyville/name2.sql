SELECT people.name, people.phone_number, people.license_plate, bank_accounts.account_number
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE people.license_plate IN ('5P2BI95','94KL13X','6P58WS2','4328GD8','G412CB7','L93JTIZ','322W7JE','0NTHK55')
AND bank_accounts.account_number IN (28500762,28296815,76054385,49610011,16153065,25506511,81061156,26013199)
AND people.phone_number IN ('(130) 555-0289','(499) 555-9472','(367) 555-5533','(286) 555-6063','(770) 555-1861','(031) 555-6622','(826) 555-1652','(338) 555-6650');
