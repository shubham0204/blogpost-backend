create table if not exists blogs(
    id varchar(20) PRIMARY KEY,
    author_id varchar(20),
    title varchar(255),
    content text,
    foreign key( author_id ) references users( id )
);