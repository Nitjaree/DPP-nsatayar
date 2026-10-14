$(document).ready(function() {
    // ดักจับเหตุการณ์เมื่อผู้ใช้คลิกปุ่มที่มี id="calculate"
    $('#calculate').on('click', function() {
        // ดึงค่าจาก input และแปลงเป็นตัวเลข (Float) ด้วย jQuery
        var num1 = parseFloat($('#number1').val());
        var num2 = parseFloat($('#number2').val());
        var operation = $('#operation').val();
        var result = 0;

        // ตรวจสอบความถูกต้องของข้อมูลเบื้องต้น
        if (isNaN(num1) || isNaN(num2)) {
            alert('Error :(');
            return;
        }

        // คํานวณตามเครื่องหมายที่เลือก
        switch(operation) {
            case 'add':
                result = num1 + num2;
                break;
            case 'subtract':
                result = num1 - num2;
                break;
            case 'multiply':
                result = num1 * num2;
                break;
            case 'divide':
                if (num2 === 0) {
                    alert('"It\'s over 9000!"');
                    return;
                }
                result = num1 / num2;
                break;
            case 'modulo':
                if (num2 === 0) {
                    alert('"It\'s over 9000!"');
                    return;
                }
                result = num1 % num2;
                break;
            default:
                result = 'Invalid Operation';
        }

        // แสดงผลลัพธ์ลงในแท็ก p ที่มี id="result" ด้วย jQuery
        alert(`The result of ${operation} is ${result}.`);
    });
});
