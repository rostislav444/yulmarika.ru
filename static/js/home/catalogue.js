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
  
  function GetFilterData() {
    let data = {}
    let inputs = document.querySelectorAll('.catalogue_filter__input')
    for (let input of inputs) {
      if (input.checked) {
        if (input.type == 'checkbox') {
          if (data[input.dataset.slug] == undefined) {
            data[input.dataset.slug] = []
          } 
          data[input.dataset.slug].push(input.dataset.id)
        } else if (input.type == 'radio') {
          data[input.name] = input.dataset.key
        }
      } else if (input.type == 'number') {
        if (parseInt(input.value) !== 0) {
          data[input.dataset.slug] = input.value
        }
      }
    }
    return data
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


  function setChosenFilters() {
    let list = document.querySelector('.chosen_filters_list')
    let inputs = document.querySelectorAll('.catalogue_filter__input')
    checked = false
    list.classList.remove('active')
    list.innerHTML = ''
    let li = document.createElement('li')
        li.innerHTML = 'Сбросить фильтры'
        li.classList.add('clear_filters')
        li.onclick = () => { clearAllFilters() }
        list.appendChild(li)
    for (let input of inputs) {
      if (input.checked && input.name!="sort_by") {
        list.classList.add('active')
        let li = document.createElement('li')
            li.innerHTML =    input.dataset.label
            li.dataset.slug = input.dataset.slug
            li.dataset.id =   input.dataset.id
        let close = document.createElement('div')
            close.classList.add('close')
            close.onclick = () => {
              parent = close.parentElement
              let inpt = document.querySelector('input[data-slug="'+parent.dataset.slug+'"][data-id="'+parent.dataset.id+'"]')
              inpt.checked = false
              parent.remove()
              catalogueRequest({page : 1})
            }
            img = document.createElement('img')
            img.src = '/static/img/ico/close.svg'
            close.appendChild(img)
            li.appendChild(close)
        list.appendChild(li)
      }
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
    if (response['page'] != undefined) { curentPage.innerHTML = response['page'] }
    preloader.classList.remove('active')
    selectAllButtonupdate()
    PriceFilterUpdate(response)
    setChosenFilters()
    upadateQTY(response['more'])
    makeBigNum()

    loadMoreButton = document.querySelector('.load_more_btn')
    if (loadMoreButton) {
      loadMoreButton.onclick = () => { loadMore() }
    }
    window.scroll({top: scrollPosition,  behavior: 'smooth' });
    

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
    return url
  }

  function catalogueRequest(extra) {
    let url = catalogueURL()
    let data = GetFilterData()
    if (extra != undefined && typeof extra === "object") {
      for (var key in extra) {
        if (data[key] === undefined) {
          data[key] = extra[key]
        }
      }
    }
    preloader.classList.add('active')
    window.history.pushState("", "", url);
    xhrOnLoad('POST', url, data=JSON.stringify(data), renderCatalogue)
  }

  // LOAD MORE
  function addMoreProducts(response) {
    response = JSON.parse(response)
    productsList.innerHTML += nunjucks.renderString(prductTpl, response)
    preloader.classList.remove('active')
    totalPages.innerHTML = response['pages']
    if (response['page'] != undefined) { curentPage.innerHTML = response['page'] }
    upadateQTY(response['more'])
    window.scroll({top: lastScrollPosition,  behavior: 'smooth' });
  }


  for (let btn of paginationButtons) {
    btn.onclick = () => {
      let page = parseInt(curentPage.innerHTML)
      if (btn.dataset.action == 'prev' && page > 1) {
        catalogueRequest({page : page - 1})
      } else if (btn.dataset.action == 'next' && page + 1 <= parseInt(totalPages.innerHTML)) {
        catalogueRequest({page : page + 1})
      }
    }
  } 


  function loadMore() {
    let url = catalogueURL()
    let data = GetFilterData()
    data['display'] = document.querySelectorAll('.product__wrapper').length
    data['page'] = parseInt(curentPage.innerHTML) + 1
    console.log(data['page']);
    preloader.classList.add('active')
    lastScrollPosition = window.scrollY
    xhrOnLoad('POST', url, data=JSON.stringify(data), addMoreProducts)
  } if (loadMoreButton) {
    loadMoreButton.onclick = () => { loadMore() }
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