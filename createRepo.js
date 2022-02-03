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

fs.readFile('todo.txt', 'utf-8', (err, data) => {
    if(err){
        console.error(err)
    }
    addRepo(data)
  })

  function addRepo(data){
    //console.log(data)
    var repo;
    values = data.split("\n")
    repo = values[0].split(":")[1]
    console.log(repo.trim().length)
    octokit.rest.repos.createInOrg({                  //working, but logging at the end gives undefined
      owner: "collaborationFactory",
      repo: repo.trim(),
      })
      .then(({data}) => {
        console.log("Script ran through")
      });
  }