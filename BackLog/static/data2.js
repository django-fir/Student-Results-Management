var url = window.location.href.split("/")
let main = `http://${url[2]}/${url[3]}/${url[4]}/${url[5]}/1`
fetch(main)
    .then((response) => response.json())
    .then((data) => gridOptions.api.setRowData(data));

