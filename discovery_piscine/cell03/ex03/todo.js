function addTask() {
    const taskList = document.getElementById('ft_list');
    const newTaskText = prompt('Enter a new task:');

    if (newTaskText !== null && newTaskText.trim() !== '') {
        const newTask = document.createElement('li');
        newTask.textContent = newTaskText.trim();
        const colors = ['lightblue',  'pink'];
        // สั่งให้ลบตัวเองเมื่อมีการคลิกที่รายการนี้
        newTask.onclick = function() {
            const deleteTask = newTask.textContent;
            const confirmed = confirm(`Are you sure you want to delete "${deleteTask}" task?`);
            if (confirmed === true) {
                this.remove();
                updateTaskCount(); // อัปเดตตัวนับหลังจากลบงานออก
            }
        };
        taskList.style.backgroundColor = colors[updateTaskCount() % colors.length]; // เปลี่ยนสีพื้นหลังของรายการงานเป็นสีขาวเมื่อมีงานใหม่ถูกเพิ่ม
        taskList.prepend(newTask);
        updateTaskCount();
    }
}

function updateTaskCount() {
    const taskList = document.getElementById('ft_list');
    const taskCount = document.getElementById('taskCount');
    const totalTasks = taskList.getElementsByTagName('li').length;
    taskCount.textContent = `Total tasks: ${totalTasks}`;
}
