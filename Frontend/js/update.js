async function update() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const newpassword = document.getElementById("newpass").value;

    const res = await fetch("http://localhost:8000/v1/update_password",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        credentials:"include",
        body:JSON.stringify({
            email: email,
            password: password,
            newpassword: newpassword
        })
    })

    const data = await res.json();
    const msgElement = document.getElementById("msg");

    if(res.ok){
        msgElement.className = "success-message";
        msgElement.innerText = "Password updated successfully ✅";
    }
    else{
        msgElement.className = "error-message";
        msgElement.innerText = data.detail || "Update failed";
    }
}
