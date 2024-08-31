function countdown(seconds) {
    var delay = 0;
    while (seconds >= 0) {
        (function () {
            var time = seconds;
            setTimeout(function () {
                console.log(time);
            }, delay * 1000);
            delay++;
        });
        seconds--;
    }
}

countdown(3);
