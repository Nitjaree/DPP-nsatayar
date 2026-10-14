$(document).ready(function() {
    // ดักจับเหตุการณ์เมื่อคลิกปุ่ม button
    $('button').on('click', function() {
        var bgcolor = randomColor();
        // เปลี่ยนสีพื้นหลังของ body ด้วยคำสั่ง .css() ของ jQuery
        $('body').css('background-color', bgcolor);
    });
});

// ฟังก์ชันสุ่มรหัสสี HEX (คงเดิมไว้เนื่องจากเป็น Logic ในการสุ่มตัวเลข)
function randomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
