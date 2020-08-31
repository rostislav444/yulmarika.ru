function Counter() {
    for (let counter of document.querySelectorAll('.counter')) {
        let input = counter.querySelector('input')
        let buttons = counter.querySelectorAll('button')
        let value = input.value
        function changeValue(value) {
            if (value >= input.min && value <= input.max) {
                input.value = value
            } else if (value > input.max) {
                input.value = input.max
            } else  {
                input.value = input.min
            }
            if ('function' in counter.dataset && value == input.value) {
                this[counter.dataset.function](counter)
            }
        }
        for (let button of buttons) {
            button.onclick = () => { 
                value = parseInt(input.value) + parseInt(button.innerHTML + 1) 
                changeValue(value)
            }
            input.onchange = () => { 
                value = parseInt(input.value) 
                changeValue(value)
            }
        }
        
    }
} Counter()

