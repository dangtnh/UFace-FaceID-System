(function(){
  const $ = (q)=>document.querySelector(q);
  const listWrap = $("#listWrap");
  const searchBox = $("#searchBox");
  const filterStatus = $("#filterStatus");
  const elPresent = $("#countPresent");
  const elTotal = $("#countTotal");
  if(!listWrap) return;

  // ====== CẤU HÌNH API VÀ TRẠNG THÁI ======
  const API_URL = 'http://localhost:8000/api/v1/face/recognize';
  const AUTO_ENROLL = true; // true: gặp ID mới -> tự thêm vào roster và cập nhật Total
  let isProcessingFrame = false; // Ngăn chặn gửi request liên tục

  // ====== Roster khởi tạo (ví dụ) ======
  // LƯU Ý: Roster này chỉ là DEMO. Trong thực tế, FE phải TẢI ROSTER TỪ API.
  const roster = [
    {id:"23BI1001", name:"Nguyen Van A", email:"a23bi1001@usth.edu.vn"},
    // ... giữ lại hoặc xóa các item demo cũ tùy ý ...
    {id:"23BI1010", name:"Phan Anh K",   email:"k23bi1010@usth.edu.vn"},
  ];

  // Dùng Map để tra nhanh và tránh trùng khóa
  const rosterMap = new Map(roster.map(s => [s.id, s]));
  const present = new Map(); // id -> {id,name,email,status,at,avatar}

  function updateTotals(){
    elTotal.textContent = rosterMap.size;
    elPresent.textContent = present.size;
  }

  function toast(msg, type = 'info'){
    const t = document.querySelector("#toast");
    if(!t) return;
    t.textContent = msg;
    t.className = `fixed left-1/2 top-6 -translate-x-1/2 rounded-lg text-sm px-4 py-2 z-50 transition ${type==='success' ? 'bg-green-600 text-white' : 'bg-black/80 text-white'}`;
    t.classList.remove("hidden");
    setTimeout(()=>t.classList.add("hidden"), 2000);
  }

  function renderList(){
    const kw = (searchBox?.value || "").trim().toLowerCase();
    const statusFilter = filterStatus?.value || "all";
    listWrap.innerHTML = "";
    // Sắp xếp theo thời gian check-in (at)
    const items = Array.from(present.values()).sort((a,b)=>a.at - b.at); 

    items.forEach(item=>{
      const matchesKw = !kw ||
        item.name.toLowerCase().includes(kw) ||
        item.id.toLowerCase().includes(kw) ||
        (item.email||"").toLowerCase().includes(kw);
      const matchesStatus = statusFilter==="all" || item.status===statusFilter;
      if(!matchesKw || !matchesStatus) return;

      const row = document.createElement("div");
      row.className="flex items-start gap-3 p-2 border rounded-xl bg-white/70";
      row.innerHTML = `
        <img src="${item.avatar || 'https://api.dicebear.com/9.x/thumbs/svg?seed='+encodeURIComponent(item.id)}"
             class="w-10 h-10 rounded-full border object-cover mt-0.5" />
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between gap-3">
            <p class="font-medium truncate">${item.name}</p>
            <span class="text-xs text-slate-500">${new Date(item.at).toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"})}</span>
          </div>
          <p class="text-xs text-slate-600 truncate">${item.id}</p>
          <p class="text-xs text-slate-500 truncate">${item.email || ""}</p>
        </div>
        <span class="${item.status==='late' ? 'chip chip-orange' : 'chip chip-green'}">
          ${item.status==='late' ? 'Late' : 'Present'}
        </span>
      `;
      listWrap.appendChild(row);
    });

    updateTotals();
  }

  // API FE để BE gọi khi nhận diện xong
  function pushPresence({id,name,avatar,email,status="present",at=Date.now()}){
    if (!id) return;

    // 1. Kiểm tra/Tự động thêm vào roster
    if(!rosterMap.has(id)){
      if (AUTO_ENROLL){
        rosterMap.set(id, {id, name: name||id, email: email||""});
      } else {
        console.warn(`[Attendance] Unknown student ${id} — ignored (STRICT MODE)`);
        toast(`Unknown student ${id} (ignored)`);
        return;
      }
    }

    // 2. Không cho trùng check-in
    if (present.has(id)) return;

    // 3. Thêm vào danh sách hiện tại
    const base = rosterMap.get(id);
    const item = {
      id,
      name: name || base.name,
      email: email || base.email,
      status: status.toLowerCase().includes("late") ? "late" : "present", // Chuyển đổi status từ BE
      at: new Date(at).getTime(), // Đảm bảo at là timestamp
      avatar
    };
    present.set(id, item);
    renderList();
    toast(`${item.name} checked in as ${item.status}`, 'success');
  }
  
  // =================================================================
  // HÀM GỌI API NHẬN DIỆN (Được gọi từ camera.js)
  // =================================================================
  async function sendFrameToAPI(blob) {
    if (isProcessingFrame) return;

    isProcessingFrame = true;
    
    const fd = new FormData();
    // Backend API /face/recognize đang đợi key là 'file'
    fd.append('file', blob, 'checkin_frame.jpg');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: fd,
            // Hủy request sau 5 giây nếu Backend chậm (Tùy chọn)
            signal: AbortSignal.timeout(5000) 
        });

        const result = await response.json();

        if (response.ok) {
            // Trường hợp nhận diện thành công
            if (result.status === "Match" || result.status === "ON TIME" || result.status === "LATE") {
                
                // Chuẩn hóa dữ liệu từ BE (mssv -> id, name, status, check_in_time -> at)
                const presenceData = {
                    id: result.mssv,
                    name: result.name,
                    status: result.status, 
                    at: result.check_in_time ? new Date().setHours(...result.check_in_time.split(':').map(Number)) : Date.now(), // Tạo timestamp giả định
                    // BE có thể trả về avatar/email, nếu không thì lấy từ rosterMap
                };
                
                pushPresence(presenceData); // Đẩy vào danh sách điểm danh
            } 
            // KHÔNG TOAST nếu là "No Face" hoặc "Unknown" để tránh làm phiền
        } else {
            // Xử lý lỗi từ server (400, 500)
            if (result.detail && result.detail !== "No face detected" && result.detail !== "Unknown student") {
                 console.error("API Error:", result.detail);
                 toast(`Server Error: ${result.detail}`, 'error');
            }
        }

    } catch (error) {
        if (error.name !== 'TimeoutError') { // Bỏ qua lỗi timeout (vì nó thường xuyên xảy ra)
             console.error("Fetch Error:", error);
        }
    } finally {
        isProcessingFrame = false; // Mở khóa để gửi frame tiếp theo
    }
  }


  // Expose hàm xử lý API ra ngoài để camera.js gọi
  window.attendanceHandler = sendFrameToAPI; 
  window.Attendance = { pushPresence };

  searchBox?.addEventListener("input", renderList);
  filterStatus?.addEventListener("change", renderList);

  // ==== XÓA Demo queue cũ ====
  // TÍNH NĂNG ĐIỂM DANH THẬT ĐÃ THAY THẾ CHO DEMO NÀY

  // init totals UI
  updateTotals();
})();