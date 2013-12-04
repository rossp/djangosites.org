UPDATE websites_website SET search_tsv=to_tsvector('pg_catalog.english', COALESCE(title, '') ||' '|| COALESCE(url, '') ||' '|| COALESCE(description, '') ||' '|| COALESCE(tags, ''));
CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE ON websites_website FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(search_tsv, 'pg_catalog.english', title, url, description, tags);

