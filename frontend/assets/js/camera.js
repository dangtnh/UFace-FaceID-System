(function(){
  // Sử dụng ID chuẩn từ HTML
  const $ = (q)=>document.querySelector(q);

  let stream = null;
  let facing = "user"; // or "environment"
  let captureInterval = null; // Biến để lưu trữ interval

  function setBadge(text, variant){
    // Dùng ID #statusBadge
    const el = $("#statusBadge"); if(!el) return; 
    const map = {
      ok: "text-green-700 bg-green-100 rounded px-2 py-0.5",
      off: "text-amber-700 bg-amber-100 rounded px-2 py-0.5",
      err: "text-red-700 bg-red-100 rounded px-2 py-0.5",
    };
    el.textContent = text;
    el.className = `text-xs font-medium ${map[variant] || map.off}`; 
  }

  function showToast(msg){
    const el = $("#toast"); if(!el) return;
    el.textContent = msg;
    el.classList.remove("hidden");
    setTimeout(()=>el.classList.add("hidden"), 1500);
  }

  // Hàm chụp ảnh và chuyển thành Blob
  async function captureFrame() {
    const video = $("#video");
    const canvas = $("#canvas");
    if (!video || !canvas || !stream) return null;

    const w = video.videoWidth;
    const h = video.videoHeight;
    if (w === 0 || h === 0) return null;

    canvas.width = w;
    canvas.height = h;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, w, h);

    // Trả về Blob (file ảnh)
    return new Promise(res => canvas.toBlob(res, 'image/jpeg', 0.8));
  }


  async function openCam(captureCallback){
    if(stream) return;
    try{
      stream = await navigator.mediaDevices.getUserMedia({
        video:{facingMode:facing, width:{ideal:640}, height:{ideal:480}},
        audio:false
      });
      const video = $("#video");
      if(video) {
        video.srcObject = stream;
        
        // Bắt đầu chụp định kỳ nếu có callback
        if (captureCallback && !captureInterval) {
            video.onloadedmetadata = () => {
                video.play();
                captureInterval = setInterval(async () => {
                    const blob = await captureFrame();
                    if (blob) {
                        captureCallback(blob); // Gọi hàm xử lý API bên ngoài
                    }
                }, 1000); // Chụp mỗi 1 giây (1000ms)
            };
        }
      }
      
      setBadge("Camera's on", "ok");
      showToast("Camera started");
    }catch(e){
      console.error(e);
      setBadge("Camera error", "err");
      showToast("Failed to open camera. Use HTTPS/localhost & allow permission.");
    }
  }

  function stopCam(){
    if(!stream) return;
    
    // DỪNG INTERVAL KHI DỪNG CAMERA
    if (captureInterval) {
        clearInterval(captureInterval);
        captureInterval = null;
    }

    stream.getTracks().forEach(t=>t.stop());
    stream = null;
    const video = $("#video"); if(video) video.srcObject = null;
    setBadge("Camera's off", "off");
    showToast("Camera stopped");
  }

  async function switchCam(){
    facing = (facing==="user") ? "environment" : "user";
    // Giả định hàm captureCallback được lưu trong window.attendanceHandler
    if(stream) stopCam();
    await openCam(window.attendanceHandler); // Truyền lại hàm xử lý
  }

  function initButtons(){
    // Gắn sự kiện cho nút #openCamBtn
    $("#openCamBtn")?.addEventListener("click", () => {
        if (!stream) {
            openCam(window.attendanceHandler); // Mở camera và bắt đầu gửi frame
        } else {
            stopCam(); // Tắt camera nếu đang bật
        }
    });
    // Đã xóa phần lỗi cú pháp ở đây
  }

  // Clock helper (nếu có #clock)
  function startClock(){
    const clock = $("#clock"); if(!clock) return;
    const tick = ()=> clock.textContent = new Date().toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"});
    tick(); setInterval(tick, 1000);
  }

  // Expose
  window.CameraCtrl = { openCam, stopCam, switchCam };

  // Auto init if elements exist
  document.addEventListener("DOMContentLoaded", ()=>{
    initButtons();
    startClock();
  });
})();