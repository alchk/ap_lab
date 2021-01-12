create table if not exists users(
    id serial PRIMARY KEY,
    first_name varchar(50),
    last_name varchar(50),
    password varchar(50),
    user_name varchar(50)
);

create table if not exists wallets(
    id serial PRIMARY KEY,
    balance bigint,
    owner_id bigint,
    is_default boolean,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

create table if not exists transactions(
    id serial PRIMARY KEY,
    sender_id bigint,
    receiver_id bigint,
    amount bigint, --in cents
    time_stamp timestamp,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);