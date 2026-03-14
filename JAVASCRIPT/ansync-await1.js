const myPromise = new Promise((resolve, reject) => {
    // simulating API call with setTimeout
    setTimeout(() => {
        let success = true
        if(success) {
            resolve('Data loaded!')    // ✅
        } else {
            reject('Something failed') // ❌
        }
    }, 2000)  // 2 second delay
})

// Old way — using .then() and .catch()
myPromise
    .then(data => console.log(data))    // success
    .catch(error => console.log(error)) // failure