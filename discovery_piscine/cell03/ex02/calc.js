function calculate() {
        document.getElementById('calculate').addEventListener('click', function() {
            const input1 = document.getElementById('number1').value;
            const input2 = document.getElementById('number2').value;
            const operation = document.getElementById('operation').value;
            if (input1.trim() === '' || input2.trim() === '') {
                alert('Error :(');
                return;
            }
            if(isNaN(input1) || isNaN(input2)) {
                alert('Error :(');
                return;
            }
            const number1 = parseFloat(input1);
            const number2 = parseFloat(input2);
            if (number1 < 0 || number2 < 0) {
                alert('Error :(');
                return;
            }  
            if (isNaN(number1) || isNaN(number2)) {
                // alert('Error :(');
            } else {
                let result;
                switch (operation) {
                    case 'add':
                        result = number1 + number2;
                        break;
                    case 'subtract':
                        result = number1 - number2              ;
                        break;
                    case 'multiply':
                        result = number1 * number2;
                        break;
                    case 'divide':
                        if (number2 === 0) {
                             alert('"It\'s over 9000!"');
                            return;
                        }
                        result = number1 / number2;
                        break;
                    case 'modulo':
                        if (number2 === 0) {
                             alert('"It\'s over 9000!"');
                            return;
                        }   
                        result = number1 % number2;
                        break;
                }
                alert(`The result of ${operation} is ${result}.`);
                console.log(`The result of ${operation} is ${result}.`);
            }
        });
    }


function handleNotUsedEvent(event) {
    alert('Please, use me...');
}
setInterval(handleNotUsedEvent, 30000);
