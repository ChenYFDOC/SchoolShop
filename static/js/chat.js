function google() {
    window.open("https://bootstrapmb.com")
}

function bing() {
    window.open("https://bootstrapmb.com")
}

var rollbackTo = false;
var originalState = false;

function storeState(a) {
    rollbackTo = a.current
}

function rollback(a) {
    if (rollbackTo != false) {
        if (originalState == false) {
            originalState = a.current.next
        }
        a.current.next = rollbackTo
    }
}

function restore(a) {
    if (originalState != false) {
        a.current.next = originalState
    }
}

jQuery(function (a) {
    var b = a("#chat").convform()
});