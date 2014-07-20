# cnxCommunitiesAddMember.py
# Author: Gert-Jan Alderlieste
# E-Mail: gert-jan@alderlieste.net
# E-Mail: 
# Blog: http://www.alderlieste.nl
# Description: Move IBM Connections Communities
# Parts of script are from klaus.bild@gmail.com

execfile( 'communitiesAdmin.py' )
state = ''
email2 = ''
parent_comm = ''
AddtoParent = ''
email = ""


def getUUID( comm_name ):
    allComm = CommunitiesService.fetchAllComm()
    result = CommunitiesListService.filterListByName(allComm, '.*' + comm_name + '.*')
    result = str(result)
    counter = result.count('uuid=')
    index = 0
    count = 0
    if (counter<1):
        print '\nThere is NO Community with this name\nPlease try again ----------->' 
        return (0,0,0,0,0,0)
    elif (counter<2):
        comm_id = result[result.find('uuid=')+5:result.find('uuid=')+41]
        comm_name = result[result.find('name=')+5:result.find('uuid=')-2]
        acl = result[result.find('type=')+5:result.find('name=')-2]
        parent = result.find('parentUuid=')
        parent_comm = result[result.find('parentUuid=')+11:result.find('created=')-2]
        return (comm_id, parent, parent_comm, comm_name, acl, 1)       
    else:
        comm_id = []
        comm_name = []
        acl = []
        parent = []
        parent_comm = []
        print '\nThere are multiple communities with this name: \n'
        while index < len(result):
            index = result.find('{', index)
            end = result.find('{', index+1)
            comm_id.append(result[result.find('uuid=', index)+5:result.find('uuid=', index)+41])
            comm_name.append(result[result.find('name=', index)+5:result.find('uuid=', index)-2])
            acl.append(result[result.find('type=', index)+5:result.find('name=', index)-2])
            parent_comm.append(result[result.find('parentUuid=', index)+11:result.find('created=', index)-2])
            parent.append(result.find('parentUuid=', index, end))
            if index == -1:
                break
            print ('\t' + str(count) + ': ' + comm_name[count])
            #print parent_comm ## for testing
            index += 1
            count += 1
        #print counter  ##


        is_valid_commNumber=0
        while not is_valid_commNumber :
                try :
                        comm_number = int(raw_input('\nPlease type the number of the community? : '))
                        if comm_number < counter and comm_number > -1:
                            is_valid_commNumber = 1 ## set it to 1 to validate input and to terminate the while..not loop
                        else:
                            print ( "'%s' is not a valid number.") % comm_number
                except ValueError, e :
                    print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])


        return (comm_id[int(comm_number)], parent[int(comm_number)], parent_comm[int(comm_number)], comm_name[int(comm_number)], acl[int(comm_number)],1)

def getNAME( parent_comm ):
    #print parent_comm ## debug
    result = CommunitiesService.fetchCommById(parent_comm)
    #print result ## debug
    result = str(result)
    comm_id = result[result.find('uuid=')+5:result.find('uuid=')+41]
    parentComm_name = result[result.find('name=')+5:result.find('uuid=')-2]
    #print parentComm_name ## debug
    return (parentComm_name)


while state != ( 'EXIT' ):
        state = raw_input( '\nPress A for adding a user to an Community, M for Menu or X for Exit : ' ).upper()
        if state == 'X':
            state = 'EXIT'
            is_valid_memberowner=0
            is_valid_adduser=0
            break
        elif state == 'M':
            state = 'MENU'
            execfile( 'ibmcnx/menu/comm.py' )
            break
        elif state =='A':
 

            email = raw_input( "Mail address of a user you want to Add: " ).lower()
            
            is_valid_comm = ''     
            while not is_valid_comm:
                
                comm_name = raw_input('\nWildcard is automatically added, just enter part of the name but the search is case sensitive!\nWhat is the name of the Community which you want to add a Member? : ')
                comm_id, parent, parent_comm, comm_fullname, acl, noresult = getUUID(comm_name)

                if noresult == 0:
                    continue
                else:
                    is_valid_comm = 1        


            #print comm_id  ## debug
            #print comm_name ## debug
            #print parent ## debug
            #print parent_comm ## debug 
            #print parentComm_name ## debug
            #print acl ## debug


#            if noresult == 0:
#                continue

