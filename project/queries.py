query_select_id = "SELECT * FROM person WHERE id='{}'"
query_select_min_age = "SELECT * FROM person WHERE date_of_birth <= '{}'"
query_select_max_age = "SELECT * FROM person WHERE date_of_birth >= '{}'"
query_select_interval_age = "SELECT * FROM person WHERE date_of_birth > '{}' AND date_of_birth <= '{}'"
query_select_address = "SELECT * FROM person WHERE address LIKE '%{}%'"
query_select_all = "SELECT * FROM person"
query_add = "INSERT INTO person(name, date_of_birth, address) VALUES('{}','{}','{}')"
query_delete = "DELETE FROM person WHERE id='{}'"
query_clear = "DELETE FROM person"
query_update = "UPDATE person SET name='{}', date_of_birth='{}', address='{}' WHERE id ='{}'"