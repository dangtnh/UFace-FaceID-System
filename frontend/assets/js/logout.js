document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logoutBtn");
    if (!logoutBtn) return;
  
    injectLogoutModal();
  
    const modal = document.getElementById("confirmLogoutModal");
    const cancelBtn = document.getElementById("btnCancelLogout");
    const confirmBtn = document.getElementById("btnConfirmLogout");
  
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      modal.classList.add("open");
    });
  
    cancelBtn.addEventListener("click", () => {
      modal.classList.remove("open");
    });
  
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.classList.remove("open");
    });
  
    confirmBtn.addEventListener("click", async () => {
      confirmBtn.innerHTML = "Logging out...";
      confirmBtn.disabled = true;
      confirmBtn.style.opacity = "0.7";
  
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
      
      setTimeout(() => {
          window.location.href = "/pages/admin-login.html";
      }, 500);
    });
  });
  
  function injectLogoutModal() {
    if (document.getElementById("confirmLogoutModal")) return;
  
    const modalHTML = `
      <div class="logout-modal-overlay" id="confirmLogoutModal">
        <div class="logout-modal">
          <div class="lm-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </div>
          <div class="lm-content">
            <h3>Sign Out?</h3>
            <p>Are you sure you want to end your session?</p>
          </div>
          <div class="lm-actions">
            <button class="lm-btn cancel" id="btnCancelLogout">Cancel</button>
            <button class="lm-btn confirm" id="btnConfirmLogout">Sign Out</button>
          </div>
        </div>
      </div>
      
      <style>
        .logout-modal-overlay {
          position: fixed; inset: 0; background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(4px);
          display: none; align-items: center; justify-content: center; z-index: 9999;
          animation: fadeIn 0.2s ease-out;
        }
        .logout-modal-overlay.open { display: flex; }
        .logout-modal {
          background: #ffffff; border-radius: 24px; padding: 24px; width: 320px;
          box-shadow: 0 20px 50px rgba(0,0,0,0.15); text-align: center;
          transform: scale(0.95); transition: transform 0.2s;
          animation: popIn 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .logout-modal-overlay.open .logout-modal { transform: scale(1); }
        .lm-icon {
          width: 60px; height: 60px; margin: 0 auto 16px; background: #fee2e2; color: #ef4444;
          border-radius: 50%; display: flex; align-items: center; justify-content: center;
        }
        .lm-content h3 { margin: 0 0 8px; font-size: 18px; font-weight: 600; color: #111827; }
        .lm-content p { margin: 0 0 24px; font-size: 13px; color: #6b7280; line-height: 1.5; }
        .lm-actions { display: flex; gap: 12px; }
        .lm-btn {
          flex: 1; padding: 10px; border-radius: 12px; border: none;
          font-size: 13px; font-weight: 500; cursor: pointer; transition: 0.1s;
        }
        .lm-btn.cancel { background: #f3f4f6; color: #374151; }
        .lm-btn.cancel:hover { background: #e5e7eb; }
        .lm-btn.confirm { background: #ef4444; color: #ffffff; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25); }
        .lm-btn.confirm:hover { background: #dc2626; transform: translateY(-1px); }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes popIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
      </style>
    `;
    document.body.insertAdjacentHTML("beforeend", modalHTML);
  }