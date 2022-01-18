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

    function askQuestion(query) {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
        });

        return new Promise(resolve => rl.question(query, ans => {
            rl.close();
            resolve(ans);
        }))
    }

    const ans = await askQuestion("What is the name of the file? ");
    console.log(ans)
    var name = ans + ".txt"
    var input = fs.readFileSync(path.join(__dirname, name),
        {encoding:'utf8', flag:'r'});
    repos = input.split('\n')
    for(let i = 0; i < repos.length; i++){
        repos[i] = repos[i].substring(0, repos[i].length-1)                                 //Cuttet letztes Zeichen weg, muss evtl. an txt angepasst werden
    }
    repos.forEach(element => {
        console.log(element)
        for (let i = 0; i < element.length; i++) {
            //console.log(element.charCodeAt(i));                                           //Gibt chars der einzelen Repos aus, um evtl falsche zu finden
          }
    })

    

    var members = []
    var rights = []

    for(let i = 0; i < repos.length; i++){
        var mem = []
        var rig = []
        try{
            var answer = await octokit.rest.repos.listCollaborators({
                owner: "collaborationFactory",
                repo: repos[i],
                per_page: 100,
            });
        }catch{
            console.log("Fehler bei Repo " + repos[i])
            //console.log(repos[i].length)
            if(repos[i].length == 0){
                break;
            }
        }
        console.log(answer.data.length)
        for(let j = 0; j < answer.data.length; j++){
            mem.push(answer.data[j].login)
            rig.push(answer.data[j].role_name)
        }
        members.push(mem)
        rights.push(rig)
    }

    var logger = fs.createWriteStream(ans +'Log.txt', {
        flags: 'a' // 'a' means appending (old data will be preserved)
      })
      for(let i = 0; i < members.length; i++){
        logger.write("\n")
        logger.write("\n")
        logger.write(repos[i]+"\n")
        for(let j = 0; j < members[i].length; j++){
            logger.write(members[i][j] + "  " + rights[i][j] +"\n")
          }
      }
}