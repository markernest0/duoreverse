#!/usr/bin/env python
# import modules in standard python library
import argparse
import os
import sys

# import external python modules
from dotenv import load_dotenv
from prettytable import PrettyTable
import duo_client

class bcolors:
    SPLASH = '\033[92m'
    INFO = '\033[94m'
    UPDATE = '\033[96m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'

def splash():
    print(bcolors.SPLASH + """

    ██████╗ ██╗   ██╗ ██████╗ ██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗███████╗
    ██╔══██╗██║   ██║██╔═══██╗██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝
    ██║  ██║██║   ██║██║   ██║██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗█████╗  
    ██║  ██║██║   ██║██║   ██║██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝  
    ██████╔╝╚██████╔╝╚██████╔╝██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║███████╗
    ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝  v1.0.0

    # @markernest0
    # medium.com/@markernest
    
    """ + bcolors.ENDC)

def parser_error(errmsg):
    splash()
    print("##### USAGE: python " + sys.argv[0] + " [Options] use -h for help" + '\n')
    print(bcolors.ERROR + "##### ERROR: " + errmsg + bcolors.ENDC + '\n')
    
def parse_args():
    splash()
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " add some things here")
    parser = argparse.ArgumentParser()
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    ### RECONNAISSANCE
    recon_admin_email = parser.add_argument_group("RECONNAISSANCE -- FIND ADMINS")
    recon_admin_email.add_argument('-rae', '--recon_admin_email', help='Enter the email of the admin to recon')
    ### PERSISTENCE
    persistence_adduser = parser.add_argument_group("PERSISTENCE -- ADD USER")
    persistence_adduser.add_argument('-au', '--add_user', help='Enter the username to create')
    persistence_addadmin = parser.add_argument_group("PERSISTENCE -- ADD ADMIN")
    persistence_addadmin.add_argument('-aau', '--add_admin_name', help='Enter the name of the admin to create')
    persistence_addadmin.add_argument('-aae', '--add_admin_email', help='Enter the email of the admin to create')
    persistence_addadmin.add_argument('-aap', '--add_admin_phone', help='Enter the phone number of the admin to create')
    persistence_addintegration = parser.add_argument_group("PERSISTENCE -- ADD INTEGRATION")
    persistence_addintegration.add_argument('-ain', '--add_api_integration', help='Enter the name of the API integration to create')
    ### DEFENSE EVASION
    defense_moduser = parser.add_argument_group("DEFENSE EVASION -- BYPASS OR DISABLE USER")
    defense_moduser.add_argument('-mu', '--modify_userid', help='Enter the user ID to disable or bypass')
    defense_moduser.add_argument('-ms', '--modify_status', choices=['bypass', 'disabled'], help='Set the user to bypass or disabled')
    ### CREDENTIAL ACCESS
    ### DISCOVERY
    discovery_listusers = parser.add_argument_group("DISCOVERY -- LIST USERS")
    discovery_listusers.add_argument('-l', '--list_user', nargs='?', const='all', help='List user by ID')
    discovery_listusers.add_argument('-lu', '--list_users', nargs='?', const='all', help='List all users')
    discovery_listusers.add_argument('-la', '--list_admins', nargs='?', const='all', help='List all admin users')
    discovery_listgroups = parser.add_argument_group("DISCOVERY -- LIST GROUPS")
    discovery_listgroups.add_argument('-lg', '--list_groups', nargs='?', const='all', help='List all groups')
    discovery_listintegrations = parser.add_argument_group("DISCOVERY -- LIST INTEGRATIONS")
    discovery_listintegrations.add_argument('-li', '--list_integrations', nargs='?', const='all', help='List all integrations')
    ### EXFILTRATION
    ### IMPACT
    impact_deluser = parser.add_argument_group("IMPACT -- DELETE USER")
    impact_deluser.add_argument('-du', '--delete_user', help='Delete a specific user ID')
    impact_deluser.add_argument('-da', '--delete_admin', help='Delete a specific admin ID')
    impact_delintegration = parser.add_argument_group("IMPACT -- DELETE INTEGRATION")
    impact_delintegration.add_argument('-di', '--delete_integration', help='Delete a specific integration')
    return parser.parse_args()

