const productColumns = document.querySelectorAll('input[name=product_columns]') 
for (let input of productColumns) {
  input.onchange = () => {
    if (input.checked) {
      if ('action' in input.dataset) {
        productsList.classList.add('wide')
      } else {
        productsList.classList.remove('wide')
      }
    }
  }
}