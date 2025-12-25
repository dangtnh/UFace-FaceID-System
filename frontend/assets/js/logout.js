// assets/js/logout.js

document.addEventListener("DOMContentLoaded", function() {
    const logoutBtn = document.getElementById("logoutBtn");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", async function(e) {
            e.preventDefault();
            
            if (!confirm("Are you sure you want to logout?")) return;
    
            const token = localStorage.getItem("accessToken");
            const API_URL = "http://localhost:8000/api/v1/users"; 
    
            if (token) {
                try {
                    await fetch(`${API_URL}/logout`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${token}`
                        }
                    });
                } catch (error) {
                    console.error("Logout API error:", error);
                }
            }
    
            localStorage.removeItem("accessToken");
            localStorage.removeItem("userInfo");
            window.location.href = "/pages/admin-login.html";
        });
    }
});