-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE street = 'Humphrey Street' AND year = 2024 AND month = 7 AND day = 28; -- get description of event

SELECT name,transcript FROM interviews WHERE year = 2024 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%'; -- get relevant transcripts and witnesses

SELECT license_plate FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 and minute < 25; -- find list of carplate number

SELECT account_number, transaction_type, amount FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 and atm_location = 'Leggett Street'; -- find list of acconut id

SELECT caller, receiver, duration FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60; -- find list of phone numbers of both caller and receiver

SELECT name, id FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 and minute < 25); -- find list of people by matching license plate and phone number

SELECT person_id FROM bank_accounts WHERE person_id in (SELECT id FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 and minute < 25))
AND account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 and atm_location = 'Leggett Street'); -- filter names even further through atm transaction

SELECT name FROM people WHERE id = (SELECT person_id FROM bank_accounts WHERE person_id in (SELECT id FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 and minute < 25))

AND account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 and atm_location = 'Leggett Street')); -- obtain thief's name

SELECT receiver FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE name = 'Bruce') and year = 2024 AND month = 7 AND day = 28 AND duration < 60; -- find accomplice phone number

SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE name = 'Bruce') and year = 2024 AND month = 7 AND day = 28 AND duration < 60); -- get accomplice name

SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE
origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
AND year = 2024 AND month = 7 AND day = 29 ORDER BY hour LIMIT 1); -- find destination of earliest flight the next day
