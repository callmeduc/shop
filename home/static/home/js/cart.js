var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)

        if (user == 'AnonymousUser') {
            addCookieItem(productId, action)
            console.log('Không Có user')
        } else {
            console.log('Có user')
        }
    })
}

function addCookieItem(productId, action) {
    console.log('Not logged in ....')
    if (action == 'add') {
        console.log('ID:')
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    } if (action == 'remove') {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0) {
            console.log('remove item')
            delete cart[productId]
        }
    }
    if (action == 'trash'){
        delete cart[productId]
    }
    console.log('Cart:',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}