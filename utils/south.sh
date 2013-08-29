# this is for first time only
./../manage.py schemamigration forum --initial

# reset south migration
rm -r ../forum/migrations/ 
./../manage.py reset south 
./../manage.py convert_to_south forum 
