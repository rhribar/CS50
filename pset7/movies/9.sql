/*

ONLY RETURNs 17965 WITH THIS SOLUTION
SELECT count(DISTINCT(name)) FROM stars
JOIN movies ON stars.movie_id = movies.id
JOIN people ON stars.person_id = people.id
WHERE movies.year = 2004
ORDER BY people.birth; */

SELECT name FROM people
WHERE id IN (
    SELECT person_id FROM stars
        WHERE movie_id IN (
            SELECT id FROM movies
            WHERE year = 2004))
            ORDER BY birth;