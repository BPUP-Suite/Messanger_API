--	          001 000 000 000 000 000 000      // user
--	          user1-user2		               // chat
-- 	          010 000 000 000 000 000 000      // group
--            100 000 000 000 000 000 000      // channel
-- 001 000 000 000 000 000 000 000 000 000 000 // message
-- 010 000 000 000 000 000 000 000 000 000 000 // files

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg120+1)
-- Dumped by pg_dump version 16.4 (Debian 16.4-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: channels; Type: TABLE; Schema: public; Owner: bpup
--

CREATE TABLE public.channels (
    chat_id text NOT NULL,
    pinned_messages text[],
    members text[] NOT NULL,
    admins text[] NOT NULL,
    description text,
    group_picture_id text[],
    theme text
);


ALTER TABLE public.channels OWNER TO bpup;

--
-- Name: chats; Type: TABLE; Schema: public; Owner: bpup
--

CREATE TABLE public.chats (
    chat_id text NOT NULL,
    pinned_messages text[]
);


ALTER TABLE public.chats OWNER TO bpup;

--
-- Name: files; Type: TABLE; Schema: public; Owner: bpup
--

CREATE TABLE public.files (
    files_id text NOT NULL,
    file_path text NOT NULL
);


ALTER TABLE public.files OWNER TO bpup;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: bpup
--

CREATE TABLE public.groups (
    chat_id text NOT NULL,
    pinned_messages text[],
    members text[] NOT NULL,
    admins text[] NOT NULL,
    description text,
    group_picture_id text[]
);


ALTER TABLE public.groups OWNER TO bpup;

--
-- Name: handles; Type: TABLE; Schema: public; Owner: bpup
--

CREATE TABLE public.handles (
    id text NOT NULL,
    handle text NOT NULL
);


ALTER TABLE public.handles OWNER TO bpup;

--
-- Name: messages; Type: TABLE; Schema: public; Owner: bpup
--

CREATE TABLE public.messages (
    message_id text NOT NULL,
    chat_id text NOT NULL,
    text text NOT NULL,
    sender text NOT NULL,
    date timestamp without time zone NOT NULL,
    forward_message_id text,
    file_id text,
    file_type text
);


ALTER TABLE public.messages OWNER TO bpup;

--
-- Name: notification; Type: TABLE; Schema: public; Owner: bpup
--

CREATE TABLE public.notification (
    user_id text NOT NULL,
    chat_id text NOT NULL,
    disable boolean DEFAULT false NOT NULL
);


ALTER TABLE public.notification OWNER TO bpup;

--
-- Name: users; Type: TABLE; Schema: public; Owner: bpup
--

CREATE TABLE public.users (
    user_id text NOT NULL,
    username text NOT NULL,
    description text,
    profile_picture_id text[],
    phone_number text NOT NULL,
    birthday date,
    theme text,
    last_access timestamp without time zone
);


ALTER TABLE public.users OWNER TO bpup;

--
-- Name: channels channels_pkey; Type: CONSTRAINT; Schema: public; 
--

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_pkey PRIMARY KEY (chat_id);


--
-- Name: chats chats_pkey; Type: CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.chats
    ADD CONSTRAINT chats_pkey PRIMARY KEY (chat_id);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (files_id);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (chat_id);


--
-- Name: handles handles_pkey; Type: CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.handles
    ADD CONSTRAINT handles_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);


--
-- Name: notification notification_pkey; Type: CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_pkey PRIMARY KEY (user_id, chat_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: handles channel_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.handles
    ADD CONSTRAINT channel_id FOREIGN KEY (id) REFERENCES public.channels(chat_id) NOT VALID;


--
-- Name: messages channel_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT channel_id FOREIGN KEY (chat_id) REFERENCES public.groups(chat_id) NOT VALID;


--
-- Name: notification channel_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT channel_id FOREIGN KEY (chat_id) REFERENCES public.channels(chat_id) NOT VALID;


--
-- Name: messages chat_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT chat_id FOREIGN KEY (chat_id) REFERENCES public.chats(chat_id) NOT VALID;


--
-- Name: notification chat_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT chat_id FOREIGN KEY (chat_id) REFERENCES public.chats(chat_id) NOT VALID;


--
-- Name: messages file_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT file_id FOREIGN KEY (file_id) REFERENCES public.files(files_id) NOT VALID;


--
-- Name: messages forward_message_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT forward_message_id FOREIGN KEY (forward_message_id) REFERENCES public.messages(message_id) NOT VALID;


--
-- Name: handles group_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.handles
    ADD CONSTRAINT group_id FOREIGN KEY (id) REFERENCES public.groups(chat_id) NOT VALID;


--
-- Name: messages group_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT group_id FOREIGN KEY (chat_id) REFERENCES public.groups(chat_id) NOT VALID;


--
-- Name: notification group_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT group_id FOREIGN KEY (chat_id) REFERENCES public.groups(chat_id) NOT VALID;


--
-- Name: messages sender; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT sender FOREIGN KEY (sender) REFERENCES public.users(user_id) NOT VALID;


--
-- Name: handles user_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.handles
    ADD CONSTRAINT user_id FOREIGN KEY (id) REFERENCES public.users(user_id) NOT VALID;


--
-- Name: notification user_id; Type: FK CONSTRAINT; Schema: public; Owner: bpup
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) NOT VALID;


--
-- PostgreSQL database dump complete
--

