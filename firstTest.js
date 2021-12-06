const { Octokit } = require("@octokit/rest");
const { createTokenAuth } = require("@octokit/auth-token");

const token = "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"

const octokit = new Octokit({
  auth: token
});

// Compare: https://docs.github.com/en/rest/reference/repos/#list-organization-repositories
const auth = createTokenAuth(token);
const authentication = auth();

octokit.rest.repos.addCollaborator({
owner: "collaborationFactory",
repo: "adminTest",
username: "CzeroDerg",
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
