const { Octokit } = require("@octokit/rest");
const { createTokenAuth } = require("@octokit/auth-token");
const fs = require('fs');
path = require('path');
filePath = path.join(__dirname, 'accessToken.txt');

const token = fs.readFileSync(filePath,
  {encoding:'utf8', flag:'r'});
  
  console.log(token)

const octokit = new Octokit({
  auth: token
});


var dev = 1

asyncCall();

async function asyncCall(){

    //Retrieve all teams from the API
    var teams = []
    for (let i = 0; i < 4; i++){
        var temp = await octokit.rest.teams.list({
            org: "collaborationFactory",
            per_page: 100,
            page: (i+1),
        });
        teams.push(temp)
    }

    //Retrieve all users from the API
    var users = []
    for (let i = 0; i < 4; i++){
        var temp = await octokit.rest.orgs.listMembers({
            org: "collaborationFactory",
            per_page: 100,
            page: (i+1),
        });
        users.push(temp)
    }
    //Create array of all users
    var allUsers = []

    users.forEach(element => {
        for (let i = 0; i < 100; i++){
            try {
            allUsers.push(element.data[i])
            } catch (error) {
                console.log("End of user list reached")
                break;
            }        
        }
    });

    //Create array of all teams 
    var allTeams = []

    teams.forEach(element => {
        for (let i = 0; i < 100; i++){
            allTeams.push(element.data[i])
            if(element.data[i].name == "VCP"){
                break;
            }
        }
    });

    var allReposPerTeam = []                    //List for all repos a team has access to. In the same order as the team list 

    for(let i = 0; i < 1; i++){ //allTeams.length
        var result = await octokit.rest.teams.listReposInOrg({
            org: "collaborationFactory",
            team_slug: allTeams[i].slug,
            per_page: 100
        })
        t = []
        r = []
        for(let j = 0; j < result.data.length; j++){            
            console.log(result.data[j].name)
            console.log(result.data[j].role_name)
            t.push(result.data[j].name)
            r.push(result.data[j].role_name)
        }
        allReposPerTeam.push([t, r])
    }

    //Retrieve all repos from the API
    var allRepos = []
    for(let i = 0; i < 4; i++){
        var repositories = await octokit.rest.repos.listForOrg({
            org: "collaborationFactory",
            per_page: 100,
            page: (i+1),
        })
        for(let j = 0; j < repositories.data.length; j++){
            allRepos.push(repositories.data[j].name)
        }
    }
    
    //List with user objects containing username, all repos and the access type
    var permissions = [] 

    //Iterate over all repos for every user and check his permission
    for(let i = 0; i < 1; i++){    //allUsers.length
        var user = {
            username: allUsers[i].login,
            repos: [],
            rights:  [],
            teams: [],
        }
        for(let j = 0; j < 1; j++){        //allRepos.length
            var check = await octokit.rest.repos.getCollaboratorPermissionLevel({
                owner: "collaborationFactory",
                repo: allRepos[j],
                username: user.username,
              });
              user.repos.push(allRepos[j])
              user.rights.push(check.data.permission)
        }
        permissions.push(user)
    }

    
    
    if(dev == 0){
        for(let i = 0; i < permissions.length ; i++){
            var user = permissions[i]

            //Find all teams a user is part of
                for(let j = 0; j < allTeams.length; j++){                    
                    try{
                        var rights = await octokit.rest.teams.getMembershipForUserInOrg({
                            org: "collaborationFactory",
                            team_slug: allTeams[j].slug, //"adminTest",
                            username: user.username, //"cf-dave"
                        });
                        if(rights.status == "200"){
                            user.teams.push(allTeams[j].slug)
                            console.log(user.username)
                            console.log(allTeams[j].slug)
                        }                        
                    }catch(error){}
                    
                };

                //Iterate over every team a user is part of an list the repos this team has access to
                for(let k = 0; k < user.teams.length; k++){                    
                    var index = allTeams.findIndex(user.teams[k])           //Index nachschalgen wo der entsprechende Eintrag in allTeams array und daher auch analog in der allReposPerTeam array zu finden ist
                    var eintrag = allReposPerTeam[index]                    // Eintrag aus allreposPerTeam array extrahieren
                    for(let l = 0; l < eintrag[0].length; l++){             //Über Array itarieren und repo sowie zugehöriges access right zu user hinzufügen
                        user.repos.push(eintrag[0][l])
                        user.rights.push(eintrag[1][l])
                    }
                }
            permissions.push(user)
        };
    }else{
        console.log("Dev mode enabled")
        var user = {
            username: "cf-dave",
            repos: [],
            rights:  [],
        }      
            try{
                var rights = await octokit.rest.teams.getMembershipForUserInOrg({
                    org: "collaborationFactory",
                    team_slug: "adminTest",
                    username: "cf-dave",
                });
                if(rights.status == "200"){
                    user.teams.push("adminTest")
                    console.log(user.username)
                    console.log("adminTest")
                }
            }catch(error){}            
            permissions.push(user)
    }
    
}