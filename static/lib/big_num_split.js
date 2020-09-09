function BigNum(num) {
  num = num.toString()
  num = num.replace(' ','')
  count = 0
  number = ''
  let point = undefined
  let points = num.split(".")
  if (points.length > 1) {
    console.log(num);
    num = points[0]
    point = points[1]
  }

  for (let n of num.split("").reverse()) {
    count += 1
    if (count == 4) {
      number += ' '
      count = 0
    } 
    number += n
  }
  number = number.split("").reverse().join('')
  if (point) {
    number += '.' + point
  }
  return number
}
function makeBigNum() {
  for (let num of document.querySelectorAll('.big_num')) {
    num.innerHTML = BigNum(num.innerHTML)
  }
}
makeBigNum()
