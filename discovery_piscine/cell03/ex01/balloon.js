function expand(balloon) {
        x=document.defaultView.getComputedStyle(balloon).width;
        x=parseInt(x);
        if (x < 420) {
        balloon.style.width = x + 10 + 'px';
        balloon.style.height = x + 10 + 'px';
        } else {
        balloon.style.width = '200px';
        balloon.style.height = '200px';
        }

        balloon.style.backgroundColor = changeColor(balloon,balloon.style.backgroundColor);
        console.log(balloon.style.backgroundColor);
    }

function shrink(balloon) {
        x=document.defaultView.getComputedStyle(balloon).width;
        x=parseInt(x);
        if (x > 200) {
            balloon.style.width = x - 5 +'px';
            balloon.style.height = x - 5 +'px';
        } else {
            balloon.style.width = '200px';
            balloon.style.height = '200px';
        }
        balloon.style.backgroundColor = reverseColor(balloon,balloon.style.backgroundColor);
}

function randomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function changeColor(balloon, color) {
    colors = ['red', 'green', 'blue'];
    if (color === colors[0]) {
        return colors[1];
    } else if (color === colors[1]) {
        return colors[2];
    } else {
        return colors[0];
    }
}

function reverseColor(balloon, color) {
    colors = ['red','blue','green'];
    if (color === colors[0]) {
        return colors[1];
    } else if (color === colors[1]) {
        return colors[2];
    } else {
        return colors[0];
    }
}