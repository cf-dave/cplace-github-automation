const { Octokit } = require("@octokit/rest");
const { createTokenAuth } = require("@octokit/auth-token");
const fs = require('fs');
path = require('path');
filePath = path.join(__dirname, 'accessToken.txt');

const token = fs.readFileSync(filePath,
  {encoding:'utf8', flag:'r'});
  
  //console.log(token)

const octokit = new Octokit({
  auth: token
});

// Compare: https://docs.github.com/en/rest/reference/repos/#list-organization-repositories
const auth = createTokenAuth(token);
const authentication = auth();


fs.readFile('todo.json', 'utf-8', (err, data) => {
  if(err){
      console.error(err)
  }
  const todo = JSON.parse(data)
  addUser(data)
})

//addUser(repo, user, level.toLowerCase())



function addUser(data){
  //console.log(data)
  var repo, user, level, justification;
  values = data.split("\n")
  user =  values[0].split(":")[1]
  repo = values[1].split(":")[1]
  level = values[2].split(":")[1]
  justification = values[3].split(":")[1]
  //console.log(repo.trim().length)
  //console.log(user)
  //console.log(level)
  octokit.rest.repos.addCollaborator({                  //working, but logging at the end gives undefined
    owner: "collaborationFactory",
    repo: repo.trim(),
    username: user.trim(),
    permission: level.trim().toLowerCase()
    })
    .then(({data}) => {
      console.log("Script ran through")
    });
}