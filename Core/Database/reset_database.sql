drop schema if exists university;
CREATE SCHEMA IF NOT EXISTS university DEFAULT CHARACTER SET utf8 ;
USE university ;

create table student (
    discord_id     varchar(255) not null,

    total_msg    int,
    last_msg     int, -- unix timestamp
    counted_msg  int,
    multiplier  double default 1,
    total_xp    double default 0,

    primary key (discord_id)
);

create table instructor (
    name varchar(255) not null,
    title varchar(255),
    email varchar(255),
    phone varchar(255),
    office varchar(255),
    picture varchar(255),

    discord_id varchar(255),

    foreign key (discord_id) references student(discord_id),

    primary key (name)
);

create TABLE department (
    dept_name    varchar(255) not null,
    website     varchar(255) ,
    location    varchar(255) ,
    phone       varchar(255) ,
    fax         varchar(255) ,
    contact     varchar(1023) ,
    chair       varchar(255) ,

    foreign key (chair) references instructor(name),

    PRIMARY KEY (dept_name)
);

create table subject (
    subj    varchar(4),
    name    varchar(255),
    dept_name   varchar(255),

    foreign key (dept_name) references department(dept_name),
    primary key (subj)
);

create table course (
    subj        varchar(4) not null,
    num         int not null,
    credits     int ,
    title       varchar(255) ,

    foreign key (subj) references subject(subj),
    primary key (subj, num)
);


create table term (
    term_id      int         not null,
    semantic    varchar(255) not null,

    primary key (term_id)
);

create table section (
    crn         int not null unique ,
    subj        varchar(255) not null,
    num         int not null,
    sec_num     varchar(10) not null,
    time        varchar(255) ,
    days        varchar(255) ,
    location    varchar(255) ,
    date        varchar(255) ,

    term_id        int,

    cap   int ,
    act   int ,
    rem   int ,

    wl_acting int,

    attribute   varchar(1023),
    rss         varchar(1023),

    foreign key (term_id) references term(term_id),

    primary key (subj, num, sec_num, term_id)
);

create table takes (
    discord_id varchar(255) not null,
    subj varchar(4) not null,
    num int not null,
    sec_num varchar(10) default 1,
    term_id int,

    foreign key (discord_id) references student(discord_id),
    foreign key (subj, num, sec_num, term_id) references section(subj, num, sec_num, term_id)

);

create table taught_by (
    is_primary bool not null,
    instructor varchar(45),
    crn int not null,


    foreign key (instructor) references instructor(name),
    foreign key (crn) references section(crn)
);


create table assignment (
    discord_id varchar(255) not null,
    ass_id int not null auto_increment,

    crn int not null,

    title   varchar(255),
    date_time varchar(255), -- can be unix time stamp so we can use discord formatting
    description varchar(1023),

    foreign key (discord_id) references student(discord_id),
    foreign key (crn) references section(crn),

    primary key (ass_id)
);


create table prerequisites (
    subj    varchar(4) not null,
    num     int not null,

    pre_subj    varchar(4) not null,
    pre_num     int not null,

    foreign key (subj, num) references course(subj, num),
    foreign key (pre_subj, pre_num) references course(subj, num),

    primary key (subj, num)
);

create table corequisites (
    subj    varchar(4) not null,
    num     int not null,

    pre_subj    varchar(4) not null,
    pre_num     int not null,

    foreign key (subj, num) references course(subj, num),
    foreign key (pre_subj, pre_num) references course(subj, num),

    primary key (subj, num)
);

create table ta(
    name varchar(255),
    discord_id varchar(255),

    foreign key (discord_id) references student(discord_id),

    primary key (name)
);

create table ta_for (
    name varchar(255) not null,
    crn int,

    foreign key (name) references ta(name),
    foreign key (crn) references section(crn),

    primary key (crn)
);


create table grader(
    name varchar(255),
    discord_id varchar(255),

    foreign key (discord_id) references student(discord_id),

    primary key (name)
);

create table grader_for (
    name varchar(255) not null,
    crn int,

    foreign key (name) references grader(name),
    foreign key (crn) references section(crn),

    primary key (crn)
);