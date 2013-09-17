# remove data.db file
rm ../data.db

# run this once for creating migrate db
./../manage.py syncdb

# reset south migration
rm -r ../forum/migrations/ 
./../manage.py reset south 
#./../manage.py convert_to_south forum 

# this is for first time only
./../manage.py schemamigration forum --initial

./../manage.py migrate forum
# if there's error like 'tag table has already exists, do the following
# which deletes unnessary migration history
#rm forum/migrations/0002_initial.py
