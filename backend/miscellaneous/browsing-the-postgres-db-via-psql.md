# Browsing the Postgres DB via psql

`psql` is a cli tool to interact with a posgres db.

### Installation (debian)

```bash
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt-get install postgresql-client-16
```

{% embed url="https://www.postgresql.org/download/linux/debian" %}

### Connecting to the db

```bash
psql -p 5332 -h localhost demos demosuser

# psql -p <db_port> -h <db_host> <db_name> <db_user>
```

Enter the `demosuser` password as `demospassword` and hit enter.

{% hint style="info" %}
credentials are defined at: `postgres/docker-compose.yml in the node repo.`
{% endhint %}

You can now list available tables using `\dt` to get started.

```
demos-# \dt
               List of relations
 Schema |       Name        | Type  |   Owner   
--------+-------------------+-------+-----------
 public | blocks            | table | demosuser
 public | consensus         | table | demosuser
 public | mempool           | table | demosuser
 public | pgp_key_server    | table | demosuser
 public | status_hashes     | table | demosuser
 public | status_native     | table | demosuser
 public | status_properties | table | demosuser
 public | transactions      | table | demosuser
 public | validators        | table | demosuser
(9 rows)
```

Have fun!
