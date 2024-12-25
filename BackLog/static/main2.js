


const gridOptions = {
  columnDefs: [
    
  { 
      headerName: 'USN',
      field: 'usn',
      type: 'dimension',     
      // rowGroup: true,
      // enableRowGroup: true,
      // hide:true,
      cellRenderer:(param)=>{
        console.log("done");
        return `<span> ${param.value}</span><span style="color:green;">(P:${param.data.student__spass}</span>,<span style="color:red;">F:${param.data.student__sfail}</span>)`
        
        
      }
    },
    
    {
      headerName: 'SEM',
      field: 'sem',      
      type: 'dimension',
      minWidth: 200,      
      // rowGroup: true,
      // enableRowGroup: true,
      // hide:true,
      cellRenderer: countryCellRenderer,
    },
    

    {
      headerName: 'Type',
      field: 'exam_type',      
      type: 'dimension',
      // rowGroup: true,
      // enableRowGroup: true,
      // hide:true,
      cellRenderer: stateCellRenderer,
    },
    
     
  {
    headerName: 'Subject',
      field: 'sub_code',      
      type: 'dimension',
      // rowGroup: true,
      // hide:true,
      cellRenderer:(params)=>{
        var color = "green"
        if(params.data.result == "P")
        {
          color = "green";
        }
        else if(params.data.result == "F")
        {
          color = "red";
        }
        else
        {
          color = "blue"
        }
        return `<span style="color:${color};">${params.value}</span>`
      }
    },
    {
    headerName: 'MAIN',
      field: 'main_marks',      
      type: 'dimension',
      
      cellRenderer:(params)=>{
        var color = "green"
        if(params.data.result == "P")
        {
          color = "green";
        }
        else if(params.data.result == "F")
        {
          color = "red";
        }
        else
        {
          color = "blue"
        }
        return `<span style="color:${color};">${params.value}</span>`
      }
    },
    {
    headerName: 'IA',
      field: 'ia_marks',      
      type: 'dimension',
      
      cellRenderer:(params)=>{
        var color = "green"
        if(params.data.result == "P")
        {
          color = "green";
        }
        else if(params.data.result == "F")
        {
          color = "red";
        }
        else
        {
          color = "blue"
        }
        return `<span style="color:${color};">${params.value}</span>`
      }
    },
    {
      headerName: 'Exam Date',
      field: 'entry_date',
      minWidth: 250,
      type: 'dimension',
      cellRenderer: (params) => {
        return `<span style="margin-left: 120px">${params.value}</span>`;

      },
    },  
    
    // {
      
    //   field:"In.. + Ass..",
    //   type: 'dimension',   
    //   cellRenderer:(params)=>{
    //     let v = params.data.obtained_marks;
    //     let a = params.data.asinment;
    //     let colorm = "red";
    //     if(v>=18)
    //     {
    //       colorm = "green";
    //     }
          
    //     if(params.node.data.exam_type__name__name == "MAIN")
    //     {
    //       let totalm = 0;
    //       let totala = 0;
          
    //       params.node.parent.childrenAfterGroup.forEach(valus=>{
    //         if(!(valus.data.exam_type__name__name=="MAIN"))
    //         {
    //         totalm+=(valus.data.obtained_marks/3);
    //         totala+=(valus.data.asinment/3);
    //         }
    //       });
    //       let colorut = "red";
          
    //       if((totalm+totala) >= 19)
    //     {
    //       colorut = "green";          
    //     }  
        
    //       return `<span style="color:${colorut};">${Math.ceil(totalm)}</span> + <span style="color:${colorut};">${Math.ceil(totala)}</span> = <span style="color:${colorut};">${Math.ceil(totala+totalm)}</span>`;
    //     }
    //     return `<span style="color:${colorm}">${v}</span> + <span style="color:${"green"}">${a}</span>`
               

    //   },
    // },
    // {
    //   field:"Total",
    //    type: 'dimension',
    //   cellRenderer:(params)=>{
    //     let v = params.data.main_marks;
    //     let a = params.data.asinment;
    //     let colorm = "red";
    //     if(v>=19)
    //     {
    //       colorm = "green";
    //     }
    //     if(params.node.data.exam_type__name__name == "MAIN")
    //     {
    //       let totalm = 0;
    //       let totala = 0;
          
    //       params.node.parent.childrenAfterGroup.forEach(valus=>{
    //         if(!(valus.data.exam_type__name__name=="MAIN"))
    //         {
    //         totalm+=(valus.data.obtained_marks/3);
    //         totala+=(valus.data.asinment/3);
    //         }
    //       });
    //       let colorut = "red";
    //       let colorum = "green";
    //       let colorui = "red";
    //       if ( (params.data.obtained_marks + totala + totalm )>= 43)
    //       {
    //         colorut = "green";
    //       }
                    
    //       if (params.data.obtained_marks < 24)
    //       {
    //         colorum = "red";
    //         colorut = "red";
    //       }
          
    //       if((totalm+totala) >= 19)
    //     {
    //       colorui = "green";          
    //     }  
    //     // return `<span style="color:${colorui};">${Math.ceil(totalm+totala)}</span> + <span style="color:${colorum};">${params.data.obtained_marks}</span> = <span style="color:${colorut}">${Math.ceil(params.data.obtained_marks + totala+totalm)}</span>`;
    //     return `<span style="color:${colorum};">${params.data.obtained_marks}</span>`
    //     }
    //     return `<span style="color:${colorm}">${v+a}</span>`


    //   },
    // },

    
    // {
    //   headerName: 'Attendence',
    //   field:"attendence",
    //    type: 'dimension',
    //   cellRenderer:AttendenceCellRenderer,
    // },
    {
      headerName: 'Result',
      field:"result",
       type: 'dimension',
      cellRenderer:resultCellRenderer,
    },    
  ],
  defaultColDef: {
    flex: 1,
    filter: true,
    // floatingFilter: true,
    minWidth: 150,
    resizable: true,
    sortable: true,
  },
  
  autoGroupColumnDef: {
    minWidth: 300,
  },
  columnTypes: {
    numberValue: {
      enableValue: true,
      aggFunc: 'sum',
      editable: true,
      valueParser: numberParser,
    },
    dimension: {
      enableRowGroup: true,
      enablePivot: true,
    },
  },
  
  // rowData: getData(),  
  groupDisplayType: 'groupRows',
  rowGroupPanelShow: 'always',
  groupDefaultExpanded: 1,
  suppressAggFuncInHeader: true,
  animateRows: true,
};

