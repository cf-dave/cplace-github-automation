const { Octokit } = require("@octokit/rest");
const { createTokenAuth } = require("@octokit/auth-token");
const fs = require('fs');
path = require('path');
filePathToken = path.join(__dirname, 'accessToken.txt');
filePathUser = path.join(__dirname, 'user.txt');
filePathRepo = path.join(__dirname, 'repo.txt');

const token = fs.readFileSync(filePathToken,
  {encoding:'utf8', flag:'r'});
  
  console.log(token)

const octokit = new Octokit({
  auth: token
});

const user = fs.readFileSync(filePathUser,
  {encoding:'utf8', flag:'r'});

const repo = fs.readFileSync(filePathRepo,
  {encoding:'utf8', flag:'r'});


asyncCall();

async function asyncCall(){

var teams = octokit.rest.teams.getMembershipForUserInOrg({
  org: "collaborationFactory",
  team_slug,
  username,
});

var check = await octokit.rest.repos.getCollaboratorPermissionLevel({
    owner: "collaborationFactory",
    repo: repo,
    username: user,
  });
if (check.status != "200"){
    console.log("Error")
}
  //console.log(check.status)
  console.log(check.data.permission)

var teams = []
for (let i = 0; i < 4; i++){
    var temp = await octokit.rest.teams.list({
        org: "collaborationFactory",
        per_page: 100,
        page: (i+1),
      });
    teams.push(temp)
}


  teams.forEach(element => {
      for (let i = 0; i < 100; i++){
          console.log(element.data[i].name)
          if(element.data[i].name == "VCP"){
              break;
          }
      }
      
  });
var users = []
for (let i = 0; i < 4; i++){
    var temp = await octokit.rest.orgs.listMembers({
        org: "collaborationFactory",
        per_page: 100,
        page: (i+1),
      });
    users.push(temp)
}


  users.forEach(element => {
      for (let i = 0; i < 100; i++){
          try {
            console.log(element.data[i].login)
          } catch (error) {
              console.log("End of user list reached")
              break;
          }

          
      }
      
  });
}