def main(reconadminemail, adduser, addadminname, addadminemail, addadminphone, addapiintegration, moduserid, modstatus, listuser, listusers, listadmins, listgroups, listintegrations, deleteuser, deleteadmin, deleteintegration):
    # Parse env file and connect to Splunk
    try:
      load_dotenv()
    except Exception as e:
      print(e)
    try:
      # Configuration and information about objects to create.
      admin_api = duo_client.Admin(
          ikey=os.getenv("ikey"),
          skey=os.getenv("skey"),
          host=os.getenv("host"))
    except Exception as e:
      print(bcolors.ERROR + "##### ERROR -", e, "Check the .env file parameters" + bcolors.ENDC)
      print('\n')
      sys.exit(1)

    # RECONNAISSANCE
    # Search an admin email
    if reconadminemail is not None:
      recon_admin_email(reconadminemail, admin_api)

    # PERSISTENCE
    # Create a new user
    if adduser is not None:
      add_user(adduser, admin_api)
    
    # Create a new admin
    if addadminname and addadminemail and addadminphone is not None:
      add_admin(addadminname, addadminemail, addadminphone, admin_api)
   
    # Create a new API integration
    if addapiintegration is not None:
      add_api_integration(addapiintegration, admin_api)

    # DEFENSE EVASION
    if moduserid is not None:
      modify_user(moduserid, modstatus, admin_api)

    # CREDENTIAL ACCESS
   
    # DISCOVERY
    # List all users
    if listuser is not None:
      list_user(listuser, admin_api)

    # List all users
    if listusers is not None:
      list_users(listusers, admin_api)

    # List all admin users
    if listadmins is not None:
      list_admins(listadmins, admin_api)

    # List all admin users
    if listgroups is not None:
      list_groups(listgroups, admin_api)
      
    # List all integrations
    if listintegrations is not None:
      list_integrations(listintegrations, admin_api)
      
    # EXFILTRATION

    # IMPACT
    # Delete a user ID
    if deleteuser is not None:
      del_user(deleteuser, admin_api)
      
    # Delete an admin ID
    if deleteadmin is not None:
      del_admin(deleteadmin, admin_api)

    # Delete an admin ID
    if deleteintegration is not None:
      del_integration(deleteintegration, admin_api)

### Functions

# PERSISTENCE
# Create new user function
# https://duo.com/docs/adminapi#create-user
def add_user(adduser, admin_api):
  try:
    user = admin_api.add_user(
      username=adduser
    )
    print(bcolors.UPDATE + "##### UPDATE - The user", adduser, "was created" + bcolors.ENDC)
    print('\n')
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant write resource\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)

# Create new admin function
# https://duo.com/docs/adminapi#create-administrator
def add_admin(addadminname, addadminemail, addadminphone, admin_api):
  try:
    admin = admin_api.add_admin(
      name=addadminname,
      email=addadminemail,
      phone=addadminphone,
      password=""
    )
    print(bcolors.UPDATE + "##### UPDATE - The admin", addadminname, "was created and an activation email was sent to", addadminemail, bcolors.ENDC)
    print('\n')
    
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant administrators\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
      if str(e) == "Received 400 Invalid request parameters (The provided email address is already in use by another admin.)":
        print("ADMIN USER FOUND: ", addadminemail)
    print('\n')
    sys.exit(1)

# Admin recon
# https://duo.com/docs/adminapi#create-administrator
def recon_admin_email(reconadminemail, admin_api):
    try:
        # Try to add a new admin using the Duo Admin API
        admin = admin_api.add_admin(
            name=reconadminemail,
            email=reconadminemail,
            phone="+17345551212",
            password=""
        )
        list_new_admin(reconadminemail, admin_api)

    except Exception as e:
        # If an exception occurs, handle it
        if e.status == 403:
            # If the exception status is 403, print an error related to permissions
            print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant administrators\" permission" + bcolors.ENDC)
        else:
            # Print existing admin email
            if str(e) == "Received 400 Invalid request parameters (The provided email address is already in use by another admin.)":
                # If the email address is already in use, print a message
                print("ADMIN USER FOUND: ", reconadminemail)
            # For other exceptions, print a general error message
            else:
              print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
        print('\n')
        sys.exit(1)  # Exit the script with an error code
    
# Create new API integration function
# https://duo.com/docs/adminapi#create-integration
def add_api_integration(addapiintegration, admin_api):
  try:
    integration = admin_api.create_integration(
      name=addapiintegration,
      integration_type="adminapi",
      adminapi_admins='1',
      adminapi_info='1',
      adminapi_integrations='1',
      adminapi_read_log='1',
      adminapi_read_resource='1',
      adminapi_settings='1',
      adminapi_write_resource='1',
    )
    print(bcolors.UPDATE + "##### UPDATE - The API", addapiintegration, "was created" + bcolors.ENDC)
    print('\n')
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant write resource\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)
    