const COUNTRY_CODES = {
  Ireland: 'ie',
  'United Kingdom': 'gb',
  USA: 'us',
};

function numberParser(params) {
  return parseInt(params.newValue);
}


function countryCellRenderer(params) {
  if (params.value === undefined || params.value === null) {
    return '';
  } else {
    const flag =
      '<img border="0" width="15" height="10" src="https://flagcdn.com/h20/' +
      COUNTRY_CODES[params.value] +
      '.png">';
    return flag + ' ' + params.value;
  }
}

function stateCellRenderer(params) {
  if (params.value === undefined || params.value === null) {
    return '';
  } else {
    const flag =
      '<img border="0" width="15" height="10" src="https://www.ag-grid.com/example-assets/gold-star.png">';
    return flag + ' ' + params.value;
  }
}

function cityCellRenderer(params) {
  if (params.value === undefined || params.value === null) {
    return '';
  } else {
    const flag =
      '<img border="0" width="15" height="10" src="https://www.ag-grid.com/example-assets/weather/sun.png">';
    return flag + ' ' + params.value;
  }
}



function AttendenceCellRenderer(params) {  
  if (params.value === undefined || params.value === null) {
    return '';
  } else if(params.value >= 75) {
    const flag =`<span style="color:green;">${params.value}</span>`;
    return flag;
  }
  else
  {
    const flag =`<span style="color:red;">${params.value}</span>`;
    return flag;
  }
}

function resultCellRenderer(params) {  
  let color = "green";

  if (params.value === undefined || params.value === null) {
    return '';
  } 
  else if(params.data.result == "Pass")
  {
    color = "Green";
  }
  else if(params.data.result == "Fail")
  {
    color = "Red";
  }      
  else
  {
    color = "Blue";
  }
  return `<span style="color:${color};">${params.data.result}</span>`;
  
}


// setup the grid after the page has finished loading
document.addEventListener('DOMContentLoaded', function () {
  const gridDiv = document.querySelector('#myGrid');
  new agGrid.Grid(gridDiv, gridOptions);
  
});

