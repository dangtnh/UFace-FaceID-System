(function(){
  const $ = (q) => document.querySelector(q);

  let stream = null;
  let facing = "user"; 
  let captureInterval = null; 

  // ID các element trong HTML
  const VIDEO_ID = "#liveVideo";        
  const OVERLAY_ID = "#overlayCanvas";  
  
  // Canvas ẩn dùng để chụp ảnh gửi API
  const captureCanvas = document.createElement('canvas'); 

  function setBadge(text, variant){
    const el = $("#cameraStatus") || $("#statusBadge"); 
    if(!el) return; 
    
    const map = {
      ok: "text-green-700 bg-green-100",
      off: "text-amber-700 bg-amber-100",
      err: "text-red-700 bg-red-100",
    };
    el.className = `text-[10px] px-1.5 py-0.5 rounded font-medium ${map[variant] || map.off}`;
    el.textContent = text;
  }

  function showToast(msg){
    const el = $("#toast"); if(!el) return;
    el.textContent = msg;
    el.classList.remove("hidden");
    if(el.hideTimeout) clearTimeout(el.hideTimeout);
    el.hideTimeout = setTimeout(()=>el.classList.add("hidden"), 2000);
  }

  // --- Chụp frame từ video ---
  async function captureFrame() {
    const video = $(VIDEO_ID);
    if (!video || !stream) return null;

    const w = video.videoWidth;
    const h = video.videoHeight;
    if (w === 0 || h === 0) return null;

    captureCanvas.width = w;
    captureCanvas.height = h;

    const ctx = captureCanvas.getContext('2d');
    ctx.drawImage(video, 0, 0, w, h);

    return new Promise(res => captureCanvas.toBlob(res, 'image/jpeg', 0.8));
  }

  // --- Mở Camera & Bắt đầu loop gửi ảnh ---
  async function openCam(captureCallback){
    if(stream) return;
    try{
      stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: facing, width: {ideal: 640}, height: {ideal: 480} },
        audio: false
      });
      
      const video = $(VIDEO_ID);
      if(video) {
        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
            video.play();
            
            // Loop chụp ảnh mỗi 300ms
            if (captureCallback && !captureInterval) {
                captureInterval = setInterval(async () => {
                    const blob = await captureFrame();
                    if (blob) captureCallback(blob); 
                }, 300); 
            }
        };
      }
      
      setBadge("Camera's on", "ok");
      showToast("Camera started");
    } catch(e){
      console.error(e);
      setBadge("Error", "err");
      showToast("Lỗi mở Camera. Kiểm tra quyền truy cập.");
    }
  }

  // --- Tắt Camera & Dọn dẹp ---
  function stopCam(){
    if(!stream) return;
    
    if (captureInterval) {
        clearInterval(captureInterval);
        captureInterval = null;
    }

    stream.getTracks().forEach(t => t.stop());
    stream = null;
    
    const video = $(VIDEO_ID); 
    if(video) video.srcObject = null;

    // Xóa hình vẽ cũ trên Canvas overlay
    const overlay = $(OVERLAY_ID);
    if(overlay){
        const ctx = overlay.getContext('2d');
        ctx.clearRect(0, 0, overlay.width, overlay.height);
    }

    setBadge("Camera's off", "off");
    showToast("Camera stopped");
  }

  async function switchCam(){
    facing = (facing==="user") ? "environment" : "user";
    if(stream) {
        stopCam();
        setTimeout(() => openCam(window.attendanceHandler), 200);
    }
  }

  function initButtons(){
    // Tìm nút bật cam (ID openCamBtn hoặc btnToggleCam)
    const btn = $("#openCamBtn") || $("#btnToggleCam");
    
    btn?.addEventListener("click", () => {
        if (!stream) {
            openCam(window.attendanceHandler); 
            if(btn.tagName === "BUTTON") {
                btn.textContent = "Stop Camera";
                btn.classList.add("bg-red-500");
            }
        } else {
            stopCam();
            if(btn.tagName === "BUTTON") {
                btn.textContent = "Start Camera";
                btn.classList.remove("bg-red-500");
            }
        }
    });
  }

  window.CameraCtrl = { openCam, stopCam, switchCam };

  document.addEventListener("DOMContentLoaded", ()=>{
    initButtons();
  });
})();