#            else:
                goBack = ''
                if parent > 0:
                    parentComm_name = getNAME(parent_comm)
                    #print parent_comm ##debug
                    #print parentComm_name ##debug				
                    is_valid_AddtoParent = ''
                    goBack = ''
                    while not is_valid_AddtoParent :
                        try :					
                                decision = raw_input('\nCommunity \"' + comm_fullname + '\" is a subCommunity of Community \"' + parentComm_name + '\"! \nDo you want to add user to both Communities (y/n)? : ')					
                                if decision == 'y' :
                                    AddtoParent = '1' 					
                                    print '\nUser will be also added to parentCommunity \"' + parentComm_name + '\"\n'
                                    is_valid_AddtoParent = 1
                                    continue
                                elif decision == 'n' :	
                                    print '\nYou can not add a user to a subCommunity if it is not a Member/Owner of the parentCommunity!\n'
                                    is_valid_AddtoParent = 1
                                    state = ''
                                    goBack = 'TRUE'
                                else:
                                    print ( "'%s' is not a valid input.") % decision
                                    continue
                        except ValueError, e :
                                print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])


                while goBack != ( 'TRUE' ):

                  ##  if state == 0:
                  ##      continue
                    #   if parent2 > 0:
                    #       print '\n' + comm_name_parent + ' is already a subcommunity, please use a Community which is NOT a subcommunity\n'
                  ##      continue
                  ##  else:
                    #   if (acl_parent=='publicInviteOnly' and acl=='public'):
                    #       print '\nThe parent Community has MODERATED access, the new subcommunity ' + comm_fullname + ' will have MODERATED access as well'
                    #   elif (acl_parent=='private' and acl=='public') or (acl_parent=='private' and acl=='publicInviteOnly'):
                    #       print '\nThe parent Community has only PRIVATE access, the new subcommunity ' + comm_fullname + ' will have PRIVATE access as well'
                        
                    ###########################
                    ## Robust error handling ##
                    ## only accept int       ##
                    ###########################
                    ## Wait for valid input in while...not ###

                    is_valid_memberowner=0
                    while not is_valid_memberowner :
                            try :
                                    memberowner = raw_input('\nDo you want to add this user as a Member(m) or as a Owner(o)? : ')
                                    if memberowner == 'm' :
                                        role = 0
                                        rolename = 'Member'
                                        is_valid_memberowner = 1													
                                    elif memberowner == 'o' :
                                        role = 1
                                        rolename = 'Owner' 
                                        is_valid_memberowner = 1													
                                    else:
                                        print ( "'%s' is not a valid input.") % memberowner
                            except ValueError, e :
                                print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])	


                    ###########################
                    ## Robust error handling ##
                    ## only accept int       ##
                    ###########################
                    ## Wait for valid input in while...not ###
                                        
                    is_valid_adduser=0
                    while not is_valid_adduser :			                    
                            try:
                                    if AddtoParent == '1':
                                        decision = raw_input('\n\tAdd User - Summary\n\t-----------------\n\temail:\t\t ' + email + '\n\tsubCommunity:\t ' + comm_fullname + '\n\tparentCommunity: ' + parentComm_name + '\n\tRole:\t\t ' + rolename + '\n\nDo you want to process (y/n/x)? : ')
                                    else:
                                        decision = raw_input('\n\tAdd User - Summary\n\t-----------------\n\temail:\t\t ' + email + '\n\tCommunity:\t ' + comm_fullname + '\n\tRole:\t\t ' + rolename + '\n\tAccess:\t\t ' + acl + '\n\nDo you want to process (y/n/x)? : ')

                                    if decision == 'y' :
                                        email2 = [email]
                                        if AddtoParent == '1' : 
                                            CommunitiesService.addMembersToCommunityByEmail(parentComm_name,role,email2)
                                            CommunitiesService.addMembersToCommunityByEmail(comm_fullname,role,email2)
                                            goBack = 'TRUE'
                                            print '\nSuccessful added user with email address \"' +  email + '\" to:\nsubCommunity \"' + comm_fullname + '\" and parentCommunity \"' + parentComm_name + '\" \n'
                                            is_valid_adduser = 1 ## set it to 1 to validate input and to terminate the while..not loop
                                        else:                            
                                            CommunitiesService.addMembersToCommunityByEmail(comm_fullname,role,email2)
                                        
                                            goBack = 'TRUE'
                                            print '\nSuccessful added user with email address \"' +  email + '\" to Community \"' + comm_fullname + '\"\n'
                                            is_valid_adduser = 1 ## set it to 1 to validate input and to terminate the while..not loop

                                    elif decision == 'n' :
                                        is_valid_adduser = 1 ## set it to 1 to validate input and to terminate the while..not loop
                                    
                                    elif decision == 'x' :
                                        is_valid_adduser = 1 ## set it to 1 to validate input and to terminate the while..not loop
                                        goBack = 'TRUE'										

                                    else:
                                        print ( "'%s' is not a valid input.") % decision
                            except ValueError, e :
                                print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])


                    continue            
        else:
            continue
