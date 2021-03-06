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

// Compare: https://docs.github.com/en/rest/reference/repos/#list-organization-repositories
const auth = createTokenAuth(token);
const authentication = auth();

octokit.rest.repos.addCollaborator({
owner: "collaborationFactory",
repo: "adminTest",
username: "cf-dave",
permission: "admin"
})
.then(({data}) => {
  console.log(data)
});

asyncCall();

async function asyncCall(){

var check = await octokit.rest.repos.checkCollaborator({
  owner: "collaborationFactory",
  repo: "adminTest",
  username: "CzeroDerg",
});
if (check.status == "204"){
  console.log("lol")
}
console.log(check.status)
}
