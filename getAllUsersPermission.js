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


asyncCall();

async function asyncCall(){

    var teams = []
    for (let i = 0; i < 4; i++){
        var temp = await octokit.rest.teams.list({
            org: "collaborationFactory",
            per_page: 100,
            page: (i+1),
        });
        teams.push(temp)
    }
    var users = []
    for (let i = 0; i < 4; i++){
        var temp = await octokit.rest.orgs.listMembers({
            org: "collaborationFactory",
            per_page: 100,
            page: (i+1),
        });
        users.push(temp)
    }

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

    var allTeams = []

    teams.forEach(element => {
        for (let i = 0; i < 100; i++){
            allTeams.push(element.data[i])
            if(element.data[i].name == "VCP"){
                break;
            }
        }
    });

    console.log(allUsers.length)
    console.log(allTeams.length)

    
    var permissions = []

    for(let i = 0; i < 3 ; i++){
        var user = {
            username: allUsers[i].login,
            repos: [],
            rights:  [],
        }
            for(let j = 0; j < allTeams.length; j++){
                
                try{
                    var rights = await octokit.rest.teams.getMembershipForUserInOrg({
                        org: "collaborationFactory",
                        team_slug: allTeams[j].slug, //"adminTest",
                        username: user.username, //"cf-dave"
                    });
                    user.repos.push(allTeams[j].slug)
                    user.rights.push(rights.data.role)
                    console.log(user.username)
                    console.log(allTeams[j].slug)
                    console.log(rights.data.role)
                }catch(error){}
                
            };
        permissions.push(user)
    };
    //es muss wohl über alle repos iteriert werden. Das hier spuckt eigene Rpos des users aus
    for(let i = 0; i < permissions.length; i++){
        var repos = await octokit.rest.repos.listForUser({              
            username: permissions[i].username
        });
        console.log(repos)
        for(let j = 0; j < repos.length; j++){
            console.log("Hallo")
            var permission = await octokit.rest.repos.getCollaboratorPermissionLevel({
                owner: "collaborationFactory",
                repo: repos[j],
                username: permissions[i].username,
            });
            console.log(permission)
        }
        console.log("permissions länger als 0")
    };
}
/*
var repos = await octokit.rest.repos.getCollaboratorPermissionLevel({
    owner: "collaborationFactory",
    repo: permissions[i].repos[j],
    username: permissions.username,
})
*/