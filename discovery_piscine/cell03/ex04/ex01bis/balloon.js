$(document).ready(function() {
    
    // 1. เหตุการณ์เมื่อคลิกที่ลูกโป่ง (Expand)
    $('div').on('click', function() {
        var $balloon = $(this);
        var currentWidth = $balloon.width(); // ดึงขนาดความกว้างปัจจุบันออกมาเป็นตัวเลขได้ทันที
        var newSize;

        if (currentWidth < 420) {
            newSize = currentWidth + 10;
        } else {
            newSize = 200;
        }

        // ปรับขนาดความกว้างและความสูงพร้อมกันด้วย jQuery .css()
        $balloon.css({
            'width': newSize + 'px',
            'height': newSize + 'px'
        });

        // ดึงสีปัจจุบัน (ส่งค่ากลับมาเป็น rgb) แล้วเปลี่ยนสี
        var currentColor = $balloon.css('background-color');
        var newColor = changeColor(currentColor);
        $balloon.css('background-color', newColor);
    });

    // 2. เหตุการณ์เมื่อเมาส์ออกจากลูกโป่ง (Shrink)
    $('div').on('mouseleave', function() { // ใช้ mouseleave แทน onmouseout เพื่อป้องกันการเกิด event ซ้อนภายใน
        var $balloon = $(this);
        var currentWidth = $balloon.width();
        var newSize;

        if (currentWidth > 200) {
            newSize = currentWidth - 5;
        } else {
            newSize = 200;
        }

        $balloon.css({
            'width': newSize + 'px',
            'height': newSize + 'px'
        });

        var currentColor = $balloon.css('background-color');
        var newColor = reverseColor(currentColor);
        $balloon.css('background-color', newColor);
    });

});

// ฟังก์ชันเปลี่ยนสีเมื่อคลิก (คำนวณจากค่า RGB ที่ jQuery ดึงออกมา)
function changeColor(color) {
    if (color === 'rgb(255, 0, 0)' || color === 'red') {
        return 'green';
    } else if (color === 'rgb(0, 128, 0)' || color === 'green') {
        return 'blue';
    } else {
        return 'red';
    }
}

// ฟังก์ชันย้อนสีเมื่อเมาส์ออก (คำนวณจากค่า RGB ที่ jQuery ดึงออกมา)
function reverseColor(color) {
    if (color === 'rgb(255, 0, 0)' || color === 'red') {
        return 'blue';
    } else if (color === 'rgb(0, 0, 255)' || color === 'blue') {
        return 'green';
    } else {
        return 'red';
    }
}
