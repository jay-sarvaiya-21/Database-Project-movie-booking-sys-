cat project/data/MoviePool.csv | psql -U pdv8883 -d pdv8883_db -c "COPY MoviePool from STDIN DELIMITER ',' CSV HEADER"
cat project/data/employee.csv | psql -U pdv8883 -d pdv8883_db -c "COPY employee from STDIN DELIMITER ',' CSV HEADER"
cat project/data/Users.csv | psql -U pdv8883 -d pdv8883_db -c "COPY Users from STDIN DELIMITER ',' CSV HEADER"
cat project/data/scm.csv | psql -U pdv8883 -d pdv8883_db -c "COPY screeningmovie from STDIN DELIMITER ',' CSV HEADER"
cat project/data/SEATS.csv | psql -U pdv8883 -d pdv8883_db -c "COPY SEATS from STDIN DELIMITER ',' CSV HEADER"
cat project/data/tickets.csv | psql -U pdv8883 -d pdv8883_db -c "COPY ticket from STDIN DELIMITER ',' CSV HEADER"