# DEFENSE EVASION
# Bypass or Disable user function
# https://duo.com/docs/adminapi#modify-user
def modify_user(moduserid, modstatus, admin_api):
  try:
    user = admin_api.update_user(
      user_id=moduserid,
      status=modstatus,
    )
    print(bcolors.UPDATE + "##### UPDATE -", moduserid, "was set to", modstatus, bcolors.ENDC)
    print('\n')
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant write resource\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)

# CREDENTIAL ACCESS

# DISCOVERY
# List user by ID function
# https://duo.com/docs/adminapi#retrieve-user-by-id
def list_user(listuser, admin_api):
  try:
    user = admin_api.get_user_by_id(listuser)
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant read resource\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)
  if user["aliases"] == {}:
    user["aliases"] = "None"
  if user["realname"] == "":
    user["realname"] = "None"
  if user["email"] == "":
    user["email"] = "None"
  if user["groups"] == []:
    user["groups"] = "None"
  table = PrettyTable([bcolors.UPDATE + 'User ID', 'Username', 'Aliases', 'Name', 'Email', 'Status' + bcolors.ENDC])
  table.add_row([bcolors.UPDATE + 
                 user["user_id"],
                 user["username"],
                 user["aliases"],
                 user["realname"],
                 user["email"],
                 user["status"]
                 + bcolors.ENDC]
               )
  print(table)
  print('\n')

# List all users function
# https://duo.com/docs/adminapi#retrieve-users
def list_users(listusers, admin_api):
  try:
    users = admin_api.get_users()
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant read resource\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)
  table = PrettyTable([bcolors.UPDATE + 'User ID', 'Username', 'Aliases', 'Name', 'Email', 'Phone ID', 'Phone', 'Type', 'Platform', 'Status' + bcolors.ENDC])
  for user in users:
    if user["aliases"] == {}:
      user["aliases"] = "None"
    if user["realname"] == "":
      user["realname"] = "None"
    if user["email"] == "":
      user["email"] = "None"
    if user["phones"] == []:
      user["phones"] = "None"
      table.add_row([bcolors.UPDATE + 
                     user["user_id"],
                     user["username"],
                     user["aliases"],
                     user["realname"],
                     user["email"],
                     user["phones"],
                     user["phones"],
                     user["phones"],
                     user["phones"],
                     user["status"]
                     + bcolors.ENDC]
                   )
    else:
      for phone in user["phones"]:
        if user["aliases"] == {}:
          user["aliases"] = "None"
        if user["realname"] == "":
          user["realname"] = "None"
        if user["email"] == "":
          user["email"] = "None"
        table.add_row([bcolors.UPDATE + 
               user["user_id"],
               user["username"],
               user["aliases"],
               user["realname"],
               user["email"],
               phone["phone_id"],
               phone["number"],
               phone["type"],
               phone["platform"],
               user["status"]
               + bcolors.ENDC]
             )
  print(table)
  print('\n')

# List all admins function
# https://duo.com/docs/adminapi#retrieve-administrators
def list_admins(listadmins, admin_api):
  try:
    admins = admin_api.get_admins()
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant administrators\" and \"Grant read resource\" permissions" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)
  table = PrettyTable([bcolors.UPDATE + 'Admin ID', 'Name', 'Email', 'Phone', 'Role', 'Admin Units', 'Status' + bcolors.ENDC])
  for admin in admins:
    table.add_row([bcolors.UPDATE + 
                   admin["admin_id"],
                   admin["name"],
                   admin["email"],
                   admin["phone"],
                   admin["role"],
                   admin["admin_units"],
                   admin["status"]
                   + bcolors.ENDC]
                 )
  print(table)
  print('\n')

# List all groups function
# https://duo.com/docs/adminapi#retrieve-groups
def list_groups(listgroups, admin_api):
  try:
    groups = admin_api.get_groups()
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant read resource\" permissions" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)
  table = PrettyTable([bcolors.UPDATE + 'Group ID', 'Name', 'Status', 'Description' + bcolors.ENDC])
  for group in groups:
    if group["desc"] == "":
      group["desc"] = "None"
    table.add_row([bcolors.UPDATE + 
                   group["group_id"],
                   group["name"],
                   group["status"],
                   group["desc"]
                   + bcolors.ENDC]
                 )
  print(table)
  print('\n')

