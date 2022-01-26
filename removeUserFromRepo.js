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

var repo = ""
var user = "s"

// Compare: https://docs.github.com/en/rest/reference/repos/#list-organization-repositories
const auth = createTokenAuth(token);
const authentication = auth();
await octokit.request('DELETE /repos/{owner}/{repo}/collaborators/{username}', {
  owner: 'octocat',
  repo: 'hello-world',
  username: 'username'
})