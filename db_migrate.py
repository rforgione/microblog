#!flask/bin/python
import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v + 1))

tmp_module = imp.new_module('old_model')
# this dumps out the python code required to create the model
# into a string
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

# we take the code string in the variable old_model
# and we execute it as python code, dumping out all of the
# variables into module we created above called tmp_module
# TODO: not sure how this works
exec(old_model, tmp_module.__dict__)

# we create the update script by using make_update_script_for_model
# and passing the db location, the db repo, the metadata from tmp_module,
# and the metadata from the database,
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                          SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta, db.metadata)

# we take all the work we've done so far on the migration script logic
# and dump it into the migration file
open(migration, "wt").write(script)

# here we actually perform the upgrade. the script created above
# allows us to go back to the old db version. there will be a different
# python script for every version of the database.
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print "New migration saved as " + migration
print "Current database version: " + str(v)
