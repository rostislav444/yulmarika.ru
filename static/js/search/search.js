  // VARS
  const preloader = document.querySelector('.preloader')
  var productsList = document.querySelector('.products_list__wrapper')
  const productsQty = document.querySelector('.catalogue_products_quantity_num')
  const productColumns = document.querySelectorAll('input[name=product_columns]') 
  const catalogueActions = document.querySelector('.catalogue__actions')
  var loadMoreButton = document.querySelector('.load_more_btn')
  const categoryBtns = document.querySelectorAll('.catalogue_category')
  const paginationButtons = document.querySelectorAll('.pagination_buton')
  // PAGES
  const totalPages = document.querySelector('.total_pages')
  const curentPage = document.querySelector('.curent_page')
  // PRODUCTS QUANTITY
  var ProductsLoaded = document.querySelectorAll('.product__wrapper').length
  var ProductsTotal = parseInt(document.querySelector('.catalogue_products_quantity_num').innerHTML)
  // PRICE INPUTS
  const maxPriceInput = document.querySelector('.max_price_input')
  const minPriceInput = document.querySelector('.min_price_input')

  var lastScrollPosition = 0
  


  function upadateQTY(more=undefined) {
    ProductsLoaded = document.querySelectorAll('.product__wrapper').length
    ProductsTotal = parseInt(document.querySelector('.catalogue_products_quantity_num').innerHTML)
    console.log('more', more);
    if (more == true) {
      loadMoreButton.classList.remove('disabled')
    } else {
      loadMoreButton.classList.add('disabled')
    }
    
  }

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
  


  function PriceFilterUpdate(response) {
   
    if (maxPriceInput && minPriceInput) {
      for (let input of [maxPriceInput, minPriceInput]) {
        input.min = response['min_price']
        input.max = response['max_price']
        
        if (input.value) {
          if (parseInt(input.value) >  parseInt(input.max)) {
            input.value = input.max
          } else if (parseInt(input.value) <  parseInt(input.min)) {
            input.value = input.min
          }
        }
      }
      maxPriceInput.placeholder = response['max_price']
      minPriceInput.placeholder = response['min_price']
    }
  }




  function renderCatalogue(response) {
    response = JSON.parse(response)
   
    for (key in response['filters']) {
      slug = response['filters'][key]['slug']
      let filter = document.querySelector('.filter__' + slug)
      
      if (filter != undefined) {
        filter.querySelector('ul').innerHTML = nunjucks.renderString(filterTpl, {filter : response['filters'][key]})
      }
    }
    productsList.innerHTML = nunjucks.renderString(prductTpl, response)
    productsQty.innerHTML = response['products_len']
    totalPages.innerHTML = response['pages']
    if (response['page'] != undefined) { 
      curentPage.dataset.value = response['page'] 
      curentPage.value = response['page'] 
      curentPage.max = response['pages']
    }
    preloader.classList.remove('active')
    
    upadateQTY(response['more'])
    makeBigNum()
    loadMoreButton = document.querySelector('.load_more_btn')
    if (loadMoreButton) {
      loadMoreButton.onclick = () => { loadMore() }
    }
    
  }





  function catalogueRequest(extra, url) {
    let data = {}
    url = window.location.href
    preloader.classList.add('active')
    xhrOnLoad('POST', url, data=JSON.stringify(data), renderCatalogue)
  }

  // LOAD MORE
  function addMoreProducts(response) {
    response = JSON.parse(response)
    productsList.innerHTML += nunjucks.renderString(prductTpl, response)
    window.scroll({top: lastScrollPosition});
    
    preloader.classList.remove('active')
    totalPages.innerHTML = response['pages']
    if (response['page'] != undefined) { 
      curentPage.dataset.value = response['page'] 
      curentPage.value = response['page'] 
      curentPage.max = response['pages']
    }
    upadateQTY(response['more'])
    makeBigNum()
    
  }


  for (let btn of paginationButtons) {
    btn.onclick = () => {
      let page = parseInt(curentPage.dataset.value)
      if (btn.dataset.action == 'prev' && page > 1) {
        catalogueRequest({page : page - 1}, url=btn.dataset.url)
      } else if (btn.dataset.action == 'next' && page + 1 <= parseInt(totalPages.innerHTML)) {
        catalogueRequest({page : page + 1}, url=btn.dataset.url)
      }
    }
  } 

  curentPage.oninput = () => {
    let input = curentPage
    let re = /[^0-9.]/g
    input.value =  input.value.replace(re, '');
  }

  curentPage.onchange = () => {
    let input = curentPage
    let value = parseInt(input.value)
    if (value >= input.min && value <= input.max) {
      input.value = value
    } else if (value > input.max) {
        input.value = input.max
    } else  {
        input.value = input.min
    }
    catalogueRequest({page : input.value})
  }


  function loadMore(url) {
    lastScrollPosition = window.scrollY
    data = {
        'display' : document.querySelectorAll('.product__wrapper').length,
        'page' :    parseInt(curentPage.dataset.value) + 1
    }
    preloader.classList.add('active')
    xhrOnLoad('POST', url, data=JSON.stringify(data), addMoreProducts)
  } if (loadMoreButton) {
    loadMoreButton.onclick = () => { loadMore(loadMoreButton.dataset.url) }
  }
  
  

