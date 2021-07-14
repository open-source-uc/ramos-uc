Run in server:
`pg_dump -U db_user -Fc db_name > /srv/ramosuc/database/YY-MM-DD.dump`

SCP from local:
`scp user@host:/srv/ramosuc/database/YY-MM-DD.dump .`

Load backup to DB:
```
scp YY-MM-DD.dump user@host:/srv/ramosuc/database/
pg_restore -U django -d ramosuc -c -v YY-MM-DD.dump
```
