
$(document).ready(function() {
    // ฟังก์ชันสำหรับนับและอัปเดตจำนวนรายการงานทั้งหมด
    function updateTaskCount() {
        var count = $(".task-item").length;
        $("#taskCount").text("Total tasks: " + count);
    }

    // 1. ตรวจจับการคลิกที่ปุ่ม "New" (id="addTaskButton")
    $("#addTaskButton").on("click", function() {
        console.log("New task button clicked");
        // แจ้งเตือนให้ผู้ใช้กรอกชื่องาน
        var taskText = prompt("กรอกรายการงานที่คุณต้องการทำ:");
        
        // ตรวจสอบว่าผู้ใช้พิมพ์ข้อความจริง ไม่ได้กด Cancel หรือปล่อยว่าง
        if (taskText && taskText.trim() !== "") {
            // สร้างโครงสร้าง HTML สำหรับรายการงานใหม่ พร้อมปุ่มลบ
            var newTask = $("<div class='task-item'></span>")
                .html("<span>" + taskText + " </span>");
            
            // แทรกชิ้นส่วน HTML ใหม่เข้าไปในกล่อง id="ft_list"
            $("#ft_list").append(newTask);
            
            // อัปเดตตัวเลขแสดงจำนวนงาน
            updateTaskCount();
        }
    });

    // 2. ตรวจจับการคลิกปุ่มลบ (X) 
    // ใช้ Delegation เนื่องจากปุ่มลบถูกสร้างขึ้นมาใหม่แบบ Dynamic หลังจากโหลดหน้าเว็บ
    $("#ft_list").on("click", ".task-item", function() {
            const deleteTask = $(this).text().trim();
            const confirmed = confirm(`Are you sure you want to delete "${deleteTask}" task?`);
            if (confirmed === true) {
                // ลบกล่องงานแถวนั้นออกไป (.task-item)
                $(this).remove();
                updateTaskCount(); // อัปเดตตัวนับหลังจากลบงานออก
            }

        
    });
});
