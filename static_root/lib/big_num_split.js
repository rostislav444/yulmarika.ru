function BigNum(num) {
  num = num.toString()
  count = 0
  number = ''
  for (let n of num.split("").reverse()) {
    count += 1
    if (count == 4) {
      number += ' '
      count = 0
    } 
    number += n
  }
  return number.split("").reverse().join('')
}
function makeBigNum() {
  for (let num of document.querySelectorAll('.big_num')) {
    num.innerHTML = BigNum(num.innerHTML)
  }
}
makeBigNum()
