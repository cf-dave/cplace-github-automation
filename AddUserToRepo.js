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

fs.readFile('todo.txt', 'utf-8', (err, data) => {
  if(err){
      console.error(err)
      return
  }
  values = data.split("\n")
  user = data[0].split(":")[1]
  repo = data[1].split(":")[1]
  level = data[2].split(":")[1]
  justification = data[3].split(":")[1]
  console.log(data)
})


octokit.rest.repos.addCollaborator({                  //working, but logging at the end gives undefined
  owner: "collaborationFactory",
  repo: repo,
  username: user,
  permission: level
  })
  .then(({data}) => {
    //console.log(data)
  });

  console.log("Script ran through")