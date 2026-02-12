async function register() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch("http://localhost:8000/v1/register",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        credentials:"include",
        body:JSON.stringify({
            username: username,
            email: email,
            password: password
        })
    })

    const data = await res.json();
    const msgElement = document.getElementById("msg");

    if(res.ok){
        msgElement.className = "success-message";
        msgElement.innerText = "Registration Successful ✅";
        
        setTimeout(() => {
            window.location.href = "dashboard.html";
        }, 1500);
    }
    else{
        msgElement.className = "error-message";
        msgElement.innerText = data.detail || "Registration failed";
    }
}
