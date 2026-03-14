const obj = {
    name: 'Sunny',
    greet: () => {
        console.log(this.name)  // this = where arrow was DEFINED
    }
}


obj.greet()    // ❌ undefined — arrow was defined in global scope
               //               global this has no name