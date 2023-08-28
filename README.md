
## Features

### Security

* Databases use UUIDs as primary keys, instead of consecutive integers to
 avoid incremental access of entities if a table is compromised in an attack.

* All random UUIDs are generated with cryptographically safe 
RNGs i.e. with `os.urandom`.

* Rate limiters are installed to each endpoint to prevent 
brute-force and DDoS attacks.

