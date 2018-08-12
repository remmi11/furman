--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.6
-- Dumped by pg_dump version 9.6.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer DEFAULT nextval('public.user_seq'::regclass) NOT NULL,
    email character varying(255),
    password character varying(255),
    remember_token character varying(100),
    updated_at timestamp with time zone,
    role_id integer,
    created_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password, remember_token, updated_at, role_id, created_at) FROM stdin;
5	melkon.chilingaryan@gmail.com	$2y$10$ezxwawNuITwoc90kcjEPHOOhpFv6uveqe4DjZ8RjR.4q3E8Yce.mC	5zuHxHimIklZUrfvncn4rWsyzKwiPaXHYBA0i60lJpCS16PlnV6RhHyEbiiO	\N	\N	\N
8	daryl@furmanland.com	$2y$10$44Bfyerdz9WxqySTTls/celDOcwC.ct52wJnZ70ZuNNPffK2Krm2O	\N	\N	\N	\N
10	ctucker@beyondmapping.com	$2y$10$Qb6xzFcD0f./hXJaQ9H0PenXCW0lHJvJUc5gFNFCuMx.YJbsPmFq6	\N	\N	\N	\N
11	nicole@furmanland.com	$2y$10$VpTGMSp2J/jtTVkf5Eq4VekgGSYLgABQ0NXfwbQ.SWimi2avdWgta	\N	\N	\N	\N
12	jennifer@furmanland.com	$2y$10$0G/6EwPmOsa4NJfYJAdcv.1v8sm028NTvE2ZBoU0HJsZUp7CTFk/S	\N	\N	\N	\N
9	jana@furmanland.com	$2y$10$CrskonYNttZYJk.xKFpzl.eLGOrmYVCwyT9BIigaK/UBJZlWmkThu	FPeEKR1ZttMEEWZ6Go8JAN5Yul9BPsVv9RQMQUSJwS3WC4g0klZdJsMPkMX4	\N	\N	\N
1	test@admin.com	$2y$10$poHcgYMDyo/5qLDOl70rZusKl4Vj/vjbjGdt7DsOOkJNSVq2BHrUW	SbLw9rgDOAaKRMMAiHdiaUc98HiHAycchpnGqq0Hm7lriYAbPPglOOPTFMh1	\N	\N	\N
7	noah@beyondmapping.com	$2y$10$xO10VUaitUXZhXT/fI9z5eeeJLzzHQ04eHPyYUJcDW/PijLHcSMrq	tyKPpS3PUi5BKf3lgupKAh6zQJ4Gae9nwuogQK60EVIHIyxcpGXbBHAugvmD	\N	\N	\N
\.


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: TABLE users; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.users TO furman;


--
-- PostgreSQL database dump complete
--

