var activeEl, activeElClass

function stopOutClickListener() {
    activeEl.classList.remove(activeElClass) 
    activeEl, activeElClass = undefined, undefined
    document.removeEventListener('mousedown', listener, false)
}


function listener(e) {
  let el = e.target
  while (el != activeEl) {
    el = el.parentNode
    if (el.tagName == 'BODY') {
      stopOutClickListener()
      break
    }
  }
}
function clickListener(obj, cls) {
  if (obj !== undefined) {
    activeEl = obj
    activeElClass = cls
    activeEl.classList.add(activeElClass)
    document.addEventListener('mousedown', listener, false)
  } 
}