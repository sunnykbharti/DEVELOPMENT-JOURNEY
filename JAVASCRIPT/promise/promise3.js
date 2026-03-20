const promiseThree = new Promise(function(resolve, reject){
    setTimeout(function(){
        let error = true
        if (!error){
            resolve({username : "Sunny", password : "10749"})
        } else {
            reject('Error : Something Went Wrong')
        }
    },1000)
})

promiseThree
.then((user) => {
    console.log(user);
    return user.username
})
.then((username) => {
    console.log(username);
})
.catch(function(error){
    console.log(error);
})
.finally(() => console.log("Finally reolved or rejected"))