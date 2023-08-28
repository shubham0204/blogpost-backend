- Added JWT auth to all blogs CRUD operations
- Changed schema for `Blog` to include `author_id`
- Modified queries in `blogs.py` for updated schema
- Added `auth` package with `jwt` script to generate and 
validate JWTs.
- Updated `utils.py` to execute SQL scripts in a given 
sequence only (to avoid foreign key errors)