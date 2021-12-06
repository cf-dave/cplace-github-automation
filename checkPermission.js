const { Octokit } = require("@octokit/rest");
const { createTokenAuth } = require("@octokit/auth-token");

const token = "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"

const octokit = new Octokit({
  auth: token
});
// Compare: https://docs.github.com/en/rest/reference/repos/#list-organization-repositories
const auth = createTokenAuth(token);
const authentication = auth();

asyncCall();

async function asyncCall(){

var check = await octokit.rest.repos.getCollaboratorPermissionLevel({
    owner: "collaborationFactory",
    repo: "adminTest",
    username: "TimHorm",
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