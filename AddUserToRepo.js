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

var user = ""
var repo = ""
var right = "s"

octokit.rest.repos.addCollaborator({                  //working, but logging at the end gives undefined
  owner: "collaborationFactory",
  repo: "adminTest",
  username: "CzeroDerg",
  permission: "admin"
  })
  .then(({data}) => {
    //console.log(data)
  });