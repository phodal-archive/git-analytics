drop table if exists pair;
create table pair (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);