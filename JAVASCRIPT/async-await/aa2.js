console.log("1. Start")
async function calculateValue(isValid) {
    if(!isValid){
        throw new Error("Invalid Output");
        console.log("2. Will I run ?");
    }
    return 42;
}

calculateValue(false)
    .then(val => console.log("2. Success : ",val))
    .catch(err => console.log("3. Caught : ",err.message));

console.log("End of Code")