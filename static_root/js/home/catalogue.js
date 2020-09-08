  // VARS
  const preloader =         document.querySelector('.preloader')
  var productsList =        document.querySelector('.products_list__wrapper')
  const productsQty =       document.querySelector('.catalogue_products_quantity_num')

  const catalogueActions =  document.querySelector('.catalogue__actions')
  var loadMoreButton =      document.querySelector('.load_more_btn')
  const categoryBtns =      document.querySelectorAll('.catalogue_category')
  const paginationButtons = document.querySelectorAll('.pagination_buton')
  // PAGES
  const totalPages =        document.querySelector('.total_pages')
  const curentPage =        document.querySelector('.curent_page')
  // PRODUCTS QUANTITY
  var ProductsLoaded =      document.querySelectorAll('.product__wrapper').length
  var ProductsTotal = parseInt(document.querySelector('.catalogue_products_quantity_num').innerHTML)
  // PRICE INPUTS
  const maxPriceInput =     document.querySelector('.max_price_input')
  const minPriceInput =     document.querySelector('.min_price_input')

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
    console.log(response);
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
    if (typeof selectAllButtonupdate !== "undefined") { selectAllButtonupdate()}
    if (typeof PriceFilterUpdate     !== "undefined") { PriceFilterUpdate(response)}
    if (typeof setChosenFilters      !== "undefined") { setChosenFilters()}
    if (typeof changeImageOnHover    !== "undefined") { changeImageOnHover()}
   
    
    upadateQTY(response['more'])
    makeBigNum()
    loadMoreButton = document.querySelector('.load_more_btn')
    if (loadMoreButton) {
      loadMoreButton.onclick = () => { loadMore() }
    }
    
  }



  function catalogueURL() {
    if (window['curUrl'] != undefined) { url = curUrl} 
    else { url = '/' }
   
    let categories = []
    for (let category of categoryBtns) {
      if (category.checked) { categories.push(category.dataset.slug) }
    }
    if (categories.length) {
      url += 'category:' + categories.join('&') + '/'
    }
    if (typeof window['GetFilterData'] === 'function') {
      let filterData = GetFilterData()
      let params = new URLSearchParams(filterData).toString()
      if (params.length > 0) {
        url += '?' + params
      }
      history.pushState({}, null, window.location.origin + url);
    } else {
      url = window.location.href
    }
   
    
    return url
  }

  function catalogueRequest(extra, url) {
    let data = {}
    if (typeof window['GetFilterData'] === 'function') {
      data = GetFilterData()
      url = catalogueURL()
    } else {
      url = window.location.href
    }
    
    if (extra != undefined && typeof extra === "object") {
      for (var key in extra) {
        if (data[key] === undefined) {
          data[key] = extra[key]
        }
      }
    }
    
     
    window.history.pushState("", "", url);
    
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
    if (url == undefined) {
      url = catalogueURL()
    }
    let data = {}
    if (typeof window['GetFilterData'] === 'function') {
      data = GetFilterData()
    }
    data['display'] = document.querySelectorAll('.product__wrapper').length
    data['page'] = parseInt(curentPage.dataset.value) + 1
    preloader.classList.add('active')
    xhrOnLoad('POST', url, data=JSON.stringify(data), addMoreProducts)
  } if (loadMoreButton) {
    loadMoreButton.onclick = () => { loadMore(loadMoreButton.dataset.url) }
  }
  
  


  var filterActionButton = document.querySelectorAll('.catalogue_filter__action_button')
  for (let button of filterActionButton) {
    button.onclick = () => {
      document.querySelector('.catalogue__actions').classList.remove('active')
      stopOutClickListener()
      catalogueRequest({page : 1})
    }
  }

  for (let category of categoryBtns) {
    category.onchange = () => {
      catalogueRequest({page : 1})
    }
  }

function clearAllFilters() {
  let inputs = document.querySelectorAll('.catalogue_filter__input')
  for (let input of inputs) {
    input.checked = false
  }
  document.querySelector('.catalogue__actions').classList.remove('active')
  catalogueRequest({page : 1})
}

let clearFilters = document.querySelectorAll('.clear_filters')
if (clearFilters) {
  for (let clearFilter of clearFilters) {
    clearFilter.onclick = () => {
      clearAllFilters()
    }
  }
}
