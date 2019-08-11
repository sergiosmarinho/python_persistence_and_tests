CREATE TABLE person(
    id integer NOT NULL,
    name character varying,
    date_of_birth timestamp without time zone,
    address character varying
);

ALTER TABLE person OWNER TO postgres;

CREATE SEQUENCE person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE person_id_seq OWNER TO postgres;

ALTER SEQUENCE person_id_seq OWNED BY person.id;

ALTER TABLE ONLY person ALTER COLUMN id SET DEFAULT nextval('person_id_seq'::regclass);

ALTER TABLE ONLY person
    ADD CONSTRAINT fk_id_person PRIMARY KEY (id);