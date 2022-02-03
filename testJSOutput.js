const fs = require('fs')

fs.readFile('todo.txt', 'utf-8', (err, data) => {
    if(err){
        console.error(err)
        return
    }
    values = data.split("\n")
    user = data[0].split(":")[1]
    repo = data[1].split(":")[1]
    level = data[2].split(":")[1]
    justification = data[3]//.split(":")
    console.log(user)
    console.log(justification)
    //console.log(data)
})
