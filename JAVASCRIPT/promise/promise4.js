const promiseFour = new Promise(function(resolve, reject){
    setTimeout(function(){
        let error = true
        if (!error){
            resolve({username : "Sunny", password : "10749"})
        } else {
            reject('Error : JS Went Wrong')
        }
    },1000)
})

async function consumePromiseFour() {
    try {
        const response = await promiseFour
        console.log(response);
    } catch (error) {
        console.log(error)
    }
}

consumePromiseFour()