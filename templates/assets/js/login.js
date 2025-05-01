function toggleUser() {
    // creates a variable to store users' choice
    let selectedPlan = document.querySelector('input[name="user-type"]:checked').value

    if (selectedPlan === "user"){
      document.getElementById("user-name").style.display = "block"
      document.getElementById("admin-name").style.display = "none"
      document.getElementById("user-email").style.display = "block"
      document.getElementById("admin-email").style.display = "none"
      document.getElementById("user-phone").style.display = "block"
      document.getElementById("admin-phone").style.display = "none"
    }
    else{
        document.getElementById("user-name").style.display = "none"
        document.getElementById("admin-name").style.display = "block"
        document.getElementById("user-email").style.display = "none"
        document.getElementById("admin-email").style.display = "block"
        document.getElementById("user-phone").style.display = "none"
        document.getElementById("user-location").style.display = "none"
        document.getElementById("admin-phone").style.display = "block"
    }
}