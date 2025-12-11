(function () {
  const $ = (q) => document.querySelector(q);
  const listWrap = $("#listWrap");
  const searchBox = $("#searchBox");
  const filterStatus = $("#filterStatus");
  const elPresent = $("#countPresent");
  const elTotal = $("#countTotal");
  
  const videoEl = document.getElementById('liveVideo');
  const canvasEl = document.getElementById('overlayCanvas');
  const ctx = canvasEl ? canvasEl.getContext('2d') : null;

  if (!listWrap) return;

  const API_URL = "http://localhost:8000/api/v1/face/recognize";
  const AUTO_ENROLL = false; 
  let isProcessingFrame = false; 

  const roster = [
    { id: "23BI1001", name: "Nguyen Van A", email: "a23bi1001@usth.edu.vn" },
    { id: "23BI1010", name: "Phan Anh K", email: "k23bi1010@usth.edu.vn" },
  ];

  const rosterMap = new Map(roster.map((s) => [s.id, s]));
  const present = new Map(); 

  function updateTotals() {
    elTotal.textContent = rosterMap.size;
    elPresent.textContent = present.size;
  }

  function toast(msg, type = "info") {
    const t = document.querySelector("#toast");
    if (!t) return;
    t.textContent = msg;

    let bgClass = "bg-black/80 text-white"; 
    if (type === "success") bgClass = "bg-green-600 text-white";
    if (type === "warning") bgClass = "bg-yellow-500 text-black";
    if (type === "error") bgClass = "bg-red-600 text-white";

    t.className = `fixed left-1/2 top-6 -translate-x-1/2 rounded-lg text-sm px-4 py-2 z-50 transition ${bgClass}`;
    t.classList.remove("hidden");
    if (t.hideTimeout) clearTimeout(t.hideTimeout);
    t.hideTimeout = setTimeout(() => t.classList.add("hidden"), 3000);
  }

  function renderList() {
    const kw = (searchBox?.value || "").trim().toLowerCase();
    const statusFilter = filterStatus?.value || "all";
    listWrap.innerHTML = "";
    const items = Array.from(present.values()).sort((a, b) => b.at - a.at);

    items.forEach((item) => {
      const matchesKw = !kw || item.name.toLowerCase().includes(kw) || item.id.toLowerCase().includes(kw);
      const matchesStatus = statusFilter === "all" || item.status === statusFilter;
      if (!matchesKw || !matchesStatus) return;

      const row = document.createElement("div");
      row.className = "flex items-start gap-3 p-2 border rounded-xl bg-white/70";
      row.innerHTML = `
        <img src="${item.avatar || "https://api.dicebear.com/9.x/thumbs/svg?seed=" + encodeURIComponent(item.id)}"
             class="w-10 h-10 rounded-full border object-cover mt-0.5" />
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between gap-3">
            <p class="font-medium truncate">${item.name}</p>
            <span class="text-xs text-slate-500">${new Date(item.at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
          </div>
          <p class="text-xs text-slate-600 truncate">${item.id}</p>
        </div>
        <span class="${item.status === "late" ? "chip chip-orange" : "chip chip-green"}">
          ${item.status === "late" ? "Late" : "Present"}
        </span>
      `;
      listWrap.appendChild(row);
    });
    updateTotals();
  }

  function pushPresence({ id, name, avatar, email, status = "present", at = Date.now() }) {
    if (!id || id === "Unknown") return; 
    if (!rosterMap.has(id) && AUTO_ENROLL) rosterMap.set(id, { id, name: name || id });
    if (present.has(id)) return;
    present.set(id, { id, name, status, at, avatar });
    renderList();
    const msgStatus = item.status === 'late' ? 'Muộn' : 'Đúng giờ';
    toast(`✅ ${item.name} - ${msgStatus}`, item.status === 'late' ? 'warning' : 'success');
  }

  // =================================================================
  // HÀM VẼ KHUNG (Đã sửa hiển thị Score dạng 0.xx)
  // =================================================================
  function drawBox(result) {
      if (!ctx || !canvasEl || !videoEl) return;

      // 1. FIX LỖI TREO KHUNG KHI TẮT CAM
      if (videoEl.paused || videoEl.ended || !videoEl.srcObject) {
          ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
          return;
      }

      // 2. Đồng bộ kích thước
      if (videoEl.videoWidth && canvasEl.width !== videoEl.videoWidth) {
          canvasEl.width = videoEl.videoWidth;
          canvasEl.height = videoEl.videoHeight;
      }

      ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);

      if (result && result.box) {
          const { x1, y1, x2, y2 } = result.box;
          const width = x2 - x1;
          const height = y2 - y1;

          // 3. FIX CHỮ NGƯỢC: Lật tọa độ X (Mirror)
          const mirroredX = canvasEl.width - x2;

          const isMatch = result.status === 'Match' || result.status === 'success';
          const color = isMatch ? '#00E676' : '#FFD600'; 
          
          // Vẽ khung
          ctx.beginPath();
          ctx.lineWidth = 4;
          ctx.strokeStyle = color;
          ctx.roundRect(mirroredX, y1, width, height, 8); 
          ctx.stroke();

          // 4. FIX MSSV + FORMAT SCORE (0.96)
          // --- THAY ĐỔI TẠI ĐÂY ---
          const scoreDisplay = result.score.toFixed(2); // VD: 0.96
          
          let labelText = result.name;
          if (result.mssv && result.mssv !== "Unknown" && result.mssv !== "") {
              labelText = `${result.mssv} - ${result.name}`;
          }
          
          // Format text: "23BI... - Tên (0.96)"
          const text = `${labelText} (${scoreDisplay})`;
          
          ctx.font = "bold 18px sans-serif";
          const textMetrics = ctx.measureText(text);
          const textHeight = 28;

          // Vẽ nền chữ
          ctx.fillStyle = color;
          ctx.beginPath();
          ctx.roundRect(mirroredX, y1 - textHeight - 4, textMetrics.width + 12, textHeight, 4);
          ctx.fill();

          // Vẽ chữ
          ctx.fillStyle = '#000';
          ctx.textBaseline = 'middle';
          ctx.fillText(text, mirroredX + 6, y1 - (textHeight/2) - 3);
      }
  }

  // =================================================================
  // HÀM GỌI API
  // =================================================================
  async function sendFrameToAPI(blob) {
    if (isProcessingFrame) return;
    
    if (videoEl.paused || videoEl.ended) return;

    isProcessingFrame = true;
    const fd = new FormData();
    fd.append("file", blob, "checkin_frame.jpg");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: fd,
        signal: AbortSignal.timeout(8000),
      });

      const result = await response.json();
      
      drawBox(result);

      if (result.status === "success" || result.status === "Match") {
        pushPresence({
          id: result.mssv,
          name: result.name,
          status: result.attendance_status === "LATE" ? "late" : "present",
          at: Date.now(),
        });

      } else if (result.status === "unknown") {
        toast("⚠️ Người lạ! Vui lòng đăng ký khuôn mặt.", "warning");
      }

    } catch (error) {
      if (error.name !== "TimeoutError" && error.name !== "AbortError") {
        console.error("Fetch Error:", error);
      }
      if (ctx) ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
    } finally {
      setTimeout(() => { isProcessingFrame = false; }, 150);
    }
  }

  window.attendanceHandler = sendFrameToAPI;
  searchBox?.addEventListener("input", renderList);
  filterStatus?.addEventListener("change", renderList);
  updateTotals();
})();