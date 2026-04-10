
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
        RAISE NOTICE 'Контакт "%" обновлён', p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone) VALUES(p_name, p_phone);
        RAISE NOTICE 'Контакт "%" добавлен', p_name;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names  VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i           INT;
    v_name      VARCHAR;
    v_phone     VARCHAR;
    v_total     INT;
BEGIN

    CREATE TEMP TABLE IF NOT EXISTS invalid_contacts (
        first_name VARCHAR,
        phone      VARCHAR,
        reason     TEXT
    ) ON COMMIT PRESERVE ROWS;
    DELETE FROM invalid_contacts;

    v_total := array_length(p_names, 1);

    IF v_total IS NULL THEN
        RAISE NOTICE 'Пустой список';
        RETURN;
    END IF;

    FOR i IN 1..v_total LOOP
        v_name  := p_names[i];
        v_phone := p_phones[i];

        IF v_phone !~ '^\+?[0-9]{10,15}$' THEN
            INSERT INTO invalid_contacts(first_name, phone, reason)
            VALUES (v_name, v_phone, 'Некорректный формат телефона');
            RAISE NOTICE 'Пропущено: % | % — некорректный телефон', v_name, v_phone;
            CONTINUE;
        END IF;

        IF v_name IS NULL OR TRIM(v_name) = '' THEN
            INSERT INTO invalid_contacts(first_name, phone, reason)
            VALUES (v_name, v_phone, 'Пустое имя');
            CONTINUE;
        END IF;

        IF EXISTS (SELECT 1 FROM phonebook WHERE phone = v_phone) THEN
            UPDATE phonebook SET first_name = v_name WHERE phone = v_phone;
            RAISE NOTICE 'Обновлён: % | %', v_name, v_phone;
        ELSE
            INSERT INTO phonebook(first_name, phone) VALUES(v_name, v_phone);
            RAISE NOTICE 'Добавлен: % | %', v_name, v_phone;
        END IF;

    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_username VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_username IS NOT NULL THEN
        DELETE FROM phonebook WHERE first_name = p_username;
        RAISE NOTICE 'Удалены контакты с именем "%"', p_username;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
        RAISE NOTICE 'Удалены контакты с телефоном "%"', p_phone;
    ELSE
        RAISE NOTICE 'Не указано ни имя, ни телефон — ничего не удалено';
    END IF;
END;
$$;

