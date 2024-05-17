--set the output format of the result set to TSV (Tab-Separated Values) to compare the query results obtained, with the autograder.
!outputformat tsv
drop view if exists "powers";
CREATE VIEW "powers" (ROWKEY VARCHAR PRIMARY KEY, "professional"."name" VARCHAR, "personal"."power" VARCHAR,
    "personal"."hero" VARCHAR, "professional"."xp" VARCHAR) ;

SELECT h1."name" AS "Name1", h2."name" AS "Name2", h1."power" AS "Power"
FROM "powers" AS h1, "powers" AS h2
WHERE h1."power" = h2."power"
and h1."hero" = 'yes'
and h2."hero" = 'yes';
--and h1."name" <= h2."name";
