function handleClick(event){
    // alert("clicked hello")
    let val = document.forms["bookform"]["bookvalue"].value;
    console.log(val)
    if (val==""){
        alert("input is required")
    }
    // $.post( "/book",{
    //     bookform_data : x
    // });
    // $.get("/book", function(data) {
    //     console.log(data)
    // })
    var form = new FormData();
    form.append("bookform_data", val);

    var settings = {
    "url": "/book",
    "method": "POST",
    "timeout": 0,
    "processData": false,
    "mimeType": "multipart/form-data",
    "contentType": false,
    "data": form
    };

    $.ajax(settings).done(function (response) {
    // console.log(response);
    const dbParam = JSON.parse(response);
    let text = "<tbody>"
    for (let x in dbParam) {
        // console.log(dbParam[x])
        text+="<tr>"
        text += "<th scope='row'><a href='javascript: null' onclick='bookFunction(this.innerHTML)'>" + dbParam[x].isbn + "</a></th>";
        text+= "<td>"+dbParam[x].Title+"</td>"
        text+= "<td>"+dbParam[x].Author+"</td>"
        text+= "<td>"+dbParam[x].Year+"</td>"
        text+="</tr>"
    }  
    text+="</tbody>" 
    // console.log(text)
    document.getElementsByTagName("tbody")[0].innerHTML = text;
    });
}

function bookFunction(content){
    // location.replace("/details.html")
    var settings = {
        "url": "/review",
        "method": "GET",
        "timeout": 0,
        "headers": {
          "Cookie": "session=eyJib29raWQiOiIxODU3MjMxMDgyIn0.YQt-pg.aY6CvSptDuE97NDvmQh5C36Hexg"
        },
      };
      
      $.ajax(settings).done(function (response) {
        $("html").html(response)
      });

    // alert(content)
    var form = new FormData();
    // form.append("bookform_data", "the");

    var settings = {
    "url": "/book/details/"+content,
    "method": "GET",
    "timeout": 0,
    "headers": {
        "Cookie": "session=eyJib29raWQiOiIxODU3MjMxMDgyIn0.YQt-pg.aY6CvSptDuE97NDvmQh5C36Hexg"
    },
    "processData": false,
    "mimeType": "multipart/form-data",
    "contentType": false,
    "data": form
    };

    $.ajax(settings).done(function (response) {
    console.log(response);
    const dbParam = JSON.parse(response);
    let text = "<tbody>"
    for (let x in dbParam.bookdetais) {
        // console.log(dbParam[x])
        text+="<tr>"
        text += "<th scope='row'><a href='javascript: null' onclick='bookFunction(this.innerHTML)'>" + dbParam.bookdetais[x].isbn + "</a></th>";
        text+= "<td>"+dbParam.bookdetais[x].Title+"</td>"
        text+= "<td>"+dbParam.bookdetais[x].Author+"</td>"
        text+= "<td>"+dbParam.bookdetais[x].Year+"</td>"
        text+="</tr>"
    }  
    text+="</tbody>" 
    // console.log(text)
    document.getElementsByTagName("tbody")[0].innerHTML = text;

    let revhtml=" "
    for(let y in dbParam.reviews_dict){
        revhtml+='<blockquote class="blockquote">'
        revhtml+= '<footer class="blockquote-footer float-left">'+ dbParam.reviews_dict[y].uname+", "+dbParam.reviews_dict[y].recorded_time+'</footer>'
        revhtml+= '<div class="float-right">'
            for(let rat in parseInt(dbParam.reviews_dict[y].rating)){
                console.log(rat)
            }
              
        revhtml+= '</div><br></br><p class="mb-0">'+dbParam.reviews_dict[y].review+'</p>'
          
        revhtml+='</blockquote><hr></hr>'
        
    }
    document.getElementById('rev').innerHTML = revhtml
    });
}

// {%if (i < review.rating)%}                
//                 <span class="fa fa-star checked"></span>
//               {%else%}
//                 <span class="fa fa-star"></span>
//               {%endif%}
//             {%endfor%}
//           </div><br></br>

//  {%for book in books%}
//       <tr>
        
//         <th scope="row"><a href="{{ url_for('get_book_details',id = book.id)}}" target="_blank">{{book.id}}</a></th>
//         <td>{{book.title}}</td>
//         <td>{{book.author}}</td>
//         <td>{{book.year}}</td>
//       </tr>
//       {%endfor%} 




// console.log(dbParam[0])
    // const xmlhttp = new XMLHttpRequest();
    // xmlhttp.onload = function() {
    //   const myObj = JSON.parse(response);
    //   console.log(myObj)
    //   let text = ""
    //   for (let x in myObj) {
    //       console.log(x)
    //       text+="<tr>"
    //     text += "<th scope='row'>" + x.isbn + "</th>";
    //     text+= "<td>"+x.title+"</td>"
    //     text+= "<td>"+x.author+"</td>"
    //     text+= "<td>"+x.year+"</td>"
    //     text+="</tr>"
    //   }   
    //   console.log(text)
    //   document.getElementById("demo").innerHTML = text;
    // }