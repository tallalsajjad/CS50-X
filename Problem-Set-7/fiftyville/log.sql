-- Keep a log of any SQL queries you execute as you solve the mystery.
--Get a liscense plate.
SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND year = 2024
AND hour = 10 AND (minute >= 15 AND minute<= 25);
--Check interviews
SELECT transcript,name FROM interviews WHERE year = 2024 AND day = 28 AND MONTH = 7;
--Check atm_bank and acccount number
SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND year = 2024
AND atm_location = 'Leggett Street';
--Get a person id.
SELECT person_id FROM bank_accounts WHERE account_number IN (
  SELECT account_number FROM atm_transactions
  WHERE month = 7 AND day = 28 AND year = 2024
  AND atm_location = 'Leggett Street'
  AND amount < 48 AND transaction_type = 'withdraw');
--Get a passport number of those people
SELECT passport_number,name
FROM people
WHERE license_plate IN (
  SELECT license_plate
  FROM bakery_security_logs
  WHERE month = 7 AND day = 28 AND year = 2024
    AND hour = 10 AND minute BETWEEN 15 AND 25
)
AND id IN (
  SELECT person_id
  FROM bank_accounts
  WHERE account_number IN (
    SELECT account_number
    FROM atm_transactions
    WHERE month = 7 AND day = 28 AND year = 2024
      AND transaction_type = 'withdraw'
      AND atm_location = 'Leggett Street'
  )
)
AND phone_number IN (
    SELECT caller
    FROM phone_calls WHERE month = 7 AND day = 28 AND year = 2024 AND duration < 60
);
--Get a city name
SELECT * FROM flights
WHERE origin_airport_id = (
SELECT id FROM airports WHERE city = 'Fiftyville'
)
AND year = 2021 AND month = 7 AND day = 29
--Check airport identity
SELECT * FROM airports;
--Check name according to license plate
SELECT passport_number FROM bank_accounts JOIN people ON bank_accounts.person_id = people.id
WHERE people.license_plate IN (
  SELECT license_plate FROM bakery_security_logs
  WHERE month = 7 AND day = 28 AND year = 2024
  AND hour = 10 AND (minute >= 15 AND minute<= 25));
--Check name of culprit
SELECT name FROM people JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passengers.flight_id = 36 AND people.name IN ('Bruce','Diana');
--Get a accomplice name
SELECT phone_calls.*, people.name FROM phone_calls JOIN people ON phone_calls.receiver = people.phone_number
WHERE month = 7 AND day = 28 AND year = 2024 AND duration < 60 AND phone_calls.caller = '(367) 555-5533';
