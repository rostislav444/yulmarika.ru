  // OPEN/CLOSE MOBLIE FILTER
  const filtersOuter = document.querySelector('.filters__outer')
  filtersOuter.onclick = (e) => {
    if(e.target == filtersOuter) {
      document.querySelector('.catalogue__actions').classList.remove('active')
    }
  }
  document.querySelector('.mobile_filter_button').onclick = () => {
    document.querySelector('.catalogue__actions').classList.add('active')
  } 
  document.querySelector('.mobile_filter_close_button').onclick = () => {
    document.querySelector('.catalogue__actions').classList.remove('active')
  } 