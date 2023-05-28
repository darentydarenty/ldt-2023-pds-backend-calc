create table result
(
    record_id      integer generated always as identity
        primary key,
    tracker_id     varchar(256)                                    not null
        unique,
    total_expenses integer,
    date_create    timestamp    default now()                      not null,
    report_name    varchar(512) default 'Отчёт'::character varying not null
);

comment on column result.date_create is 'Дата формирования отчёта';

alter table result
    owner to "ds-user";

create table staff
(
    record_id         integer not null
        primary key
        constraint fk_record_id
            references result
        constraint fk_record_id
            references result
            on delete cascade,
    staff_expenses    integer,
    salaries_expenses integer,
    pension_expenses  integer,
    medical_expenses  integer
);

alter table staff
    owner to "ds-user";

create table estate
(
    record_id         integer not null
        primary key
        constraint fk_record_id
            references result
        constraint fk_record_id
            references result
            on delete cascade,
    estate_expenses   integer,
    land_expenses     integer,
    building_expenses integer
);

alter table estate
    owner to "ds-user";

create table taxes
(
    record_id    integer not null
        primary key
        constraint "fk_record_Id"
            references result
        constraint "fk_record_Id"
            references result
            on delete cascade,
    tax_expenses integer,
    land_tax     integer,
    estate_tax   integer,
    income_tax   integer
);

alter table taxes
    owner to "ds-user";

create table services
(
    record_id            integer not null
        primary key
        constraint fk_record_id
            references result
        constraint fk_record_id
            references result
            on delete cascade,
    service_expenses     integer,
    duty_expenses        integer,
    bookkeeping_expenses integer,
    patent_expenses      integer,
    machine_expenses     integer
);

alter table services
    owner to "ds-user";

create table company_short
(
    record_id         integer not null
        primary key
        constraint fk_record_id
            references result
        constraint fk_record_id
            references result
            on delete cascade,
    user_id           integer,
    project_name      varchar(128),
    industry          integer,
    organization_type varchar(4),
    workers_quantity  integer,
    county            integer
);

alter table company_short
    owner to "ds-user";

create table company_full
(
    record_id          integer not null
        primary key
        constraint fk_record_id
            references result
        constraint fk_record_id
            references result
            on delete cascade,
    land_area          integer,
    building_area      integer,
    machine_names      integer[],
    machine_quantities integer[],
    patent_type        integer,
    bookkeeping        boolean,
    tax_system         varchar(8),
    operations         integer,
    other_needs        integer[]
);

alter table company_full
    owner to "ds-user";



create table mean_salaries
(
    industry_id   integer generated always as identity
        primary key,
    industry_name varchar(120) not null
        unique,
    salary        integer      not null
);

comment on table mean_salaries is 'Таблица со средними зарплатами по отрослям';

alter table mean_salaries
    owner to "ds-user";

create table machine_prices
(
    machine_id    integer generated always as identity
        primary key,
    machine_name  varchar(120) not null
        unique,
    machine_price integer      not null
);

comment on table machine_prices is 'Таблица с ценами за оборудование';

alter table machine_prices
    owner to "ds-user";

create table county_prices
(
    county_id    integer generated always as identity
        primary key,
    county_name  varchar(20)    not null
        unique,
    county_price numeric(12, 2) not null
);

comment on table county_prices is 'Таблица с ценами за м2 по округам';

alter table county_prices
    owner to "ds-user";

create table other_needs
(
    need_id    integer generated always as identity
        primary key,
    need_name  varchar(50)   not null
        unique
        constraint other_needs_need_name_key1
            unique,
    need_coeff numeric(6, 4) not null
);

comment on table other_needs is 'Таблица с коэффицентами важности иных потребностей';

alter table other_needs
    owner to "ds-user";

create table patent_prices
(
    patent_id    integer generated always as identity
        primary key,
    patent_name  varchar(600) not null
        unique,
    patent_price integer      not null
);

comment on table patent_prices is 'Таблица с ценами на виды патентов';

alter table patent_prices
    owner to "ds-user";

create table auth
(
    id          serial
        primary key,
    name        varchar(54)  not null
        unique,
    public_key  varchar(256) not null
        unique,
    private_key varchar(512) not null
        unique,
    url         varchar(256)
);

alter table auth
    owner to root;

