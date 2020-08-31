const body = document.querySelector('body')
const FilterGroupButton = document.querySelectorAll('.drop_button__wrapper')

function removeAllActive(list) {
  for (let el of list) {
    el.classList.remove('is_visible')
    document.removeEventListener('mousedown', listener, false)
  }
}



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