# After creating a new admin, list the admin ID. Used for admin recon.
# https://duo.com/docs/adminapi#retrieve-administrators
def list_new_admin(search_email, admin_api):
    try:
        # Try to retrieve information about all administrators using the Duo Admin API
        admins = admin_api.get_admins()
        
    except Exception as e:
        # If an exception occurs, handle it
        if e.status == 403:
            # If the exception status is 403, print an error related to permissions
            print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant administrators\" and \"Grant read resource\" permissions" + bcolors.ENDC)
        else:
            # For other exceptions, print a general error message
            print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
        
        print('\n')
        sys.exit(1)  # Exit the script with an error code
    
    # Check if the search_email matches any admin's email and print the corresponding Admin ID
    found_admin_id = None
    for admin in admins:
        if admin["email"] == search_email:
            found_admin_id = admin["admin_id"]
            break
    
    if found_admin_id is not None:
        print(f"Admin ID for email '{search_email}': {found_admin_id}")
        del_admin(found_admin_id, admin_api)
    else:
        print(f"No admin found with email '{search_email}'")

# List all integrations
# https://duo.com/docs/adminapi#retrieve-integrations
def list_integrations(listintegrations, admin_api):
  try:
    integrations = admin_api.get_integrations()
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant read resource\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)
  table = PrettyTable([bcolors.UPDATE + 'Name', 'Type', 'Self-Service', 'Normalization', 'Groups', 'IKEY', 'SKEY', 'Notes' + bcolors.ENDC])
  for integration in integrations:
    if integration["self_service_allowed"] == 1:
      integration["self_service_allowed"] = "True"
    if integration["groups_allowed"] == []:
      integration["groups_allowed"] = "None"
    if integration["notes"] == "":
      integration["notes"] = "None"
    table.add_row([bcolors.UPDATE + 
                   integration["name"],
                   integration["type"],
                   integration["self_service_allowed"],
                   integration["username_normalization_policy"],
                   integration["groups_allowed"],
                   integration["integration_key"],
                   integration["secret_key"],
                   integration["notes"]
                   + bcolors.ENDC]
                 )
  print(table)
  print('\n')
  
# EXFILTRATION

# IMPACT
# Delete a user ID function
# https://duo.com/docs/adminapi#delete-user
def del_user(deleteuser, admin_api):
  try:
    user = admin_api.delete_user(
      user_id=deleteuser
    )
    print(bcolors.UPDATE + "##### UPDATE - The user", deleteuser, "was deleted" + bcolors.ENDC)
    print('\n')
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant write resource\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)

# Delete an admin ID function
# https://duo.com/docs/adminapi#delete-administrator
def del_admin(deleteadmin, admin_api):
  try:
    admin = admin_api.delete_admin(
      admin_id=deleteadmin
    )
    print(bcolors.UPDATE + "##### UPDATE - The admin", deleteadmin, "was deleted" + bcolors.ENDC)
    print('\n')
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant administrators\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)

# Delete an integration function
# https://duo.com/docs/adminapi#delete-integration
def del_integration(deleteintegration, admin_api):
  try:
    integration = admin_api.delete_integration(
      integration_key=deleteintegration
    )
    print(bcolors.UPDATE + "##### UPDATE - The integration", deleteintegration, "was deleted" + bcolors.ENDC)
    print('\n')
  except Exception as e:
    if e.status == 403:
      print(bcolors.ERROR + "##### ERROR -", e, "- Check the Admin API \"Grant applications\" permission" + bcolors.ENDC)
    else:
      print(bcolors.ERROR + "##### ERROR -", e, bcolors.ENDC)
    print('\n')
    sys.exit(1)

# All the argparse options returned to main
def interactive():
    args = parse_args()
    reconadminemail = args.recon_admin_email
    adduser = args.add_user
    addadminname = args.add_admin_name
    addadminemail = args.add_admin_email
    addadminphone = args.add_admin_phone
    addapiintegration = args.add_api_integration
    moduserid = args.modify_userid
    modstatus = args.modify_status
    listuser = args.list_user
    listusers = args.list_users
    listadmins = args.list_admins
    listgroups = args.list_groups
    listintegrations = args.list_integrations
    deleteuser = args.delete_user
    deleteadmin = args.delete_admin
    deleteintegration = args.delete_integration
    res = main(
      reconadminemail,
      adduser,
      addadminname,
      addadminemail,
      addadminphone,
      addapiintegration,
      moduserid,
      modstatus,
      listuser,
      listusers,
      listadmins,
      listgroups,
      listintegrations,
      deleteuser,
      deleteadmin,
      deleteintegration)
    
if __name__ == "__main__":
    interactive()
