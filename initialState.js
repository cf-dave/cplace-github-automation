const { Octokit } = require("@octokit/rest");
const { createTokenAuth } = require("@octokit/auth-token");
const fs = require('fs');
const readline = require('readline');

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

asyncCall();

async function asyncCall(){
   
    var repos = []
    for(let i = 0; i < 4; i++){
        var repositories = await octokit.rest.repos.listForOrg({
            org: "collaborationFactory",
            per_page: 100,
            page: (i+1),
        })
        for(let j = 0; j < repositories.data.length; j++){
            repos.push(repositories.data[j].name)
        }
    }

    

    var members = []
    var rights = []
    console.log(repos.length)
    for(let i = 0; i < repos.length; i++){    
        var mem = []
        var rig = []
        var complete = []
        console.log(repos[i])
        for(let j = 0; j < 10; j++){
            try{
                var answer = await octokit.rest.repos.listCollaborators({
                    owner: "collaborationFactory",
                    repo: repos[i],
                    per_page: 100,
                    page: [j+1]
                });
                answer.data.forEach(element => {
                    complete.push(element)
                })
            }catch{
                console.log("Fehler bei Repo " + repos[i])
                //console.log(repos[i].length)
                if(repos[i].length == 0){
                    break;
                }
            }
        }
        console.log(complete.length)
        for(let j = 0; j < complete.length; j++){
            mem.push(complete[j].login)
            rig.push(complete[j].role_name)
        }
        members.push(mem)
        rights.push(rig)
    }   

    var logger = fs.createWriteStream("full" +'Log.txt', {
        flags: 'a' // 'a' means appending (old data will be preserved)
      })
      for(let i = 0; i < members.length; i++){ 
        logger.write(repos[i]+"\n")
        for(let j = 0; j < members[i].length; j++){
            logger.write(members[i][j] + "  " + rights[i][j] +"\n")
        }
        //logger.write('$')       
        logger.write('\n')
        logger.write('\n')
      }
}