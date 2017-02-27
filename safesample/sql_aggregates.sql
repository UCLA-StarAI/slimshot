-- from Oblivious Bounds on the Probability of Boolean Functions 2014, Gatterbauer and Suciu
create or replace function ior_sfunc (double precision, double precision) returns double precision as
'select max(val) from (
VALUES($1 * (1.0 - $2)),
(0.00001))
AS Vals(val)'
language SQL;

create or replace function ior_finalfunc (double precision) returns double precision as
'select 1.0 - $1'
language SQL;

drop aggregate if exists ior (double precision);
create aggregate ior (double precision) (
sfunc = ior_sfunc,
stype = double precision,
finalfunc = ior_finalfunc,
initcond = '1.0');

create or replace function l_ior_sfunc (double precision, double precision) returns double precision as
'select $1 + $2'
language SQL;

drop aggregate if exists l_ior (double precision);
create aggregate l_ior (double precision) (
  sfunc = l_ior_sfunc,
  stype = double precision,
  initcond = '0.0');

create or replace function l1prod (double precision, double precision) returns double precision as
'select m + ln(exp($1-m) + exp($2-m) - exp($1+$2-m)) from(
select max(val) as m from (
 VALUES($1),
       ($2))
       AS Vals(val)) as foo'
language SQL;

create or replace function l1diff (double precision, double precision) returns double precision as
'select ln(1 - exp($2) + exp($1))'
language SQL;

create or replace function l1sum (double precision, double precision) returns double precision as
'select ln(exp($1) + exp($2) - 1)'
language SQL;
