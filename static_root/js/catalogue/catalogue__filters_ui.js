const body = document.querySelector('body')
const FilterGroupButton = document.querySelectorAll('.drop_button__wrapper')

function removeAllActive(list) {
  for (let el of list) {
    el.classList.remove('is_visible')
    document.removeEventListener('mousedown', listener, false)
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
        if (input.dataset.key != 'default') {
          data[input.name] = input.dataset.key
        }
        
      }
    } else if (input.type == 'number') {
      if (input.value) {

        data[input.dataset.slug] = parseInt(input.value)
      }
    }
  }
  return data
}

function setChosenFilters() {
  let list = document.querySelector('.chosen_filters_list')
  if (list) {
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

} setChosenFilters()


function selectAllButton(parent) {
  let objects = parent.querySelectorAll('.catalogue_filter__input')
  let inputCheckAll = parent.querySelector('.check-all')
  if (inputCheckAll) {
    inputCheckAll.onchange = () => {
      console.log(1);
      for (let obj of objects) {
        obj.checked = inputCheckAll.checked
        obj.onchange = () => {
          if (obj.checked == false) {
              inputCheckAll.checked = false
          }
        }
      }
    }
  }
}

function selectAllButtonupdate() {
  for (let block of FilterGroupButton) {
    selectAllButton(block)
  }
}




for (let block of FilterGroupButton) {
  block.addEventListener('mousedown', function(e) {
    let dropButton = block.querySelector('.drop_button')
    let target = e.target
    if (block.classList.contains('is_visible') == false) {
        removeAllActive(FilterGroupButton)
        clickListener(block, 'is_visible')
    } else {
      if (target == block || target == dropButton || dropButton.contains(target) || target.parentNode == block) {
        removeAllActive(FilterGroupButton)
      }
    }
  }, false)
}

selectAllButtonupdate()






