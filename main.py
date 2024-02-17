# Setting things up
# -venv - DONE
# -gitignore - DONE
# -Known required folders - DONE
# - requirements.txt - NOT DONE
# - check if everything is set up - NOT DONE

from app.DbAccessActions import DbAccessActions as dbaa
from app.DbPersonalActions import DbPersonalActions as dbpa

# Run here the database test code (temporary)


dba = dbaa("localhost", "root", "anyadkinnya", "cotton", "access")
dbp = dbpa("localhost", "root", "anyadkinnya", "cotton", "persoane")
print(dba.table)
print(dbp.table)