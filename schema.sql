drop table if exists pair;
create table pair (
  id integer primary key autoincrement,
  'story_type' text not null,
  'story_number' text not null,
  'story_description' text not null,
  'story_title' text not null,
  'user' text not null,
  'story_day' integer not null
);