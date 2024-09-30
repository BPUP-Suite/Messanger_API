--	          001 000 000 000 000 000 000      // user
--	          user1-user2		               // chat
-- 	          010 000 000 000 000 000 000      // group
--            100 000 000 000 000 000 000      // channel
-- 001 000 000 000 000 000 000 000 000 000 000 // message
-- 010 000 000 000 000 000 000 000 000 000 000 // files

CREATE DATABASE "BPUP_DB"
    WITH
    OWNER = bpup
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


BEGIN;


CREATE TABLE IF NOT EXISTS public.channels
(
    chat_id text COLLATE pg_catalog."default" NOT NULL,
    pinned_messages text[] COLLATE pg_catalog."default",
    members text[] COLLATE pg_catalog."default" NOT NULL,
    admins text[] COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    group_picture_id text[] COLLATE pg_catalog."default",
    theme text COLLATE pg_catalog."default",
    CONSTRAINT channels_pkey PRIMARY KEY (chat_id)
);

CREATE TABLE IF NOT EXISTS public.chats
(
    chat_id text COLLATE pg_catalog."default" NOT NULL,
    pinned_messages text[] COLLATE pg_catalog."default",
    CONSTRAINT chats_pkey PRIMARY KEY (chat_id)
);

CREATE TABLE IF NOT EXISTS public.files
(
    files_id text COLLATE pg_catalog."default" NOT NULL,
    file_path text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT files_pkey PRIMARY KEY (files_id)
);

CREATE TABLE IF NOT EXISTS public.groups
(
    chat_id text COLLATE pg_catalog."default" NOT NULL,
    pinned_messages text[] COLLATE pg_catalog."default",
    members text[] COLLATE pg_catalog."default" NOT NULL,
    admins text[] COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    group_picture_id text[] COLLATE pg_catalog."default",
    CONSTRAINT groups_pkey PRIMARY KEY (chat_id)
);

CREATE TABLE IF NOT EXISTS public.handles
(
    id text COLLATE pg_catalog."default" NOT NULL,
    handle text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT handles_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.messages
(
    message_id text COLLATE pg_catalog."default" NOT NULL,
    chat_id text COLLATE pg_catalog."default" NOT NULL,
    text text COLLATE pg_catalog."default" NOT NULL,
    sender text COLLATE pg_catalog."default" NOT NULL,
    date timestamp without time zone NOT NULL,
    forward_message_id text COLLATE pg_catalog."default",
    file_id text COLLATE pg_catalog."default",
    file_type text COLLATE pg_catalog."default",
    CONSTRAINT messages_pkey PRIMARY KEY (message_id)
);

CREATE TABLE IF NOT EXISTS public.notification
(
    user_id text COLLATE pg_catalog."default" NOT NULL,
    chat_id text COLLATE pg_catalog."default" NOT NULL,
    disable boolean NOT NULL DEFAULT false,
    CONSTRAINT notification_pkey PRIMARY KEY (user_id, chat_id)
);

CREATE TABLE IF NOT EXISTS public.users
(
    user_id text COLLATE pg_catalog."default" NOT NULL,
    username text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    profile_picture_id text[] COLLATE pg_catalog."default",
    phone_number text COLLATE pg_catalog."default",
    email text COLLATE pg_catalog."default" NOT NULL,
    birthday date,
    theme text COLLATE pg_catalog."default",
    last_access timestamp without time zone,
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS public.api_key
(
    user_id text NOT NULL,
    api_key text NOT NULL,
    PRIMARY KEY (user_id),
    CONSTRAINT api_key UNIQUE (api_key)
);

ALTER TABLE IF EXISTS public.handles
    ADD CONSTRAINT channel_id FOREIGN KEY (id)
    REFERENCES public.channels (chat_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX IF NOT EXISTS handles_pkey
    ON public.handles(id);


ALTER TABLE IF EXISTS public.handles
    ADD CONSTRAINT group_id FOREIGN KEY (id)
    REFERENCES public.groups (chat_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX IF NOT EXISTS handles_pkey
    ON public.handles(id);


ALTER TABLE IF EXISTS public.handles
    ADD CONSTRAINT user_id FOREIGN KEY (id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX IF NOT EXISTS handles_pkey
    ON public.handles(id);


ALTER TABLE IF EXISTS public.messages
    ADD CONSTRAINT channel_id FOREIGN KEY (chat_id)
    REFERENCES public.groups (chat_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.messages
    ADD CONSTRAINT chat_id FOREIGN KEY (chat_id)
    REFERENCES public.chats (chat_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.messages
    ADD CONSTRAINT file_id FOREIGN KEY (file_id)
    REFERENCES public.files (files_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.messages
    ADD CONSTRAINT forward_message_id FOREIGN KEY (forward_message_id)
    REFERENCES public.messages (message_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.messages
    ADD CONSTRAINT group_id FOREIGN KEY (chat_id)
    REFERENCES public.groups (chat_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.messages
    ADD CONSTRAINT sender FOREIGN KEY (sender)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.notification
    ADD CONSTRAINT channel_id FOREIGN KEY (chat_id)
    REFERENCES public.channels (chat_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.notification
    ADD CONSTRAINT chat_id FOREIGN KEY (chat_id)
    REFERENCES public.chats (chat_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.notification
    ADD CONSTRAINT group_id FOREIGN KEY (chat_id)
    REFERENCES public.groups (chat_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.notification
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.api_key
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;