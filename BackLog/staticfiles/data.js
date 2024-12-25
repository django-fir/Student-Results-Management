var url = window.location.href.split("/")
fetch(`http://${url[2]}/search/${url[4]}`)
    .then((response) => response.json())
    .then((data) => gridOptions.api.setRowData(data));

