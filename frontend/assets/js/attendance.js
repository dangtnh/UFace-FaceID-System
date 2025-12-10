(function () {
  const $ = (q) => document.querySelector(q);
  const listWrap = $("#listWrap");
  const searchBox = $("#searchBox");
  const filterStatus = $("#filterStatus");
  const elPresent = $("#countPresent");
  const elTotal = $("#countTotal");
  if (!listWrap) return;

  // ====== CẤU HÌNH API VÀ TRẠNG THÁI ======
  const API_URL = "http://localhost:8000/api/v1/face/recognize";
  const AUTO_ENROLL = false; // Tắt tự động thêm (chỉ nhận diện ai có trong DB)
  let isProcessingFrame = false; // Cờ khóa để ngăn gửi request dồn dập

  // ====== Roster giả lập (Để hiển thị Total ban đầu) ======
  // Trong thực tế, bạn nên gọi API để lấy danh sách lớp học
  const roster = [
    { id: "23BI1001", name: "Nguyen Van A", email: "a23bi1001@usth.edu.vn" },
    { id: "23BI1010", name: "Phan Anh K", email: "k23bi1010@usth.edu.vn" },
  ];

  const rosterMap = new Map(roster.map((s) => [s.id, s]));
  const present = new Map(); // id -> {id,name,email,status,at,avatar}

  function updateTotals() {
    elTotal.textContent = rosterMap.size;
    elPresent.textContent = present.size;
  }

  // Hàm hiển thị thông báo (Toast)
  // type: 'info', 'success', 'warning', 'error'
  function toast(msg, type = "info") {
    const t = document.querySelector("#toast");
    if (!t) return;
    t.textContent = msg;

    let bgClass = "bg-black/80 text-white"; // Default (Info)
    if (type === "success") bgClass = "bg-green-600 text-white";
    if (type === "warning") bgClass = "bg-yellow-500 text-black";
    if (type === "error") bgClass = "bg-red-600 text-white";

    t.className = `fixed left-1/2 top-6 -translate-x-1/2 rounded-lg text-sm px-4 py-2 z-50 transition ${bgClass}`;
    t.classList.remove("hidden");

    // Xóa timeout cũ nếu có để tránh ẩn nhầm
    if (t.hideTimeout) clearTimeout(t.hideTimeout);
    t.hideTimeout = setTimeout(() => t.classList.add("hidden"), 3000);
  }

  function renderList() {
    const kw = (searchBox?.value || "").trim().toLowerCase();
    const statusFilter = filterStatus?.value || "all";
    listWrap.innerHTML = "";
    // Sắp xếp theo thời gian check-in mới nhất lên đầu
    const items = Array.from(present.values()).sort((a, b) => b.at - a.at);

    items.forEach((item) => {
      const matchesKw =
        !kw ||
        item.name.toLowerCase().includes(kw) ||
        item.id.toLowerCase().includes(kw) ||
        (item.email || "").toLowerCase().includes(kw);
      const matchesStatus =
        statusFilter === "all" || item.status === statusFilter;
      if (!matchesKw || !matchesStatus) return;

      const row = document.createElement("div");
      row.className =
        "flex items-start gap-3 p-2 border rounded-xl bg-white/70";
      row.innerHTML = `
        <img src="${
          item.avatar ||
          "https://api.dicebear.com/9.x/thumbs/svg?seed=" +
            encodeURIComponent(item.id)
        }"
             class="w-10 h-10 rounded-full border object-cover mt-0.5" />
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between gap-3">
            <p class="font-medium truncate">${item.name}</p>
            <span class="text-xs text-slate-500">${new Date(
              item.at
            ).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}</span>
          </div>
          <p class="text-xs text-slate-600 truncate">${item.id}</p>
          <p class="text-xs text-slate-500 truncate">${item.email || ""}</p>
        </div>
        <span class="${
          item.status === "late" ? "chip chip-orange" : "chip chip-green"
        }">
          ${item.status === "late" ? "Late" : "Present"}
        </span>
      `;
      listWrap.appendChild(row);
    });

    updateTotals();
  }

  // Hàm thêm vào danh sách điểm danh (Gọi nội bộ sau khi API trả về)
  function pushPresence({
    id,
    name,
    avatar,
    email,
    status = "present",
    at = Date.now(),
  }) {
    if (!id) return;

    // 1. Nếu chưa có trong danh sách tổng, thêm vào (nếu AUTO_ENROLL bật)
    if (!rosterMap.has(id)) {
      if (AUTO_ENROLL) {
        rosterMap.set(id, { id, name: name || id, email: email || "" });
      }
      // Nếu không AUTO_ENROLL thì vẫn cho hiện lên nhưng không cộng vào Total Roster
    }

    // 2. Nếu đã điểm danh rồi thì bỏ qua (hoặc update thời gian nếu cần)
    if (present.has(id)) return;

    // 3. Chuẩn bị dữ liệu hiển thị
    const base = rosterMap.get(id) || {};
    const item = {
      id,
      name: name || base.name || id,
      email: email || base.email || "",
      status: status.toLowerCase().includes("late") ? "late" : "present",
      at: new Date(at).getTime(),
      avatar,
    };

    present.set(id, item);
    renderList();
    
    // Toast thông báo thành công
    const msgStatus = item.status === 'late' ? 'Muộn' : 'Đúng giờ';
    toast(`✅ ${item.name} - ${msgStatus}`, item.status === 'late' ? 'warning' : 'success');
  }

  // =================================================================
  // HÀM GỌI API NHẬN DIỆN (Được gọi từ camera.js)
  // =================================================================
  async function sendFrameToAPI(blob) {
    if (isProcessingFrame) return; // Nếu đang xử lý frame trước thì bỏ qua frame này

    isProcessingFrame = true;

    const fd = new FormData();
    fd.append("file", blob, "checkin_frame.jpg");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: fd,
        signal: AbortSignal.timeout(8000), // Timeout 8s
      });

      // Backend trả về JSON dù thành công hay lỗi (400)
      const result = await response.json();

      // --- XỬ LÝ LOGIC ---
      if (result.status === "success") {
        // 1. NHẬN DIỆN THÀNH CÔNG
        const presenceData = {
          id: result.mssv,
          name: result.name,
          // Backend trả về 'attendance_status': 'ON TIME' hoặc 'LATE'
          status: result.attendance_status === "LATE" ? "late" : "present",
          at: Date.now(),
        };
        pushPresence(presenceData);

      } else if (result.status === "unknown") {
        // 2. NGƯỜI LẠ (UNKNOWN) -> Hiện cảnh báo vàng
        console.warn("Unknown face detected");
        toast("⚠️ Người lạ! Vui lòng đăng ký khuôn mặt.", "warning");

      } else {
        // 3. CÁC TRƯỜNG HỢP KHÁC (No face, lỗi xử lý...)
        // Không làm gì hoặc log nhẹ để debug, tránh spam toast lỗi
        if (result.detail && result.detail !== "No face detected") {
           console.log("API Info:", result.detail);
        }
      }

    } catch (error) {
      // Bỏ qua lỗi timeout hoặc mạng chập chờn để không làm gián đoạn UI camera
      if (error.name !== "TimeoutError" && error.name !== "AbortError") {
        console.error("Fetch Error:", error);
      }
    } finally {
      // Mở khóa để xử lý frame tiếp theo sau một khoảng delay nhỏ
      // Giúp UI đỡ bị giật nếu API trả về quá nhanh
      setTimeout(() => {
        isProcessingFrame = false;
      }, 500); 
    }
  }

  // Expose hàm xử lý API ra ngoài để camera.js gọi
  window.attendanceHandler = sendFrameToAPI;

  // Lắng nghe sự kiện UI
  searchBox?.addEventListener("input", renderList);
  filterStatus?.addEventListener("change", renderList);

  // Khởi tạo UI
  updateTotals();
})();